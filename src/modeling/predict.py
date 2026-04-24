import pandas as pd


def predict_anomalies(model, scaler, df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate anomaly predictions.
    """

    FEATURE_COLUMNS = [
        "trades_per_day",
        "total_trade_volume_per_day",
        "avg_trade_size",
        "avg_time_between_trades",
    ]

    X = df[FEATURE_COLUMNS].fillna(0)
    X_scaled = scaler.transform(X)

    df = df.copy()

    df["anomaly_score"] = model.decision_function(X_scaled)
    df["is_anomaly"] = model.predict(X_scaled)

    # Convert (-1, 1) → (1 = anomaly)
    df["is_anomaly"] = df["is_anomaly"].map({1: 0, -1: 1})

    return df
