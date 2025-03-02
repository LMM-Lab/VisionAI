from fastapi import APIRouter

from api.routes import object_detection

router = APIRouter()


# 物体検出エンドポイントを統合
router.include_router(object_detection.router, prefix="")


@router.get("/predict")
def predict():
    """
    VisionAI モデルで画像を処理する
    """
    return {"message": "VisionAI prediction endpoint"}
