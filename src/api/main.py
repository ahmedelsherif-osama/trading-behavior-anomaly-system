from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import joblib
import pandas as pd
from src.core.logger import get_logger
from src.modeling.predict import predict_anomalies
from fastapi import UploadFile, File
import pandas as pd
import io
from src.preprocessing.preprocess_trades import preprocess_trading_data
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


@app.get("/")
def health():
    return {"status": "Trading Behavior Anomaly System is Online"}


@app.post("/predict/csv")
def predict_csv(file: UploadFile = File(...)):
    contents = file.file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    # STEP 1: preprocess RAW transactions
    features = preprocess_trading_data(df)

    # STEP 2: inference
    results = predict_anomalies(model, scaler, features)

    return {
        "summary": {
            "total": len(results),
            "anomalies": int(results["is_anomaly"].sum()),
        },
        "results": results.to_dict(orient="records"),
    }
