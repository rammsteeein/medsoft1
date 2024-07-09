import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    name = "Андрей"
    response = client.get("/", params={"name": name})
    assert response.status_code == 200
    assert response.json() == {"message": f"Hello {name}"}