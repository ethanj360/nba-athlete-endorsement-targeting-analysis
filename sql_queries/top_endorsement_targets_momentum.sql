SELECT
  athlete,
  bucket,
  brand_signed_with,
  has_signature_shoe,
  age,
  current_team,
  position,
  ig_follower_count,
  engagement_rate_pct,
  google_trends_12mo_avg,
  google_trends_pct_change,
  minutes_per_game,
  points_per_game,
  usage_rate_pct
FROM `still-smithy-442121-n3.athelete_shoes.v_athletes_master`
WHERE has_signature_shoe IN ('N')
ORDER BY
  google_trends_pct_change DESC,
  engagement_rate_pct DESC,
  usage_rate_pct DESC;
