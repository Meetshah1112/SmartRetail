"""Module 10 - Export compact JSON aggregates for the React dashboard webapp.

Everything the webapp shows is precomputed here from the cleaned pipeline
outputs, so the app ships a small static JSON instead of the 100MB fact table.
"""
import json

import numpy as np
import pandas as pd

from config import (CLEAN_PARQUET, DATA_DIR, PROJECT_ROOT, RETURNS_PARQUET,
                    RFM_CSV)

OUT_PATH = PROJECT_ROOT / "webapp" / "src" / "data" / "dashboard.json"

# Deterministic results captured from the Module 5/6 runs (random_state=42).
MODEL_METRICS = {
    "forecast": {"mape": 0.065, "mae": 70460, "r2Train": 0.977,
                 "algorithm": "Linear Regression (trend + monthly seasonality)"},
    "classification": {
        "logistic": {"accuracy": 0.950, "f1": 0.974},
        "tree": {"accuracy": 0.981, "f1": 0.990},
        "algorithm": "Decision Tree (max_depth=6) vs Logistic Regression",
    },
    "hypothesis": [
        {"name": "T-test: discounts vs profit", "pValue": "3.1e-31",
         "verdict": "High discounts significantly reduce line profit"},
        {"name": "ANOVA: sales across categories", "pValue": "8.0e-315",
         "verdict": "Categories have genuinely different revenue profiles"},
        {"name": "Chi-square: category vs segment", "pValue": "< 1e-300",
         "verdict": "Customer segments buy distinct category mixes"},
    ],
}

SEGMENT_ORDER = ["Premium", "Regular", "Occasional", "Inactive"]


def round_records(df: pd.DataFrame, ndigits: int = 0) -> list[dict]:
    out = df.copy()
    for col in out.select_dtypes(include=["float64", "float32"]).columns:
        out[col] = out[col].round(ndigits)
    return json.loads(out.to_json(orient="records"))


def kpis_with_delta(df: pd.DataFrame, returns: pd.DataFrame) -> dict:
    end = pd.Timestamp("2011-12-01")            # last complete month boundary
    cur = df[(df["invoice_date"] >= end - pd.DateOffset(months=12)) & (df["invoice_date"] < end)]
    prev = df[(df["invoice_date"] >= end - pd.DateOffset(months=24)) &
              (df["invoice_date"] < end - pd.DateOffset(months=12))]

    def block(part: pd.DataFrame) -> dict:
        sales = part["revenue"].sum()
        profit = part["est_profit"].sum()
        return {
            "sales": sales, "profit": profit,
            "orders": part["invoice"].nunique(),
            "customers": part["customer_id"].nunique(),
            "margin": profit / sales if sales else 0,
        }

    current, previous = block(cur), block(prev)
    total = block(df)
    deltas = {k: (current[k] - previous[k]) / previous[k] if previous[k] else 0
              for k in ("sales", "profit", "orders", "customers")}
    deltas["margin"] = current["margin"] - previous["margin"]
    return {
        "total": {**total, "aov": total["sales"] / total["orders"],
                  "returnedValue": float(returns["revenue"].abs().sum()),
                  "products": int(df["stock_code"].nunique()),
                  "countries": int(df["country"].nunique()),
                  "records": int(len(df))},
        "delta": deltas,
        "deltaWindow": "Dec 2010 – Nov 2011 vs previous 12 months",
    }


def monthly_series(df: pd.DataFrame) -> list[dict]:
    m = (df.set_index("invoice_date").resample("MS")
           .agg(sales=("revenue", "sum"), profit=("est_profit", "sum"),
                orders=("invoice", "nunique")))
    m = m.iloc[:-1]  # drop partial Dec 2011
    m.index = m.index.strftime("%b %y")
    return round_records(m.reset_index(names="month"))


def category_breakdown(df: pd.DataFrame) -> list[dict]:
    cat = (df.groupby("category")
             .agg(sales=("revenue", "sum"), profit=("est_profit", "sum"),
                  units=("quantity", "sum"))
             .sort_values("sales", ascending=False).reset_index(names="name"))
    return round_records(cat)


def top_products(df: pd.DataFrame) -> dict:
    g = df.groupby("description").agg(sales=("revenue", "sum"),
                                      profit=("est_profit", "sum"),
                                      units=("quantity", "sum"))
    top = g.nlargest(10, "sales").reset_index(names="name")
    top["name"] = top["name"].str.title()
    scatter = (g[g["sales"] > 500].sample(min(400, len(g)), random_state=42)
                 .reset_index(names="name"))
    scatter["name"] = scatter["name"].str.title()
    return {"top": round_records(top), "scatter": round_records(scatter)}


def top_customers(df: pd.DataFrame, rfm: pd.DataFrame) -> list[dict]:
    seg = rfm.set_index("customer_id")["segment"]
    g = (df.dropna(subset=["customer_id"]).groupby("customer_id")
           .agg(sales=("revenue", "sum"), orders=("invoice", "nunique"))
           .nlargest(10, "sales").reset_index())
    g["segment"] = g["customer_id"].map(seg)
    g["customer_id"] = g["customer_id"].astype(int)
    return round_records(g)


def country_breakdown(df: pd.DataFrame) -> list[dict]:
    g = (df.groupby("country")
           .agg(sales=("revenue", "sum"), customers=("customer_id", "nunique"),
                orders=("invoice", "nunique"))
           .sort_values("sales", ascending=False).head(12)
           .reset_index(names="name"))
    return round_records(g)


