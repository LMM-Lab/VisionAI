# /health エンドポイントのテスト
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health_check() -> None:
    """ /health エンドポイントが 200 を返すか """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
