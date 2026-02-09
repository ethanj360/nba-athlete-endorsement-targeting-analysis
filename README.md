# NBA Athlete Endorsement Targeting Analysis
### A Data-Driven Look at Signature Shoe and Endorsement Upside

---

## Overview

I’ve always been interested in how certain NBA players end up with signature shoes or long-term footwear deals even when, at the time, they were not obvious “face of the league” superstars. Players like Klay Thompson, Kevin Love, and Donovan Mitchell didn’t enter the league with the same hype as players like LeBron or KD, yet their endorsements became major brand assets.

That gap between star power and endorsement success is what sparked this project.

Rather than asking why certain deals worked in hindsight, I wanted to understand how athletic shoe brands might identify those opportunities before they become obvious. What signals actually matter when deciding which athletes are worth betting on long term?

This project analyzes NBA athletes using a combination of on-court performance data, social engagement metrics, and public interest trends to identify which players — and which types of players — offer the highest endorsement upside right now. While the focus is on basketball, the analytical framework is intentionally transferable to other industries such as influencer marketing, celebrity endorsements, and brand partnerships.

---

## Core Business Question

**Which NBA athletes or athlete profiles offer the highest endorsement upside for athletic shoe brands?**

This project intentionally avoids framing the question as “who should brands sign next.” In practice, most NBA players are already under exclusive endorsement contracts or receive player-exclusive colorways with their current brand.

Instead, the analysis reflects how brands actually operate:
- Which athletes should receive deeper investment?
- Who is best positioned for signature shoe development?
- Which players represent high-ROI opportunities that are not yet fully locked in?
- Where is momentum building before it becomes obvious?

---

## Client Context

**Client Type**  
Athletic shoe companies such as Nike, Adidas, Puma, Anta, Jordan Brand, and similar brands.

**Business Objective**  
Support endorsement and marketing decision-making by identifying athletes with strong growth signals, engagement quality, and long-term brand value rather than relying solely on reputation or existing star status.

---

## Factors Considered

This project combines performance indicators with off-court audience signals to better reflect real endorsement decision-making.

Key factors include:
- Instagram engagement rate (not just follower count)
- Audience growth and interaction quality
- Google Trends momentum over time
- Usage rate, minutes, and on-court role
- Career stage and age
- Endorsement saturation and cost efficiency

The goal is not to rank basketball skill, but to estimate endorsement potential.

---

## Athlete Selection Strategy

Athletes were selected using a **stratified sampling approach** across career stage, endorsement status, and market visibility to model real-world endorsement decision-making rather than ranking player skill.

To ensure comparability across athletes, all performance and popularity metrics were measured over the same recent time window. Historical signature shoe data was used for classification and benchmarking rather than time-aligned modeling.

### Athlete Buckets

**Established Signature Athletes (Benchmark Group)**  
LeBron James  
Kevin Durant  
Stephen Curry  
Damian Lillard  
Giannis Antetokounmpo  
James Harden  

**Young Signature Bets**  
Anthony Edwards  
Ja Morant  
Zion Williamson  
LaMelo Ball  
Cade Cunningham  
Tyrese Maxey  
Tyrese Haliburton  
Deni Avdija  

**High-Value Targets (No Signature Shoe)**  
Domantas Sabonis  
Alperen Sengun  
Jamal Murray  
Pascal Siakam  
Jrue Holiday  
Jalen Duren  
Chet Holmgren  
Scottie Barnes  
Evan Mobley  
Jalen Williams  
Brandon Miller  
Amen Thompson  
Ausar Thompson  
Keyonte George  

**Marketable Role Players / Undervalued Plays**  
Austin Reaves  
Mikal Bridges  
Jordan Clarkson  
Bronny James  

**Risk or Mixed Outcomes**  
Andrew Wiggins  
Lonzo Ball  
Klay Thompson  

---

## Data Sources

