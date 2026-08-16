"""
Unit tests for the framework-free logic in data_loader.py.

Run with: pytest tests/test_data_loader.py -v
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data_loader import (  # noqa: E402
    EmptyDataError,
    MissingSalesColumnError,
    clean_dataframe,
    detect_columns,
    find_column,
)

SALES_CANDIDATES = ["total sales", "sales amount", "sales value", "net sales",
                     "revenue", "sales", "amount", "total"]


def test_find_column_exact_match_wins_over_generic_fallback():
    """Regression test: a 'Discount Total' column must NOT be picked as the
    sales column when a real 'Sales' column is also present."""
    columns = ["Order ID", "Discount Total", "Sales", "Region"]
    assert find_column(columns, SALES_CANDIDATES) == "Sales"


def test_find_column_prefers_specific_phrase_over_generic_word():
    columns = ["Order ID", "Total Sales", "Discount Total"]
    assert find_column(columns, SALES_CANDIDATES) == "Total Sales"


def test_find_column_returns_none_when_nothing_matches():
    columns = ["Order ID", "Region"]
    assert find_column(columns, ["sales", "revenue"]) is None


def test_find_column_respects_exclude_set():
    columns = ["Sales", "Sales Rep"]
    assert find_column(columns, ["sales"], exclude={"Sales"}) == "Sales Rep"


def test_detect_columns_does_not_reuse_a_column_for_two_fields():
    df = pd.DataFrame({
        "Order Date": ["2024-01-01"],
        "Sales": [100],
        "Region": ["South"],
    })
    column_map = detect_columns(df)

    assigned = [v for v in (column_map.date, column_map.sales, column_map.region,
                             column_map.customer) if v is not None]
    assert len(assigned) == len(set(assigned))
    assert column_map.sales == "Sales"
    assert column_map.region == "Region"


def test_clean_dataframe_drops_invalid_sales_rows():
    df = pd.DataFrame({"Sales": ["100", "abc", "50"], "Region": ["A", "B", "C"]})
    column_map = detect_columns(df)

    cleaned, removed = clean_dataframe(df, column_map)

    assert removed == 1
    assert len(cleaned) == 2
    assert cleaned["Sales"].tolist() == [100.0, 50.0]


def test_clean_dataframe_raises_when_sales_column_missing():
    df = pd.DataFrame({"Region": ["A", "B"]})
    column_map = detect_columns(df)

    with pytest.raises(MissingSalesColumnError):
        clean_dataframe(df, column_map)


def test_clean_dataframe_raises_when_all_sales_values_invalid():
    df = pd.DataFrame({"Sales": ["abc", "xyz"]})
    column_map = detect_columns(df)

    with pytest.raises(EmptyDataError):
        clean_dataframe(df, column_map)
