SELECT
  athlete,
  bucket,
  brand_signed_with,
  has_signature_shoe,
  google_trends_pct_change,
  google_trends_12mo_avg
FROM `still-smithy-442121-n3.athelete_shoes.v_athletes_master`
ORDER BY google_trends_pct_change DESC
LIMIT 10;
