from fastapi.testclient import TestClient
import sys

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": True, "python": sys.version, "env": 'test'}
