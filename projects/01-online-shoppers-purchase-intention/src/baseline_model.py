"""Run the first reproducible classification experiment for Project 01."""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path
from typing import Any

import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


TARGET = "Revenue"
POSITIVE_LABEL = True
RANDOM_STATE = 42
TEST_SIZE = 0.20
LOGISTIC_MAX_ITER = 1000

DATASET_RELATIVE_PATH = Path("datasets") / "online_shoppers_intention.csv"

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

NUMERIC_FEATURES = [
    "Administrative",
    "Administrative_Duration",
    "Informational",
    "Informational_Duration",
    "ProductRelated",
    "ProductRelated_Duration",
    "BounceRates",
    "ExitRates",
    "SpecialDay",
]

CATEGORICAL_FEATURES = [
    "Month",
    "OperatingSystems",
    "Browser",
    "Region",
    "TrafficType",
    "VisitorType",
    "Weekend",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def class_distribution(labels: pd.Series) -> dict[str, dict[str, float | int]]:
    counts = labels.value_counts().reindex([False, True], fill_value=0)
    total = len(labels)
    return {
        "False": {
            "count": int(counts.loc[False]),
            "percentage": round(float(counts.loc[False] / total * 100), 4),
        },
        "True": {
            "count": int(counts.loc[True]),
            "percentage": round(float(counts.loc[True] / total * 100), 4),
        },
    }


def positive_scores(estimator: Any, features: pd.DataFrame) -> Any:
    probabilities = estimator.predict_proba(features)
    classes = list(estimator.classes_)
    positive_index = next(
        index for index, label in enumerate(classes) if bool(label) is POSITIVE_LABEL
    )
    return probabilities[:, positive_index]


def evaluate_classifier(
    estimator: Any,
    features: pd.DataFrame,
    labels: pd.Series,
) -> dict[str, Any]:
    predictions = estimator.predict(features)
    scores = positive_scores(estimator, features)

    if labels.nunique() == 2:
        roc_auc = float(roc_auc_score(labels, scores))
        pr_auc = float(average_precision_score(labels, scores))
    else:
        roc_auc = None
        pr_auc = None

    matrix = confusion_matrix(labels, predictions, labels=[False, True])
    return {
        "metrics": {
            "accuracy": float(accuracy_score(labels, predictions)),
            "precision": float(
                precision_score(
                    labels,
                    predictions,
                    pos_label=POSITIVE_LABEL,
                    zero_division=0,
                )
            ),
            "recall": float(
                recall_score(
                    labels,
                    predictions,
                    pos_label=POSITIVE_LABEL,
                    zero_division=0,
                )
            ),
            "f1": float(
                f1_score(
                    labels,
                    predictions,
                    pos_label=POSITIVE_LABEL,
                    zero_division=0,
                )
            ),
            "roc_auc": roc_auc,
            "pr_auc": pr_auc,
        },
        "confusion_matrix": [[int(value) for value in row] for row in matrix],
    }


def build_logistic_pipeline(
    numeric_features: list[str], categorical_features: list[str]
) -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", StandardScaler(), numeric_features),
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_features,
            ),
        ]
    )
    classifier = LogisticRegression(
        max_iter=LOGISTIC_MAX_ITER,
        random_state=RANDOM_STATE,
    )
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier),
        ]
    )


def coefficient_records(coefficients: pd.Series, ascending: bool) -> list[dict[str, float | str]]:
    selected = coefficients.sort_values(ascending=ascending).head(10)
    return [
        {"feature": str(feature), "coefficient": round(float(value), 8)}
        for feature, value in selected.items()
    ]


def run_logistic_experiment(
    question: str,
    include_page_values: bool,
    x_train: pd.DataFrame,
    x_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
) -> tuple[dict[str, Any], dict[str, Any]]:
    numeric_features = list(NUMERIC_FEATURES)
    if include_page_values:
        numeric_features.append("PageValues")

    features = numeric_features + list(CATEGORICAL_FEATURES)
    if include_page_values:
        assert "PageValues" in features
    else:
        assert "PageValues" not in features

    pipeline = build_logistic_pipeline(numeric_features, CATEGORICAL_FEATURES)
    pipeline.fit(x_train[features], y_train)
    evaluation = evaluate_classifier(pipeline, x_test[features], y_test)

    preprocessor = pipeline.named_steps["preprocessor"]
    classifier = pipeline.named_steps["classifier"]
    feature_names = preprocessor.get_feature_names_out()
    coefficients = pd.Series(classifier.coef_[0], index=feature_names)

    result = {
        "model": "LogisticRegression",
        "question": question,
        "include_page_values": include_page_values,
        "features": features,
        "numeric_features": numeric_features,
        "categorical_features": list(CATEGORICAL_FEATURES),
        "parameters": {
            "random_state": RANDOM_STATE,
            "max_iter": LOGISTIC_MAX_ITER,
            "class_weight": None,
        },
        **evaluation,
    }
    coefficient_result = {
        "positive": coefficient_records(coefficients, ascending=False),
        "negative": coefficient_records(coefficients, ascending=True),
        "feature_count_after_preprocessing": int(len(feature_names)),
    }
    return result, coefficient_result


