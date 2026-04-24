import hashlib
import pandas as pd


def compute_file_hash(path: str) -> str:
    """
    Compute hash of raw file for integrity tracking.
    """

    hasher = hashlib.md5()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)

    return hasher.hexdigest()
