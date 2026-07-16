# Hypothesis Testing

Significance level alpha = 0.05

## Test 1 - T-test: does discounting affect profit?

- H0: discount has no effect on line profit
- H1: discount significantly affects line profit

| | Discounted (>10%) | Full price |
|---|---|---|
| Lines | 81,040 | 922,142 |
| Mean est. profit/line | £1.16 | £5.26 |

Welch t = **-11.6**, p-value = **3.08e-31** -> **Reject H0**

**Business insight:** heavily discounted lines earn significantly less profit per line - high discounts erode margin.

## Test 2 - ANOVA: do line sales differ across categories?

- H0: all categories have the same average line revenue
- H1: at least one category differs

| category            |   mean line revenue (£) |
|:--------------------|------------------------:|
| Bags & Accessories  |                   20.43 |
| Candles & Fragrance |                   21.22 |
| Home Decor          |                   21.08 |
| Kitchen & Dining    |                   21.25 |
| Other               |                   15.6  |
| Stationery & Craft  |                   15.01 |

F = **293.4**, p-value = **7.95e-315** -> **Reject H0**

**Business insight:** categories have genuinely different revenue profiles, so category-level planning (stocking, pricing) is justified.

## Test 3 - Chi-square: is category related to customer segment?

- H0: purchase category mix is independent of customer segment
- H1: segments buy different category mixes

| category            |   Light |   Occasional |   Premium |   Regular |
|:--------------------|--------:|-------------:|----------:|----------:|
| Bags & Accessories  |    1995 |         4837 |     58622 |     12025 |
| Candles & Fragrance |    2230 |         5197 |     30298 |      9964 |
| Home Decor          |    5064 |        13805 |    117035 |     33162 |
| Kitchen & Dining    |    4182 |        11010 |     98308 |     26225 |
| Other               |    4699 |        11834 |     87371 |     26432 |
| Stationery & Craft  |    2527 |         6060 |     46191 |     14122 |

Chi2 = **3,114** (dof 15), p-value = **0.00e+00** -> **Reject H0**

**Business insight:** customer segments have distinct category preferences - targeted category promotions per segment are worthwhile.
