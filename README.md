# CryptoLake 🪙

Personal Data Lakehouse on GCP processing real-time cryptocurrency data.

## Architecture

CoinGecko API → Cloud Scheduler → Cloud Run (Python) → GCS bronze/ → BigQuery silver/gold → Looker Studio

## Stack

- Python 3.11
- Google Cloud Run (Functions)
- Google Cloud Storage (GCS)
- Google Cloud Scheduler
- BigQuery
- Looker Studio
- CoinGecko API (free tier)

## Data Flow

### Bronze layer
Raw JSON files from CoinGecko API stored hourly in GCS.

### Silver layer
Cleaned and structured data loaded into BigQuery with defined schema.

### Gold layer
Aggregated views for analytics:
- `gold_daily_prices`: daily avg/max/min price per coin
- `gold_daily_ranking`: daily ranking by market cap
- `gold_hourly_variation`: hourly price variation percentage

## Dashboard
Live dashboard built in Looker Studio connected to BigQuery gold layer.

## Infrastructure
- All services deployed on GCP Free Tier (us-central1)
- Hourly ingestion scheduled via Cloud Scheduler
- Serverless architecture, zero idle cost
