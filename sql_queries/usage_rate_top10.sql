SELECT
  athlete,
  bucket,
  brand_signed_with,
  has_signature_shoe,
  usage_rate_pct,
  minutes_per_game,
  points_per_game
FROM `still-smithy-442121-n3.athelete_shoes.v_athletes_master`
ORDER BY usage_rate_pct DESC
LIMIT 10;
