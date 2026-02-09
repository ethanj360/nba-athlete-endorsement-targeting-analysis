SELECT
  athlete,
  bucket,
  brand_signed_with,
  age,
  current_team,
  position,
  minutes_per_game,
  points_per_game,
  usage_rate_pct,
  ig_follower_count,
  engagement_rate_pct,
  google_trends_pct_change
FROM `still-smithy-442121-n3.athelete_shoes.v_athletes_master`
WHERE has_signature_shoe IN ('N')
ORDER BY
  google_trends_pct_change DESC,
  engagement_rate_pct DESC,
  usage_rate_pct DESC,
  minutes_per_game DESC
LIMIT 10;
