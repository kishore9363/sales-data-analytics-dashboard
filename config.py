"""
Central configuration for the Sales & Customer Analytics dashboard.

Keeping styling, currency options and column-detection rules here keeps
`app.py` and the other modules free of magic strings and inline CSS.
"""

from __future__ import annotations

APP_TITLE = "Sales & Customer Analytics"
APP_SUBTITLE = (
    "Interactive Business Intelligence Dashboard for "
    "sales, profit, products, regions and customers."
)
PAGE_ICON = "📊"

# Symbol -> human readable label, shown in the sidebar currency picker.
CURRENCY_OPTIONS = {
    "₹": "INR (₹)",
    "$": "USD ($)",
    "€": "EUR (€)",
    "£": "GBP (£)",
    "¥": "JPY (¥)",
}
DEFAULT_CURRENCY = "₹"

# Ordered, most-specific-first. `data_loader.find_column` checks every
# candidate for an *exact* normalized match before any candidate is allowed
# to match as a partial/whole-word match. That ordering is what stops a
# generic fallback term (e.g. "total") from grabbing an unrelated column
# (e.g. "Discount Total") when a precise column (e.g. "Sales") also exists.
COLUMN_CANDIDATES: dict[str, list[str]] = {
    "date": [
        "order date",
        "sales date",
        "invoice date",
        "transaction date",
        "date",
    ],
    "sales": [
        "total sales",
        "sales amount",
        "sales value",
        "net sales",
        "revenue",
        "sales",
        "amount",
        "total",
    ],
    "profit": [
        "net profit",
        "gross profit",
        "profit",
    ],
    "quantity": [
        "units sold",
        "quantity sold",
        "qty",
        "quantity",
        "units",
    ],
    "region": [
        "region",
        "state",
        "province",
        "zone",
        "area",
    ],
    "product": [
        "product name",
        "product",
        "item name",
        "item",
    ],
    "category": [
        "product category",
        "category",
        "type",
    ],
    "customer": [
        "customer name",
        "customer",
        "client name",
        "client",
        "buyer name",
        "buyer",
        "customer id",
        "client id",
    ],
}

# Order in which fields are detected. Each field excludes columns already
# claimed by an earlier field so the same column can't be reused twice.
COLUMN_DETECTION_ORDER = [
    "date", "sales", "profit", "quantity",
    "region", "product", "category", "customer",
]

# Shared brand palette, reused by charts.py and pdf_report.py.
BRAND_PRIMARY = "#2563EB"
BRAND_DARK = "#172033"
BRAND_MUTED = "#667085"
BRAND_BORDER = "#D0D5DD"
BRAND_STRIPE = "#F8FAFC"
BRAND_TINT = "#EFF6FF"

CUSTOM_CSS = """
<style>
.stApp { background-color: #f5f7fb; }

.dashboard-title { font-size: 42px; font-weight: 800; color: #172033; }
.dashboard-subtitle { font-size: 17px; color: #667085; margin-bottom: 20px; }

div[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #e4e7ec;
    border-radius: 14px;
    padding: 18px 12px;
    box-shadow: 0 4px 12px rgba(16, 24, 40, 0.06);
}
div[data-testid="stMetricValue"] { font-size: 28px !important; font-weight: 700 !important; color: #172033 !important; white-space: nowrap !important; }
div[data-testid="stMetricLabel"] { font-size: 14px !important; font-weight: 600 !important; color: #667085 !important; }

section[data-testid="stSidebar"] { background-color: #172033; }
section[data-testid="stSidebar"] > div { color: white; }
section[data-testid="stSidebar"] label { color: white !important; }

section[data-testid="stSidebar"] div[data-baseweb="select"] { background-color: white !important; }
section[data-testid="stSidebar"] div[data-baseweb="select"] * { color: #172033 !important; }

section[data-testid="stSidebar"] div[data-testid="stDateInput"] { color: #172033 !important; }
section[data-testid="stSidebar"] div[data-testid="stDateInput"] input { color: #172033 !important; background-color: white !important; -webkit-text-fill-color: #172033 !important; }

section[data-testid="stSidebar"] div[data-baseweb="input"] { background-color: white !important; }
section[data-testid="stSidebar"] div[data-baseweb="input"] input { color: #172033 !important; background-color: white !important; -webkit-text-fill-color: #172033 !important; }
section[data-testid="stSidebar"] div[data-baseweb="input"] svg { color: #172033 !important; }

div[data-baseweb="calendar"] { color: #172033 !important; background-color: white !important; }
div[data-baseweb="calendar"] * { color: #172033 !important; }

.section-title { color: #172033; font-size: 24px; font-weight: 750; margin-top: 15px; margin-bottom: 12px; }

.insight-card { background-color: white; border-radius: 14px; padding: 18px; border-left: 5px solid #2563EB; box-shadow: 0 3px 10px rgba(16, 24, 40, 0.06); min-height: 120px; }
.insight-title { color: #667085; font-size: 14px; font-weight: 600; }
.insight-value { color: #172033; font-size: 23px; font-weight: 750; margin-top: 7px; margin-bottom: 5px; }

.stDownloadButton button { background-color: #2563EB; color: white; border: none; border-radius: 9px; font-weight: 650; }
.stDownloadButton button:hover { background-color: #1D4ED8; color: white; }

section[data-testid="stFileUploaderDropzone"] { border: 2px dashed #2563EB; border-radius: 14px; }

footer { visibility: hidden; }
</style>
"""
