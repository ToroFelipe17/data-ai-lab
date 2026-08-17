"""Generate the reproducible EDA figures selected for Project 01."""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


TARGET = "Revenue"
DATASET_RELATIVE_PATH = Path("datasets") / "online_shoppers_intention.csv"
MONTH_ORDER = ["Feb", "Mar", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
VISITOR_ORDER = ["New_Visitor", "Other", "Returning_Visitor"]
EXPECTED_COLUMNS = [
    "Administrative",
    "Administrative_Duration",
    "Informational",
    "Informational_Duration",
    "ProductRelated",
    "ProductRelated_Duration",
    "BounceRates",
    "ExitRates",
    "PageValues",
    "SpecialDay",
    "Month",
    "OperatingSystems",
    "Browser",
    "Region",
    "TrafficType",
    "VisitorType",
    "Weekend",
    "Revenue",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def revenue_label(value: bool) -> str:
    return "Compra" if value else "Sin compra"


def percentage(value: float) -> float:
    return round(float(value) * 100, 4)


def conversion_summary(data: pd.DataFrame, column: str) -> dict[str, dict[str, float | int]]:
    grouped = data.groupby(column, sort=False, observed=True)[TARGET].agg(["count", "sum", "mean"])
    return {
        str(category): {
            "sessions": int(row["count"]),
            "purchases": int(row["sum"]),
            "conversion_rate_percent": percentage(row["mean"]),
        }
        for category, row in grouped.iterrows()
    }


def numeric_summary(data: pd.DataFrame, column: str) -> dict[str, dict[str, float | int]]:
    grouped = data.groupby(TARGET, sort=True, observed=True)[column].agg(["count", "mean", "median"])
    return {
        str(revenue_label(bool(revenue))): {
            "sessions": int(row["count"]),
            "mean": round(float(row["mean"]), 6),
            "median": round(float(row["median"]), 6),
        }
        for revenue, row in grouped.iterrows()
    }


def save_boxplot(
    data: pd.DataFrame,
    column: str,
    filename: str,
    title: str,
    ylabel: str,
    output_dir: Path,
) -> None:
    groups = [
        data.loc[data[TARGET] == False, column],
        data.loc[data[TARGET] == True, column],
    ]
    figure, axis = plt.subplots(figsize=(6.4, 4.8), dpi=160)
    axis.boxplot(
        groups,
        tick_labels=["False", "True"],
        showfliers=True,
        flierprops={
            "marker": "o",
            "markerfacecolor": "none",
            "markeredgecolor": "black",
            "markersize": 4,
        },
        medianprops={"color": "black", "linewidth": 1.5},
    )
    axis.set_title(title)
    axis.set_xlabel("Compra realizada")
    axis.set_ylabel(ylabel)
    axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    figure.savefig(output_dir / filename, bbox_inches="tight")
    plt.close(figure)


def save_conversion_barplot(
    summary: dict[str, dict[str, float | int]],
    categories: list[str],
    filename: str,
    title: str,
    output_dir: Path,
) -> None:
    rates = [float(summary[category]["conversion_rate_percent"]) for category in categories]
    figure, axis = plt.subplots(figsize=(6.4, 4.8), dpi=160)
    axis.bar(categories, rates, color="#1f77b4")
    axis.set_title(title)
    axis.set_ylabel("Tasa de conversión (%)")
    axis.set_xlabel("Tipo de visitante" if "visitor" in filename else "Mes")
    axis.set_ylim(0, max(rates) * 1.1)
    axis.grid(axis="y", alpha=0.25)
    if "visitor" in filename:
        axis.tick_params(axis="x", rotation=15)
        for label in axis.get_xticklabels():
            label.set_ha("right")
    else:
        axis.tick_params(axis="x", rotation=0)
    figure.tight_layout()
    figure.savefig(output_dir / filename, bbox_inches="tight")
    plt.close(figure)


def main() -> None:
    repository_root = Path(__file__).resolve().parents[3]
    dataset_path = repository_root / DATASET_RELATIVE_PATH
    output_root = repository_root / "projects" / "01-online-shoppers-purchase-intention" / "outputs"
    figure_dir = output_root / "figures"
    figure_dir.mkdir(parents=True, exist_ok=True)

    if not dataset_path.is_file():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    source_hash_before = sha256_file(dataset_path)
    data = pd.read_csv(dataset_path)
    assert data.columns.tolist() == EXPECTED_COLUMNS, "Unexpected dataset columns"
    assert int(data.isna().sum().sum()) == 0, "Missing values found"
    assert data[TARGET].dtype == bool, "Revenue must be parsed as boolean"

    visitor_summary = conversion_summary(data, "VisitorType")
    month_data = data.loc[data["Month"].isin(MONTH_ORDER)].copy()
    month_summary = conversion_summary(month_data, "Month")
    assert set(month_summary) == set(MONTH_ORDER), "Unexpected month coverage"

    save_boxplot(
        data,
        "ProductRelated",
        "product_related_by_revenue.png",
        "Páginas relacionadas con productos según compra",
        "Páginas relacionadas con productos",
        figure_dir,
    )
    save_boxplot(
        data,
        "ProductRelated_Duration",
        "product_related_duration_by_revenue.png",
        "Tiempo en páginas de producto según compra",
        "Duración de páginas de productos",
        figure_dir,
    )
    save_boxplot(
        data,
        "PageValues",
        "page_values_by_revenue.png",
        "PageValues según compra",
        "PageValues",
        figure_dir,
    )
    save_conversion_barplot(
        visitor_summary,
        VISITOR_ORDER,
        "conversion_by_visitor_type.png",
        "Tasa de conversión según tipo de visitante",
        figure_dir,
    )
    save_conversion_barplot(
        month_summary,
        MONTH_ORDER,
        "conversion_by_month.png",
        "Tasa de conversión según mes",
        figure_dir,
    )

    source_hash_after = sha256_file(dataset_path)
    assert source_hash_before == source_hash_after, "The source CSV changed during execution"

    summary = {
        "dataset": {
            "path": DATASET_RELATIVE_PATH.as_posix(),
            "source_sha256": source_hash_before,
            "shape": [int(value) for value in data.shape],
            "missing_values": int(data.isna().sum().sum()),
            "duplicate_rows_removed_for_ml": int(data.duplicated(keep="first").sum()),
            "duplicate_rows_involved": int(data.duplicated(keep=False).sum()),
            "duplicate_patterns": int(data.loc[data.duplicated(keep=False)].drop_duplicates().shape[0]),
            "revenue_distribution": {
                "False": {"sessions": int((data[TARGET] == False).sum()), "percentage": percentage((data[TARGET] == False).mean())},
                "True": {"sessions": int((data[TARGET] == True).sum()), "percentage": percentage((data[TARGET] == True).mean())},
            },
        },
        "weekend_conversion": conversion_summary(data, "Weekend"),
        "visitor_type_conversion": {
            category: visitor_summary[category] for category in VISITOR_ORDER
        },
        "month_conversion": {category: month_summary[category] for category in MONTH_ORDER},
        "numeric_by_revenue": {
            "ProductRelated": numeric_summary(data, "ProductRelated"),
            "ProductRelated_Duration": numeric_summary(data, "ProductRelated_Duration"),
            "PageValues": numeric_summary(data, "PageValues"),
        },
        "figures": [
            "figures/product_related_by_revenue.png",
            "figures/product_related_duration_by_revenue.png",
            "figures/page_values_by_revenue.png",
            "figures/conversion_by_visitor_type.png",
            "figures/conversion_by_month.png",
        ],
        "software": {
            "python": platform.python_version(),
            "pandas": pd.__version__,
            "matplotlib": matplotlib.__version__,
        },
    }
    summary_path = output_root / "eda_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Generated figures: {len(summary['figures'])}")
    print(f"Summary: {summary_path.relative_to(repository_root)}")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
