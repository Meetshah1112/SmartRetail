"""Module 7 - Customer segmentation with RFM + K-Means.

RFM per identified customer:
  Recency   = days since last purchase (from day after last transaction)
  Frequency = number of distinct orders
  Monetary  = total revenue

Features are log-transformed and standardized; K chosen with the elbow
method; the 4 clusters are labeled Premium / Regular / Occasional /
Inactive based on their RFM profile, matching the brief.
"""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from config import CLEAN_PARQUET, RANDOM_STATE, REPORTS_DIR, RFM_CSV
from plotting import init_style, money, save_fig
import matplotlib.pyplot as plt

K_RANGE = range(2, 9)
N_CLUSTERS = 4


def build_rfm(df: pd.DataFrame) -> pd.DataFrame:
    known = df.dropna(subset=["customer_id"])
    snapshot = known["invoice_date"].max() + pd.Timedelta(days=1)
    rfm = known.groupby("customer_id").agg(
        recency_days=("invoice_date", lambda s: (snapshot - s.max()).days),
        frequency=("invoice", "nunique"),
        monetary=("revenue", "sum"),
        first_purchase=("invoice_date", "min"),
        country=("country", "first"),
    )
    rfm["avg_order_value"] = rfm["monetary"] / rfm["frequency"]
    return rfm[rfm["monetary"] > 0]


def scale_features(rfm: pd.DataFrame) -> np.ndarray:
    feats = np.log1p(rfm[["recency_days", "frequency", "monetary"]])
    return StandardScaler().fit_transform(feats)


def elbow_chart(X: np.ndarray) -> None:
    inertias = [KMeans(k, n_init=10, random_state=RANDOM_STATE).fit(X).inertia_
                for k in K_RANGE]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(list(K_RANGE), inertias, marker="o", color="#6C4EE0")
    ax.axvline(N_CLUSTERS, color="#F0862E", ls="--", label=f"chosen k={N_CLUSTERS}")
    ax.set_title("Elbow Method - choosing K")
    ax.set_xlabel("k")
    ax.set_ylabel("Inertia")
    ax.legend()
    save_fig(fig, "07_elbow_method")


def label_clusters(rfm: pd.DataFrame) -> pd.DataFrame:
    """Rank clusters by an RFM score and assign business names."""
    profile = rfm.groupby("cluster").agg(
        recency=("recency_days", "mean"),
        frequency=("frequency", "mean"),
        monetary=("monetary", "mean"),
    )
    score = (profile["monetary"].rank() + profile["frequency"].rank()
             - profile["recency"].rank())
    names = ["Inactive", "Occasional", "Regular", "Premium"]
    mapping = {cluster: names[i] for i, cluster in
               enumerate(score.sort_values().index)}
    out = rfm.copy()
    out["segment"] = out["cluster"].map(mapping)
    return out


def plot_clusters(rfm: pd.DataFrame) -> None:
    order = ["Premium", "Regular", "Occasional", "Inactive"]
    colors = {"Premium": "#6C4EE0", "Regular": "#2E9BF0",
              "Occasional": "#F0862E", "Inactive": "#B0B0C0"}

    fig, ax = plt.subplots(figsize=(9, 6))
    for seg in order:
        part = rfm[rfm["segment"] == seg]
        ax.scatter(part["recency_days"], part["monetary"], s=8, alpha=0.4,
                   color=colors[seg], label=f"{seg} ({len(part):,})")
    ax.set_yscale("log")
    ax.set_title("Customer Segments: Recency vs Monetary")
    ax.set_xlabel("Recency (days since last purchase)")
    ax.set_ylabel("Total spend (£, log scale)")
    ax.legend(markerscale=2)
    save_fig(fig, "07_clusters_recency_monetary")

    sizes = rfm["segment"].value_counts().reindex(order)
    revenue = rfm.groupby("segment")["monetary"].sum().reindex(order)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    axes[0].bar(sizes.index, sizes.values, color=[colors[s] for s in order])
    axes[0].set_title("Customers per Segment")
    axes[1].bar(revenue.index, revenue.values / 1e6, color=[colors[s] for s in order])
    axes[1].set_title("Revenue per Segment (£M)")
    save_fig(fig, "07_segment_sizes_revenue")


def main() -> None:
    init_style()
    df = pd.read_parquet(CLEAN_PARQUET)
    rfm = build_rfm(df)
    X = scale_features(rfm)

    elbow_chart(X)
    km = KMeans(N_CLUSTERS, n_init=10, random_state=RANDOM_STATE).fit(X)
    rfm["cluster"] = km.labels_
    rfm = label_clusters(rfm)
    plot_clusters(rfm)
    rfm.reset_index().to_csv(RFM_CSV, index=False)

    profile = (rfm.groupby("segment")
                  .agg(customers=("frequency", "size"),
                       avg_recency_days=("recency_days", "mean"),
                       avg_orders=("frequency", "mean"),
                       avg_spend=("monetary", "mean"),
                       total_revenue=("monetary", "sum"))
                  .reindex(["Premium", "Regular", "Occasional", "Inactive"]))
    lines = [
        "# Customer Segmentation (RFM + K-Means)\n",
        f"Customers clustered: **{len(rfm):,}** (guest checkouts excluded)\n",
        "## Segment profile\n",
        profile.round(1).to_markdown(),
        "\n## Reading the segments\n",
        "- **Premium** - recent, frequent, high-spend. Protect with VIP service.",
        "- **Regular** - steady repeat buyers. Grow with cross-sell.",
        "- **Occasional** - infrequent, lower spend. Nurture with campaigns.",
        "- **Inactive** - long-lapsed. Win-back offers or let churn.\n",
        f"\nOutput written to `{RFM_CSV.name}` for the Power BI customer dashboard.\n",
    ]
    (REPORTS_DIR / "07_segmentation.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
