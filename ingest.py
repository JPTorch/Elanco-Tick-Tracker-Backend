import requests
from datetime import datetime

def fetch_data(url: str) -> list[dict]:
    response = requests.get(url, timeout=10)
    status = response.raise_for_status()

    if status is not None:
        raise Exception(f"Failed to fetch data from {url}. Status code: {response.status_code}")

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