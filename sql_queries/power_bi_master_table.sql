CREATE OR REPLACE VIEW `still-smithy-442121-n3.athelete_shoes.v_athletes_master` AS
SELECT
  athlete,
  bucket,
  brand_signed_with,
  has_signature_shoe,

  current_team,
  position,
  age,
  year_drafted,

  games_played,
  games_played_pct,
  minutes_per_game,
  points_per_game,
  usage_rate_pct,

  ig_follower_count,
  engagement_rate_pct,

  google_trends_12mo_avg,
  google_trends_early_12_wk_avg,
  google_trends_recent_12wk_avg,
  google_trends_pct_change,

##better for charts
  SAFE_DIVIDE(points_per_game, NULLIF(minutes_per_game, 0)) * 36 AS points_per_36,
  SAFE_DIVIDE(usage_rate_pct, NULLIF(minutes_per_game, 0)) AS usage_per_minute,

  LOG(ig_follower_count + 1) AS log_ig_followers,

  CASE
    WHEN google_trends_pct_change >= 0.25 THEN 'Rising Fast'
    WHEN google_trends_pct_change >= 0.10 THEN 'Rising'
    WHEN google_trends_pct_change > -0.10 THEN 'Stable'
    ELSE 'Declining'
  END AS trends_momentum

FROM `still-smithy-442121-n3.athelete_shoes.athlete_shoes_data_set`;
