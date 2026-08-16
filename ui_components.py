"""
Streamlit rendering helpers. All Streamlit-specific UI code lives here so
`app.py` stays a thin orchestrator, and the analytical logic in
data_loader.py / charts.py / pdf_report.py stays framework-free and testable.
"""

from __future__ import annotations

from typing import List

import pandas as pd
import streamlit as st

import charts
from config import APP_SUBTITLE, APP_TITLE, CURRENCY_OPTIONS, DEFAULT_CURRENCY
from data_loader import ColumnMap
from pdf_report import ReportInsight, ReportKpis


def render_header() -> None:
    st.markdown(f'<div class="dashboard-title">{APP_TITLE}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="dashboard-subtitle">{APP_SUBTITLE}</div>', unsafe_allow_html=True)
    st.divider()


def render_landing_page() -> None:
    st.info("👆 Upload an Excel, CSV or JSON sales file to start the analysis.")
    st.markdown(
        "### 📊 Dashboard Features\n"
        "- 💰 Sales and profit analysis\n"
        "- 👥 Customer analysis\n"
        "- 🛍️ Product performance\n"
        "- 🌍 Regional performance\n"
        "- 📅 Monthly sales trends\n"
        "- 🎯 Interactive filters\n"
        "- 💡 Business insights\n"
        "- 📥 CSV download\n"
        "- 📄 PDF report download"
    )


def render_currency_picker() -> str:
    """Sidebar currency selector. Replaces the old hardcoded '₹' symbol."""
    symbols = list(CURRENCY_OPTIONS.keys())
    labels = list(CURRENCY_OPTIONS.values())
    label = st.sidebar.selectbox("💱 Currency", options=labels, index=symbols.index(DEFAULT_CURRENCY))
    return symbols[labels.index(label)]


def render_sidebar_filters(df: pd.DataFrame, column_map: ColumnMap, file_name: str) -> pd.DataFrame:
    """Render every sidebar filter and return the filtered DataFrame."""
    st.sidebar.markdown("## 🎯 Dashboard Filters")
    st.sidebar.caption(f"Dataset: {file_name}")

    filtered = df.copy()

    if column_map.customer:
        values = sorted(filtered[column_map.customer].dropna().astype(str).unique())
        selected = st.sidebar.multiselect("👤 Customer", values, default=values)
        filtered = filtered[filtered[column_map.customer].astype(str).isin(selected)]
    else:
        st.sidebar.info("👤 Customer column not detected")

    if column_map.region:
        values = sorted(filtered[column_map.region].dropna().astype(str).unique())
        selected = st.sidebar.multiselect("🌍 Region", values, default=values)
        filtered = filtered[filtered[column_map.region].astype(str).isin(selected)]

    if column_map.product:
        values = sorted(filtered[column_map.product].dropna().astype(str).unique())
        selected = st.sidebar.multiselect("🛍️ Product", values, default=values)
        filtered = filtered[filtered[column_map.product].astype(str).isin(selected)]

    if column_map.date:
        valid_dates = filtered[column_map.date].dropna()
        if not valid_dates.empty:
            min_date, max_date = valid_dates.min().date(), valid_dates.max().date()
            date_range = st.sidebar.date_input("📅 Date Range", value=(min_date, max_date),
                                                min_value=min_date, max_value=max_date)
            if len(date_range) == 2:
                start = pd.to_datetime(date_range[0])
                end = pd.to_datetime(date_range[1]) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
                filtered = filtered[(filtered[column_map.date] >= start) & (filtered[column_map.date] <= end)]

    return filtered


def compute_kpis(df: pd.DataFrame, column_map: ColumnMap) -> ReportKpis:
    """Aggregate the headline KPIs for the currently filtered DataFrame."""
    total_sales = df[column_map.sales].sum()
    total_profit = df[column_map.profit].sum() if column_map.profit else 0
    total_quantity = df[column_map.quantity].sum() if column_map.quantity else 0
    total_orders = len(df)
    total_customers = df[column_map.customer].nunique() if column_map.customer else 0
    profit_margin = (total_profit / total_sales * 100) if (column_map.profit and total_sales > 0) else 0
    return ReportKpis(total_sales, total_profit, total_quantity, total_orders, total_customers, profit_margin)


def render_kpis(kpis: ReportKpis, currency: str) -> None:
    st.markdown('<div class="section-title">📌 Key Performance Indicators</div>', unsafe_allow_html=True)
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("💰 Total Sales", f"{currency}{kpis.total_sales:,.0f}")
    k2.metric("📈 Total Profit", f"{currency}{kpis.total_profit:,.0f}")
    k3.metric("📦 Quantity", f"{kpis.total_quantity:,.0f}")
    k4.metric("🧾 Orders", f"{kpis.total_orders:,}")
    k5.metric("👥 Customers", f"{kpis.total_customers:,}")
    st.metric("💹 Profit Margin", f"{kpis.profit_margin:.2f}%")
    st.divider()


