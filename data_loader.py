"""
File loading, column detection and cleaning for the sales dashboard.

The core logic here (`find_column`, `detect_columns`, `clean_dataframe`,
`read_uploaded_file`) is pure pandas / stdlib with no Streamlit calls, so it
can be unit tested in isolation — see tests/test_data_loader.py. Only
`load_and_clean` touches Streamlit, purely to get `@st.cache_data`.
"""

from __future__ import annotations

import io
import logging
import re
from dataclasses import dataclass
from typing import Optional, Sequence, Set, Tuple

import pandas as pd
import streamlit as st

from config import COLUMN_CANDIDATES, COLUMN_DETECTION_ORDER

logger = logging.getLogger(__name__)


class UnsupportedFileError(ValueError):
    """Raised when an uploaded file's extension isn't one we can parse."""


class EmptyDataError(ValueError):
    """Raised when a file has no usable rows/columns after cleanup."""


class MissingSalesColumnError(ValueError):
    """Raised when no sales/revenue column could be detected."""


@dataclass
class ColumnMap:
    """Detected column names for each analytical field, if found."""

    date: Optional[str] = None
    sales: Optional[str] = None
    profit: Optional[str] = None
    quantity: Optional[str] = None
    region: Optional[str] = None
    product: Optional[str] = None
    category: Optional[str] = None
    customer: Optional[str] = None


def _normalize(name: object) -> str:
    """Lowercase and collapse punctuation/whitespace for fuzzy matching."""
    return re.sub(r"[^a-z0-9]+", " ", str(name).lower()).strip()


def find_column(
    columns: Sequence[str],
    candidates: Sequence[str],
    exclude: Optional[Set[str]] = None,
) -> Optional[str]:
    """Find the best-matching column name for an ordered list of candidates.

    Candidates are checked most-specific-first, and for *every* candidate we
    try an exact normalized match across all columns before any candidate is
    allowed to match as a whole-word/partial match. This ordering is what
    stops a generic fallback term (like "total") from grabbing an unrelated
    column (like "Discount Total") when a precise column (like "Sales")
    exists elsewhere in the sheet.
    """
    exclude = exclude or set()
    normalized = {col: _normalize(col) for col in columns if col not in exclude}

    for candidate in candidates:
        for col, norm in normalized.items():
            if norm == candidate:
                return col

    for candidate in candidates:
        pattern = rf"\b{re.escape(candidate)}\b"
        for col, norm in normalized.items():
            if re.search(pattern, norm):
                return col

    return None


def detect_columns(df: pd.DataFrame) -> ColumnMap:
    """Detect date/sales/profit/... columns.

    Fields are resolved in `COLUMN_DETECTION_ORDER`, and each field excludes
    columns already claimed by an earlier (higher priority) field so the
    same column is never assigned to two different roles.
    """
    columns = list(df.columns)
    claimed: Set[str] = set()
    column_map = ColumnMap()

    for field_name in COLUMN_DETECTION_ORDER:
        match = find_column(columns, COLUMN_CANDIDATES[field_name], exclude=claimed)
        setattr(column_map, field_name, match)
        if match:
            claimed.add(match)

    logger.info("Detected columns: %s", column_map)
    return column_map


def read_uploaded_file(uploaded_file) -> pd.DataFrame:
    """Parse an uploaded xlsx/csv/json file-like object into a DataFrame."""
    name = uploaded_file.name.lower()

    if name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    elif name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif name.endswith(".json"):
        df = pd.read_json(uploaded_file)
    else:
        raise UnsupportedFileError(f"Unsupported file format: {uploaded_file.name}")

    df = df.dropna(axis=1, how="all").dropna(axis=0, how="all")
    if df.empty:
        raise EmptyDataError("No usable data was found in the file.")

    return df


def clean_dataframe(df: pd.DataFrame, column_map: ColumnMap) -> Tuple[pd.DataFrame, int]:
    """Coerce numeric/date columns and drop rows with an invalid sales value.

    Returns the cleaned DataFrame plus the number of rows removed because
    the sales column couldn't be parsed as a number.
    """
    if column_map.sales is None:
        raise MissingSalesColumnError(
            "Sales or Revenue column was not detected. Your dataset needs a "
            "column such as Sales, Revenue, Amount or Total Sales."
        )

    df = df.copy()
    df[column_map.sales] = pd.to_numeric(df[column_map.sales], errors="coerce")

    rows_before = len(df)
    df = df.dropna(subset=[column_map.sales])
    removed_rows = rows_before - len(df)

    if df.empty:
        raise EmptyDataError("The Sales column contains no valid numeric values.")

    if column_map.profit:
        df[column_map.profit] = pd.to_numeric(df[column_map.profit], errors="coerce")

    if column_map.quantity:
        df[column_map.quantity] = pd.to_numeric(df[column_map.quantity], errors="coerce")

    if column_map.date:
        df[column_map.date] = pd.to_datetime(df[column_map.date], errors="coerce")

    logger.info("Cleaned dataframe: %d rows kept, %d rows removed", len(df), removed_rows)
    return df, removed_rows


class _UploadShim(io.BytesIO):
    """Minimal in-memory file object carrying a `.name`, so the cached
    loader can work from raw bytes instead of Streamlit's UploadedFile."""

    def __init__(self, data: bytes, name: str):
        super().__init__(data)
        self.name = name


@st.cache_data(show_spinner=False)
def load_and_clean(file_bytes: bytes, file_name: str) -> Tuple[pd.DataFrame, ColumnMap, int]:
    """Cached end-to-end load: parse -> detect columns -> clean.

    The cache key is the raw file bytes plus name, so changing a sidebar
    filter elsewhere in the app doesn't trigger a full re-parse of the
    source file on every Streamlit rerun.
    """
    df = read_uploaded_file(_UploadShim(file_bytes, file_name))
    column_map = detect_columns(df)
    df, removed_rows = clean_dataframe(df, column_map)
    return df, column_map, removed_rows
