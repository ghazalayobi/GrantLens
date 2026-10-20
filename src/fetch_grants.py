import requests

url = "https://www.mott.org/grants/"

response = requests.get(url, timeout=20)

print("Status code:", response.status_code)

print("Content type:", response.headers.get("Content-Type"))

print("Response length:", len(response.content))

from pathlib import Path

if response.status_code == 200 and "text/html" in response.headers.get("Content-Type", ""):

    output_path = Path("data/raw/grants_page.html")

    output_path.write_bytes(response.content)

    print("Raw HTML saved successfully.")

else:
    print("HTML was not saved. Check the server response.")