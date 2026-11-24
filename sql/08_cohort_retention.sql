-- Day 1 / 7 / 30 retention by weekly signup cohort
-- "Day N retention" = % of players who still played on or after day N after signing up
-- Day 30 is blank for players who signed up too late to measure (after 2025-05-31)

WITH player_days AS (
  SELECT
    p.player_id,
    p.signup_date,
    date(p.signup_date, '-6 days', 'weekday 1') AS cohort_week,
    MAX(julianday(s.session_date) - julianday(p.signup_date)) AS last_day
  FROM players p
  LEFT JOIN sessions s ON p.player_id = s.player_id
  GROUP BY p.player_id, p.signup_date
)
SELECT
  cohort_week,
  COUNT(*) AS signups,
  ROUND(100.0 * AVG(CASE WHEN last_day >= 1 THEN 1 ELSE 0 END), 1) AS day1_pct,
  ROUND(100.0 * AVG(CASE WHEN last_day >= 7 THEN 1 ELSE 0 END), 1) AS day7_pct,
  ROUND(100.0 * SUM(CASE WHEN last_day >= 30 AND signup_date <= '2025-05-31' THEN 1 ELSE 0 END)
              / SUM(CASE WHEN signup_date <= '2025-05-31' THEN 1 ELSE 0 END), 1) AS day30_pct
FROM player_days
GROUP BY cohort_week
ORDER BY cohort_week;