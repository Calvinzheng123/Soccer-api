from pathlib import Path

from fastapi.testclient import TestClient

from LionAPI.app.main import app
from LionAPI.services import database
from LionAPI.services.database import insert_event, query_events


def test_insert_and_query_events_use_local_sqlite(tmp_path, monkeypatch):
    db_path = tmp_path / "lionapi-test.db"
    monkeypatch.setenv("LIONAPI_DB_PATH", str(db_path))

    insert_event(
        {
            "homeTeam": "Liverpool",
            "awayTeam": "Chelsea",
            "eventID": 12345,
            "homeScore": 2,
            "awayScore": 1,
            "tournamentName": "Premier League",
            "seasonID": 1,
            "tournamentID": 2,
            "eventDate": "2024-10-20",
        }
    )

    events = query_events("2024-10-19", "2024-10-21")

    assert db_path.exists()
    assert len(events) == 1
    assert events.iloc[0]["event_id"] == 12345
    assert events.iloc[0]["home_team"] == "Liverpool"


def test_events_route_returns_scraped_events_and_persists_them(tmp_path, monkeypatch):
    db_path = tmp_path / "lionapi-route.db"
    monkeypatch.setenv("LIONAPI_DB_PATH", str(db_path))

    sample_events = [
        {
            "homeTeam": "Arsenal",
            "awayTeam": "Tottenham",
            "eventID": 999,
            "homeScore": 3,
            "awayScore": 2,
            "tournamentName": "Premier League",
            "seasonID": 10,
            "tournamentID": 20,
            "eventDate": "2024-10-21",
        }
    ]

    monkeypatch.setattr("LionAPI.routers.events.date_query", lambda *_: sample_events)

    client = TestClient(app)
    response = client.get("/events/", params={"start_date": "2024-10-21", "end_date": "2024-10-21"})

    assert response.status_code == 200
    assert response.json() == sample_events

    stored_events = query_events("2024-10-21", "2024-10-21")
    assert len(stored_events) == 1
    assert stored_events.iloc[0]["away_team"] == "Tottenham"


def test_database_path_defaults_to_local_project_file(monkeypatch):
    monkeypatch.delenv("LIONAPI_DB_PATH", raising=False)

    db_path = database.get_database_path()

    assert db_path.name == "lionapi.db"
    assert isinstance(db_path, Path)


def test_events_route_surfaces_upstream_fetch_failures(monkeypatch):
    monkeypatch.setattr(
        "LionAPI.routers.events.date_query",
        lambda *_: (_ for _ in ()).throw(RuntimeError("SofaScore rejected the request with HTTP 403")),
    )

    client = TestClient(app)
    response = client.get("/events/", params={"start_date": "2026-03-10", "end_date": "2026-03-10"})

    assert response.status_code == 500
    assert "HTTP 403" in response.json()["detail"]
