"""
Plotly chart builders for the sales dashboard. Kept separate from UI code
so charts can be reused or unit tested without touching Streamlit.
"""

from __future__ import annotations

from typing import Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import BRAND_PRIMARY

# A palette that scales to however many distinct regions exist in the data,
# instead of a hardcoded {"North": ..., "South": ...} map that silently
# breaks for any dataset using different region names.
REGION_PALETTE = px.colors.qualitative.Set2


def sales_by_region_chart(df: pd.DataFrame, region_col: str, sales_col: str) -> go.Figure:
    """Bar chart of total sales per region."""
    data = (
        df.groupby(region_col)[sales_col]
        .sum()
        .reset_index()
        .sort_values(sales_col, ascending=False)
    )
    fig = px.bar(
        data, x=region_col, y=sales_col, title="🌍 Sales by Region",
        text_auto=".2s", color=region_col, color_discrete_sequence=REGION_PALETTE,
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, xaxis_title="Region", yaxis_title="Sales",
                       plot_bgcolor="white", paper_bgcolor="white")
    return fig


def monthly_sales_trend_chart(df: pd.DataFrame, date_col: str, sales_col: str) -> Optional[go.Figure]:
    """Line chart of sales aggregated by month, or None if no valid dates exist."""
    trend = df.dropna(subset=[date_col])
    if trend.empty:
        return None

    monthly = trend.groupby(trend[date_col].dt.to_period("M"))[sales_col].sum().reset_index()
    monthly["Month"] = monthly[date_col].astype(str)

    fig = px.line(monthly, x="Month", y=sales_col, markers=True, title="📅 Monthly Sales Trend")
    fig.update_traces(line=dict(width=4, color=BRAND_PRIMARY))
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
    return fig


def top_customers_chart(customer_data: pd.DataFrame, customer_col: str, top_n: int = 10) -> go.Figure:
    """Horizontal bar chart of the top N customers by sales."""
    top = customer_data.head(top_n)
    fig = px.bar(
        top, x="Sales", y=customer_col, orientation="h", title=f"🏆 Top {top_n} Customers",
        text_auto=".2s", color="Sales", color_continuous_scale="Blues",
    )
    fig.update_layout(yaxis=dict(categoryorder="total ascending"))
    return fig


def orders_by_customer_chart(customer_data: pd.DataFrame, customer_col: str, top_n: int = 10) -> go.Figure:
    """Bar chart of order counts for the top N customers."""
    top = customer_data.head(top_n)
    return px.bar(
        top, x=customer_col, y="Orders", title="🧾 Orders by Top Customers",
        text_auto=True, color="Orders", color_continuous_scale="Teal",
    )


def product_sales_chart(df: pd.DataFrame, product_col: str, sales_col: str) -> go.Figure:
    """Bar chart of total sales per product."""
    data = (
        df.groupby(product_col)[sales_col]
        .sum()
        .reset_index()
        .sort_values(sales_col, ascending=False)
    )
    fig = px.bar(
        data, x=product_col, y=sales_col, title="🏆 Product Sales Performance",
        text_auto=".2s", color=sales_col, color_continuous_scale="Teal",
    )
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
    return fig


def profit_by_category_chart(df: pd.DataFrame, category_col: str, profit_col: str) -> go.Figure:
    """Donut chart of profit share per category."""
    data = df.groupby(category_col)[profit_col].sum().reset_index()
    return px.pie(data, names=category_col, values=profit_col, title="💰 Profit by Category", hole=0.45)
