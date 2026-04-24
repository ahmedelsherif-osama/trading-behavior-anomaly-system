import pandas as pd
from sklearn.preprocessing import StandardScaler

from src.core.logger import get_logger
from src.modeling.model import build_model

logger = get_logger(__name__)


FEATURE_COLUMNS = [
    "trades_per_day",
    "total_trade_volume_per_day",
    "avg_trade_size",
    "avg_time_between_trades",
]


def train_model(df: pd.DataFrame):
    """
    Train anomaly detection model.
    """

    logger.info("Starting model training")

    X = df[FEATURE_COLUMNS].fillna(0)

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = build_model()
    model.fit(X_scaled)

    logger.info("Model training completed")

    return model, scaler
