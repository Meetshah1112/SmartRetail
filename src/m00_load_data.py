"""Module 0 - Load the raw Excel workbook once and cache it as parquet.

The workbook has two sheets ("Year 2009-2010", "Year 2010-2011") totalling
~1.07M invoice lines. Reading xlsx is slow, so every later module reads the
parquet cache instead.
"""
import sys
import time

import pandas as pd

from config import RAW_PARQUET, RAW_XLSX

COLUMN_RENAME = {
    "Invoice": "invoice",
    "StockCode": "stock_code",
    "Description": "description",
    "Quantity": "quantity",
    "InvoiceDate": "invoice_date",
    "Price": "unit_price",
    "Customer ID": "customer_id",
    "Country": "country",
}


def load_workbook() -> pd.DataFrame:
    if not RAW_XLSX.exists():
        sys.exit(f"ERROR: dataset not found at {RAW_XLSX}")
    sheets = pd.read_excel(RAW_XLSX, sheet_name=None, dtype={"Invoice": str, "StockCode": str})
    frames = []
    for name, frame in sheets.items():
        frame["source_sheet"] = name
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)


def main() -> None:
    start = time.time()
    df = load_workbook()
    df = df.rename(columns=COLUMN_RENAME)
    for col in ("invoice", "stock_code", "description", "country"):
        df[col] = df[col].astype("string")
    df.to_parquet(RAW_PARQUET, index=False)
    print(f"Loaded {len(df):,} rows from {len(df['source_sheet'].unique())} sheets "
          f"in {time.time() - start:.0f}s -> {RAW_PARQUET}")
    print(df.dtypes)
    print(df.head())


if __name__ == "__main__":
    main()
