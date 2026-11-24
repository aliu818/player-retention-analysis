SELECT
  (SELECT COUNT(*) FROM players)  AS players,
  (SELECT COUNT(*) FROM matches)  AS matches,
  (SELECT COUNT(*) FROM sessions) AS sessions,
  (SELECT COUNT(*) FROM patches)  AS patches;