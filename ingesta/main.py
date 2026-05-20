import functions_framework
import requests
import json
from datetime import datetime
from google.cloud import storage

BUCKET_NAME = "cryptolake-data-ian"  # cambia esto por el nombre exacto de tu bucket

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"

PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 20,
    "page": 1,
    "sparkline": False
}

@functions_framework.http
def ingest_crypto(request):
    try:
        # Llamar a CoinGecko
        response = requests.get(COINGECKO_URL, params=PARAMS)
        response.raise_for_status()
        data = response.json()

        # Añadir timestamp de ingesta
        payload = {
            "ingested_at": datetime.utcnow().isoformat(),
            "data": data
        }

        # Guardar en GCS bronze/
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"bronze/crypto_{timestamp}.json"

        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(filename)
        blob.upload_from_string(
            json.dumps(payload, indent=2),
            content_type="application/json"
        )

        return f"OK: {filename} guardado en GCS", 200

    except Exception as e:
        return f"Error: {str(e)}", 500