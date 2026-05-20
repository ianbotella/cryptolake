import functions_framework
import json
from datetime import datetime
from google.cloud import storage, bigquery

BUCKET_NAME = "cryptolake-data-ian"  # cambia por tu bucket
PROJECT_ID = "spheric-method-420317"
DATASET = "cryptolake"
TABLE = "silver_crypto"

@functions_framework.http
def transform_to_silver(request):
    try:
        storage_client = storage.Client()
        bq_client = bigquery.Client()
        bucket = storage_client.bucket(BUCKET_NAME)

        # Listar archivos en bronze/ no procesados
        blobs = list(bucket.list_blobs(prefix="bronze/"))
        if not blobs:
            return "No hay archivos en bronze/", 200

        rows_inserted = 0
        processed_files = 0

        for blob in blobs:
            if not blob.name.endswith(".json"):
                continue

            # Leer el JSON
            content = json.loads(blob.download_as_text())
            ingested_at = content.get("ingested_at")
            coins = content.get("data", [])

            # Transformar cada moneda
            rows = []
            for coin in coins:
                rows.append({
                    "coin_id":     coin.get("id"),
                    "name":        coin.get("name"),
                    "symbol":      coin.get("symbol"),
                    "price_usd":   coin.get("current_price"),
                    "market_cap":  coin.get("market_cap"),
                    "volume_24h":  coin.get("total_volume"),
                    "change_24h":  coin.get("price_change_percentage_24h"),
                    "ingested_at": ingested_at,
                    "loaded_at":   datetime.utcnow().isoformat()
                })

            # Insertar en BigQuery
            table_ref = f"{PROJECT_ID}.{DATASET}.{TABLE}"
            errors = bq_client.insert_rows_json(table_ref, rows)
            if errors:
                return f"Error insertando en BQ: {errors}", 500

            rows_inserted += len(rows)
            processed_files += 1

        return f"OK: {processed_files} archivos procesados, {rows_inserted} filas insertadas en silver", 200

    except Exception as e:
        return f"Error: {str(e)}", 500