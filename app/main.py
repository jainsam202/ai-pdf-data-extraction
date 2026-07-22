from fastapi import FastAPI

from app.config.settings import settings
from app.api.routes.health import router as health_router
from app.core.logging import logger

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)
app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["Health"],
)

logger.info("Application Started")


@app.get("/")
def root():
    logger.info("Root endpoint called")

    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }