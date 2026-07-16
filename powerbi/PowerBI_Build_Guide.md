# Power BI Dashboard — Step-by-Step Build Guide

You do **not** need to import any data or write any DAX — that part is already
built for you. The project file already contains the 5 data tables, the
relationships between them, and ~20 ready-made measures (Total Sales, Profit
Margin, YoY %, etc.). You only place visuals on the canvas by drag-and-drop.

---

## Step 0 — Open the project (2 minutes)

1. Double-click **`powerbi/RetailIQ/RetailIQ.pbip`**. Power BI Desktop opens.
2. The model is defined but empty of data, so click **Refresh** (Home ribbon).
   It reads the CSVs from `powerbi/data/` — takes 1–2 minutes for the ~1M rows.
   - If asked about privacy levels, choose **Ignore privacy levels / Public** and OK.
   - If the files were moved, fix the path once: `Transform data ▸ Edit parameters ▸ DataFolder`.
3. Apply the custom theme: **View ▸ Themes (dropdown arrow) ▸ Browse for themes ▸
   `powerbi/RetailIQ_theme.json`**. This gives every visual the purple RetailIQ look.
4. Save. You'll see 5 empty pages at the bottom, one per dashboard.

**What's already inside** (check the Data pane on the right):

| Table | What it is |
|---|---|
| `fact_sales` | 1M+ invoice lines (sales + returns) — **all measures live here** |
| `dim_product` | 4,706 products: category, movement class, restock flag |
| `dim_customer` | 5,852 customers: RFM values + K-Means segment |
| `dim_date` | Calendar table (marked as date table) |
| `forecast_monthly` | Actuals + regression forecast from Module 5 |

> Everywhere below: **measures** (e.g. `Total Sales`) come from `fact_sales`,
> and when a chart needs a month axis use `dim_date[year_month]` (or `date`).

---

## Page 1 — Executive Dashboard (copy of the sample image)

