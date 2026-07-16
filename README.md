# SmartRetail — Retail Analytics, Forecasting & Customer Segmentation

End-to-end data science project on the **Online Retail II** dataset
(1,067,371 real e-commerce transactions, Dec 2009 – Dec 2011), ending in a
5-page Power BI dashboard.

## Project pipeline

```
online_retail_II.xlsx  →  Cleaning  →  EDA  →  Statistics  →  Hypothesis tests
      →  Regression forecast  →  Classification  →  K-Means segmentation
      →  Inventory analysis  →  Power BI star schema  →  Dashboards
```

## How to run everything

```powershell
py -m pip install -r requirements.txt
cd src
py m00_load_data.py        # one-off: xlsx → parquet cache (~1–2 min)
py m01_cleaning.py         # Module 1: cleaning + derived columns
py m02_eda.py              # Module 2: EDA charts + KPI summary
py m03_statistics.py       # Module 3: mean/median/mode, dispersion, 95% CI
py m04_hypothesis.py       # Module 4: t-test, ANOVA, chi-square
py m05_regression.py       # Module 5: linear-regression sales forecast
py m06_classification.py   # Module 6: profitable-order classifiers
py m07_segmentation.py     # Module 7: RFM + K-Means segments
py m08_inventory.py        # Module 8: sales velocity, restock, dead stock
py m09_powerbi_export.py   # Module 9: star-schema CSVs for Power BI
py m10_webapp_export.py    # Module 10: JSON aggregates for the React webapp
```

Outputs land in:

| Folder | Contents |
|---|---|
| `outputs/figures/` | Every chart (PNG) |
| `outputs/reports/` | Markdown result reports per module |
| `powerbi/data/` | fact_sales, dim_product, dim_customer, dim_date, forecast_monthly |
| `powerbi/RetailIQ/` | **Ready-made Power BI project** (open `RetailIQ.pbip`) |
| `webapp/` | **React dashboard webapp** (`cd webapp && npm run dev`) — 8 pages, light/dark |

## Headline results

| KPI | Value |
|---|---|
| Total sales | £19.35M |
| Estimated profit | £4.95M (25.6% margin) |
| Orders | 39,511 |
| Customers | 5,852 |
| Avg order value | £490 (95% CI: £479–£501) |
| Forecast accuracy | 6.5% MAPE on 3-month holdout |
| Best classifier | Decision Tree, 98.1% accuracy |
| Segments | Premium 1,186 customers → 64% of revenue |

## Dataset adaptation (important, be honest about this in your write-up)

The raw data has no *Profit*, *Discount*, *Category* or *Segment* columns, so
the project **derives** them:

- **Reference price** = median observed price per product
- **Discount %** = how far below its reference price a line was sold
- **Estimated unit cost** = 70% of reference price (assumption)
- **Estimated profit** = (price − est. cost) × quantity, minus £3.50/order
  handling in the classification module
- **Category** = keyword mapping over product descriptions (12 groups)
- **Segment** = K-Means clusters on RFM features (Premium/Regular/Occasional/Inactive)

## Power BI

Open `powerbi/RetailIQ/RetailIQ.pbip` in Power BI Desktop, press **Refresh**,
then follow `powerbi/PowerBI_Build_Guide.md` — the data model, relationships
and all DAX measures are pre-built; you only drag visuals onto the canvas.
