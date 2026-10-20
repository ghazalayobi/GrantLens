
from pathlib import Path
from bs4 import BeautifulSoup

# Locate the HTML file we downloaded earlier.
html_path = Path("data/raw/grants_page.html")

# Read the saved HTML.
html = html_path.read_text(encoding="utf-8")

# Parse the HTML into a structure Python can navigate.
soup = BeautifulSoup(html, "html.parser")

# Extract the page title.
print("PAGE TITLE:")
print(soup.title.get_text(strip=True) if soup.title else "No title found")

# Extract the main headings.
print("\nHEADINGS:")
for heading in soup.find_all(["h1", "h2", "h3"])[:15]:
    print(heading.name, "-", heading.get_text(" ", strip=True))

# Extract the first 20 links.
print("\nLINKS:")
for link in soup.find_all("a", href=True)[:20]:
    text = link.get_text(" ", strip=True)
    url = link["href"]
    if text:
        print(text, "->", url)
