
import csv
import time
from datetime import date
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.mott.org"
GRANTS_URL = f"{BASE_URL}/grants/"

MAX_PAGES = 3
REQUEST_DELAY = 2

RAW_DIR = Path("data/raw")
OUTPUT_FILE = Path("data/processed/grants_sample.csv")

FIELDNAMES = [
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


def fetch_page(page_number):
    """Download one page and preserve its original HTML."""

    if page_number == 1:
        url = GRANTS_URL
    else:
        url = f"{GRANTS_URL}?pg={page_number}"

    print(f"Fetching page {page_number}: {url}")

    response = requests.get(
        url,
        timeout=20,
        headers={
            "User-Agent": "GrantLensResearchDemo/0.1"
        },
    )

    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")

    if "text/html" not in content_type.lower():
        raise ValueError(
            f"Unexpected content type: {content_type}"
        )

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    raw_path = RAW_DIR / f"grants_page_{page_number}.html"
    raw_path.write_bytes(response.content)

    return response.content


def get_text(parent, selector):
    """Extract text safely from an HTML element."""

    element = parent.select_one(selector)

    if element is None:
        return ""

    return element.get_text(" ", strip=True)


def extract_grants(html):
    """Extract structured grant records from one HTML page."""

    soup = BeautifulSoup(html, "html.parser")

    cards = soup.select("article.card6")

    records = []

    for card in cards:

        link = card.select_one("a.card6-link[href]")

        if link is None:
            continue

        source_url = urljoin(BASE_URL, link["href"])
        parsed_url = urlparse(source_url)

        if (
            parsed_url.netloc != "www.mott.org"
            or not parsed_url.path.startswith("/grants/")
        ):
            continue

        grant_id = parsed_url.path.rstrip("/").split("/")[-1]

        amount_text = get_text(card, ".card6-amount")

        amount_clean = (
            amount_text.replace("$", "")
            .replace(",", "")
            .strip()
        )

        amount_usd = (
            int(amount_clean)
            if amount_clean.isdigit()
            else ""
        )

        metadata = {}

        for item in card.select(".card6-details li"):

            label = get_text(item, "strong").rstrip(":").strip()
            value = get_text(item, "span")

            if label:
                metadata[label.casefold()] = value

        records.append({
            "grant_id": grant_id,
            "title": get_text(card, ".card6-title"),
            "recipient": get_text(card, ".card6-subtitle"),
            "amount_usd": amount_usd,
            "location": metadata.get("location", ""),
            "program_area": metadata.get("program", ""),
            "grant_period": metadata.get("grant period", ""),
            "program_initiative": metadata.get(
                "program initiative", ""
            ),
            "source_url": source_url,
            "retrieved_at": date.today().isoformat(),
        })

    return records


def save_csv(records):
    """Save the combined records to CSV."""

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDNAMES,
        )

        writer.writeheader()
        writer.writerows(records)


def main():

    all_records = []

    for page_number in range(1, MAX_PAGES + 1):

        try:
            html = fetch_page(page_number)

            records = extract_grants(html)

            print(
                f"Page {page_number}: "
                f"{len(records)} records extracted."
            )

            all_records.extend(records)

        except requests.RequestException as error:
            print(f"Request failed: {error}")
            break

        except ValueError as error:
            print(f"Validation failed: {error}")
            break

        if page_number < MAX_PAGES:
            time.sleep(REQUEST_DELAY)

    # Remove duplicate grant IDs.
    unique_records = {}

    for record in all_records:
        grant_id = record["grant_id"]

        if grant_id:
            unique_records[grant_id] = record

    final_records = list(unique_records.values())

    print("\nCOLLECTION SUMMARY")
    print("----------------------")
    print(f"Total extracted: {len(all_records)}")
    print(f"Unique records: {len(final_records)}")
    print(
        f"Duplicates removed: "
        f"{len(all_records) - len(final_records)}"
    )

    save_csv(final_records)

    print(f"Dataset saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
