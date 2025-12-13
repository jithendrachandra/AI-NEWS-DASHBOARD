"""
Manually trigger news ingestion
Useful for testing
"""
import sys
sys.path.append('/app')

import asyncio
from app.core.database import SessionLocal
from app.services.ingestion_service import IngestionService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_ingestion():
    db = SessionLocal()
    try:
        logger.info("🚀 Starting manual ingestion...")
        service = IngestionService(db)
        await service.run_ingestion_cycle()
        logger.info("✅ Ingestion complete!")
    except Exception as e:
        logger.error(f"❌ Ingestion failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(run_ingestion())