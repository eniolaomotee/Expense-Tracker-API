import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.database.main import init_db, close_db
from src.utils.logging_conf import configure_logging
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Application starting")
    configure_logging()
    await init_db()
    logger.info("Logging works")
    yield
    await close_db()
    print("Application shutdown complete. ")
    
version = "v1"
version_prefix = f"/api/{version}"


app = FastAPI(
    title="Expense Tracker API",
    description="This API allows users to create, read, update, and delete expenses. Users can sign up and log in to the application. Each user  have their own set of expenses",
    version=version,
    lifespan=lifespan
)

# Include Routers here below