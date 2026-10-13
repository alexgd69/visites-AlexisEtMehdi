import fakeredis
import pytest
from fastapi.testclient import TestClient

from app import main


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(main, "r", fakeredis.FakeRedis(decode_responses=True))
    return TestClient(main.app)


def test_root_incremente_le_compteur(client):
    assert client.get("/").json() == {"visites": 1}
    assert client.get("/").json() == {"visites": 2}


def test_health_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_metrics_expose_les_compteurs(client):
    client.get("/")
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text


def test_en_tete_version(client):
    response = client.get("/health")
    assert response.headers["X-Visites-Version"] == "0.1.0"
