import uvicorn

from settings.config import settings
from logging import getLogger
from app.app import library_app

LOGGER = getLogger(__name__)

if __name__ == "__main__":
    LOGGER.info("Run main app.")
    uvicorn.run(
        app="main:library_app",
        port=settings.SERVICE_PORT,
        reload=True,
        host="0.0.0.0",
    )