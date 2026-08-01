import uvicorn
from fastapi import FastAPI
from .config.project_config import settings
from .routes import router as main_router

app = FastAPI(title="Translation Service")
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run("src.main:app", host=settings.app.host, port=settings.app.port, reload=True)
