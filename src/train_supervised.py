import argparse
import hashlib
import json
from contextlib import nullcontext
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import joblib
import mlflow
import yaml
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

from features import clean_features, load_dataset, scale_features, split_X_y


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train the intrusion detection model using a YAML config."
    )
    parser.add_argument(
        "--config",
        default="configs/train_default.yaml",
        help="Path to the training configuration file.",
    )
    parser.add_argument(
        "--run-name",
        default=None,
        help="Optional MLflow run name override.",
    )
    return parser.parse_args()


def load_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_model(model_cfg: Dict[str, Any], random_state: int) -> RandomForestClassifier:
    params = model_cfg.get("params", {})
    params.setdefault("random_state", random_state)
    return RandomForestClassifier(**params)


def ensure_registry_entry(registry_path: Path, entry: Dict[str, Any]) -> None:
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    if registry_path.exists():
        try:
            with open(registry_path, "r", encoding="utf-8") as f:
                registry = json.load(f)
        except json.JSONDecodeError:
            registry = []
    else:
        registry = []

    registry.append(entry)
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)


def train_from_config(config: Dict[str, Any], run_name_override: str | None = None) -> Dict[str, Any]:
    dataset_path = config["dataset"]["path"]
    df = load_dataset(dataset_path)
    df = clean_features(df)

    X, y, numeric_columns = split_X_y(df)
    X_scaled, scaler = scale_features(X)

    split_cfg = config.get("split", {})
    test_size = split_cfg.get("test_size", 0.2)
    stratify = y if split_cfg.get("stratify", True) else None
    random_state = config.get("random_state", 42)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify,
    )

    model_cfg = config.get("model", {})
    model = build_model(model_cfg, random_state=random_state)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    cm = confusion_matrix(y_test, y_pred).tolist()
    metrics = {
        "accuracy": report.get("accuracy"),
        "macro_precision": report["macro avg"]["precision"],
        "macro_recall": report["macro avg"]["recall"],
        "macro_f1": report["macro avg"]["f1-score"],
    }

    # --- MLflow Tracking ---
    mlflow_cfg = config.get("mlflow", {})
    mlflow_enabled = mlflow_cfg.get("enabled", True)
    run_name = run_name_override or mlflow_cfg.get("run_name") or f"run-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"

    # --- Versioned Model Saving + Registry ---
    output_cfg = config.get("output", {})
    output_dir = Path(output_cfg.get("dir", "src/models"))
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    model_id = f"rf-{timestamp}"
    versioned_path = output_dir / f"{model_id}.joblib"
    bundle = {
        "model": model,
        "scaler": scaler,
        "features": numeric_columns,
        "trained_at": timestamp,
    }

    if mlflow_enabled:
        mlflow.set_tracking_uri(mlflow_cfg.get("tracking_uri", "mlruns"))
        mlflow.set_experiment(mlflow_cfg.get("experiment_name", "default"))
        mlflow_context = mlflow.start_run(run_name=run_name)
    else:
        mlflow_context = nullcontext()

    with mlflow_context:
        if mlflow_enabled:
            mlflow.log_params(
                {
                    "dataset": dataset_path,
                    "test_size": test_size,
                    "random_state": random_state,
                    **{f"model__{k}": v for k, v in model_cfg.get("params", {}).items()},
                }
            )
            mlflow.log_metrics(metrics)
            mlflow.log_dict(report, "artifacts/classification_report.json")
            mlflow.log_dict({"confusion_matrix": cm}, "artifacts/confusion_matrix.json")

        joblib.dump(bundle, versioned_path)
        joblib.dump(bundle, output_dir / "rf.pk1")  # maintain compatibility with the API

        if mlflow_enabled:
            mlflow.log_artifact(versioned_path)

    # --- Model Registry Entry ---
    config_hash = hashlib.sha256(json.dumps(config, sort_keys=True).encode("utf-8")).hexdigest()[:12]
    registry_path = Path(output_cfg.get("registry_path", output_dir / "model_registry.json"))
    metadata = {
        "model_id": model_id,
        "model_path": str(versioned_path),
        "created_at_utc": timestamp,
        "dataset_path": dataset_path,
        "metrics": metrics,
        "config_hash": config_hash,
        "features": numeric_columns,
    }
    ensure_registry_entry(registry_path, metadata)

    return {
        "model_id": model_id,
        "metrics": metrics,
        "model_path": str(versioned_path),
        "registry_path": str(registry_path),
        "classification_report": report,
    }


def run_training(config_path: str, run_name: str | None = None) -> Dict[str, Any]:
    config = load_config(config_path)
    return train_from_config(config, run_name_override=run_name)


if __name__ == "__main__":
    args = parse_args()
    results = run_training(args.config, run_name=args.run_name)
    print(f"✔ Trained model {results['model_id']} saved to {results['model_path']}")
    print(f"Metrics: {json.dumps(results['metrics'], indent=2)}")