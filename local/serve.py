import os
import joblib
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

ARTIFACTS_DIR = os.environ.get("ARTIFACTS_DIR", "artifacts")
MODEL_PATH = os.environ.get("MODEL_PATH", os.path.join(ARTIFACTS_DIR, "model.joblib"))

app = FastAPI(title="ML Model API (Local Demo)")

model = None

class PredictRequest(BaseModel):
    # For simplicity, we accept raw numeric features as a list.
    # Breast cancer dataset has 30 features.
    features: List[float]

@app.on_event("startup")
def load_model():
    global model
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError(f"Model file not found at {MODEL_PATH}. Run training first.")
    model = joblib.load(MODEL_PATH)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(req: PredictRequest):
    if len(req.features) != 30:
        return {"error": "Expected 30 features for this demo dataset."}

    pred = int(model.predict([req.features])[0])
    prob = float(model.predict_proba([req.features])[0][1])
    return {"prediction": pred, "probability_class_1": prob}
