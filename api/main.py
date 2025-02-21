import sys
import os
from fastapi import FastAPI

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.routes import vision, health

app = FastAPI()

# ルーターの追加
app.include_router(vision.router, prefix="/visionai")
app.include_router(health.router, prefix="")

@app.get("/")
def root():
    return {"message": "VisionAI API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)