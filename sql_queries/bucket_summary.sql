SELECT
  bucket,
  COUNT(*) AS athletes,
  AVG(age) AS avg_age,
  AVG(minutes_per_game) AS avg_mpg,
  AVG(points_per_game) AS avg_ppg,
  AVG(usage_rate_pct) AS avg_usage,
  AVG(engagement_rate_pct) AS avg_engagement,
  AVG(google_trends_12mo_avg) AS avg_trends_12mo,
  AVG(google_trends_pct_change) AS avg_trends_change
FROM `still-smithy-442121-n3.athelete_shoes.v_athletes_master`
GROUP BY bucket
ORDER BY avg_trends_change DESC;
