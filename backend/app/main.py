import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import text

from app.core.config import settings
from app.core.database import engine, SessionLocal
from app.db.base import Base
from app.db import models
from app.api.v1.api import api_router
from app.services.ingestion_service import IngestionService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

async def fetch_news_job():
    db = SessionLocal()
    try:
        service = IngestionService(db)
        await service.run_ingestion_cycle()
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Application startup")

    # Ensure pgvector exists (idempotent, safe)
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))

    logger.info("✅ pgvector ready")

    # Create tables
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database schema ready")

    scheduler.add_job(fetch_news_job, "interval", minutes=15)
    scheduler.start()

    yield

    scheduler.shutdown()
    logger.info("🛑 Application shutdown")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(o) for o in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
def health():
    return {"status": "ok"}
