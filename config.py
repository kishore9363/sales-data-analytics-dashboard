"""
Central configuration for the Sales & Customer Analytics Dashboard.

This file contains:
- Application settings
- Currency options
- Column detection rules
- Shared brand colors
- Global Streamlit CSS
"""

from __future__ import annotations


# =========================================================
# APPLICATION
# =========================================================

APP_TITLE = "Sales & Customer Analytics"

APP_SUBTITLE = (
    "Interactive Business Intelligence Dashboard for "
    "sales, profit, products, regions and customers."
)

PAGE_ICON = "📊"


# =========================================================
# CURRENCY
# =========================================================

CURRENCY_OPTIONS = {
    "₹": "INR (₹)",
    "$": "USD ($)",
    "€": "EUR (€)",
    "£": "GBP (£)",
    "¥": "JPY (¥)",
}

DEFAULT_CURRENCY = "₹"


# =========================================================
# COLUMN DETECTION
# =========================================================

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


# =========================================================
# COLUMN DETECTION ORDER
# =========================================================

COLUMN_DETECTION_ORDER = [
    "date",
    "sales",
    "profit",
    "quantity",
    "region",
    "product",
    "category",
    "customer",
]


# =========================================================
# BRAND COLORS
# =========================================================

BRAND_PRIMARY = "#2563EB"
BRAND_DARK = "#172033"
BRAND_MUTED = "#667085"
BRAND_BORDER = "#D0D5DD"
BRAND_STRIPE = "#F8FAFC"
BRAND_TINT = "#EFF6FF"


# =========================================================
# PROFESSIONAL STREAMLIT CSS
# =========================================================

