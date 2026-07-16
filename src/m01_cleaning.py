"""Module 1 - Data cleaning.

Steps (mirrors the project brief):
  1. Fix data types and standardize column values.
  2. Backfill missing product descriptions from other rows of the same product.
  3. Remove duplicate rows.
  4. Split off cancelled orders / returns (invoice starts with 'C' or qty < 0).
  5. Remove non-product rows (postage, fees, manual adjustments, bad prices).
  6. Handle extreme outliers.
  7. Derive business columns the raw data lacks:
       revenue, reference price, discount %, estimated unit cost,
       estimated profit, product category (keyword mapping).

Assumptions (the raw data has no cost/discount columns):
  * reference price  = median unit price observed for that product
  * discount %       = how far below reference price a line was sold
  * estimated cost   = ASSUMED_COST_RATIO x reference price
  * estimated profit = (unit price - estimated cost) x quantity
"""
import re

import numpy as np
import pandas as pd

from config import (ASSUMED_COST_RATIO, CLEAN_PARQUET, MAX_LINE_QUANTITY,
                    MAX_UNIT_PRICE, NON_PRODUCT_CODES, RAW_PARQUET,
                    REPORTS_DIR, RETURNS_PARQUET)

# Keyword -> category mapping. First match wins (order matters).
CATEGORY_RULES = [
    ("Christmas & Seasonal", r"CHRISTMAS|XMAS|SANTA|REINDEER|ADVENT|EASTER|HALLOWEEN|VALENTINE"),
    ("Candles & Fragrance", r"CANDLE|T-LIGHT|TLIGHT|INCENSE|SCENT|FRAGRANCE|OIL BURNER"),
    ("Kitchen & Dining", r"MUG|CUP |TEACUP|BOWL|PLATE|TEAPOT|TEA SET|COFFEE|CAKE|BAKING|"
                         r"JAM |LUNCH BOX|CUTLERY|TRAY|JUG|SAUCER|NAPKIN|BREAD BIN|EGG|KITCHEN|BOTTLE"),
    ("Bags & Accessories", r"BAG|PURSE|WALLET|UMBRELLA|SCARF|HANDBAG|PASSPORT|JEWELLERY ROLL"),
    ("Jewellery", r"NECKLACE|BRACELET|EARRING|RING |BROOCH|JEWEL|BEAD|HAIR "),
    ("Toys & Games", r"TOY|GAME|PLAYHOUSE|PUZZLE|SPACEBOY|DOLL|JIGSAW|SKIPPING|"
                     r"SOLDIER|KNITTED|BINGO|DOMINO"),
    ("Stationery & Craft", r"CARD |CARDS|WRAP|PAPER|PEN |PENS|PENCIL|NOTEBOOK|JOURNAL|"
                           r"STICKER|TAPE|CRAFT|CHALK|BOOK |ENVELOPE|GIFT TAG"),
    ("Garden & Outdoor", r"GARDEN|PLANT|WATERING|BIRD|PARASOL|PICNIC|THERMOMETER|OUTDOOR"),
    ("Lighting", r"LIGHT|LAMP|LANTERN|NIGHTLIGHT"),
    ("Home Decor", r"HEART|FRAME|SIGN|WICKER|DECORATION|CUSHION|DOORMAT|CLOCK|DRAWER|"
                   r"SHELF|MIRROR|VASE|HOOK|BUNTING|WALL|HANGING|ORNAMENT|TIN |TINS|BOX"),
    ("Vintage & Retro", r"VINTAGE|RETRO|REGENCY|ANTIQUE"),
]


