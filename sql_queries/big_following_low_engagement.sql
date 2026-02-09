SELECT
  athlete,
  bucket,
  brand_signed_with,
  ig_follower_count,
  engagement_rate_pct,
  google_trends_pct_change,
  has_signature_shoe
FROM `still-smithy-442121-n3.athelete_shoes.v_athletes_master`
ORDER BY ig_follower_count DESC, engagement_rate_pct ASC;
