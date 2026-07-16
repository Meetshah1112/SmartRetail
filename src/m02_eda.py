"""Module 2 - Exploratory Data Analysis.

Answers the business questions from the brief (sales, profit, products,
customers, regions, discounts) and saves every chart to outputs/figures.
"""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from config import ACCENT, CLEAN_PARQUET, PALETTE, REPORTS_DIR, RETURNS_PARQUET
from plotting import init_style, money, save_fig


def kpi_summary(df: pd.DataFrame, returns: pd.DataFrame) -> list[str]:
    total_sales = df["revenue"].sum()
    total_profit = df["est_profit"].sum()
    lines = [
        "# EDA Summary\n",
        f"| KPI | Value |\n|---|---|",
        f"| Total Sales | {money(total_sales)} |",
        f"| Estimated Profit | {money(total_profit)} |",
        f"| Profit Margin | {total_profit / total_sales:.1%} |",
        f"| Orders | {df['invoice'].nunique():,} |",
        f"| Customers (identified) | {df['customer_id'].nunique():,} |",
        f"| Products | {df['stock_code'].nunique():,} |",
        f"| Avg Order Value | {money(df.groupby('invoice')['revenue'].sum().mean())} |",
        f"| Return/cancel lines | {len(returns):,} |",
        f"| Returned value | {money(returns['revenue'].abs().sum())} |",
    ]
    return lines


def plot_monthly_trend(df: pd.DataFrame) -> None:
    monthly = df.groupby("month")[["revenue", "est_profit"]].sum().reset_index()
    fig, ax = plt.subplots()
    ax.plot(monthly["month"], monthly["revenue"] / 1e3, marker="o", color=ACCENT, lw=2)
    ax.fill_between(monthly["month"], monthly["revenue"] / 1e3, alpha=0.15, color=ACCENT)
    ax.set_title("Monthly Sales Trend")
    ax.set_ylabel("Sales (£K)")
    ax.tick_params(axis="x", rotation=60)
    save_fig(fig, "02_monthly_sales_trend")

    fig, ax = plt.subplots()
    ax.plot(monthly["month"], monthly["est_profit"] / 1e3, marker="o", color="#2EBFA5", lw=2)
    ax.fill_between(monthly["month"], monthly["est_profit"] / 1e3, alpha=0.15, color="#2EBFA5")
    ax.set_title("Monthly Estimated Profit Trend")
    ax.set_ylabel("Profit (£K)")
    ax.tick_params(axis="x", rotation=60)
    save_fig(fig, "02_monthly_profit_trend")


def plot_category_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    cat = (df.groupby("category")[["revenue", "est_profit"]].sum()
             .sort_values("revenue", ascending=False))
    fig, ax = plt.subplots(figsize=(9, 6))
    top = cat.head(10)
    ax.pie(top["revenue"], labels=top.index, autopct="%1.1f%%",
           colors=PALETTE, pctdistance=0.8, wedgeprops={"width": 0.45})
    ax.set_title("Sales by Category")
    save_fig(fig, "02_sales_by_category")
    return cat


def plot_top_products(df: pd.DataFrame) -> pd.DataFrame:
    prod = (df.groupby("description")["revenue"].sum()
              .sort_values(ascending=False))
    fig, ax = plt.subplots()
    top10 = prod.head(10).iloc[::-1]
    ax.barh([d[:32] for d in top10.index], top10.values / 1e3, color=ACCENT)
    ax.set_title("Top 10 Products by Sales")
    ax.set_xlabel("Sales (£K)")
    save_fig(fig, "02_top10_products")
    return prod


def plot_top_customers(df: pd.DataFrame) -> pd.DataFrame:
    cust = (df.dropna(subset=["customer_id"])
              .groupby("customer_id")["revenue"].sum()
              .sort_values(ascending=False))
    fig, ax = plt.subplots()
    top10 = cust.head(10).iloc[::-1]
    ax.barh([f"Customer {int(c)}" for c in top10.index], top10.values / 1e3, color="#2E9BF0")
    ax.set_title("Top 10 Customers by Sales")
    ax.set_xlabel("Sales (£K)")
    save_fig(fig, "02_top10_customers")
    return cust


