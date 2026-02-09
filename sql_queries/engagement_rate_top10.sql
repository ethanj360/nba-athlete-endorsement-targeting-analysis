SELECT
  athlete,
  bucket,
  brand_signed_with,
  has_signature_shoe,
  engagement_rate_pct,
  ig_follower_count
FROM `still-smithy-442121-n3.athelete_shoes.v_athletes_master`
ORDER BY engagement_rate_pct DESC
LIMIT 10;
