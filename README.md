# LionAPI

LionAPI is a FastAPI application and Python package for pulling soccer match data from SofaScore and storing match metadata locally.

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn LionAPI.app.main:app --reload
```

The API now uses a local SQLite database file instead of AWS/RDS. By default it creates:

```bash
./lionapi.db
```

You can override that path with:

```bash
export LIONAPI_DB_PATH=/full/path/to/lionapi.db
```

## Example Usage

```python
from LionAPI import get_shots, query_events

events = query_events("2024-10-19", "2024-10-23")
shots = get_shots("Liverpool", "Chelsea", "2024-10-20")
```

To populate local event data, call the API route first:

```bash
curl "http://127.0.0.1:8000/events/?start_date=2024-10-19&end_date=2024-10-23"
```

## Current SofaScore Status

As of March 12, 2026, direct server-side requests to the two SofaScore endpoints used here return HTTP `403` from this environment:

- `/api/v1/sport/football/scheduled-events/{date}`
- `/api/v1/event/{event_id}/shotmap`

The package now reports that clearly, but live event ingestion may require a different data source or a browser-automation based fetcher if SofaScore keeps blocking non-browser clients.
