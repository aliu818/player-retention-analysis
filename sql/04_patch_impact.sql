-- Active players in the week before each patch vs. the two weeks after
-- (Launch is skipped because there is no "week before" it)

WITH patch_activity AS (
  SELECT
    p.patch_id,
    p.note,
    COUNT(DISTINCT CASE WHEN s.session_date >= date(p.release_date, '-7 days')
                         AND s.session_date <  p.release_date
                        THEN s.player_id END) AS active_before,
    COUNT(DISTINCT CASE WHEN s.session_date >= p.release_date
                         AND s.session_date <  date(p.release_date, '+7 days')
                        THEN s.player_id END) AS active_week1,
    COUNT(DISTINCT CASE WHEN s.session_date >= date(p.release_date, '+7 days')
                         AND s.session_date <  date(p.release_date, '+14 days')
                        THEN s.player_id END) AS active_week2
  FROM patches p
  CROSS JOIN sessions s
  WHERE p.note <> 'Launch'
  GROUP BY p.patch_id, p.note
)
SELECT
  patch_id,
  note,
  active_before,
  active_week1,
  active_week2,
  ROUND(100.0 * (active_week1 - active_before) / active_before, 1) AS change_week1_pct,
  ROUND(100.0 * (active_week2 - active_before) / active_before, 1) AS change_week2_pct
FROM patch_activity
ORDER BY patch_id;