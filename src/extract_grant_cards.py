
import csv
from datetime import date
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

# 1. Define file paths.
input_path = Path("data/raw/grants_page.html")
output_path = Path("data/processed/grants_preview.csv")

BASE_URL = "https://www.mott.org"

# 2. Read the HTML we already downloaded.
html = input_path.read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")

# 3. Find the individual grant cards.
cards = soup.select("article.card6")

print(f"Grant cards found: {len(cards)}")

# 4. Define the fields we want to extract.
fieldnames = [
    "grant_id",
    "title",
    "recipient",
    "amount_usd",
    "location",
    "program_area",
    "grant_period",
    "program_initiative",
    "source_url",
    "retrieved_at",
]


def get_text(parent, selector):
    """Return cleaned text from an element, or an empty string."""
    element = parent.select_one(selector)
    return element.get_text(" ", strip=True) if element else ""


records = []

# 5. Extract information from each card.
for card in cards:
    link = card.select_one("a.card6-link[href]")

    if link is None:
        print("Skipping card without a grant URL.")
        continue

    source_url = urljoin(BASE_URL, link["href"])

    # Keep only links that point to Mott grant pages.
    parsed_url = urlparse(source_url)

    if (
        parsed_url.netloc != "www.mott.org"
        or not parsed_url.path.startswith("/grants/")
    ):
        print(f"Skipping unexpected URL: {source_url}")
        continue

    grant_id = parsed_url.path.rstrip("/").split("/")[-1]

    title = get_text(card, ".card6-title")
    recipient = get_text(card, ".card6-subtitle")
    amount_text = get_text(card, ".card6-amount")

    # Convert "$250,000" into 250000.
    amount_digits = (
        amount_text.replace("$", "")
        .replace(",", "")
        .strip()
    )

    amount_usd = (
        int(amount_digits)
        if amount_digits.isdigit()
        else ""
    )

    # Extract metadata from the labeled list items.
    metadata = {}

    for item in card.select(".card6-details li"):
        label = get_text(item, "strong").rstrip(":").strip()
        value = get_text(item, "span")

        if label:
            metadata[label.casefold()] = value

    record = {
        "grant_id": grant_id,
        "title": title,
        "recipient": recipient,
        "amount_usd": amount_usd,
        "location": metadata.get("location", ""),
        "program_area": metadata.get("program", ""),
        "grant_period": metadata.get("grant period", ""),
        "program_initiative": metadata.get(
            "program initiative", ""
        ),
        "source_url": source_url,
        "retrieved_at": date.today().isoformat(),
    }

    records.append(record)

# 6. Save the extracted records.
output_path.parent.mkdir(parents=True, exist_ok=True)

with output_path.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(records)

print(f"Records extracted: {len(records)}")
print(f"Output saved to: {output_path}")

# 7. Preview a few records in the terminal.
for record in records[:3]:
    print(
        record["grant_id"],
        "|",
        record["title"],
        "|",
        record["recipient"],
        "|",
        record["amount_usd"],
    )
