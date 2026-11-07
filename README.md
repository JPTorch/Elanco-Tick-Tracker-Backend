# Elanco Tick Tracker Backend

## Overview

This API pulls tick sighting data from Elanco's service, lets you filter it by
species, location, and date, and gives you summary reports by location and month.
It is a small FastAPI project designed to make messy external data easier to
query and review.

## Tech stack

- Python
- FastAPI
- Uvicorn
- Requests

## Run it locally

From the project folder, install the dependencies and start the server:

```bash
pip install fastapi uvicorn requests
uvicorn main:app --reload
```

Once it's running, the API is available at `http://127.0.0.1:8000`.

- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI schema: `http://127.0.0.1:8000/openapi.json`

## Endpoints

- `GET /sightings` returns the sightings data. You can filter with `species`,
  `location`, `time_start`, and `time_end`.
- `GET /reports/sightings-per-location` shows how many sightings occurred at each location.
- `GET /reports/monthly-sightings` groups sightings by month.

### Query behavior

- Species and location searches are case-insensitive and match partial values.
- Date filters are inclusive and use ISO 8601 timestamps.
- If a timestamp has no timezone, the API treats it as UTC.
- Records with missing required fields, invalid dates, or duplicate IDs are excluded.

## Examples

These examples assume the API is running on your machine. The sightings
response uses a record from the current data source; report counts are excerpts
and may change when the source data changes.

### Get sightings

```http
GET http://127.0.0.1:8000/sightings
```

Filter by species, location, and date range:

```http
GET http://127.0.0.1:8000/sightings?species=marsh%20tick&location=Manchester&time_start=2022-08-01T00:00:00Z&time_end=2022-08-01T23:59:59Z
```

Example response:

```json
{
  "query": {
    "species": "marsh tick",
    "location": "Manchester",
    "time_start": "2022-08-01T00:00:00Z",
    "time_end": "2022-08-01T23:59:59Z"
  },
  "count": 1,
  "data": [
    {
      "date": "2022-08-01T06:40:31",
      "id": "02WNholuSg6ndCk4c1dA",
      "latinName": "Ixodes apronophorus",
      "location": "Manchester",
      "species": "Marsh tick"
    }
  ]
}
```

### Count sightings by location

```http
GET http://127.0.0.1:8000/reports/sightings-per-location
```

Example response excerpt:

```json
{
  "sighting counts": {
    "Nottingham": 95,
    "Birmingham": 82,
    "Glasgow": 78
  }
}
```

### Count sightings by month

```http
GET http://127.0.0.1:8000/reports/monthly-sightings
```

Example response excerpt:

```json
{
  "monthly sightings": {
    "2017-06": 16,
    "2013-09": 14,
    "2018-02": 13
  }
}
```

## Data source and limitations

The app reads sighting data from:
`https://dev-task.elancoapps.com/data/tick-sightings`

It fetches fresh data on every request and does not save or cache anything locally.
If the upstream service is unavailable, the request may fail, and each fetch has a
10-second timeout.

Records must include `id`, `date`, `location`, and `species`, and the date must be
valid ISO 8601. Incomplete or invalid records are skipped. If two valid records
share the same ID, only the first one is kept. There are no retry attempts or
fallback data sources.

If the source returns no sightings, `/sightings` returns `null`. The summary
report endpoints do not currently handle that case explicitly.