CUSTOM_CSS = """
<style>

/* =====================================================
   MAIN APPLICATION
   ===================================================== */

.stApp {
    background-color: #f5f7fb;
    color: #172033;
}

/* Main page text */
.stApp p,
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp h5,
.stApp h6 {
    color: #172033;
}


/* =====================================================
   DASHBOARD HEADER
   ===================================================== */

.dashboard-title {
    font-size: 42px;
    font-weight: 800;
    color: #172033 !important;
    margin-bottom: 5px;
}

.dashboard-subtitle {
    font-size: 17px;
    color: #667085 !important;
    margin-bottom: 20px;
}


/* =====================================================
   SECTION TITLES
   ===================================================== */

.section-title {
    color: #172033 !important;
    font-size: 24px;
    font-weight: 750;
    margin-top: 15px;
    margin-bottom: 12px;
}


/* =====================================================
   KPI METRICS
   ===================================================== */

div[data-testid="stMetric"] {
    background-color: #ffffff;
    border: 1px solid #e4e7ec;
    border-radius: 14px;
    padding: 18px 12px;
    box-shadow: 0 4px 12px rgba(16, 24, 40, 0.06);
}

div[data-testid="stMetricValue"] {
    font-size: 28px !important;
    font-weight: 700 !important;
    color: #172033 !important;
    white-space: nowrap !important;
}

div[data-testid="stMetricLabel"] {
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #667085 !important;
}


/* =====================================================
   SIDEBAR
   ===================================================== */

section[data-testid="stSidebar"] {
    background-color: #172033 !important;
}

section[data-testid="stSidebar"] > div {
    color: white;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {
    color: white !important;
}


/* =====================================================
   SIDEBAR SELECT BOX
   ===================================================== */

section[data-testid="stSidebar"] div[data-baseweb="select"] {
    background-color: #ffffff !important;
    border-radius: 8px;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] * {
    color: #172033 !important;
}


/* =====================================================
   SIDEBAR MULTISELECT
   ===================================================== */

section[data-testid="stSidebar"] div[data-baseweb="select"] span {
    color: #172033 !important;
}


/* Selected filter tags */
section[data-testid="stSidebar"] div[data-baseweb="tag"] {
    background-color: #2563EB !important;
}

section[data-testid="stSidebar"] div[data-baseweb="tag"] * {
    color: #ffffff !important;
}


/* =====================================================
   SIDEBAR DATE INPUT
   ===================================================== */

section[data-testid="stSidebar"] div[data-testid="stDateInput"] {
    color: #172033 !important;
    background-color: #ffffff !important;
    border-radius: 8px;
}

section[data-testid="stSidebar"]
div[data-testid="stDateInput"] input {
    color: #172033 !important;
    background-color: #ffffff !important;
    -webkit-text-fill-color: #172033 !important;
}


/* =====================================================
   SIDEBAR TEXT INPUT
   ===================================================== */

section[data-testid="stSidebar"] div[data-baseweb="input"] {
    background-color: #ffffff !important;
}

section[data-testid="stSidebar"]
div[data-baseweb="input"] input {
    color: #172033 !important;
    background-color: #ffffff !important;
    -webkit-text-fill-color: #172033 !important;
}

section[data-testid="stSidebar"]
div[data-baseweb="input"] svg {
    color: #172033 !important;
}


/* =====================================================
   DATE CALENDAR
   ===================================================== */

div[data-baseweb="calendar"] {
    color: #172033 !important;
    background-color: #ffffff !important;
}

div[data-baseweb="calendar"] * {
    color: #172033 !important;
}


/* =====================================================
   FILE UPLOADER
   ===================================================== */

section[data-testid="stFileUploaderDropzone"] {
    background-color: #ffffff !important;
    border: 2px dashed #2563EB !important;
    border-radius: 14px !important;
    padding: 15px !important;
}

section[data-testid="stFileUploaderDropzone"] * {
    color: #172033 !important;
}


/* Upload button */
section[data-testid="stFileUploaderDropzone"] button {
    background-color: #2563EB !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 650 !important;
}

section[data-testid="stFileUploaderDropzone"] button * {
    color: #ffffff !important;
}


/* =====================================================
   INFORMATION / WARNING / ERROR BOXES
   ===================================================== */

div[data-testid="stAlert"] {
    color: #172033 !important;
}

div[data-testid="stAlert"] p,
div[data-testid="stAlert"] span,
div[data-testid="stAlert"] div {
    color: #172033 !important;
}


/* =====================================================
   BUSINESS INSIGHTS
   ===================================================== */

.insight-card {
    background-color: #ffffff;
    border-radius: 14px;
    padding: 18px;
    border-left: 5px solid #2563EB;
    box-shadow: 0 3px 10px rgba(16, 24, 40, 0.06);
    min-height: 120px;
}

.insight-title {
    color: #667085 !important;
    font-size: 14px;
    font-weight: 600;
}

.insight-value {
    color: #172033 !important;
    font-size: 23px;
    font-weight: 750;
    margin-top: 7px;
    margin-bottom: 5px;
}

.insight-card div {
    color: #172033 !important;
}


/* =====================================================
   DOWNLOAD BUTTON
   ===================================================== */

.stDownloadButton button {
    background-color: #2563EB !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 9px !important;
    font-weight: 650 !important;
}

.stDownloadButton button:hover {
    background-color: #1D4ED8 !important;
    color: #ffffff !important;
}


/* =====================================================
   PRIMARY BUTTON
   ===================================================== */

.stButton button {
    background-color: #2563EB !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 9px !important;
    font-weight: 650 !important;
}

.stButton button:hover {
    background-color: #1D4ED8 !important;
    color: #ffffff !important;
}


/* =====================================================
   TABS
   ===================================================== */

button[data-baseweb="tab"] {
    color: #172033 !important;
    font-weight: 600 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #2563EB !important;
    font-weight: 700 !important;
}


/* =====================================================
   DATAFRAME
   ===================================================== */

div[data-testid="stDataFrame"] {
    background-color: #ffffff;
    border-radius: 12px;
}


/* =====================================================
   CAPTIONS
   ===================================================== */

[data-testid="stCaptionContainer"] {
    color: #667085 !important;
}


/* =====================================================
   EXPANDER
   ===================================================== */

[data-testid="stExpander"] {
    background-color: #ffffff;
    border: 1px solid #e4e7ec;
    border-radius: 10px;
}

[data-testid="stExpander"] * {
    color: #172033;
}


/* =====================================================
   DIVIDER
   ===================================================== */

hr {
    border-color: #e4e7ec !important;
}


/* =====================================================
   FOOTER
   ===================================================== */

footer {
    visibility: hidden;
}

</style>
"""