def standardize(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["invoice"] = out["invoice"].astype(str).str.strip()
    out["stock_code"] = out["stock_code"].astype(str).str.strip().str.upper()
    out["description"] = out["description"].astype("string").str.strip().str.upper()
    out["invoice_date"] = pd.to_datetime(out["invoice_date"])
    out["customer_id"] = out["customer_id"].astype("Int64")
    out["country"] = out["country"].astype("string").str.strip()
    return out


def backfill_descriptions(df: pd.DataFrame) -> pd.DataFrame:
    lookup = (df.dropna(subset=["description"])
                .groupby("stock_code")["description"]
                .agg(lambda s: s.mode().iat[0]))
    out = df.copy()
    missing = out["description"].isna()
    out.loc[missing, "description"] = out.loc[missing, "stock_code"].map(lookup)
    return out


def split_returns(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    is_return = df["invoice"].str.startswith("C") | (df["quantity"] < 0)
    return df[~is_return].copy(), df[is_return].copy()


def drop_non_products(df: pd.DataFrame) -> pd.DataFrame:
    is_fee_code = df["stock_code"].isin({c.upper() for c in NON_PRODUCT_CODES})
    # real products have stock codes like 85123A / 22423 (5 digits + optional letters)
    looks_like_product = df["stock_code"].str.match(r"^\d{5}[A-Z]*$", na=False)
    keep = looks_like_product & ~is_fee_code & (df["unit_price"] > 0)
    return df[keep].copy()


def drop_outliers(df: pd.DataFrame) -> pd.DataFrame:
    keep = (df["quantity"] <= MAX_LINE_QUANTITY) & (df["unit_price"] <= MAX_UNIT_PRICE)
    return df[keep].copy()


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["revenue"] = out["quantity"] * out["unit_price"]

    ref_price = out.groupby("stock_code")["unit_price"].transform("median")
    out["reference_price"] = ref_price
    out["discount_pct"] = ((ref_price - out["unit_price"]) / ref_price).clip(lower=0.0)

    unit_cost = ASSUMED_COST_RATIO * ref_price
    out["est_unit_cost"] = unit_cost
    out["est_profit"] = (out["unit_price"] - unit_cost) * out["quantity"]

    out["is_guest"] = out["customer_id"].isna()
    out["year"] = out["invoice_date"].dt.year
    out["month"] = out["invoice_date"].dt.to_period("M").astype(str)
    return out


def assign_category(description: str) -> str:
    if not isinstance(description, str):
        return "Other"
    for name, pattern in CATEGORY_RULES:
        if re.search(pattern, description):
            return name
    return "Other"


def add_categories(df: pd.DataFrame) -> pd.DataFrame:
    unique_desc = df["description"].dropna().unique()
    mapping = {d: assign_category(d) for d in unique_desc}
    out = df.copy()
    out["category"] = out["description"].map(mapping).fillna("Other")
    return out


def main() -> None:
    raw = pd.read_parquet(RAW_PARQUET)
    report = [f"# Data Cleaning Report\n", f"Raw rows: **{len(raw):,}**\n"]

    df = standardize(raw)
    df = backfill_descriptions(df)

    before = len(df)
    df = df.drop_duplicates(subset=["invoice", "stock_code", "quantity",
                                    "invoice_date", "unit_price", "customer_id"])
    report.append(f"Duplicate rows removed: **{before - len(df):,}**\n")

    df, returns = split_returns(df)
    report.append(f"Cancelled/return lines split off: **{len(returns):,}**\n")

    before = len(df)
    df = drop_non_products(df)
    report.append(f"Non-product lines removed (postage, fees, manual, price<=0): "
                  f"**{before - len(df):,}**\n")

    before = len(df)
    df = drop_outliers(df)
    report.append(f"Extreme outliers removed (qty>{MAX_LINE_QUANTITY:,} or "
                  f"price>{MAX_UNIT_PRICE:,.0f}): **{before - len(df):,}**\n")

    df = add_derived_columns(df)
    df = add_categories(df)
    returns = add_derived_columns(add_categories(
        backfill_descriptions(standardize(returns))))

    missing_ids = int(df["is_guest"].sum())
    report += [
        f"Rows with missing Customer ID kept but flagged as guest checkout: "
        f"**{missing_ids:,}** ({missing_ids / len(df):.1%})\n",
        f"\nClean sales rows: **{len(df):,}**\n",
        f"Date range: {df['invoice_date'].min():%d %b %Y} to "
        f"{df['invoice_date'].max():%d %b %Y}\n",
        f"Unique products: {df['stock_code'].nunique():,} | "
        f"Unique customers: {df['customer_id'].nunique():,} | "
        f"Countries: {df['country'].nunique()}\n",
        "\n## Category distribution\n",
        df["category"].value_counts().to_frame("rows").to_markdown(),
        "\n\n## Assumptions\n",
        f"- Reference price = median observed price per product\n",
        f"- Estimated unit cost = {ASSUMED_COST_RATIO:.0%} of reference price\n",
        f"- Discount % = shortfall of the sold price vs reference price\n",
        f"- Estimated profit = (unit price - est. cost) x quantity\n",
    ]

    df.to_parquet(CLEAN_PARQUET, index=False)
    returns.to_parquet(RETURNS_PARQUET, index=False)
    (REPORTS_DIR / "01_cleaning_report.md").write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report))


if __name__ == "__main__":
    main()
