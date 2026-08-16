"""
PDF report generation (ReportLab) for the sales dashboard.
"""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from typing import List, Optional

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from config import BRAND_BORDER, BRAND_DARK, BRAND_PRIMARY, BRAND_STRIPE, BRAND_TINT

MAX_TABLE_ROWS = 500


@dataclass
class ReportKpis:
    total_sales: float
    total_profit: float
    total_quantity: float
    total_orders: int
    total_customers: int
    profit_margin: float


@dataclass
class ReportInsight:
    label: str
    name: str
    value: float


def _kpi_table(kpis: ReportKpis, currency: str) -> Table:
    header = ["Total Sales", "Total Profit", "Quantity", "Orders", "Customers", "Profit Margin"]
    values = [
        f"{currency}{kpis.total_sales:,.0f}",
        f"{currency}{kpis.total_profit:,.0f}",
        f"{kpis.total_quantity:,.0f}",
        f"{kpis.total_orders:,}",
        f"{kpis.total_customers:,}",
        f"{kpis.profit_margin:.2f}%",
    ]
    table = Table([header, values], colWidths=[115, 115, 100, 90, 100, 110])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(BRAND_PRIMARY)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor(BRAND_TINT)),
        ("TEXTCOLOR", (0, 1), (-1, 1), colors.HexColor(BRAND_DARK)),
        ("FONTNAME", (0, 0), (-1, 1), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor(BRAND_BORDER)),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return table


def _data_table(df: pd.DataFrame, date_col: Optional[str] = None) -> Optional[Table]:
    if df.empty:
        return None

    subset = df.head(MAX_TABLE_ROWS).copy()

    # Render the date column as a plain date (no time-of-day / milliseconds)
    # rather than pandas' default str(Timestamp) representation.
    if date_col and date_col in subset.columns:
        subset[date_col] = subset[date_col].dt.strftime("%Y-%m-%d")

    subset = subset.fillna("")
    rows = [[str(c) for c in subset.columns]] + subset.astype(str).values.tolist()

    page_width = landscape(A4)[0] - 50
    col_width = page_width / len(rows[0])

    table = Table(rows, repeatRows=1, colWidths=[col_width] * len(rows[0]))
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(BRAND_DARK)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 6),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor(BRAND_BORDER)),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor(BRAND_STRIPE)]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


def generate_pdf_report(
    source_file_name: str,
    kpis: ReportKpis,
    insights: List[ReportInsight],
    filtered_df: pd.DataFrame,
    currency: str,
    date_col: Optional[str] = None,
) -> bytes:
    """Build the downloadable PDF report and return its bytes."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=landscape(A4),
        rightMargin=25, leftMargin=25, topMargin=25, bottomMargin=25,
    )
    styles = getSampleStyleSheet()
    elements = [
        Paragraph("Sales & Customer Analytics Report", styles["Title"]),
        Spacer(1, 10),
        Paragraph(f"Source File: {source_file_name}", styles["Normal"]),
        Spacer(1, 15),
        _kpi_table(kpis, currency),
        Spacer(1, 20),
        Paragraph("Business Insights", styles["Heading2"]),
    ]

    for insight in insights:
        elements.append(Paragraph(
            f"{insight.label}: {insight.name} ({currency}{insight.value:,.0f})",
            styles["Normal"],
        ))

    elements.append(Spacer(1, 15))
    elements.append(Paragraph("Filtered Sales Data", styles["Heading2"]))

    data_table = _data_table(filtered_df, date_col=date_col)
    if data_table is not None:
        elements.append(data_table)

    elements.append(Spacer(1, 15))
    elements.append(Paragraph(
        f"Report generated from {len(filtered_df):,} filtered records.", styles["Normal"],
    ))
    if len(filtered_df) > MAX_TABLE_ROWS:
        elements.append(Paragraph(
            "Note: PDF contains the first 500 filtered records. Use CSV for the complete dataset.",
            styles["Normal"],
        ))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()