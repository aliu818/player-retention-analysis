-- Average session length: players who quit vs. players who stayed
-- Churned = no session on or after 2025-06-17

WITH player_status AS (
  SELECT player_id,
         CASE WHEN MAX(session_date) < '2025-06-17' THEN 'Churned' ELSE 'Retained' END AS status,
         AVG(duration_min) AS avg_session_min
  FROM sessions
  GROUP BY player_id
)
SELECT
  status,
  COUNT(*) AS players,
  ROUND(AVG(avg_session_min), 1) AS avg_session_min
FROM player_status
GROUP BY status;