def main() -> None:
    repository_root = Path(__file__).resolve().parents[3]
    dataset_path = repository_root / DATASET_RELATIVE_PATH
    output_path = repository_root / "projects" / "01-online-shoppers-purchase-intention" / "outputs" / "baseline_metrics.json"

    if not dataset_path.is_file():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    source_hash_before = sha256_file(dataset_path)
    raw_data = pd.read_csv(dataset_path)

    assert raw_data.columns.tolist() == EXPECTED_COLUMNS, "Unexpected dataset columns"
    assert TARGET in raw_data.columns
    missing_values = int(raw_data.isna().sum().sum())
    assert missing_values == 0, "Missing values found before modeling"
    assert raw_data[TARGET].dtype == bool, "Revenue must be parsed as boolean"

    duplicate_mask = raw_data.duplicated(keep="first")
    duplicate_rows_removed = int(duplicate_mask.sum())
    duplicate_rows_involved = int(raw_data.duplicated(keep=False).sum())
    duplicate_patterns = int(
        raw_data.loc[raw_data.duplicated(keep=False)].drop_duplicates().shape[0]
    )

    model_data = raw_data.loc[~duplicate_mask].reset_index(drop=True)
    assert len(model_data) == len(raw_data) - duplicate_rows_removed
    assert model_data.columns.tolist() == EXPECTED_COLUMNS
    assert set(bool(value) for value in model_data[TARGET].unique()) == {False, True}

    x_all = model_data.drop(columns=[TARGET])
    y_all = model_data[TARGET].astype(bool)
    assert TARGET not in x_all.columns
    assert len(x_all) == len(y_all)

    train_indices, test_indices = train_test_split(
        list(model_data.index),
        test_size=TEST_SIZE,
        stratify=y_all,
        random_state=RANDOM_STATE,
    )
    assert set(train_indices).isdisjoint(test_indices)
    assert set(train_indices).union(test_indices) == set(model_data.index)

    x_train = x_all.loc[train_indices]
    x_test = x_all.loc[test_indices]
    y_train = y_all.loc[train_indices]
    y_test = y_all.loc[test_indices]

    split = {
        "test_size": TEST_SIZE,
        "random_state": RANDOM_STATE,
        "same_split_used_for_both_logistic_experiments": True,
        "train_rows": int(len(train_indices)),
        "test_rows": int(len(test_indices)),
        "train_distribution": class_distribution(y_train),
        "test_distribution": class_distribution(y_test),
    }

    baseline = DummyClassifier(strategy="most_frequent")
    baseline.fit(x_train, y_train)
    baseline_result = {
        "model": "DummyClassifier(strategy='most_frequent')",
        "features_used": "none by design",
        **evaluate_classifier(baseline, x_test, y_test),
    }

    experiment_a, coefficients_a = run_logistic_experiment(
        question="Predict Revenue using session behavior and context without PageValues.",
        include_page_values=False,
        x_train=x_train,
        x_test=x_test,
        y_train=y_train,
        y_test=y_test,
    )
    experiment_b, coefficients_b = run_logistic_experiment(
        question="Measure the change after adding PageValues to the same pipeline and split.",
        include_page_values=True,
        x_train=x_train,
        x_test=x_test,
        y_train=y_train,
        y_test=y_test,
    )

    metric_names = ["accuracy", "precision", "recall", "f1", "roc_auc", "pr_auc"]
    comparison = {
        "with_page_values_minus_without_page_values": {
            metric: round(
                experiment_b["metrics"][metric] - experiment_a["metrics"][metric],
                8,
            )
            for metric in metric_names
        }
    }

    source_hash_after = sha256_file(dataset_path)
    assert source_hash_before == source_hash_after, "The source CSV changed during execution"

    output = {
        "experiment": "Project 01 first machine learning experiment",
        "dataset": {
            "path": DATASET_RELATIVE_PATH.as_posix(),
            "source_sha256": source_hash_before,
            "original_shape": [int(value) for value in raw_data.shape],
            "missing_values": missing_values,
            "original_revenue_distribution": class_distribution(raw_data[TARGET]),
            "duplicate_rows_removed": duplicate_rows_removed,
            "duplicate_rows_involved": duplicate_rows_involved,
            "duplicate_patterns": duplicate_patterns,
            "final_shape_used_for_ml": [int(value) for value in model_data.shape],
            "final_revenue_distribution": class_distribution(y_all),
        },
        "target": {
            "column": TARGET,
            "positive_label": "Revenue=True",
            "problem_type": "binary classification",
        },
        "feature_design": {
            "numeric": list(NUMERIC_FEATURES),
            "categorical": list(CATEGORICAL_FEATURES),
            "page_values": "numeric only in Experiment B",
        },
        "split": split,
        "baseline": baseline_result,
        "experiment_a_without_page_values": experiment_a,
        "experiment_b_with_page_values": experiment_b,
        "comparison": comparison,
        "coefficients": {
            "interpretation_note": "Coefficients represent learned associations and do not demonstrate causality.",
            "without_page_values": coefficients_a,
            "with_page_values": coefficients_b,
        },
        "software": {
            "python": platform.python_version(),
            "pandas": pd.__version__,
            "scikit_learn": sklearn.__version__,
        },
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Output: {output_path.relative_to(repository_root)}")
    print(f"Original shape: {raw_data.shape[0]} rows x {raw_data.shape[1]} columns")
    print(f"Duplicate rows removed: {duplicate_rows_removed}")
    print(f"Rows used for ML: {len(model_data)}")
    print(f"Train/test: {len(train_indices)}/{len(test_indices)}")
    for label, result in [
        ("Baseline", baseline_result),
        ("Logistic without PageValues", experiment_a),
        ("Logistic with PageValues", experiment_b),
    ]:
        print(f"{label}: {result['metrics']}")


if __name__ == "__main__":
    main()
