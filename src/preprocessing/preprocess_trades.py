import pandas as pd
from src.core.logger import get_logger

logger = get_logger(__name__)


def preprocess_trading_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform raw transaction-level data into user-day behavioral features.
    """

    logger.info("Starting preprocessing")

    df = df.copy()

    df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="ms")
    df["date"] = df["Timestamp"].dt.date

    grouped = df.groupby(["Account", "date"])

    features_df = grouped.agg(
        trades_per_day=("Account", "count"),
        total_trade_volume_per_day=("Size USD", "sum"),
        avg_trade_size=("Size USD", "mean"),
    ).reset_index()

    logger.info(f"Aggregated features shape: {features_df.shape}")

    df_sorted = df.sort_values(["Account", "Timestamp"])

    df_sorted["time_diff"] = (
        df_sorted.groupby("Account")["Timestamp"].diff().dt.total_seconds()
    )

    time_between = (
        df_sorted.groupby(["Account", "date"])["time_diff"]
        .mean()
        .reset_index(name="avg_time_between_trades")
    )

    features_df = features_df.merge(time_between, on=["Account", "date"], how="left")

    logger.info("Preprocessing completed")

    return features_df
