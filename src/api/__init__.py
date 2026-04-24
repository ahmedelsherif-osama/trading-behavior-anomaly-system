from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import joblib
import pandas as pd

from src.core.logger import get_logger
from src.modeling.predict import predict_anomalies

logger = get_logger(__name__)

app = FastAPI(title="Trading Anomaly Detection API")


MODEL_PATH = Path("data/artifacts/model.joblib")
SCALER_PATH = Path("data/artifacts/scaler.joblib")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

logger.info("Model and scaler loaded successfully")


class TradeFeatures(BaseModel):
    trades_per_day: float
    total_trade_volume_per_day: float
    avg_trade_size: float
    avg_time_between_trades: float


class PredictionRequest(BaseModel):
    data: list[TradeFeatures]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(request: PredictionRequest):
    df = pd.DataFrame([item.model_dump() for item in request.data])

    results = predict_anomalies(model, scaler, df)

    return {
        "predictions": results[["anomaly_score", "is_anomaly"]].to_dict(
            orient="records"
        )
    }
