from fastapi import FastAPI

from app.config.settings import settings
from app.api.routes.health import router as health_router
from app.core.logging import logger
from app.api.routes.document import router as document_router
from app.api.routes.redis import router as redis_router
from app.api.routes.search import router as search_router
from app.db.database import engine
from app.db.base import Base

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

Prefix = "/api/v1"

app.include_router(health_router,prefix=Prefix,tags=["Health"])
app.include_router(document_router,prefix=Prefix,tags=["Document"])
app.include_router(redis_router, prefix=Prefix)
app.include_router(search_router, prefix=Prefix)

logger.info("Application Started")

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    logger.info("Root endpoint called")

    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }