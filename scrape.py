import requests
from bs4 import BeautifulSoup
import json

URL = "https://nilesat.org/channel/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=HEADERS, timeout=20)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

channels = []

for row in soup.select("tr"):
    cols = row.find_all("td")
    if len(cols) == 4:
        name = cols[0].get_text(strip=True)
        frequency = cols[1].get_text(strip=True)
        polarization = cols[2].get_text(strip=True)
        sr_fec = cols[3].get_text(strip=True)

        channels.append({
            "name": name,
            "frequency": frequency,
            "polarization": polarization,
            "sr_fec": sr_fec
        })

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(channels, f, ensure_ascii=False, indent=2)

print(f"Saved {len(channels)} channels to data.json")
