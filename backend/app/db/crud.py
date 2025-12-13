from app.schemas.news import NewsItemCreate
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from datetime import datetime

from app.db.models import NewsItem, Source, Favorite, BroadcastLog



def get_news(db: Session, skip: int = 0, limit: int = 50, min_impact: int = 0):
    return (
        db.query(NewsItem)
        .filter(NewsItem.impact_score >= min_impact)
        .order_by(desc(NewsItem.impact_score), desc(NewsItem.published_at))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_news_by_id(db: Session, news_id: int):
    return db.query(NewsItem).filter(NewsItem.id == news_id).first()


def create_source(db: Session, name: str, url: str, source_type: str = "rss"):
    """Create or update source - prevents duplicates"""
    # Check if source already exists
    existing = db.query(Source).filter(Source.name == name).first()
    if existing:
        # Update URL if different
        if existing.url != url:
            existing.url = url
            existing.source_type = source_type
            db.commit()
            db.refresh(existing)
        return existing
    
    # Create new source
    db_source = Source(name=name, url=url, source_type=source_type)
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source


def get_active_sources(db: Session):
    return db.query(Source).filter(Source.is_active == True).all()


def update_source_fetch_stats(db: Session, source_id: int):
    """Update source fetch statistics"""
    source = db.query(Source).filter(Source.id == source_id).first()
    if source:
        source.last_fetched = datetime.utcnow()
        source.fetch_count += 1
        db.commit()


def toggle_favorite(db: Session, news_id: int, user_id: int = 1):
    existing = (
        db.query(Favorite)
        .filter(
            Favorite.news_item_id == news_id,
            Favorite.user_id == user_id,
        )
        .first()
    )

    if existing:
        db.delete(existing)
        db.commit()
        return False

    new_fav = Favorite(news_item_id=news_id, user_id=user_id)
    db.add(new_fav)
    db.commit()
    return True


def get_favorites(db: Session, user_id: int = 1):
    """Get all favorited news items for a user"""
    favorites = (
        db.query(NewsItem)
        .join(Favorite)
        .filter(Favorite.user_id == user_id)
        .order_by(desc(Favorite.created_at))
        .all()
    )
    return favorites


def log_broadcast(db: Session, news_id: int, platform: str, status: str = "success"):
    """Log a broadcast action"""
    log = BroadcastLog(news_item_id=news_id, platform=platform, status=status)
    db.add(log)
    
    # Increment broadcast count
    news = db.query(NewsItem).filter(NewsItem.id == news_id).first()
    if news:
        news.broadcast_count += 1
    
    db.commit()


def get_news_stats(db: Session):
    """Get dashboard statistics"""
    total_news = db.query(func.count(NewsItem.id)).scalar()
    total_sources = db.query(func.count(Source.id)).filter(Source.is_active == True).scalar()
    avg_impact = db.query(func.avg(NewsItem.impact_score)).scalar()
    
    return {
        "total_news": total_news,
        "total_sources": total_sources,
        "avg_impact_score": round(avg_impact, 2) if avg_impact else 0
    }
