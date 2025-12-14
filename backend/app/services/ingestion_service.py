import feedparser
import asyncio
from sqlalchemy.orm import Session
from datetime import datetime
from time import mktime
import logging

from app.db.models import NewsItem, Source
from app.services.huggingface_service import hf_service
from app.db import crud

logger = logging.getLogger(__name__)

# Global headers for RSS feeds (CRITICAL)
RSS_HEADERS = {
    "User-Agent": "Mozilla/5.0 (AI News Dashboard; +https://localhost)"
}


class IngestionService:
    def __init__(self, db: Session):
        self.db = db

    async def fetch_and_process_feed(self, source: Source):
        """
        Fetch a single RSS feed, deduplicate, analyze, embed, and store.
        """
        logger.info(f" Fetching {source.name}...")

        try:
            # IMPORTANT: feedparser must receive headers
            feed = await asyncio.to_thread(
                feedparser.parse,
                source.url,
                request_headers=RSS_HEADERS
            )

            if not feed.entries:
                logger.warning(f" No entries found for {source.name}")
                return

            processed_count = 0

            for entry in feed.entries[:10]:  # Limit to latest 10
                try:
                    # Basic validation
                    if not hasattr(entry, "link") or not hasattr(entry, "title"):
                        continue

                    # 1. Deduplication
                    exists = (
                        self.db.query(NewsItem)
                        .filter(NewsItem.url == entry.link)
                        .first()
                    )
                    if exists:
                        continue

                    # 2. Prepare text
                    summary = entry.get("summary", "")
                    raw_text = f"{entry.title}. {summary}"

                    # 3. AI analysis
                    analysis = await hf_service.analyze_news_item(
                        entry.title,
                        raw_text
                    )

                    # 4. Embedding
                    embedding = await hf_service.generate_embedding(raw_text)
                    if not embedding:
                        logger.warning(f" No embedding generated: {entry.title}")
                        continue

                    # 5. Parse published date safely
                    published_at = datetime.utcnow()
                    if getattr(entry, "published_parsed", None):
                        try:
                            published_at = datetime.fromtimestamp(
                                mktime(entry.published_parsed)
                            )
                        except Exception:
                            pass

                    # 6. Save
                    news_item = NewsItem(
                        source_id=source.id,
                        title=entry.title,
                        url=entry.link,
                        published_at=published_at,
                        summary=analysis.get("summary"),
                        impact_score=analysis.get("impact_score", 50),
                        sentiment=analysis.get("sentiment", "Neutral"),
                        category_cluster=analysis.get("category_cluster", "General"),
                        embedding=embedding,
                    )

                    self.db.add(news_item)
                    processed_count += 1

                    logger.info(
                        f" Saved: {entry.title[:60]} "
                        f"(Impact: {analysis.get('impact_score', 50)})"
                    )

                except Exception as entry_error:
                    logger.error(
                        f" Error processing entry from {source.name}: {entry_error}"
                    )
                    continue

            self.db.commit()

            # Update source fetch stats
            crud.update_source_fetch_stats(self.db, source.id)

            logger.info(
                f" {source.name}: Processed {processed_count} new items"
            )

        except Exception as feed_error:
            logger.error(f" Failed to fetch {source.name}: {feed_error}")
            self.db.rollback()

    async def run_ingestion_cycle(self):
        """
        Run ingestion for all active sources.
        """
        logger.info(" Starting ingestion cycle...")

        sources = (
            self.db.query(Source)
            .filter(Source.is_active.is_(True))
            .all()
        )

        if not sources:
            logger.warning(" No active sources found")
            return

        # Run concurrently
        await asyncio.gather(
            *[self.fetch_and_process_feed(source) for source in sources],
            return_exceptions=True,
        )

        logger.info(" Ingestion cycle completed")
