"""Module 6 - Classification: predict whether an ORDER is profitable.

Label: order-level estimated profit (sum of line profits minus a fixed
handling cost per order) > 0.
Features: order sales, quantity, number of lines, average discount,
dominant category.
Models: Logistic Regression and Decision Tree, evaluated with a
confusion matrix, per the brief.

Honest caveat (documented in the report): profit is *estimated* from the
pricing model in Module 1, so the classifiers are learning back our own
cost assumptions - the exercise demonstrates the ML workflow, not a
production profitability model.
"""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (ConfusionMatrixDisplay, accuracy_score,
                             classification_report, confusion_matrix, f1_score)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

from config import CLEAN_PARQUET, HANDLING_COST_PER_ORDER, RANDOM_STATE, REPORTS_DIR
from plotting import init_style, save_fig
import matplotlib.pyplot as plt

NUMERIC = ["sales", "quantity", "n_lines", "avg_discount"]
CATEGORICAL = ["main_category"]


def build_order_table(df: pd.DataFrame) -> pd.DataFrame:
    orders = df.groupby("invoice").agg(
        sales=("revenue", "sum"),
        quantity=("quantity", "sum"),
        n_lines=("stock_code", "count"),
        avg_discount=("discount_pct", "mean"),
        line_profit=("est_profit", "sum"),
        main_category=("category", lambda s: s.mode().iat[0]),
    )
    orders["order_profit"] = orders["line_profit"] - HANDLING_COST_PER_ORDER
    orders["is_profitable"] = (orders["order_profit"] > 0).astype(int)
    return orders.reset_index()


def make_pipeline(model) -> Pipeline:
    pre = ColumnTransformer([
        ("num", StandardScaler(), NUMERIC),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
    ])
    return Pipeline([("pre", pre), ("model", model)])


def fit_and_report(name: str, model, X_train, X_test, y_train, y_test) -> tuple[list[str], np.ndarray]:
    pipe = make_pipeline(model)
    pipe.fit(X_train, y_train)
    pred = pipe.predict(X_test)
    cm = confusion_matrix(y_test, pred)
    lines = [
        f"## {name}\n",
        f"- Accuracy: **{accuracy_score(y_test, pred):.3f}**",
        f"- F1 score: **{f1_score(y_test, pred):.3f}**\n",
        "```",
        classification_report(y_test, pred,
                              target_names=["Not profitable", "Profitable"]),
        "```\n",
    ]
    return lines, cm


def plot_confusion(cm_lr: np.ndarray, cm_dt: np.ndarray) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for ax, cm, title in ((axes[0], cm_lr, "Logistic Regression"),
                          (axes[1], cm_dt, "Decision Tree")):
        ConfusionMatrixDisplay(cm, display_labels=["Not profitable", "Profitable"]).plot(
            ax=ax, colorbar=False, cmap="Purples", values_format=",")
        ax.set_title(title)
    save_fig(fig, "06_confusion_matrices")


def main() -> None:
    init_style()
    df = pd.read_parquet(CLEAN_PARQUET)
    orders = build_order_table(df)

    X = orders[NUMERIC + CATEGORICAL]
    y = orders["is_profitable"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, stratify=y, random_state=RANDOM_STATE)

    lines = [
        "# Order Profitability Classification\n",
        f"Orders: **{len(orders):,}** | Profitable: **{y.mean():.1%}** "
        f"(order profit = line profits - £{HANDLING_COST_PER_ORDER:.2f} handling)\n",
        f"Features: {', '.join(NUMERIC + CATEGORICAL)}\n",
    ]
    lr_lines, cm_lr = fit_and_report(
        "Logistic Regression", LogisticRegression(max_iter=2000),
        X_train, X_test, y_train, y_test)
    dt_lines, cm_dt = fit_and_report(
        "Decision Tree (max_depth=6)",
        DecisionTreeClassifier(max_depth=6, random_state=RANDOM_STATE),
        X_train, X_test, y_train, y_test)
    lines += lr_lines + dt_lines
    plot_confusion(cm_lr, cm_dt)

    lines += [
        "## Caveat\n",
        "Profit labels come from the estimated-cost model (Module 1 assumptions), "
        "so scores are optimistic: the models partially re-learn the rule that "
        "generated the labels. With real cost data the same pipeline applies unchanged.\n",
    ]
    (REPORTS_DIR / "06_classification.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
