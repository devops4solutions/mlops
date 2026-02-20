import json
import os
from datetime import datetime

import joblib
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ARTIFACTS_DIR = os.environ.get("ARTIFACTS_DIR", "artifacts")


def main():
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

    # 1) Load sample dataset (no CSV needed)
    data = load_breast_cancer()
    X = data.data
    y = data.target  # 0/1

    # 2) Split into train/validation
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 3) Build a simple model pipeline
    # StandardScaler helps Logistic Regression work better
    model = Pipeline(steps=[
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=2000))
    ])

    # 4) Train
    model.fit(X_train, y_train)

    # 5) Validate
    y_pred = model.predict(X_val)
    y_prob = model.predict_proba(X_val)[:, 1]

    metrics = {
        "accuracy": float(accuracy_score(y_val, y_pred)),
        "f1": float(f1_score(y_val, y_pred)),
        "roc_auc": float(roc_auc_score(y_val, y_prob)),
        "rows_train": int(len(X_train)),
        "rows_val": int(len(X_val)),
        "trained_at": datetime.utcnow().isoformat() + "Z",
        "dataset": "sklearn.datasets.load_breast_cancer",
        "model": "LogisticRegression + StandardScaler",
    }

    # 6) Save artifacts
    model_path = os.path.join(ARTIFACTS_DIR, "model.joblib")
    metrics_path = os.path.join(ARTIFACTS_DIR, "metrics.json")

    joblib.dump(model, model_path)
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)

    print("✅ Training complete")
    print("Saved:", model_path)
    print("Saved:", metrics_path)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
