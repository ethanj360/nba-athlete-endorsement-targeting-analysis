## Create a scored view that ranks athletes by overall endorsement potential
## This view is meant to help answer: who is worth targeting next and why

CREATE OR REPLACE VIEW `still-smithy-442121-n3.athelete_shoes.v_athletes_scored` AS

## Step 1: create a base table with percentile ranks
## Percentile ranks can compare metrics that are on very different scales
## (followers, engagement, usage, age, etc.)

WITH base AS (
  SELECT
    *,

    ## Public interest momentum relative to everyone else
    PERCENT_RANK() OVER (ORDER BY google_trends_pct_change) AS pr_trends_change,

    ## How strong an athlete’s engagement is compared to peers
    PERCENT_RANK() OVER (ORDER BY engagement_rate_pct) AS pr_engagement,

    ## Offensive involvement relative to others
    PERCENT_RANK() OVER (ORDER BY usage_rate_pct) AS pr_usage,

    ## Playing time as a proxy for role and trust
    PERCENT_RANK() OVER (ORDER BY minutes_per_game) AS pr_mpg,

    ## Overall audience size, but kept as a lighter factor
    PERCENT_RANK() OVER (ORDER BY ig_follower_count) AS pr_followers,

    ## Age percentile (used later as a small penalty)
    PERCENT_RANK() OVER (ORDER BY age) AS pr_age

  FROM `still-smithy-442121-n3.athelete_shoes.v_athletes_master`
)

## Step 2: calculate a final endorsement score
## The weights reflect how brands usually think:
## momentum + engagement matter more than raw fame,
## while age slightly reduces long-term runway

SELECT
  athlete,
  bucket,
  brand_signed_with,
  has_signature_shoe,
  age,
  current_team,
  position,

  ## Raw metrics kept for transparency and dashboard tooltips
  google_trends_pct_change,
  engagement_rate_pct,
  usage_rate_pct,
  minutes_per_game,
  ig_follower_count,

  ## Final composite endorsement score
  ## Higher score = stronger overall endorsement opportunity
  ROUND(
    (0.35 * pr_trends_change) +   -- momentum matters most
    (0.30 * pr_engagement) +      -- strong fan engagement
    (0.15 * pr_usage) +           -- on-court importance
    (0.10 * pr_mpg) +             -- consistent role
    (0.10 * pr_followers) -        -- existing reach (lighter weight)
    (0.10 * pr_age)               -- small penalty for age
  , 4) AS endorsement_score

FROM base;
