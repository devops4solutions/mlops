import os
import joblib
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# SageMaker sets this to where model.tar.gz gets extracted
MODEL_DIR = os.environ.get("SM_MODEL_DIR", "/opt/ml/model")
MODEL_PATH = os.path.join(MODEL_DIR, "model.joblib")

app = FastAPI()
model = None

class PredictRequest(BaseModel):
    features: List[float]

@app.on_event("startup")
def load_model():
    global model
    model = joblib.load(MODEL_PATH)

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.post("/invocations")
def invocations(req: PredictRequest):
    pred = int(model.predict([req.features])[0])
    prob = float(model.predict_proba([req.features])[0][1])
    return {"prediction": pred, "probability_class_1": prob}
