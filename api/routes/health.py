from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    """
    API のヘルスチェック
    """
    return {"status": "ok"}
