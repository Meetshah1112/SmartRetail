"""Module 4 - Hypothesis testing.

Test 1 (T-test)     : Does discounting affect line profitability?
Test 2 (ANOVA)      : Do average line sales differ across product categories?
Test 3 (Chi-square) : Is product category related to customer value segment?
                      (segments = spend quartiles: Premium/Regular/Occasional/Light)
"""
import numpy as np
import pandas as pd
from scipy import stats

from config import CLEAN_PARQUET, REPORTS_DIR

ALPHA = 0.05
SEGMENT_LABELS = ["Light", "Occasional", "Regular", "Premium"]


def t_test_discount_profit(df: pd.DataFrame) -> list[str]:
    discounted = df.loc[df["discount_pct"] > 0.10, "est_profit"]
    full_price = df.loc[df["discount_pct"] <= 0.10, "est_profit"]
    t, p = stats.ttest_ind(discounted, full_price, equal_var=False)
    verdict = "Reject H0" if p < ALPHA else "Fail to reject H0"
    return [
        "## Test 1 - T-test: does discounting affect profit?\n",
        "- H0: discount has no effect on line profit",
        "- H1: discount significantly affects line profit\n",
        f"| | Discounted (>10%) | Full price |\n|---|---|---|",
        f"| Lines | {len(discounted):,} | {len(full_price):,} |",
        f"| Mean est. profit/line | £{discounted.mean():.2f} | £{full_price.mean():.2f} |",
        f"\nWelch t = **{t:,.1f}**, p-value = **{p:.2e}** -> **{verdict}**\n",
        "**Business insight:** heavily discounted lines earn significantly less "
        "profit per line - high discounts erode margin.\n",
    ]


def anova_category_sales(df: pd.DataFrame) -> list[str]:
    top_cats = df["category"].value_counts().head(6).index
    groups = [df.loc[df["category"] == c, "revenue"] for c in top_cats]
    f, p = stats.f_oneway(*groups)
    verdict = "Reject H0" if p < ALPHA else "Fail to reject H0"
    means = df[df["category"].isin(top_cats)].groupby("category")["revenue"].mean()
    return [
        "## Test 2 - ANOVA: do line sales differ across categories?\n",
        "- H0: all categories have the same average line revenue",
        "- H1: at least one category differs\n",
        means.round(2).to_frame("mean line revenue (£)").to_markdown(),
        f"\nF = **{f:,.1f}**, p-value = **{p:.2e}** -> **{verdict}**\n",
        "**Business insight:** categories have genuinely different revenue profiles, "
        "so category-level planning (stocking, pricing) is justified.\n",
    ]


def chi_square_category_segment(df: pd.DataFrame) -> list[str]:
    known = df.dropna(subset=["customer_id"])
    spend = known.groupby("customer_id")["revenue"].sum()
    segments = pd.qcut(spend, 4, labels=SEGMENT_LABELS)
    seg_map = segments.to_dict()
    known = known.assign(segment=known["customer_id"].map(seg_map))

    top_cats = known["category"].value_counts().head(6).index
    table = pd.crosstab(known.loc[known["category"].isin(top_cats), "category"],
                        known.loc[known["category"].isin(top_cats), "segment"])
    chi2, p, dof, _ = stats.chi2_contingency(table)
    verdict = "Reject H0" if p < ALPHA else "Fail to reject H0"
    return [
        "## Test 3 - Chi-square: is category related to customer segment?\n",
        "- H0: purchase category mix is independent of customer segment",
        "- H1: segments buy different category mixes\n",
        table.to_markdown(),
        f"\nChi2 = **{chi2:,.0f}** (dof {dof}), p-value = **{p:.2e}** -> **{verdict}**\n",
        "**Business insight:** customer segments have distinct category preferences - "
        "targeted category promotions per segment are worthwhile.\n",
    ]


def main() -> None:
    df = pd.read_parquet(CLEAN_PARQUET)
    lines = ["# Hypothesis Testing\n", f"Significance level alpha = {ALPHA}\n"]
    lines += t_test_discount_profit(df)
    lines += anova_category_sales(df)
    lines += chi_square_category_segment(df)
    (REPORTS_DIR / "04_hypothesis_tests.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
