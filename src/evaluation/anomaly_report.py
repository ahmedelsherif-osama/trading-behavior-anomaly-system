import pandas as pd
from src.core.logger import get_logger

logger = get_logger(__name__)


def generate_anomaly_report(df: pd.DataFrame) -> dict:
    """
    Generate structured anomaly insights from model output.
    """

    logger.info("Generating anomaly report")

    report = {}

    total = len(df)
    anomalies = df["is_anomaly"].sum()

    report["summary"] = {
        "total_samples": total,
        "anomalies": int(anomalies),
        "anomaly_rate": float(anomalies / total),
    }

    top_accounts = (
        df[df["is_anomaly"] == 1]
        .groupby("Account")
        .size()
        .sort_values(ascending=False)
        .head(10)
    )

    report["top_anomalous_accounts"] = top_accounts.to_dict()

    feature_cols = [
        "trades_per_day",
        "total_trade_volume_per_day",
        "avg_trade_size",
    ]

    comparison = {}

    normal = df[df["is_anomaly"] == 0]
    anomalous = df[df["is_anomaly"] == 1]

    for col in feature_cols:
        comparison[col] = {
            "normal_mean": float(normal[col].mean()),
            "anomaly_mean": float(anomalous[col].mean()),
            "normal_std": float(normal[col].std()),
            "anomaly_std": float(anomalous[col].std()),
        }

    report["feature_comparison"] = comparison

    top_anomalies = df[df["is_anomaly"] == 1].copy()

    top_anomalies = top_anomalies.sort_values(
        "total_trade_volume_per_day", ascending=False
    ).head(5)

    report["example_anomalies"] = top_anomalies.to_dict(orient="records")

    logger.info("Anomaly report generated successfully")

    return report
