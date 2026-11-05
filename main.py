from datetime import datetime, timezone

from ingest import fetch_data, clean_raw_data

url = "https://dev-task.elancoapps.com/data/tick-sightings"

def _parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed

def get_sightings(species: str | None = None, location: str | None = None, time_start: str | None = None, time_end: str | None = None) -> dict:
    raw = fetch_data(url)

    if not raw:
        return

    data = clean_raw_data(raw)

    filtered = data

    if species:
        filtered = [
            item for item in filtered
            if species.lower() in item.get("species", "").lower()
        ]

    if location:
        filtered = [
            item for item in filtered
            if location.lower() in item.get("location", "").lower()
        ]

    if time_start:
        start = datetime.fromisoformat(time_start.replace("Z", "+00:00"))
        if start.tzinfo is None:
            start = start.replace(tzinfo=timezone.utc)
        filtered = [
            item for item in filtered
            if item.get("date") is not None
            and _parse_time(item["date"]) >= start
        ]

    if time_end:
        end = datetime.fromisoformat(time_end.replace("Z", "+00:00"))
        if end.tzinfo is None:
            end = end.replace(tzinfo=timezone.utc)
        filtered = [
            item for item in filtered
            if item.get("date") is not None
            and _parse_time(item["date"]) <= end
        ]

    return {
        "query": {"species": species, "location": location, "time_start": time_start, "time_end": time_end},
        "count": len(filtered),
        "data": filtered
    }