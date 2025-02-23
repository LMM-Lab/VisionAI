# /visionai エンドポイントのテスト
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.main import app  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

client = TestClient(app)


def test_visionai_endpoint_predict():
    """/visionai の基本的なレスポンスを確認"""
    response = client.get("visionai/predict")
    assert response.status_code == 200


# def test_visionai_endpoint():
#     """ 物体検出を作成した時のサンプル """
#     response = client.post("/visionai/detect", json={"image_url": "https://example.com/image.jpg"})
#     assert response.status_code == 200
#     assert "detections" in response.json()
