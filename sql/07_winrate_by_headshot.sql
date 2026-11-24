-- Win rate by headshot % bucket (one row per match)

SELECT
  CASE
    WHEN headshot_pct < 15 THEN '1) Under 15%'
    WHEN headshot_pct < 20 THEN '2) 15-20%'
    WHEN headshot_pct < 25 THEN '3) 20-25%'
    WHEN headshot_pct < 30 THEN '4) 25-30%'
    ELSE                        '5) 30% and up'
  END AS headshot_bucket,
  COUNT(*) AS matches,
  ROUND(100.0 * AVG(win), 1) AS win_rate_pct
FROM matches
GROUP BY headshot_bucket
ORDER BY headshot_bucket;