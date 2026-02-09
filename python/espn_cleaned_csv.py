import re
import pandas as pd


RAW_FILE = "espn_signature_shoes_all_pages.csv"          # your current file name
CLEAN_FILE = "espn_signature_shoes_cleaned.csv"          # new cleaned output

# Brand normalization map
BRAND_NORMALIZE = {
    "UA": "Under Armour",
    "Under": "Under Armour",
    "Under Armour": "Under Armour",
    "NB": "New Balance",
    "New Balance": "New Balance",
    "Li-Ning": "Li-Ning",
    "361": "361 Degrees",
    "Curry": "Under Armour",          # Curry line is Under Armour
    "BBB": "Big Baller Brand",
    "Jordan": "Jordan",
}

# For cases where brand is missing or wrong, infer from signature_line prefix
# Order matters: check longer phrases first
BRAND_KEYWORDS = [
    ("Under Armour", "Under Armour"),
    ("New Balance", "New Balance"),
    ("Li-Ning", "Li-Ning"),
    ("Converse", "Converse"),
    ("Adidas", "Adidas"),
    ("Jordan", "Jordan"),
    ("Nike", "Nike"),
    ("Puma", "Puma"),
    ("Anta", "Anta"),
    ("Peak", "Peak"),
    ("Rigorer", "Rigorer"),
    ("HOLO", "HOLO"),
    ("Q4", "Q4"),
    ("K8RIOS", "K8RIOS"),
    ("Ethics", "Ethics"),
    ("Reebok", "Reebok"),
    ("361", "361 Degrees"),
]

def clean_text(x):
    if pd.isna(x):
        return ""
    s = str(x).strip()
    s = re.sub(r"\s+", " ", s)
    return s

def infer_brand_from_signature(signature_line: str) -> str:
    s = clean_text(signature_line)
    for key, val in BRAND_KEYWORDS:
        if s.startswith(key + " ") or s == key:
            return val
    # fallback: first token (works for many)
    first = s.split(" ")[0] if s else ""
    return BRAND_NORMALIZE.get(first, first)

def parse_model_count(x):
    """
    Handles values like:
    2.0
    "2"
    "2 models"
    "1 model"
    ""
    """
    s = clean_text(x)
    if not s:
        return pd.NA
    m = re.search(r"(\d+)", s)
    if not m:
        return pd.NA
    return int(m.group(1))

def looks_like_person_name(s: str) -> bool:
    # simple heuristic: two words, both start with letters, often works for athlete names
    s = clean_text(s)
    parts = s.split()
    return len(parts) >= 2 and all(p[0].isalpha() for p in parts)

df = pd.read_csv(RAW_FILE, dtype=str).fillna("")

# Normalize column names if needed
df.columns = [c.strip().lower() for c in df.columns]

required = ["brand", "signature_line", "athlete", "years", "model_count"]
missing_cols = [c for c in required if c not in df.columns]
if missing_cols:
    raise ValueError(f"Missing expected columns: {missing_cols}. Your CSV headers must be: {required}")

# Basic trimming
for c in required:
    df[c] = df[c].map(clean_text)


# Fix rows polluted by UI "Newest" badge
# Example bad row:
# brand=Newest, signature_line=Newest, athlete=Converse SHAI, years=Shai Gilgeous-Alexander, model_count=""
# We shift fields and infer brand from the signature_line

mask_newest_shift = (df["brand"].str.lower() == "newest") & (df["signature_line"].str.lower() == "newest")

if mask_newest_shift.any():
    # shift columns
    sig = df.loc[mask_newest_shift, "athlete"]
    ath = df.loc[mask_newest_shift, "years"]

    df.loc[mask_newest_shift, "signature_line"] = sig
    df.loc[mask_newest_shift, "athlete"] = ath
    df.loc[mask_newest_shift, "years"] = ""          # unknown in these rows unless you scraped it elsewhere
    df.loc[mask_newest_shift, "model_count"] = ""    # unknown in these rows unless you scraped it elsewhere

    # brand inference from signature_line
    df.loc[mask_newest_shift, "brand"] = df.loc[mask_newest_shift, "signature_line"].map(infer_brand_from_signature)

# Drop any leftover pure UI rows (brand or signature_line equals "Newest")
df = df[~(df["brand"].str.lower() == "newest")]
df = df[~(df["signature_line"].str.lower() == "newest")]

# Normalize brands
df["brand"] = df["brand"].replace(BRAND_NORMALIZE)

# If brand is still empty or suspiciously short, infer from signature_line
mask_brand_empty = df["brand"].eq("") | df["brand"].isna()
df.loc[mask_brand_empty, "brand"] = df.loc[mask_brand_empty, "signature_line"].map(infer_brand_from_signature)

# Also correct some known short codes
df["brand"] = df["brand"].replace(BRAND_NORMALIZE)


# Replace weird hyphen variants and normalize em dash to a simple dash
df["years"] = df["years"].str.replace("—", "-", regex=False).str.replace("–", "-", regex=False)

# Fill missing years for iconic or unknown entries
df.loc[df["years"].eq(""), "years"] = "Multiple decades"

# Optional: If years accidentally contains an athlete name (rare), fix
# Example: if years looks like a person name and athlete is empty, swap
mask_years_is_name = df["years"].map(looks_like_person_name) & df["athlete"].eq("")
df.loc[mask_years_is_name, "athlete"] = df.loc[mask_years_is_name, "years"]
df.loc[mask_years_is_name, "years"] = "Multiple decades"

# Model count cleanup
df["model_count"] = df["model_count"].map(parse_model_count)


# Remove exact duplicates
df = df.drop_duplicates(subset=["brand", "signature_line", "athlete", "years", "model_count"])

# Sort for readability
df = df.sort_values(by=["brand", "signature_line", "athlete"]).reset_index(drop=True)

# Save
df.to_csv(CLEAN_FILE, index=False)
print(f"Saved cleaned file: {CLEAN_FILE} | rows: {len(df)}")
