SELECT
  athlete,
  bucket,
  has_signature_shoe,
  brand_signed_with,
  log_ig_followers AS x_log_followers,
  engagement_rate_pct AS y_engagement,
  google_trends_pct_change AS tooltip_trends_change,
  usage_rate_pct AS tooltip_usage
FROM `still-smithy-442121-n3.athelete_shoes.v_athletes_master`;
