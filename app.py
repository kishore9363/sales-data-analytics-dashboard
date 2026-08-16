"""
Sales & Customer Analytics — Streamlit entry point.

This module only orchestrates: it wires together file upload, the cached
data-loading pipeline in `data_loader.py`, and the rendering helpers in
`ui_components.py`. Business logic and UI building blocks live in their own
modules so each piece can be tested and reused independently.

Run with: streamlit run app.py
"""

from __future__ import annotations

import logging

import streamlit as st

import ui_components as ui
from config import APP_TITLE, CUSTOM_CSS, PAGE_ICON
from data_loader import EmptyDataError, MissingSalesColumnError, UnsupportedFileError, load_and_clean
from pdf_report import generate_pdf_report

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, page_icon=PAGE_ICON, layout="wide",
                        initial_sidebar_state="expanded")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    ui.render_header()

    uploaded_file = st.file_uploader("📁 Upload Sales Data", type=["xlsx", "csv", "json"],
                                      help="Upload Excel, CSV or JSON sales data.")
    if uploaded_file is None:
        ui.render_landing_page()
        st.stop()

    try:
        df, column_map, removed_rows = load_and_clean(uploaded_file.getvalue(), uploaded_file.name)
    except (UnsupportedFileError, EmptyDataError, MissingSalesColumnError) as error:
        logger.warning("Rejected upload %s: %s", uploaded_file.name, error)
        st.error(f"❌ {error}")
        st.stop()
    except Exception:
        logger.exception("Unexpected error while loading %s", uploaded_file.name)
        st.error("❌ Something went wrong while reading this file.")
        st.stop()

    st.success(f"✅ Successfully loaded: {uploaded_file.name}")
    if removed_rows > 0:
        st.warning(f"⚠️ {removed_rows} rows with invalid sales values were removed.")

    currency = ui.render_currency_picker()
    filtered_df = ui.render_sidebar_filters(df, column_map, uploaded_file.name)

    if filtered_df.empty:
        st.warning("⚠️ No data matches the selected filters.")
        st.stop()

    kpis = ui.compute_kpis(filtered_df, column_map)
    ui.render_kpis(kpis, currency)

    insights = ui.compute_top_insights(filtered_df, column_map)
    ui.render_insights(insights, currency)

    ui.render_tabs(filtered_df, column_map)
    ui.render_data_table(filtered_df, column_map)

    pdf_bytes = generate_pdf_report(uploaded_file.name, kpis, insights, filtered_df, currency,
                                     date_col=column_map.date)
    ui.render_downloads(filtered_df, pdf_bytes)

    st.divider()
    st.caption("Sales & Customer Analytics Dashboard | Python • Pandas • Plotly • Streamlit")


if __name__ == "__main__":
    main()