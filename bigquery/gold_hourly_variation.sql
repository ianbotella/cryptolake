CREATE OR REPLACE VIEW `cryptolake.gold_hourly_variation` AS
SELECT
  coin_id,
  name,
  symbol,
  ingested_at,
  price_usd,
  LAG(price_usd) OVER (
    PARTITION BY coin_id
    ORDER BY ingested_at
  ) AS prev_price,
  ROUND(
    (price_usd - LAG(price_usd) OVER (
      PARTITION BY coin_id ORDER BY ingested_at
    )) / NULLIF(LAG(price_usd) OVER (
      PARTITION BY coin_id ORDER BY ingested_at
    ), 0) * 100, 4
  ) AS pct_change
FROM `cryptolake.silver_crypto`
ORDER BY ingested_at DESC, coin_id;
