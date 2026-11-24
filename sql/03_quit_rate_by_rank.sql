-- Quit rate per play-day at each rank
-- For each day a player played, find their rank at the end of that day.
-- Then: what % of those days were the player's last day before quitting?

WITH end_of_day AS (
  SELECT player_id, match_date, MAX(match_id) AS last_match_id
  FROM matches
  GROUP BY player_id, match_date
),
day_rank AS (
  SELECT e.player_id, e.match_date, m.rank_tier
  FROM end_of_day e
  JOIN matches m ON m.match_id = e.last_match_id
),
final_day AS (
  SELECT player_id, MAX(match_date) AS last_played
  FROM matches
  GROUP BY player_id
)
SELECT
  d.rank_tier,
  COUNT(*) AS play_days,
  SUM(CASE WHEN d.match_date = f.last_played AND f.last_played < '2025-06-17' THEN 1 ELSE 0 END) AS quit_days,
  ROUND(100.0 * SUM(CASE WHEN d.match_date = f.last_played AND f.last_played < '2025-06-17' THEN 1 ELSE 0 END) / COUNT(*), 1) AS quit_rate_pct
FROM day_rank d
JOIN final_day f ON d.player_id = f.player_id
GROUP BY d.rank_tier
ORDER BY quit_rate_pct DESC;