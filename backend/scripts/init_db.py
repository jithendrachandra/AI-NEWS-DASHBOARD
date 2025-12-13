"""
Initialize database with pgvector extension
Run this once before first migration
"""

from sqlalchemy import text
from app.core.database import engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """Initialize database with required extensions"""
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        logger.info("✅ pgvector extension created")

    logger.info("✅ Database initialization complete")

if __name__ == "__main__":
    init_database()
