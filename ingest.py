import requests

def fetch_data(url: str) -> list[dict]:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()

url = "https://dev-task.elancoapps.com/data/tick-sightings"
raw = fetch_data(url)