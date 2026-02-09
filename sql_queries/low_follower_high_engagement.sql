SELECT
  athlete,
  bucket,
  brand_signed_with,
  ig_follower_count,
  engagement_rate_pct,
  google_trends_pct_change,
  minutes_per_game,
  usage_rate_pct
FROM `still-smithy-442121-n3.athelete_shoes.v_athletes_master`
WHERE has_signature_shoe IN ('N')
ORDER BY
  engagement_rate_pct DESC,
  google_trends_pct_change DESC,
  ig_follower_count ASC
LIMIT 10;

