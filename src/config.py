"""Central configuration for the SmartRetail analytics project."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_XLSX = PROJECT_ROOT / "online_retail_II.xlsx"
DATA_DIR = PROJECT_ROOT / "data" / "processed"
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"
POWERBI_DIR = PROJECT_ROOT / "powerbi" / "data"

RAW_PARQUET = DATA_DIR / "retail_raw.parquet"
CLEAN_PARQUET = DATA_DIR / "retail_clean.parquet"
RETURNS_PARQUET = DATA_DIR / "retail_returns.parquet"
RFM_CSV = DATA_DIR / "customer_rfm_segments.csv"

# --- Business assumptions (documented; dataset has no cost/discount columns) ---
# Estimated unit cost as a share of a product's reference (usual) selling price.
ASSUMED_COST_RATIO = 0.70
# Estimated fixed fulfilment/handling cost per order (GBP).
HANDLING_COST_PER_ORDER = 3.50

# --- Cleaning thresholds ---
MAX_LINE_QUANTITY = 5_000        # drop wholesale mega-outliers above this
MAX_UNIT_PRICE = 5_000.0         # drop manual/fee entries above this
NON_PRODUCT_CODES = {
    "POST", "D", "DOT", "M", "S", "C2", "CRUK", "PADS", "B",
    "AMAZONFEE", "BANK CHARGES", "TEST001", "TEST002", "ADJUST",
    "ADJUST2", "SP1002", "m", "GIFT",
}

RANDOM_STATE = 42

# Consistent chart palette (matches the purple RetailIQ dashboard look)
PALETTE = ["#6C4EE0", "#8E7CE8", "#2E9BF0", "#F0862E", "#2EBFA5",
           "#E04E7A", "#59C15D", "#B04EE0", "#4E6CE0", "#E0B04E"]
ACCENT = "#6C4EE0"

for _d in (DATA_DIR, FIGURES_DIR, REPORTS_DIR, POWERBI_DIR):
    _d.mkdir(parents=True, exist_ok=True)
