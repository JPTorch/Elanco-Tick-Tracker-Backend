import requests
from datetime import datetime

def fetch_data(url: str) -> list[dict]:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()

def clean_raw_data(raw: list[dict]) -> list[dict]:
    seen_ids = set()
    clean_data = []
    required_fields = ["id", "date", "location", "species"]

    for element in raw:
        try:
            if not isinstance(element, dict):
                continue

            is_complete = all(element.get(field) for field in required_fields)

            if not is_complete:
                continue

            datetime.fromisoformat(element.get("date"))

            id = element.get("id")

            if id not in seen_ids:
                clean_data.append(element)
                seen_ids.add(id)

        except:
            continue

    return clean_data

url = "https://dev-task.elancoapps.com/data/tick-sightings"
raw = fetch_data(url)
data = clean_raw_data(raw)