def time_patterns(df: pd.DataFrame) -> dict:
    dows = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    dow = (df.assign(d=df["invoice_date"].dt.dayofweek)
             .groupby("d")["revenue"].sum().reindex(range(7), fill_value=0))
    hours = (df.assign(h=df["invoice_date"].dt.hour)
               .groupby("h")["revenue"].sum())
    heat = (df.assign(d=df["invoice_date"].dt.dayofweek,
                      m=df["invoice_date"].dt.month)
              .groupby(["d", "m"])["revenue"].sum().reset_index())
    return {
        "weekday": [{"day": dows[i], "sales": round(v)} for i, v in dow.items()],
        "hourly": [{"hour": int(h), "sales": round(v)} for h, v in hours.items()],
        "heatmap": [{"day": dows[int(r.d)], "month": int(r.m), "sales": round(r.revenue)}
                    for r in heat.itertuples()],
    }


def segments(rfm: pd.DataFrame) -> dict:
    prof = (rfm.groupby("segment")
               .agg(customers=("customer_id", "size"),
                    revenue=("monetary", "sum"),
                    avgRecency=("recency_days", "mean"),
                    avgOrders=("frequency", "mean"),
                    avgSpend=("monetary", "mean"))
               .reindex(SEGMENT_ORDER).reset_index(names="name"))
    sample = pd.concat([
        part.sample(min(250, len(part)), random_state=42)
        for _, part in rfm.groupby("segment")
    ])[["recency_days", "monetary", "segment", "frequency"]]
    return {"profile": round_records(prof, 1),
            "scatter": round_records(sample.reset_index(drop=True), 1)}


def forecast_series() -> list[dict]:
    fc = pd.read_csv(DATA_DIR / "monthly_sales_forecast.csv", parse_dates=["month"])
    fc["month"] = fc["month"].dt.strftime("%b %y")
    return round_records(fc)


def inventory() -> dict:
    inv = pd.read_csv(DATA_DIR / "inventory_analysis.csv")
    movement = (inv.groupby("movement")
                   .agg(products=("stock_code", "size"), revenue=("revenue", "sum"))
                   .reindex(["Fast", "Medium", "Slow", "Dormant"])
                   .reset_index(names="name"))
    fastest = inv.nlargest(10, "sales_velocity")[
        ["description", "category", "sales_velocity", "units_sold"]].copy()
    fastest["description"] = fastest["description"].str.title()
    restock = inv[inv["restock_recommended"]].nlargest(12, "sales_velocity")[
        ["description", "category", "sales_velocity", "units_sold", "days_since_sale"]].copy()
    restock["description"] = restock["description"].str.title()
    return {
        "movement": round_records(movement),
        "fastest": round_records(fastest, 1),
        "restock": round_records(restock, 1),
        "deadStock": int((inv["movement"] == "Dormant").sum()),
        "totalProducts": int(len(inv)),
    }


def discount_bands(df: pd.DataFrame) -> list[dict]:
    bins = pd.cut(df["discount_pct"] * 100, [0, 0.01, 10, 20, 30, 50, 100],
                  labels=["None", "0-10%", "10-20%", "20-30%", "30-50%", "50%+"],
                  include_lowest=True)
    g = df.groupby(bins, observed=True).apply(
        lambda x: pd.Series({"margin": x["est_profit"].sum() / x["revenue"].sum(),
                             "sales": x["revenue"].sum()}), include_groups=False)
    return [{"band": str(i), "margin": round(r.margin, 4), "sales": round(r.sales)}
            for i, r in g.iterrows()]


def statistics_block(df: pd.DataFrame) -> dict:
    from scipy import stats as st
    ov = df.groupby("invoice")["revenue"].sum()
    lo, hi = st.t.interval(0.95, len(ov) - 1, loc=ov.mean(), scale=st.sem(ov))
    return {"meanOrder": round(ov.mean(), 2), "medianOrder": round(ov.median(), 2),
            "stdOrder": round(ov.std(), 2), "ci95": [round(lo, 2), round(hi, 2)]}


def main() -> None:
    df = pd.read_parquet(CLEAN_PARQUET)
    returns = pd.read_parquet(RETURNS_PARQUET)
    rfm = pd.read_csv(RFM_CSV)

    payload = {
        "meta": {
            "title": "RetailIQ — Retail Analytics & Business Intelligence",
            "dataset": "Online Retail II (UCI) — 1,067,371 raw transactions",
            "window": "01 Dec 2009 – 09 Dec 2011",
            "generated": pd.Timestamp.now().strftime("%d %b %Y %H:%M"),
            "currency": "GBP",
        },
        "kpis": kpis_with_delta(df, returns),
        "monthly": monthly_series(df),
        "categories": category_breakdown(df),
        "products": top_products(df),
        "topCustomers": top_customers(df, rfm),
        "countries": country_breakdown(df),
        "patterns": time_patterns(df),
        "segments": segments(rfm),
        "forecast": forecast_series(),
        "inventory": inventory(),
        "discountBands": discount_bands(df),
        "stats": statistics_block(df),
        "models": MODEL_METRICS,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, indent=1), encoding="utf-8")
    print(f"Wrote {OUT_PATH} ({OUT_PATH.stat().st_size / 1e3:.0f} KB)")


if __name__ == "__main__":
    main()
