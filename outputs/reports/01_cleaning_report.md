# Data Cleaning Report

Raw rows: **1,067,371**

Duplicate rows removed: **34,337**

Cancelled/return lines split off: **22,497**

Non-product lines removed (postage, fees, manual, price<=0): **7,325**

Extreme outliers removed (qty>5,000 or price>5,000): **30**

Rows with missing Customer ID kept but flagged as guest checkout: **226,637** (22.6%)


Clean sales rows: **1,003,182**

Date range: 01 Dec 2009 to 09 Dec 2011

Unique products: 4,706 | Unique customers: 5,852 | Countries: 43


## Category distribution

| category             |   rows |
|:---------------------|-------:|
| Home Decor           | 212699 |
| Kitchen & Dining     | 179516 |
| Other                | 172037 |
| Bags & Accessories   | 102043 |
| Stationery & Craft   |  87877 |
| Candles & Fragrance  |  60350 |
| Christmas & Seasonal |  50596 |
| Garden & Outdoor     |  36531 |
| Toys & Games         |  34749 |
| Vintage & Retro      |  28948 |
| Jewellery            |  24544 |
| Lighting             |  13292 |


## Assumptions

- Reference price = median observed price per product

- Estimated unit cost = 70% of reference price

- Discount % = shortfall of the sold price vs reference price

- Estimated profit = (unit price - est. cost) x quantity
