SELECT
  brand_signed_with,
  COUNT(*) AS athletes,
  AVG(google_trends_pct_change) AS avg_trends_change,
  AVG(engagement_rate_pct) AS avg_engagement,
  AVG(usage_rate_pct) AS avg_usage
FROM `still-smithy-442121-n3.athelete_shoes.v_athletes_master`
GROUP BY brand_signed_with
ORDER BY avg_trends_change DESC;
