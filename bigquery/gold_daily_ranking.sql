CREATE OR REPLACE VIEW `cryptolake.gold_daily_ranking` AS
SELECT
  date,
  coin_id,
  name,
  symbol,
  avg_price,
  avg_market_cap,
  RANK() OVER (
    PARTITION BY date
    ORDER BY avg_market_cap DESC
  ) AS ranking
FROM (
  SELECT
    DATE(ingested_at)          AS date,
    coin_id,
    name,
    symbol,
    ROUND(AVG(price_usd), 4)   AS avg_price,
    ROUND(AVG(market_cap), 0)  AS avg_market_cap
  FROM `cryptolake.silver_crypto`
  GROUP BY DATE(ingested_at), coin_id, name, symbol
)
ORDER BY date DESC, ranking ASC;
