"""Module 9 - Export a Power BI-ready star schema to powerbi/data/.

Tables:
  fact_sales.csv        one row per invoice line (sales + returns flagged)
  dim_product.csv       product attributes + inventory metrics
  dim_customer.csv      customer attributes + RFM segment
  dim_date.csv          calendar covering the data + forecast horizon
  forecast_monthly.csv  actuals, model fit and 3-month forecast
"""
import pandas as pd

from config import (CLEAN_PARQUET, DATA_DIR, POWERBI_DIR, RETURNS_PARQUET,
                    RFM_CSV)

FACT_COLUMNS = ["invoice", "invoice_date", "stock_code", "customer_id", "country",
                "quantity", "unit_price", "revenue", "discount_pct", "est_profit",
                "is_return"]


def export_fact() -> pd.DataFrame:
    sales = pd.read_parquet(CLEAN_PARQUET).assign(is_return=False)
    returns = pd.read_parquet(RETURNS_PARQUET).assign(is_return=True)
    returns = returns[returns["stock_code"].str.match(r"^\d{5}[A-Z]*$", na=False)]
    fact = pd.concat([sales, returns], ignore_index=True)
    fact["date"] = fact["invoice_date"].dt.date
    fact = fact[FACT_COLUMNS + ["date"]]
    fact.to_csv(POWERBI_DIR / "fact_sales.csv", index=False)
    return fact


def export_dim_product() -> None:
    inv = pd.read_csv(DATA_DIR / "inventory_analysis.csv")
    inv.to_csv(POWERBI_DIR / "dim_product.csv", index=False)


def export_dim_customer() -> None:
    rfm = pd.read_csv(RFM_CSV)
    rfm["customer_id"] = rfm["customer_id"].astype(int)
    rfm.rename(columns={"monetary": "lifetime_value"}).to_csv(
        POWERBI_DIR / "dim_customer.csv", index=False)


def export_dim_date(fact: pd.DataFrame) -> None:
    start = pd.Timestamp(fact["invoice_date"].min().date())
    end = pd.Timestamp(fact["invoice_date"].max().date()) + pd.DateOffset(months=4)
    dates = pd.date_range(start, end, freq="D")
    dim = pd.DataFrame({
        "date": dates.date,
        "year": dates.year,
        "quarter": "Q" + dates.quarter.astype(str),
        "month_number": dates.month,
        "month_name": dates.strftime("%b"),
        "year_month": dates.strftime("%Y-%m"),
        "week": dates.isocalendar().week,
        "day_name": dates.strftime("%a"),
        "is_weekend": dates.dayofweek >= 5,
    })
    dim.to_csv(POWERBI_DIR / "dim_date.csv", index=False)


def export_forecast() -> None:
    fc = pd.read_csv(DATA_DIR / "monthly_sales_forecast.csv")
    fc.to_csv(POWERBI_DIR / "forecast_monthly.csv", index=False)


def main() -> None:
    fact = export_fact()
    export_dim_product()
    export_dim_customer()
    export_dim_date(fact)
    export_forecast()
    for f in sorted(POWERBI_DIR.glob("*.csv")):
        print(f"{f.name:>24}  {f.stat().st_size / 1e6:8.1f} MB")


if __name__ == "__main__":
    main()