def compute_top_insights(df: pd.DataFrame, column_map: ColumnMap) -> List[ReportInsight]:
    """Compute the top customer / product / region by sales, skipping any
    field that wasn't detected in the source data."""
    insights: List[ReportInsight] = []

    for label, col in (("Top Customer", column_map.customer),
                        ("Top Product", column_map.product),
                        ("Top Region", column_map.region)):
        if not col:
            continue
        totals = df.groupby(col)[column_map.sales].sum().sort_values(ascending=False)
        if not totals.empty:
            insights.append(ReportInsight(label=label, name=str(totals.index[0]), value=float(totals.iloc[0])))

    return insights


def render_insights(insights: List[ReportInsight], currency: str) -> None:
    if not insights:
        return

    st.markdown('<div class="section-title">💡 Business Insights</div>', unsafe_allow_html=True)
    icons = {"Top Customer": "👤", "Top Product": "🏆", "Top Region": "🌍"}
    columns = st.columns(len(insights))

    for col, insight in zip(columns, insights):
        with col:
            st.markdown(
                f"""
                <div class="insight-card">
                    <div class="insight-title">{icons.get(insight.label, "💡")} {insight.label}</div>
                    <div class="insight-value">{insight.name}</div>
                    <div>Sales: {currency}{insight.value:,.0f}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.divider()


def render_sales_tab(df: pd.DataFrame, column_map: ColumnMap) -> None:
    col1, col2 = st.columns(2)

    if column_map.region:
        with col1:
            st.plotly_chart(charts.sales_by_region_chart(df, column_map.region, column_map.sales),
                             use_container_width=True)

    if column_map.date:
        fig = charts.monthly_sales_trend_chart(df, column_map.date, column_map.sales)
        if fig is not None:
            with col2:
                st.plotly_chart(fig, use_container_width=True)


def render_customer_tab(df: pd.DataFrame, column_map: ColumnMap) -> None:
    if not column_map.customer:
        st.warning("👤 Customer information was not detected.")
        st.info("Add a Customer Name, Customer ID, Client or Buyer column to enable customer analysis.")
        return

    st.subheader("👥 Customer Analysis")
    customer_data = (
        df.groupby(column_map.customer)
        .agg(Sales=(column_map.sales, "sum"), Orders=(column_map.sales, "count"))
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(charts.top_customers_chart(customer_data, column_map.customer), use_container_width=True)
    with col2:
        st.plotly_chart(charts.orders_by_customer_chart(customer_data, column_map.customer), use_container_width=True)

    st.subheader("📋 Customer Performance")
    st.dataframe(customer_data, use_container_width=True, height=350)


def render_product_tab(df: pd.DataFrame, column_map: ColumnMap) -> None:
    if not column_map.product:
        st.warning("🛍️ Product information was not detected.")
        return

    st.subheader("🛍️ Product Analysis")
    st.plotly_chart(charts.product_sales_chart(df, column_map.product, column_map.sales), use_container_width=True)


def render_profit_tab(df: pd.DataFrame, column_map: ColumnMap) -> None:
    if not column_map.profit:
        st.warning("💰 Profit column was not detected.")
        st.info("Add a Profit, Net Profit or Gross Profit column to enable profit analysis.")
        return

    st.subheader("💰 Profit Analysis")
    if column_map.category:
        st.plotly_chart(charts.profit_by_category_chart(df, column_map.category, column_map.profit),
                         use_container_width=True)
    else:
        st.info("Category information was not detected.")


def render_tabs(df: pd.DataFrame, column_map: ColumnMap) -> None:
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Sales", "👥 Customers", "🛍️ Products", "💰 Profit"])
    with tab1:
        render_sales_tab(df, column_map)
    with tab2:
        render_customer_tab(df, column_map)
    with tab3:
        render_product_tab(df, column_map)
    with tab4:
        render_profit_tab(df, column_map)


def render_data_table(df: pd.DataFrame, column_map: ColumnMap) -> None:
    """Render the filtered data table. The date column is *displayed* as a
    plain date (no time-of-day / milliseconds); the underlying DataFrame
    keeps full datetime precision for filtering and monthly aggregation."""
    st.divider()
    st.markdown('<div class="section-title">📋 Filtered Sales Data</div>', unsafe_allow_html=True)

    column_config = {}
    if column_map.date:
        column_config[column_map.date] = st.column_config.DateColumn(
            column_map.date, format="YYYY-MM-DD"
        )

    st.dataframe(df, use_container_width=True, height=400, column_config=column_config)


def render_downloads(df: pd.DataFrame, pdf_bytes: bytes) -> None:
    st.divider()
    st.markdown('<div class="section-title">📥 Download Reports</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.download_button("⬇️ Download Filtered Data (CSV)", data=df.to_csv(index=False).encode("utf-8"),
                            file_name="sales_analysis.csv", mime="text/csv", use_container_width=True)
    with col2:
        st.download_button("📄 Download Sales Report (PDF)", data=pdf_bytes,
                            file_name="sales_analysis_report.pdf", mime="application/pdf",
                            use_container_width=True)