- [Google Trends](https://trends.google.com/trends/)
- Instagram public metrics via [Social Blade](https://socialblade.com/instagram)
- [Basketball Reference](https://www.basketball-reference.com/) for NBA player statistics
- Public endorsement and signature shoe history
- [ESPN sneaker database](https://www.espn.com/espn/feature/story/_/id/39771146/sneakerhead-guide-every-nba-wnba-signature-sneaker-history)

---

## Data Collection and Preparation

### Web Scraping and Extraction

Python was used to extract endorsement-related data:
- `requests` to retrieve web content
- `BeautifulSoup4` to parse HTML
- `pandas` to clean and structure data

Extracted information included athlete names, shoe lines, brands, leagues, and time periods. Cleaned datasets were exported to CSV files for SQL analysis and visualization.

### Manual Validation

Certain metrics — especially engagement rate calculations and Google Trends comparisons — required manual validation to ensure consistent time windows and realistic comparisons. This tradeoff was intentional to prioritize data quality over full automation.

---

## Data Cleaning Challenges

###TLDR

- Data came from multiple sources, so a lot of time went into making sure metrics were comparable before analysis

- BigQuery schema issues required manually defining data types to prevent silent ingestion errors

- Percentage fields were inconsistent across tools and had to be normalized and revalidated in Power BI

- Raw follower counts were misleading, so engagement rate was used to better measure audience quality

- Midway through the project, the business question was reframed to focus on endorsement upside rather than unrealistic contract signings


This project involved more hands-on data cleaning than I initially expected. Because the data came from multiple sources (web scraping, manual tracking, and public datasets), a lot of the work was about making sure numbers actually meant the same thing before comparing them.

One of the first issues I ran into was schema conflicts when loading data into BigQuery. Some fields were being inferred incorrectly, especially percentages and numeric columns pulled from CSV exports. Instead of relying on auto-detection, I manually defined the schema and validated each column to avoid silent type errors that would affect downstream calculations.

Another recurring issue was inconsistent percentage formatting. Some metrics were stored as decimals, others as percentages, and a few changed formats between tools. I normalized these values in Power Query, then double-checked them again in Power BI’s model view after noticing visuals still rendering decimals instead of percentages. That extra validation step ended up catching multiple formatting issues that would have gone unnoticed otherwise.

Social media metrics introduced their own problems. Raw follower counts were heavily skewed toward established stars, which made it hard to compare newer or less visible players. To avoid overstating popularity, I shifted the analysis toward engagement rate rather than total followers. This decision better reflected how actively an audience interacts with a player, not just how large the audience is.

Finally, there was a framing issue that emerged mid-project. I initially approached the analysis as “which athletes should brands sign next,” but that didn’t reflect how endorsement deals actually work. Most players are already tied to brands, and outright contract poaching isn’t realistic. I reworked the business question to focus on endorsement upside instead: identifying which athletes brands should invest in more deeply through signature shoes, expanded marketing, or long-term positioning. That reframing made the analysis more practical and aligned it with real brand decision-making.


---

## Final Dataset Schema

athlete
games_played
games_played_pct
minutes_per_game
points_per_game
usage_rate_pct
ig_follower_count
engagement_rate_pct
google_trends_12mo_avg
google_trends_recent_12wk_avg
google_trends_early_12wk_avg
google_trends_pct_change
age
position
current_team
year_drafted
has_signature_shoe
brand_signed_with
bucket

##Analysis Approach

The analysis is driven by SQL views built in Google BigQuery. Percentile-based normalization was used to compare athletes across metrics with different scales.

A weighted endorsement score was created to reflect how brands balance:

- Momentum and engagement

- On-court role and visibility

- Audience size

- Long-term runway (age)

This mirrors real-world endorsement decision-making more closely than pure performance rankings.

##Deliverables

1. Clear definition of the business task and client objective

2. Documented data sources and collection methods

3. Cleaned and structured endorsement dataset

4. SQL-based analytical views and scoring logic

5. Power BI dashboard with narrative-driven visualizations

6. Athlete segmentation and bucket analysis

7. Brand-specific endorsement targeting insights

8. Strategic takeaways and recommendations for future analysis

##Key Takeaways

- Engagement and momentum often matter more than raw follower count

- Several non-signature athletes show stronger growth signals than current signature holders

- Young players with high usage and rising public interest represent strong long-term endorsement bets

- Some established endorsements show declining momentum despite large audiences

##Why This Project Matters

Endorsement decisions are ultimately bets made under uncertainty. This project focuses on reducing that uncertainty by combining performance, audience behavior, and public interest signals into a single analytical framework.

The same logic applies beyond basketball; anywhere brands need to decide who to invest in before the upside is obvious.

##What I Learned

This project strengthened my ability to:

- Translate open-ended business questions into measurable analytical problems

- Work through real-world data quality issues instead of ideal datasets

- Balance automation with manual validation when accuracy matters

- Use SQL not just for querying, but for modeling business decisions

- Communicate analysis in a way that reflects how brands actually operate

- More importantly, it reinforced that strong analysis often comes from reframing the question, not just running more queries.