### 1a. Slicers (top-right row)
- Insert a **Slicer**, drag `dim_date[date]` into it → it becomes a date-range slider ("Select Date Range").
- Second slicer: `fact_sales[country]` → dropdown style (this dataset's "Region").
- Third slicer: `dim_customer[segment]` → dropdown ("Segment": Premium/Regular/Occasional/Inactive).
  - Style: select slicer ▸ Format ▸ Slicer settings ▸ Style ▸ **Dropdown**.

### 1b. Five KPI cards (top row)
For each: click **Card** visual, drag the measure in, resize to a small tile.
1. `Total Sales`
2. `Total Profit`
3. `Total Orders`
4. `Total Customers`
5. `Profit Margin`

To show the green/red "vs previous period" like the sample, use the **New card**
visual and add reference labels, or simply place a small text of `Sales YoY %`
(and the other `... YoY %` measures) under each number — those measures are ready.

### 1c. Charts (match positions of the sample image)
| Sample visual | Power BI visual | Fields |
|---|---|---|
| Sales Trend Over Time | **Area chart** | X = `dim_date[year_month]`, Y = `Total Sales` |
| Sales by Category | **Donut chart** | Legend = `dim_product[category]`, Values = `Total Sales` |
| Sales by Region (map) | **Filled map** | Location = `fact_sales[country]`, Color saturation/tooltip = `Total Sales` |
| Top 10 Products by Sales | **Bar chart** | Y = `dim_product[description]`, X = `Total Sales`, then Filters pane ▸ description ▸ **Top N** = 10 by `Total Sales` |
| Profit vs Sales (scatter) | **Scatter chart** | Values = `dim_product[description]`, X = `dim_product[revenue]`, Y = `dim_product[est_profit]` |
| Sales by Segment | **Donut chart** | Legend = `dim_customer[segment]`, Values = `Total Sales` |
| Monthly Profit Trend | **Area chart** | X = `dim_date[year_month]`, Y = `Total Profit` |
| Profit by Sub-Category | **Bar chart** | Y = `dim_product[category]`, X = `Total Profit` |
| Sales by Country (Top 10) | **Bar chart** | Y = `fact_sales[country]`, X = `Total Sales`, Top N = 10 |
| Key Insights panel | **Text box** | Type the findings from `outputs/reports/` (e.g. "Premium segment drives 64% of revenue") |

> Tip: build one nice-looking card/chart first, then copy-paste it (Ctrl+C/V)
> and just swap the fields — keeps sizes consistent.

---

## Page 2 — Sales Dashboard

| Visual | Fields |
|---|---|
| **Line chart** – Monthly Sales | X = `dim_date[year_month]`, Y = `Total Sales` |
| **Column chart** – Sales by Weekday | X = `dim_date[day_name]`, Y = `Total Sales` |
| **Bar chart** – Top 10 Products | as on page 1 |
| **Bar chart** – Top 10 Customers | Y = `fact_sales[customer_id]`, X = `Total Sales`, Top N = 10 |
| **Matrix** – Sales heatmap | Rows = `dim_date[day_name]`, Columns = `dim_date[month_name]`, Values = `Total Sales`; Format ▸ Cell elements ▸ Background color = On |
| **Line chart** – Sales Forecast | X = `forecast_monthly[month]`, Y = `forecast_monthly[sales]` **and** `forecast_monthly[fitted]`, Legend optional: `kind`. Orange dashed part after Nov 2011 = the ML forecast |

---

## Page 3 — Customer Dashboard

| Visual | Fields |
|---|---|
| **Donut** – Customers per Segment | Legend = `dim_customer[segment]`, Values = Count of `customer_id` |
| **Bar** – Revenue per Segment | Y = `segment`, X = `dim_customer[lifetime_value]` (Sum) |
| **Scatter** – RFM view | X = `recency_days`, Y = `lifetime_value` (Sum), Values = `customer_id`, Legend = `segment` |
| **Histogram-style column** – Purchase Frequency | X = `dim_customer[frequency]`, Y = Count of `customer_id` |
| **Map** – Geographic distribution | Location = `dim_customer[country]`, Size = Count of `customer_id` |
| **Table** – Top customers | `customer_id`, `segment`, `frequency`, `lifetime_value`, sorted by lifetime_value desc |

---

## Page 4 — Inventory Dashboard

| Visual | Fields |
|---|---|
| **Donut** – Products by Movement | Legend = `dim_product[movement]`, Values = Count of `stock_code` |
| **Bar** – Revenue by Movement | Y = `movement`, X = `dim_product[revenue]` |
| **Bar** – Fastest movers | Y = `description`, X = `sales_velocity` (Average), Top N = 10 |
| **Table** – Restock list | `description`, `category`, `sales_velocity`, `units_sold`, `days_since_sale`; Filters pane ▸ `restock_recommended` = True |
| **Bar** – Category analysis | Y = `category`, X = `units_sold` |
| **Card** – Dead stock count | Count of `stock_code`, filter `movement` = Dormant |

---

## Page 5 — Profit Dashboard

| Visual | Fields |
|---|---|
| **Bar** – Profit by Product (Top 10) | Y = `description`, X = `Total Profit`, Top N = 10 |
| **Bar** – Profit by Country | Y = `country`, X = `Total Profit`, Top N = 10 |
| **Scatter** – Profit vs Discount | X = `Avg Discount`, Y = `Total Profit`, Values = `dim_product[description]` |
| **Area** – Monthly Profit Trend | X = `dim_date[year_month]`, Y = `Total Profit` |
| **Column** – Margin by discount band | recreate from `outputs/figures/02_margin_by_discount_band.png` or use `Avg Discount` grouping |
| **Cards** – `Total Profit`, `Profit Margin`, `Return Rate`, `Returned Value` | |

---

## Finishing touches

- **Sort month axes correctly**: `month_name` is already set to sort by
  `month_number` in the model.
- **Card icons/colors** like the sample: Insert ▸ Shapes/Image for icons, or
  keep it clean — the theme already colors everything consistently.
- **Cross-filtering** works automatically: click a category in the donut and
  every other visual filters itself.
- **Publish** (optional): Home ▸ Publish → sign in with a work/school account
  → pick a workspace → get a shareable web link.

## Troubleshooting

| Problem | Fix |
|---|---|
| "Couldn't find file" on refresh | Transform data ▸ Edit parameters ▸ set `DataFolder` to the actual `powerbi\data` folder path |
| Map shows nothing | Enable map visuals: File ▸ Options ▸ Security ▸ allow Map/Filled Map |
| YoY measures blank | They need at least a year of history in the filter window — clear date slicers |
| Refresh slow | Normal on first load (1M rows); later refreshes are only needed if CSVs change |
