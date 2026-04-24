import hashlib
import pandas as pd


def compute_dataframe_hash(df: pd.DataFrame) -> str:
    """
    Compute deterministic hash for dataset version tracking.
    """

    return hashlib.md5(pd.util.hash_pandas_object(df, index=True).values).hexdigest()
