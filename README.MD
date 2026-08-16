# Sales & Customer Analytics Dashboard

A Streamlit BI dashboard for sales, profit, product, region and customer
analysis, with CSV/PDF export.

## Project structure

```
sales_dashboard/
├── app.py              # Thin orchestrator: wires everything together
├── config.py            # Styling, currency options, column-detection rules
├── data_loader.py       # File parsing, column detection, cleaning (cached)
├── charts.py             # Plotly chart builders
├── pdf_report.py         # ReportLab PDF report generation
├── ui_components.py      # Streamlit rendering helpers
├── tests/
│   └── test_data_loader.py
└── requirements.txt
```

Each analytical module (`data_loader.py`, `charts.py`, `pdf_report.py`) has
no Streamlit dependency beyond a single `@st.cache_data` decorator, so the
detection/cleaning logic can be unit tested without spinning up the app.

## What changed from the single-file version

- **Formatting**: normal PEP8/black-style calls instead of one argument per
  line — same behavior, a third of the line count.
- **Modularity**: split into `config` / `data_loader` / `charts` /
  `pdf_report` / `ui_components` / `app`, each with a single responsibility.
- **Caching**: `data_loader.load_and_clean` is wrapped in `@st.cache_data`,
  keyed on the uploaded file's bytes + name, so filter changes no longer
  re-parse and re-clean the source file on every Streamlit rerun.
- **Type hints & docstrings** on every public function.
- **Configurable currency**: a sidebar picker (₹ / $ / € / £ / ¥) replaces
  the hardcoded `₹` symbol.
- **Dynamic region colors**: `charts.sales_by_region_chart` uses a
  Plotly qualitative palette sized to however many regions are present,
  instead of a hardcoded `{"North": ..., "South": ...}` map that silently
  fell back to default colors for any other region naming.
- **Fixed fragile column detection**: `find_column` now checks every
  candidate for an *exact* normalized match, across all columns, before any
  candidate is allowed to match as a whole-word/partial match — and each
  detected column is excluded from later lookups. This is what stops a
  column named e.g. "Discount Total" from being picked as the sales column
  ahead of a real "Sales" column. See
  `tests/test_data_loader.py::test_find_column_exact_match_wins_over_generic_fallback`
  for the regression test.
- **Tests**: `tests/test_data_loader.py` covers column detection (including
  the bug above) and data cleaning, no Streamlit runtime required.
- **Logging**: `logging` instead of silent failures, configured once in
  `app.py`; each module logs through its own `logging.getLogger(__name__)`.

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Run tests

```bash
pytest tests/ -v
```
