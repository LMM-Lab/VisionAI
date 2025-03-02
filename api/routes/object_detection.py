import base64
import json
from typing import Any, Optional

import cv2
import numpy as np
from api.services.object_detection import run_object_detection
from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    UploadFile,
    WebSocket,
    WebSocketDisconnect,
)

router = APIRouter()


@router.post("/object-detection")
async def detect_objects(
    file: UploadFile = File(...),  # 画像ファイル
    model: str = Form(...),  # モデル名
    version: Optional[str] = Form(...),  # モデルのバージョン
    subtask: str = Form(...),  # タスクの種類
    annotate: bool = Form(True),  # アノテーションされた画像を返すか
    parameters: Optional[str] = Form("{}"),
) -> dict[str, Any]:
    """
    物体検出のエンドポイント
    """
    try:
        parameters_dict: dict[str, Any] = json.loads(parameters) if parameters else {}
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400, detail="Invalid JSON format for parameters"
        )

    image_bytes = file.file.read()
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = np.asarray(cv2.imdecode(image_array, cv2.IMREAD_COLOR), dtype=np.uint8)

    response = run_object_detection(
        image, model, version, subtask, annotate, parameters_dict
    )

    return response


@router.websocket("/object-detection/stream")
async def websocket_object_detection(websocket: WebSocket):
    """
    🔥 WebSocket を使ったリアルタイム物体検出エンドポイント
    - クライアントから Base64 エンコードされた画像を受信
    - YOLO で物体検出を行い、アノテーション画像を返却
    """
    await websocket.accept()
    print("✅ WebSocket 接続が確立されました")

    try:
        while True:
            # クライアントからデータを受信
            data = await websocket.receive_text()
            request = json.loads(data)

            # 必要なパラメータの取得
            image_data = request.get("image_base64")
            model = request.get("model", "yolov8n")
            version = request.get("version", "latest")
            subtask = request.get("subtask", "normal")
            annotate = request.get("annotate", True)
            parameters = (
                json.loads(request.get("parameters", "{}"))
                if isinstance(request.get("parameters"), str)
                else request.get("parameters")
            )

            if not image_data:
                await websocket.send_text(
                    json.dumps({"error": "No image data provided"})
                )
                continue

            # Base64 から OpenCV 画像へ変換
            image_bytes = base64.b64decode(image_data)
            image_array = np.frombuffer(image_bytes, dtype=np.uint8)
            image = np.asarray(
                cv2.imdecode(image_array, cv2.IMREAD_COLOR), dtype=np.uint8
            )

            # 物体検出を実行
            response = run_object_detection(
                image=image,
                model_name=model,
                version=version,
                subtask=subtask,
                annotate=annotate,
                parameters=parameters,
            )

            # 結果を WebSocket で送信
            await websocket.send_text(json.dumps(response))

    except WebSocketDisconnect:
        print("❌ WebSocket 接続が切断されました")
    except Exception as e:
        await websocket.send_text(json.dumps({"error": str(e)}))
        print(f"⚠️ WebSocket エラー: {e}")
