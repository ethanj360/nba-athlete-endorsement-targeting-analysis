import requests
from bs4 import BeautifulSoup

URL = "https://www.espn.com/espn/feature/story/_/id/39771146/sneakerhead-guide-every-nba-wnba-signature-sneaker-history"

headers = {
    "User-Agent": "Mozilla/5.0"
}

resp = requests.get(URL, headers=headers, timeout=30)
print("Status:", resp.status_code)
print("Length:", len(resp.text))

soup = BeautifulSoup(resp.text, "html.parser")

# quick sanity check: print the page title
title = soup.title.get_text(strip=True) if soup.title else "No title found"
print("Title:", title)

# article title

article = soup.find("article")

if not article:
    print("No <article> tag found. Trying fallback containers...")
    article = soup.find("div")

text = article.get_text("\n", strip=True)

print("\n--- ARTICLE TEXT PREVIEW ---\n")
print(text[:2000])
