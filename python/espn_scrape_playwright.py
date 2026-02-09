from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

URL = "https://www.espn.com/espn/feature/story/_/id/39771146/sneakerhead-guide-every-nba-wnba-signature-sneaker-history"

print("Starting Playwright...")

with sync_playwright() as p:
    print("Launching browser...")
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    print("Going to URL...")
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)

    print("Waiting a few seconds for content to load...")
    page.wait_for_timeout(8000)

    html = page.content()
    print("HTML length:", len(html))
    with open("espn_page.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Saved espn_page.html")

    browser.close()

print("Parsing HTML...")
soup = BeautifulSoup(html, "html.parser")

title = soup.title.get_text(strip=True) if soup.title else "No title found"
print("Title:", title)

article = soup.find("article") or soup.select_one("main") or soup.body
text = article.get_text("\n", strip=True) if article else ""

print("\n--- ARTICLE TEXT PREVIEW ---\n")
print(text[:2000])

with open("espn_article_text.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("\nSaved to espn_article_text.txt")
