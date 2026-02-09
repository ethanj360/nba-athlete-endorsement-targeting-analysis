from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

URL = "https://www.espn.com/espn/feature/story/_/id/39771146/sneakerhead-guide-every-nba-wnba-signature-sneaker-history"

def parse_model_count(text: str) -> int:
    m = re.search(r"(\d+)\s*model", text.lower())
    return int(m.group(1)) if m else None

def scrape_current_page(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    rows = []

    cards = soup.select("a[href*='/espn/feature/story/_/id/']")  # broad
    # The ESPN page uses many links, so we filter by ones that contain a model count line
    for a in cards:
        text = a.get_text("\n", strip=True)
        if "model" not in text.lower():
            continue

        lines = [ln.strip() for ln in text.split("\n") if ln.strip()]

        # Typical card lines look like
        # Brand Line Name
        # Athlete
        # Years
        # X models

        if len(lines) < 4:
            continue

        signature_line = lines[0]
        athlete = lines[1]
        years = lines[2]
        model_count = parse_model_count(lines[3])

        brand = signature_line.split()[0] if signature_line else None

        rows.append({
            "brand": brand,
            "signature_line": signature_line,
            "athlete": athlete,
            "years": years,
            "model_count": model_count
        })

    return rows

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print("Loading page...")
    page.goto(URL, wait_until="domcontentloaded", timeout=120000)
    print("Page loaded")
    print("Current URL:", page.url)

    # Wait for cards to load
    page.wait_for_timeout(3000)

    all_rows = []
    page_num = 1

    while True:
        print("Scraping page", page_num)

        html = page.content()
        rows = scrape_current_page(html)
        print("Rows found:", len(rows))

        all_rows.extend(rows)

        # Try clicking "Last" or "Next" depends on ESPN UI
        # click the ">" button 
        next_button = page.locator("text=>").first

        if next_button.count() == 0:
            print("No next button found. Stopping.")
            break

        # if it is disabled or not clickable, stop
        try:
            next_button.click(timeout=5000)
        except:
            print("Next button not clickable. Stopping.")
            break

        page.wait_for_timeout(2500)
        page_num += 1

    browser.close()

df = pd.DataFrame(all_rows).drop_duplicates()
df.to_csv("espn_signature_shoes_all_pages.csv", index=False)
print("Saved espn_signature_shoes_all_pages.csv with", len(df), "rows")
