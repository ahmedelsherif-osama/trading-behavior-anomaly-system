import json
from pathlib import Path
import pandas as pd
from jsonschema import validate, ValidationError

from src.validation.base_validator import BaseValidator
from src.core.logger import get_logger

logger = get_logger(__name__)


class SchemaValidator(BaseValidator):
    """
    Validates dataframe against JSON schema and required columns.
    """

    def __init__(self, schema_path: Path, required_columns: list[str]):
        self.schema_path = Path(schema_path)
        self.required_columns = required_columns
        self.schema = self._load_schema()

    def _load_schema(self) -> dict:
        if not self.schema_path.exists():
            raise FileNotFoundError(f"Schema not found: {self.schema_path}")

        with open(self.schema_path, "r") as f:
            return json.load(f)

    def validate(self, df: pd.DataFrame) -> None:
        """
        Run full validation pipeline.
        """

        logger.info("Starting schema validation")

        self._validate_required_columns(df)
        self._validate_json_schema(df)

        logger.info("Schema validation passed")

    def _validate_required_columns(self, df: pd.DataFrame) -> None:
        missing = set(self.required_columns) - set(df.columns)

        if missing:
            logger.error(f"Missing required columns: {missing}")
            raise ValueError(f"Missing required columns: {missing}")

    def _validate_json_schema(self, df: pd.DataFrame) -> None:
        """
        Validate structure using JSON schema.
        Uses first row as lightweight proxy.
        """

        if df.empty:
            raise ValueError("Cannot validate empty dataframe")

        sample = df.iloc[0].to_dict()

        try:
            validate(instance=sample, schema=self.schema)
        except ValidationError as e:
            logger.error("JSON schema validation failed")
            raise
