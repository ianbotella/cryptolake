CREATE OR REPLACE VIEW `cryptolake.gold_daily_prices` AS
SELECT
  coin_id,
  name,
  symbol,
  DATE(ingested_at) AS date,
  ROUND(AVG(price_usd), 4)  AS avg_price,
  ROUND(MAX(price_usd), 4)  AS max_price,
  ROUND(MIN(price_usd), 4)  AS min_price,
  ROUND(AVG(change_24h), 2) AS avg_change_24h,
  ROUND(AVG(market_cap), 0) AS avg_market_cap
FROM `cryptolake.silver_crypto`
GROUP BY coin_id, name, symbol, DATE(ingested_at)
ORDER BY date DESC, avg_market_cap DESC;
