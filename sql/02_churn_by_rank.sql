-- Churn rate by highest rank each player reached
-- Churned = no session on or after 2025-06-17 (the last 14 days of the data)

WITH ranked_matches AS (
  SELECT player_id,
         CASE rank_tier
           WHEN 'Iron'     THEN 1
           WHEN 'Bronze'   THEN 2
           WHEN 'Silver'   THEN 3
           WHEN 'Gold'     THEN 4
           WHEN 'Platinum' THEN 5
           WHEN 'Diamond'  THEN 6
         END AS rank_num
  FROM matches
),
highest_rank AS (
  SELECT player_id, MAX(rank_num) AS top_rank
  FROM ranked_matches
  GROUP BY player_id
),
last_session AS (
  SELECT player_id, MAX(session_date) AS last_played
  FROM sessions
  GROUP BY player_id
)
SELECT
  CASE h.top_rank
    WHEN 1 THEN 'Iron'   WHEN 2 THEN 'Bronze'   WHEN 3 THEN 'Silver'
    WHEN 4 THEN 'Gold'   WHEN 5 THEN 'Platinum' WHEN 6 THEN 'Diamond'
  END AS highest_rank,
  COUNT(*) AS players,
  SUM(CASE WHEN l.last_played < '2025-06-17' THEN 1 ELSE 0 END) AS churned,
  ROUND(100.0 * SUM(CASE WHEN l.last_played < '2025-06-17' THEN 1 ELSE 0 END) / COUNT(*), 1) AS churn_pct
FROM highest_rank h
JOIN last_session l ON h.player_id = l.player_id
GROUP BY h.top_rank
ORDER BY h.top_rank;