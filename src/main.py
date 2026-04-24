from pathlib import Path
from src.ingestion.loader import load_raw_data
from src.validation.schema_validator import SchemaValidator
from src.preprocessing.preprocess_trades import preprocess_trading_data
from src.modeling.train import train_model
from src.modeling.predict import predict_anomalies
from src.evaluation.anomaly_report import generate_anomaly_report

from src.core.logger import get_logger

logger = get_logger(__name__)


def run_pipeline():
    logger.info("Starting ML pipeline")

    df = load_raw_data(Path("data/raw/historical_data.csv"))

    validator = SchemaValidator(
        schema_path=Path("configs/schemas/trading_schema.json"),
        required_columns=["Account", "Timestamp", "Size USD"],
    )
    validator.validate(df)

    features = preprocess_trading_data(df)

    model, scaler = train_model(features)

    results = predict_anomalies(model, scaler, features)

    report = generate_anomaly_report(results)

    logger.info(f"Anomaly report: {report}")

    print(report)


if __name__ == "__main__":
    run_pipeline()
