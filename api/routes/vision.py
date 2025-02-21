from fastapi import APIRouter

router = APIRouter()

@router.get("/predict")
def predict():
    """
    VisionAI モデルで画像を処理する
    """
    return {"message": "VisionAI prediction endpoint"}
