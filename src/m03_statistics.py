"""Module 3 - Statistical analysis: central tendency, dispersion, confidence interval."""
import numpy as np
import pandas as pd
from scipy import stats

from config import CLEAN_PARQUET, REPORTS_DIR
from plotting import init_style, money, save_fig
import matplotlib.pyplot as plt


def central_tendency(order_values: pd.Series) -> list[str]:
    mode = order_values.round(0).mode()
    return [
        "## Central tendency (order value, £)\n",
        "| Statistic | Value |\n|---|---|",
        f"| Mean | {order_values.mean():,.2f} |",
        f"| Median | {order_values.median():,.2f} |",
        f"| Mode (rounded to £) | {mode.iat[0]:,.0f} |",
        "\nMean >> median: a small number of very large wholesale orders pulls "
        "the average up, so the median is the better 'typical order' figure.\n",
    ]


def dispersion(order_values: pd.Series, df: pd.DataFrame) -> list[str]:
    lines = [
        "## Dispersion (order value, £)\n",
        "| Statistic | Value |\n|---|---|",
        f"| Variance | {order_values.var():,.0f} |",
        f"| Std deviation | {order_values.std():,.2f} |",
        f"| Range | {order_values.min():,.2f} - {order_values.max():,.2f} |",
        f"| IQR | {order_values.quantile(0.25):,.2f} - {order_values.quantile(0.75):,.2f} |",
        "\n### Variability by category (std of line revenue)\n",
    ]
    by_cat = (df.groupby("category")["revenue"].agg(["mean", "std"])
                .sort_values("std", ascending=False))
    lines.append(by_cat.round(2).to_markdown())
    top, bottom = by_cat.index[0], by_cat.index[-1]
    lines.append(f"\n**Interpretation:** {top} shows the highest sales variability, "
                 f"{bottom} the most stable.\n")
    return lines


def confidence_interval(order_values: pd.Series) -> list[str]:
    mean = order_values.mean()
    sem = stats.sem(order_values)
    low, high = stats.t.interval(0.95, len(order_values) - 1, loc=mean, scale=sem)
    return [
        "## 95% confidence interval - average order value\n",
        f"Mean = **{money(mean)}**, 95% CI = **{money(low)} to {money(high)}** "
        f"(±{money(high - mean)})\n",
        f"We are 95% confident the true average order value lies between "
        f"{money(low)} and {money(high)}.\n",
    ]


def plot_distribution(order_values: pd.Series) -> None:
    fig, ax = plt.subplots()
    clipped = order_values[order_values <= order_values.quantile(0.99)]
    ax.hist(clipped, bins=80, color="#6C4EE0", alpha=0.85)
    ax.axvline(order_values.mean(), color="#E04E7A", ls="--", lw=2,
               label=f"Mean {order_values.mean():,.0f}")
    ax.axvline(order_values.median(), color="#2EBFA5", ls="--", lw=2,
               label=f"Median {order_values.median():,.0f}")
    ax.set_title("Order Value Distribution (99th pct clipped)")
    ax.set_xlabel("Order value (£)")
    ax.legend()
    save_fig(fig, "03_order_value_distribution")


def main() -> None:
    init_style()
    df = pd.read_parquet(CLEAN_PARQUET)
    order_values = df.groupby("invoice")["revenue"].sum()

    lines = ["# Statistical Analysis\n"]
    lines += central_tendency(order_values)
    lines += dispersion(order_values, df)
    lines += confidence_interval(order_values)
    plot_distribution(order_values)

    (REPORTS_DIR / "03_statistics.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
