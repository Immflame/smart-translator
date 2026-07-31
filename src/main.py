import uvicorn
from fastapi import FastAPI
from src.routes import router as main_router
from src.config.project_config import settings

app = FastAPI(title="Translation Service")
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=settings.app.port)
