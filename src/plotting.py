"""Shared matplotlib/seaborn styling so every figure looks consistent."""
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns

from config import ACCENT, FIGURES_DIR, PALETTE


def init_style() -> None:
    sns.set_theme(style="whitegrid", palette=PALETTE)
    plt.rcParams.update({
        "figure.figsize": (11, 5.5),
        "figure.dpi": 120,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.spines.top": False,
        "axes.spines.right": False,
    })


def save_fig(fig, name: str) -> None:
    path = FIGURES_DIR / f"{name}.png"
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved figure: {path.name}")


def money(value: float) -> str:
    """Compact GBP formatting: 1234567 -> '£1.23M'."""
    for div, suffix in ((1e9, "B"), (1e6, "M"), (1e3, "K")):
        if abs(value) >= div:
            return f"£{value / div:,.2f}{suffix}"
    return f"£{value:,.0f}"
