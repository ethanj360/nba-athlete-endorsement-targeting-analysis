import re
import pandas as pd

RAW_FILE = "espn_signature_shoes_all_pages.csv"
CLEAN_FILE = "espn_signature_shoes_cleaned.csv"

BRAND_NORMALIZE = {
    "UA": "Under Armour",
    "Under": "Under Armour",
    "NB": "New Balance",
    "361": "361 Degrees",
    "Curry": "Under Armour",
    "BBB": "Big Baller Brand",
}

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
    first = s.split(" ")[0] if s else ""
    return BRAND_NORMALIZE.get(first, first)

def parse_model_count(x):
    s = clean_text(x)
    if not s:
        return pd.NA
    m = re.search(r"(\d+)", s)
    return int(m.group(1)) if m else pd.NA

df = pd.read_csv(RAW_FILE, dtype=str).fillna("")
df.columns = [c.strip().lower() for c in df.columns]

for c in ["brand", "signature_line", "athlete", "years", "model_count"]:
    df[c] = df[c].map(clean_text)

# Fix "Newest" shifted rows
mask_newest_shift = (df["brand"].str.lower() == "newest") & (df["signature_line"].str.lower() == "newest")
if mask_newest_shift.any():
    df.loc[mask_newest_shift, "signature_line"] = df.loc[mask_newest_shift, "athlete"]
    df.loc[mask_newest_shift, "athlete"] = df.loc[mask_newest_shift, "years"]
    df.loc[mask_newest_shift, "years"] = ""
    df.loc[mask_newest_shift, "model_count"] = ""

    df.loc[mask_newest_shift, "brand"] = df.loc[mask_newest_shift, "signature_line"].map(infer_brand_from_signature)

# Drop leftover pure UI "Newest" rows
df = df[~(df["brand"].str.lower() == "newest")]
df = df[~(df["signature_line"].str.lower() == "newest")]

# Normalize brand names
df["brand"] = df["brand"].replace(BRAND_NORMALIZE)

# If brand is Iconic, move it into a tag and infer real brand
df["tag"] = pd.NA
mask_iconic = df["brand"].str.lower() == "iconic"
df.loc[mask_iconic, "tag"] = "Iconic"
df.loc[mask_iconic, "brand"] = df.loc[mask_iconic, "signature_line"].map(infer_brand_from_signature)

# Years cleanup: normalize dash but do NOT force "Multiple decades"
df["years"] = df["years"].str.replace("—", "-", regex=False).str.replace("–", "-", regex=False)
df.loc[df["years"].eq(""), "years"] = pd.NA

# Model count cleanup
df["model_count"] = df["model_count"].map(parse_model_count).astype("Int64")

# Remove duplicates
df = df.drop_duplicates(subset=["brand", "signature_line", "athlete", "years", "model_count", "tag"])

# Sort
df = df.sort_values(by=["brand", "signature_line", "athlete"], na_position="last").reset_index(drop=True)

df.to_csv(CLEAN_FILE, index=False)
print(f"Saved cleaned file: {CLEAN_FILE} | rows: {len(df)}")
