# Trading Behavior Anomaly Detection

Detect abnormal trading patterns using unsupervised learning on
user-level behavioral data.

Identifies suspicious accounts based on trading frequency, volume,
and behavior anomalies.

------------------------------------------------------------------------

## Problem

Financial trading platforms need to detect unusual user behavior that
may indicate: - automated trading bots - high-risk strategies -
potential fraud or manipulation

However, labeled anomaly data is rare → requires unsupervised methods.

------------------------------------------------------------------------

## Approach

-   Aggregated raw transactions into **user-day behavioral features**
-   Engineered features:
    -   trades_per_day
    -   total_trade_volume_per_day
    -   avg_trade_size
    -   avg_time_between_trades
-   Applied **Isolation Forest** for anomaly detection
-   Built modular ML pipeline: ingestion → validation → preprocessing →
    modeling → evaluation

------------------------------------------------------------------------

## Results

-   Total samples: 102
-   Anomalies detected: 2
-   Anomaly rate: \~2%

Key finding: Anomalous users show **10--15x higher trading volume and
trade size**

------------------------------------------------------------------------

## Key Insights

-   Anomalies exhibit:
    -   extremely high trade volume spikes
    -   unusually large average trade sizes
    -   irregular trading frequency patterns
-   Likely indicators of:
    -   automated trading behavior
    -   non-standard strategies
    -   high-risk accounts

------------------------------------------------------------------------

## Tech Stack

-   Python, Pandas, Scikit-learn
-   Isolation Forest
-   Modular ML pipeline architecture

------------------------------------------------------------------------

## Future Work

-   Compare Isolation Forest vs LOF / One-Class SVM
-   Tune contamination parameter
-   Add temporal sequence modeling (RNN / Transformers)