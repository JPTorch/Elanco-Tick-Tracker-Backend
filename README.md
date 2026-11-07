# Elanco Tick Tracker Backend

## What this API does

This API gets tick sightings from Elanco's data service. You can filter the
sightings by species, location, or date, or get summaries by location and month.

## Run it locally

Install FastAPI, Uvicorn, and Requests, then start the server from the project
folder:

```bash
uvicorn main:app --reload
```

The API runs at `http://127.0.0.1:8000`. Try the endpoints in
`http://127.0.0.1:8000/docs`, or view the schema at
`http://127.0.0.1:8000/openapi.json`.

## Endpoints

- `GET /sightings` returns sightings. You can optionally pass `species`,
  `location`, `time_start`, and `time_end` query parameters.
- `GET /reports/sightings-per-location` counts sightings at each location.
- `GET /reports/monthly-sightings` counts sightings by month.

Species and location filters ignore capitalization and match part of a value.
The date limits are inclusive and use ISO 8601 timestamps. If a timestamp has
no timezone, the API treats it as UTC. Records without required fields, with an
invalid date, or with an ID already seen are left out.

## Examples

These requests assume the server is running on your computer. The response
values below are examples; actual results depend on the data source.

### Get sightings

To get all sightings:

```http
GET http://127.0.0.1:8000/sightings
```

To filter by species, location, and date range:

```http
GET http://127.0.0.1:8000/sightings?species=deer&location=Texas&time_start=2026-01-01T00:00:00Z&time_end=2026-01-31T23:59:59Z
```

For example:

```json
{
  "query": {
    "species": "deer",
    "location": "Texas",
    "time_start": "2026-01-01T00:00:00Z",
    "time_end": "2026-01-31T23:59:59Z"
  },
  "count": 1,
  "data": [
    {
      "id": "sighting-123",
      "date": "2026-01-15T12:30:00Z",
      "location": "Austin, Texas",
      "species": "Deer tick"
    }
  ]
}
```

### Count sightings by location

```http
GET http://127.0.0.1:8000/reports/sightings-per-location
```

For example:

```json
{
  "sighting counts": {
    "Austin, Texas": 12,
    "Dallas, Texas": 7
  }
}
```

### Count sightings by month

```http
GET http://127.0.0.1:8000/reports/monthly-sightings
```

For example:

```json
{
  "monthly sightings": {
    "2026-01": 19,
    "2025-12": 14
  }
}
```

## Data source and limitations

Sightings come from `https://dev-task.elancoapps.com/data/tick-sightings`.
The API fetches fresh data for each request and doesn't save or cache it. If the
upstream service is unavailable, the request can fail; each fetch has a
10-second timeout.

Records need an `id`, `date`, `location`, and `species`, and the date must be
valid ISO 8601. Incomplete or invalid records are skipped. If two valid records
have the same ID, only the first is used. There are no retries or fallback data.
If the source returns no sightings, `/sightings` returns `null`; the report
endpoints currently don't handle that case.