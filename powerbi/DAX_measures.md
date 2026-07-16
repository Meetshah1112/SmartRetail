# DAX Measures Reference

All measures below are **already built into** `RetailIQ.pbip` (on the
`fact_sales` table). This file documents them so you can explain each one in
your project report — or rebuild them by hand if you ever start a fresh file.

## 1 — Core KPIs

```dax
Total Sales = CALCULATE(SUM(fact_sales[revenue]), fact_sales[is_return] = FALSE())

Total Profit = CALCULATE(SUM(fact_sales[est_profit]), fact_sales[is_return] = FALSE())

Profit Margin = DIVIDE([Total Profit], [Total Sales])

Total Orders = CALCULATE(DISTINCTCOUNT(fact_sales[invoice]), fact_sales[is_return] = FALSE())

Total Customers = CALCULATE(DISTINCTCOUNT(fact_sales[customer_id]), fact_sales[is_return] = FALSE())

Total Quantity = CALCULATE(SUM(fact_sales[quantity]), fact_sales[is_return] = FALSE())

Avg Order Value = DIVIDE([Total Sales], [Total Orders])

Avg Discount = CALCULATE(AVERAGE(fact_sales[discount_pct]), fact_sales[is_return] = FALSE())
```

Why the `is_return = FALSE()` filter: the fact table contains both sales and
cancelled/return lines (flagged by `is_return`), so core KPIs count only real
sales. Returns get their own measures below.

## 2 — Time intelligence ("vs Previous Period" numbers on the KPI cards)

```dax
Sales LY = CALCULATE([Total Sales], SAMEPERIODLASTYEAR(dim_date[date]))

Sales YoY % = DIVIDE([Total Sales] - [Sales LY], [Sales LY])

Profit LY = CALCULATE([Total Profit], SAMEPERIODLASTYEAR(dim_date[date]))
Profit YoY % = DIVIDE([Total Profit] - [Profit LY], [Profit LY])

Orders LY = CALCULATE([Total Orders], SAMEPERIODLASTYEAR(dim_date[date]))
Orders YoY % = DIVIDE([Total Orders] - [Orders LY], [Orders LY])

Customers LY = CALCULATE([Total Customers], SAMEPERIODLASTYEAR(dim_date[date]))
Customers YoY % = DIVIDE([Total Customers] - [Customers LY], [Customers LY])

Margin LY = DIVIDE([Profit LY], [Sales LY])
Margin Change = [Profit Margin] - [Margin LY]
```

These work because `dim_date` is a contiguous calendar table **marked as the
date table** and related to `fact_sales[date]`.

## 3 — Returns

```dax
Returned Value = ABS(CALCULATE(SUM(fact_sales[revenue]), fact_sales[is_return] = TRUE()))

Return Rate = DIVIDE([Returned Value], [Total Sales])
```

## Data model (star schema)

```
                 dim_date (1)
                     │
                     ▼ (many)
dim_product (1) ─► fact_sales ◄─ (1) dim_customer
                     
forecast_monthly (standalone — ML output from Module 5)
```

- `fact_sales[stock_code]`  → `dim_product[stock_code]`
- `fact_sales[customer_id]` → `dim_customer[customer_id]`
- `fact_sales[date]`        → `dim_date[date]`
