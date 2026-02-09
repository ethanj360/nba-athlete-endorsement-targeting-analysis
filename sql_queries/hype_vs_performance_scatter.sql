SELECT
  athlete,
  bucket,
  has_signature_shoe,
  brand_signed_with,
  usage_rate_pct AS x_usage,
  google_trends_pct_change AS y_trends_change,
  engagement_rate_pct AS bubble_engagement,
  ig_follower_count AS bubble_followers
FROM `still-smithy-442121-n3.athelete_shoes.v_athletes_master`;
