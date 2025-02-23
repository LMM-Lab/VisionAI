# Fast APIのエンドポイントテスト
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.main import app  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

client = TestClient(app)


def test_root() -> None:
    """ルートエンドポイントの動作確認"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "VisionAI API is running"}
