"""Module 8 - Inventory analysis.

The dataset has no stock-on-hand column, so inventory health is inferred
from sales behaviour:
  sales velocity   = units sold per active week
  days since sale  = staleness signal
  movement class   = Fast / Medium / Slow / Dormant (velocity quartiles + staleness)
  restock flag     = fast movers still selling recently
"""
import numpy as np
import pandas as pd

from config import CLEAN_PARQUET, DATA_DIR, REPORTS_DIR
from plotting import init_style, save_fig
import matplotlib.pyplot as plt

DORMANT_AFTER_DAYS = 90


def build_product_table(df: pd.DataFrame) -> pd.DataFrame:
    """One row per stock_code (canonical description/category = most frequent),
    so the table can serve as a proper product dimension in Power BI."""
    snapshot = df["invoice_date"].max()
    canon = df.groupby("stock_code").agg(
        description=("description", lambda s: s.mode().iat[0]),
        category=("category", lambda s: s.mode().iat[0]),
    )
    prod = df.groupby("stock_code").agg(
        units_sold=("quantity", "sum"),
        revenue=("revenue", "sum"),
        est_profit=("est_profit", "sum"),
        n_orders=("invoice", "nunique"),
        first_sold=("invoice_date", "min"),
        last_sold=("invoice_date", "max"),
    )
    prod = canon.join(prod).reset_index()

    active_weeks = ((prod["last_sold"] - prod["first_sold"]).dt.days / 7).clip(lower=1)
    prod["sales_velocity"] = prod["units_sold"] / active_weeks
    prod["days_since_sale"] = (snapshot - prod["last_sold"]).dt.days
    return prod


def classify_movement(prod: pd.DataFrame) -> pd.DataFrame:
    out = prod.copy()
    q = out["sales_velocity"].quantile([0.5, 0.8])
    conditions = [
        out["days_since_sale"] > DORMANT_AFTER_DAYS,
        out["sales_velocity"] >= q[0.8],
        out["sales_velocity"] >= q[0.5],
    ]
    out["movement"] = np.select(conditions, ["Dormant", "Fast", "Medium"], default="Slow")
    out["restock_recommended"] = (out["movement"] == "Fast") & (out["days_since_sale"] <= 14)
    return out


def plot_movement(prod: pd.DataFrame) -> None:
    counts = prod["movement"].value_counts().reindex(["Fast", "Medium", "Slow", "Dormant"])
    colors = ["#2EBFA5", "#2E9BF0", "#F0862E", "#B0B0C0"]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    axes[0].bar(counts.index, counts.values, color=colors)
    axes[0].set_title("Products by Movement Class")
    rev = prod.groupby("movement")["revenue"].sum().reindex(counts.index)
    axes[1].bar(rev.index, rev.values / 1e6, color=colors)
    axes[1].set_title("Revenue by Movement Class (£M)")
    save_fig(fig, "08_inventory_movement")

    top = prod.nlargest(10, "sales_velocity").iloc[::-1]
    fig, ax = plt.subplots()
    ax.barh([d[:32] for d in top["description"]], top["sales_velocity"], color="#2EBFA5")
    ax.set_title("Fastest Moving Products (units/week)")
    save_fig(fig, "08_fastest_movers")


def main() -> None:
    init_style()
    df = pd.read_parquet(CLEAN_PARQUET)
    prod = classify_movement(build_product_table(df))
    plot_movement(prod)
    prod.to_csv(DATA_DIR / "inventory_analysis.csv", index=False)

    restock = prod[prod["restock_recommended"]].nlargest(15, "sales_velocity")
    dormant = prod[prod["movement"] == "Dormant"]
    lines = [
        "# Inventory Analysis\n",
        f"Products analysed: **{len(prod):,}**\n",
        "| Movement | Products | Share of revenue |\n|---|---|---|",
    ]
    total_rev = prod["revenue"].sum()
    for mv in ["Fast", "Medium", "Slow", "Dormant"]:
        part = prod[prod["movement"] == mv]
        lines.append(f"| {mv} | {len(part):,} | {part['revenue'].sum() / total_rev:.1%} |")
    lines += [
        f"\nDormant = no sale in {DORMANT_AFTER_DAYS}+ days.\n",
        "## Top restock candidates (fast movers, sold within 14 days)\n",
        restock[["description", "category", "sales_velocity", "units_sold"]]
            .round(1).to_markdown(index=False),
        f"\n## Dead stock\n{len(dormant):,} products have not sold in "
        f"{DORMANT_AFTER_DAYS}+ days - candidates for clearance.\n",
    ]
    (REPORTS_DIR / "08_inventory.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
