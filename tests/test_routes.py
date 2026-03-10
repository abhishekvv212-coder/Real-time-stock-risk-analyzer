from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"

def test_get_real_stock():
    response = client.get("/stock/AAPL")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "AAPL"
    assert "price" in data
    assert "company" in data

def test_get_invalid_stock():
    response = client.get("/stock/INVALIDXYZ123")
    assert response.status_code == 404

def test_saved_stocks():
    response = client.get("/stocks/saved")
    assert response.status_code == 200
    assert isinstance(response.json(), list)