from fastapi import FastAPI

from app.config.settings import settings
from app.api.routes.health import router as health_router
from app.core.logging import logger
from app.api.routes.document import router as document_router
from app.db.database import engine
from app.db.base import Base

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)
app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["Health"],
)
app.include_router(document_router)

logger.info("Application Started")

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    logger.info("Root endpoint called")

    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }