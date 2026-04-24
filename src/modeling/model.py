from sklearn.ensemble import IsolationForest


def build_model(random_state: int = 42) -> IsolationForest:
    """
    Build Isolation Forest model.
    """

    model = IsolationForest(
        n_estimators=100,
        contamination=0.01,  # assume 1% anomalies
        random_state=random_state,
    )

    return model
