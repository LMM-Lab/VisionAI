# /health エンドポイントのテスト
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.main import app  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

client = TestClient(app)


def test_health_check() -> None:
    """/health エンドポイントが 200 を返すか"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
