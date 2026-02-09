SELECT
  CASE
    WHEN has_signature_shoe IN ('Y') THEN 'Has Signature Shoe'
    ELSE 'No Signature Shoe'
  END AS signature_group,
  COUNT(*) AS athletes,
  AVG(minutes_per_game) AS avg_mpg,
  AVG(points_per_game) AS avg_ppg,
  AVG(usage_rate_pct) AS avg_usage,
  AVG(ig_follower_count) AS avg_followers,
  AVG(engagement_rate_pct) AS avg_engagement,
  AVG(google_trends_12mo_avg) AS avg_trends_12mo,
  AVG(google_trends_pct_change) AS avg_trends_change
FROM `still-smithy-442121-n3.athelete_shoes.v_athletes_master`
GROUP BY signature_group
ORDER BY signature_group;
