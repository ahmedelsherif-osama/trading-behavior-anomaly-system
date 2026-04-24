import joblib
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from src.core.paths import ARTIFACTS_DIR
from src.core.logger import get_logger
from src.modeling.model import build_model

logger = get_logger(__name__)


FEATURE_COLUMNS = [
    "trades_per_day",
    "total_trade_volume_per_day",
    "avg_trade_size",
    "avg_time_between_trades",
]


def train_model(df):
    logger.info("Starting model training")

    features = df.copy()

    X = df[FEATURE_COLUMNS].copy()
    X = X.fillna(0)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = build_model()
    model.fit(X_scaled)

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, ARTIFACTS_DIR / "model.joblib")
    joblib.dump(scaler, ARTIFACTS_DIR / "scaler.joblib")

    logger.info("Model + scaler saved to artifacts/")

    return model, scaler
