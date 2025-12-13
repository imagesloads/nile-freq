import requests
from bs4 import BeautifulSoup
import json
import time

URL = "https://nilesat.org/channel/"

session = requests.Session()

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://nilesat.org/",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

response = session.get(URL, headers=headers, timeout=30)

if response.status_code != 200:
    raise Exception(f"Request blocked, status code: {response.status_code}")

soup = BeautifulSoup(response.text, "html.parser")

channels = []

for row in soup.select("tr"):
    cols = row.find_all("td")
    if len(cols) == 4:
        channels.append({
            "name": cols[0].get_text(strip=True),
            "frequency": cols[1].get_text(strip=True),
            "polarization": cols[2].get_text(strip=True),
            "sr_fec": cols[3].get_text(strip=True)
        })

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(channels, f, ensure_ascii=False, indent=2)

print(f"✔ Saved {len(channels)} channels")
