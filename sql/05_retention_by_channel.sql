-- Retention by acquisition channel
-- churn_pct      = % of players with no session on or after 2025-06-17
-- avg_days_kept  = average days between signup and last session

WITH last_session AS (
  SELECT player_id, MAX(session_date) AS last_played
  FROM sessions
  GROUP BY player_id
)
SELECT
  p.acquisition_channel,
  COUNT(*) AS players,
  ROUND(100.0 * SUM(CASE WHEN l.last_played < '2025-06-17' THEN 1 ELSE 0 END) / COUNT(*), 1) AS churn_pct,
  ROUND(AVG(julianday(l.last_played) - julianday(p.signup_date)), 1) AS avg_days_kept
FROM players p
JOIN last_session l ON p.player_id = l.player_id
GROUP BY p.acquisition_channel
ORDER BY avg_days_kept DESC;