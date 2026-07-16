# Customer Segmentation (RFM + K-Means)

Customers clustered: **5,852** (guest checkouts excluded)

## Segment profile

| segment    |   customers |   avg_recency_days |   avg_orders |   avg_spend |    total_revenue |
|:-----------|------------:|-------------------:|-------------:|------------:|-----------------:|
| Premium    |        1186 |               27.7 |         19.2 |     10400.5 |      1.2335e+07  |
| Regular    |        1454 |              228   |          5.1 |      1905.8 |      2.77108e+06 |
| Occasional |        1249 |               28.4 |          3   |       839.3 |      1.04834e+06 |
| Inactive   |        1963 |              393.4 |          1.4 |       315.5 | 619414           |

## Reading the segments

- **Premium** - recent, frequent, high-spend. Protect with VIP service.
- **Regular** - steady repeat buyers. Grow with cross-sell.
- **Occasional** - infrequent, lower spend. Nurture with campaigns.
- **Inactive** - long-lapsed. Win-back offers or let churn.


Output written to `customer_rfm_segments.csv` for the Power BI customer dashboard.
