from pathlib import Path
import pandas as pd
from src.core.logger import get_logger

logger = get_logger(__name__)


def load_raw_data(path: Path) -> pd.DataFrame:
    """
    Pure ingestion layer:
    - loads file
    - validates existence
    - ensures non-empty output
    """

    logger.info(f"Loading raw data from: {path}")

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    try:
        df = pd.read_csv(path)
    except Exception:
        logger.exception("Failed to read CSV file")
        raise

    if df.empty:
        raise ValueError("Dataset is empty")

    logger.info(f"Data loaded: shape={df.shape}")

    return df
