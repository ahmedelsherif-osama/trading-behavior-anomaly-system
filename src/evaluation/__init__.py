import pandas as pd


def generate_anomaly_report(df: pd.DataFrame) -> dict:
    """
    Simple evaluation layer for anomaly detection.
    """

    total = len(df)
    anomalies = df["is_anomaly"].sum()

    report = {
        "total_samples": total,
        "anomalies": int(anomalies),
        "anomaly_rate": anomalies / total,
    }

    return report
