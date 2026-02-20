import os, json
import joblib
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, accuracy_score

# SageMaker convention:
# /opt/ml/model -> model artifacts go here (SageMaker will package into model.tar.gz)
MODEL_DIR = os.environ.get("SM_MODEL_DIR", "/opt/ml/model")
OUTPUT_DIR = os.environ.get("SM_OUTPUT_DATA_DIR", "/opt/ml/output/data")

def main():
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    data = load_breast_cancer()
    X, y = data.data, data.target

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=2000))
    ])

    model.fit(X_train, y_train)
    y_pred = model.predict(X_val)

    metrics = {
        "accuracy": float(accuracy_score(y_val, y_pred)),
        "f1": float(f1_score(y_val, y_pred)),
    }

    # Save model into SageMaker model directory
    joblib.dump(model, os.path.join(MODEL_DIR, "model.joblib"))

    # Save metrics (nice for gating later)
    with open(os.path.join(OUTPUT_DIR, "metrics.json"), "w") as f:
        json.dump(metrics, f)

    print("✅ Training complete:", metrics)

if __name__ == "__main__":
    main()
