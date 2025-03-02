import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.routes import health, vision  # noqa: E402

app = FastAPI()

# CORS設定（WebSocketを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要なら特定のオリジンに制限
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの追加
app.include_router(vision.router, prefix="/visionai")
app.include_router(health.router, prefix="")


@app.get("/")
def root():
    return {"message": "VisionAI API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8006)
