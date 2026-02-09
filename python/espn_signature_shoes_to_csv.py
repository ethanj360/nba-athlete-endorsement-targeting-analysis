import re
import pandas as pd
from bs4 import BeautifulSoup

with open("espn_page.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# Grab all visible text as a list of tokens, in order
tokens = list(soup.stripped_strings)

def is_models_token(s: str) -> bool:
    s = s.lower()
    return "model" in s and any(ch.isdigit() for ch in s)

rows = []
i = 0

# The page repeats card blocks that look like:
# Newest
# Nike KD
# Kevin Durant
# 2009—2025
# 28 models
while i < len(tokens):
    if tokens[i] == "Newest":
        # Defensive parsing: check the next few tokens exist
        if i + 4 < len(tokens):
            line_name = tokens[i + 1]
            athlete = tokens[i + 2]
            years = tokens[i + 3]
            models = tokens[i + 4]

            # Confirm it is really a card by checking the models text
            if is_models_token(models):
                # Extract brand from the line name (first word usually)
                brand_guess = line_name.split()[0]

                # Extract model count number
                m = re.search(r"(\d+)", models)
                model_count = int(m.group(1)) if m else None

                rows.append({
                    "brand": brand_guess,
                    "signature_line": line_name,
                    "athlete": athlete,
                    "years": years,
                    "model_count": model_count
                })

        i += 1
    else:
        i += 1

df = pd.DataFrame(rows).drop_duplicates()

print("Rows found:", len(df))
print(df.head(15))

df.to_csv("espn_signature_shoes.csv", index=False)
print("Saved espn_signature_shoes.csv")
