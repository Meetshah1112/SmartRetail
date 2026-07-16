# Sales Forecasting (Linear Regression)

Complete months used: **24** (Dec 2009 - Nov 2011)

## Holdout evaluation (last 3 months)

| invoice_date        |      actual |        predicted |   err_pct |
|:--------------------|------------:|-----------------:|----------:|
| 2011-09-01 00:00:00 | 1.02831e+06 | 865629           |       -16 |
| 2011-10-01 00:00:00 | 1.10331e+06 |      1.09401e+06 |        -1 |
| 2011-11-01 00:00:00 | 1.45158e+06 |      1.41219e+06 |        -3 |

| Metric | Value |
|---|---|
| MAE | £70.46K |
| MAPE | 6.5% |
| R² (train) | 0.977 |

## Forecast

| month               |   fitted |
|:--------------------|---------:|
| 2011-12-01 00:00:00 |   811911 |
| 2012-01-01 00:00:00 |   626812 |
| 2012-02-01 00:00:00 |   545864 |

Model = linear trend + month-of-year seasonality. The strong Q4 seasonal peak (Sep-Nov) dominates the pattern.