def plot_country_analysis(df: pd.DataFrame) -> pd.DataFrame:
    ctry = df.groupby("country")["revenue"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots()
    top10 = ctry.head(10).iloc[::-1]
    ax.barh(top10.index, top10.values / 1e3, color=PALETTE[2])
    ax.set_title("Sales by Country (Top 10)")
    ax.set_xlabel("Sales (£K)")
    save_fig(fig, "02_sales_by_country")

    non_uk = ctry.drop("United Kingdom", errors="ignore")
    fig, ax = plt.subplots()
    top10 = non_uk.head(10).iloc[::-1]
    ax.barh(top10.index, top10.values / 1e3, color=PALETTE[3])
    ax.set_title("Sales by Country excl. UK (Top 10)")
    ax.set_xlabel("Sales (£K)")
    save_fig(fig, "02_sales_by_country_excl_uk")
    return ctry


def plot_time_patterns(df: pd.DataFrame) -> None:
    dow = (df.assign(dow=df["invoice_date"].dt.day_name())
             .groupby("dow")["revenue"].sum()
             .reindex(["Monday", "Tuesday", "Wednesday", "Thursday",
                       "Friday", "Saturday", "Sunday"]))
    fig, ax = plt.subplots()
    ax.bar(dow.index, dow.values / 1e3, color=PALETTE[:7])
    ax.set_title("Sales by Day of Week")
    ax.set_ylabel("Sales (£K)")
    save_fig(fig, "02_sales_by_weekday")

    hourly = (df.assign(hour=df["invoice_date"].dt.hour)
                .groupby("hour")["revenue"].sum())
    fig, ax = plt.subplots()
    ax.bar(hourly.index, hourly.values / 1e3, color=ACCENT)
    ax.set_title("Sales by Hour of Day")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Sales (£K)")
    save_fig(fig, "02_sales_by_hour")


def plot_discount_analysis(df: pd.DataFrame) -> None:
    sample = df[df["discount_pct"] > 0].sample(min(20_000, (df["discount_pct"] > 0).sum()),
                                               random_state=42)
    fig, ax = plt.subplots()
    ax.scatter(sample["discount_pct"] * 100, sample["est_profit"],
               s=6, alpha=0.25, color=ACCENT)
    ax.axhline(0, color="red", lw=1, ls="--")
    ax.set_title("Discount vs Estimated Profit (line level)")
    ax.set_xlabel("Implied discount (%)")
    ax.set_ylabel("Estimated profit (£)")
    ax.set_ylim(-300, 300)
    save_fig(fig, "02_discount_vs_profit")

    bins = pd.cut(df["discount_pct"] * 100, [0, 0.01, 10, 20, 30, 50, 100],
                  labels=["No discount", "0-10%", "10-20%", "20-30%", "30-50%", "50%+"],
                  include_lowest=True)
    margin = df.groupby(bins, observed=True).apply(
        lambda g: g["est_profit"].sum() / g["revenue"].sum(), include_groups=False)
    fig, ax = plt.subplots()
    colors = ["#2EBFA5" if v > 0 else "#E04E7A" for v in margin.values]
    ax.bar(margin.index.astype(str), margin.values * 100, color=colors)
    ax.set_title("Profit Margin by Discount Band")
    ax.set_ylabel("Margin (%)")
    save_fig(fig, "02_margin_by_discount_band")


def main() -> None:
    init_style()
    df = pd.read_parquet(CLEAN_PARQUET)
    returns = pd.read_parquet(RETURNS_PARQUET)

    lines = kpi_summary(df, returns)
    plot_monthly_trend(df)
    cat = plot_category_breakdown(df)
    prod = plot_top_products(df)
    cust = plot_top_customers(df)
    ctry = plot_country_analysis(df)
    plot_time_patterns(df)
    plot_discount_analysis(df)

    lines += [
        "\n## Top 5 categories by sales\n",
        cat.head(5).to_markdown(floatfmt=",.0f"),
        "\n## Best / worst sellers\n",
        f"- Best seller: **{prod.index[0]}** ({money(prod.iloc[0])})",
        f"- Weakest seller: **{prod.index[-1]}** ({money(prod.iloc[-1])})",
        f"\n## Top customer\n- Customer {int(cust.index[0])}: {money(cust.iloc[0])}",
        "\n## Regions\n",
        f"- Best market: **{ctry.index[0]}** ({money(ctry.iloc[0])})",
        f"- Top market outside UK: "
        f"**{ctry.drop('United Kingdom', errors='ignore').index[0]}**",
        f"\n## Discounts\n- Average implied discount: {df['discount_pct'].mean():.1%}",
        f"- Lines sold below reference price: {(df['discount_pct'] > 0).mean():.1%}",
    ]
    (REPORTS_DIR / "02_eda_summary.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
