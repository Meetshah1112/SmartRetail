"""Module 5 - Regression: monthly sales forecasting.

Model: Linear Regression on a monthly time index + month-of-year dummies
(trend + seasonality). Trained on all complete months except the last 3,
which are held out for evaluation, then refit on everything to forecast
the next 3 months.
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, r2_score

from config import CLEAN_PARQUET, DATA_DIR, REPORTS_DIR
from plotting import init_style, money, save_fig
import matplotlib.pyplot as plt

TEST_MONTHS = 3
FORECAST_MONTHS = 3


def monthly_sales(df: pd.DataFrame) -> pd.DataFrame:
    monthly = (df.set_index("invoice_date")
                 .resample("MS")["revenue"].sum()
                 .to_frame("sales"))
    # drop the final partial month (data stops mid-month)
    last_day = df["invoice_date"].max()
    if last_day.day < 25:
        monthly = monthly.iloc[:-1]
    return monthly


def build_features(index: pd.DatetimeIndex, start: pd.Timestamp) -> pd.DataFrame:
    t = ((index.year - start.year) * 12 + (index.month - start.month)).astype(float)
    feats = pd.DataFrame({"t": t}, index=index)
    month_dummies = pd.get_dummies(index.month.astype(str), prefix="m").set_index(index)
    return pd.concat([feats, month_dummies], axis=1)


def align_columns(train: pd.DataFrame, other: pd.DataFrame) -> pd.DataFrame:
    return other.reindex(columns=train.columns, fill_value=0)


def evaluate(monthly: pd.DataFrame) -> tuple[LinearRegression, pd.DataFrame, dict]:
    start = monthly.index[0]
    X = build_features(monthly.index, start)
    y = monthly["sales"]

    X_train, X_test = X.iloc[:-TEST_MONTHS], X.iloc[-TEST_MONTHS:]
    y_train, y_test = y.iloc[:-TEST_MONTHS], y.iloc[-TEST_MONTHS:]

    model = LinearRegression().fit(X_train, y_train)
    pred = model.predict(align_columns(X_train, X_test))
    metrics = {
        "MAE": mean_absolute_error(y_test, pred),
        "MAPE": mean_absolute_percentage_error(y_test, pred),
        "R2_train": r2_score(y_train, model.predict(X_train)),
    }
    holdout = pd.DataFrame({"actual": y_test, "predicted": pred}, index=y_test.index)
    return model, holdout, metrics


def forecast_future(monthly: pd.DataFrame) -> pd.DataFrame:
    start = monthly.index[0]
    X_full = build_features(monthly.index, start)
    model = LinearRegression().fit(X_full, monthly["sales"])

    future_idx = pd.date_range(monthly.index[-1] + pd.offsets.MonthBegin(),
                               periods=FORECAST_MONTHS, freq="MS")
    X_future = align_columns(X_full, build_features(future_idx, start))
    fitted = model.predict(X_full)
    future = model.predict(X_future)

    hist = pd.DataFrame({"month": monthly.index, "sales": monthly["sales"].values,
                         "fitted": fitted, "kind": "actual"})
    fut = pd.DataFrame({"month": future_idx, "sales": np.nan,
                        "fitted": future, "kind": "forecast"})
    return pd.concat([hist, fut], ignore_index=True)


def plot_forecast(result: pd.DataFrame) -> None:
    fig, ax = plt.subplots()
    hist = result[result["kind"] == "actual"]
    fut = result[result["kind"] == "forecast"]
    ax.plot(hist["month"], hist["sales"] / 1e3, marker="o", lw=2,
            color="#6C4EE0", label="Actual")
    ax.plot(hist["month"], hist["fitted"] / 1e3, lw=1.5, ls="--",
            color="#2E9BF0", label="Model fit")
    ax.plot(fut["month"], fut["fitted"] / 1e3, marker="s", lw=2, ls="--",
            color="#F0862E", label="Forecast")
    ax.set_title("Monthly Sales: Actual, Fit and 3-Month Forecast")
    ax.set_ylabel("Sales (£K)")
    ax.legend()
    save_fig(fig, "05_sales_forecast")


def main() -> None:
    init_style()
    df = pd.read_parquet(CLEAN_PARQUET)
    monthly = monthly_sales(df)

    _, holdout, metrics = evaluate(monthly)
    result = forecast_future(monthly)
    plot_forecast(result)
    result.to_csv(DATA_DIR / "monthly_sales_forecast.csv", index=False)

    fut = result[result["kind"] == "forecast"]
    lines = [
        "# Sales Forecasting (Linear Regression)\n",
        f"Complete months used: **{len(monthly)}** "
        f"({monthly.index[0]:%b %Y} - {monthly.index[-1]:%b %Y})\n",
        "## Holdout evaluation (last 3 months)\n",
        holdout.assign(err_pct=lambda d: (d.predicted / d.actual - 1) * 100)
               .round(0).to_markdown(),
        f"\n| Metric | Value |\n|---|---|",
        f"| MAE | {money(metrics['MAE'])} |",
        f"| MAPE | {metrics['MAPE']:.1%} |",
        f"| R² (train) | {metrics['R2_train']:.3f} |",
        "\n## Forecast\n",
        fut[["month", "fitted"]].assign(fitted=lambda d: d.fitted.round(0)).to_markdown(index=False),
        "\nModel = linear trend + month-of-year seasonality. The strong Q4 "
        "seasonal peak (Sep-Nov) dominates the pattern.\n",
    ]
    (REPORTS_DIR / "05_regression_forecast.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
