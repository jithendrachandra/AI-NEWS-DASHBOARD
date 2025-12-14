from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
from typing import List, Optional

from app.core.database import get_db
from app.schemas.news import NewsItem, NewsSearchRequest
from app.db import crud
from app.db.models import NewsItem as NewsItemModel
from app.services.huggingface_service import hf_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


# -----------------------------
# List news (main feed)
# -----------------------------
@router.get("/", response_model=List[NewsItem])
def read_news(
    skip: int = 0,
    limit: int = 50,
    min_impact: int = 0,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Get latest news, sorted by impact score.
    Optional filtering by category.
    """
    query = db.query(NewsItemModel).filter(NewsItemModel.impact_score >= min_impact)

    if category and category != "all":
        query = query.filter(NewsItemModel.category_cluster == category)

    return (
        query.order_by(
            desc(NewsItemModel.impact_score),
            desc(NewsItemModel.published_at),
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


# -----------------------------
# Favorites (static path BEFORE /{news_id})
# -----------------------------
@router.get("/favorites", response_model=List[NewsItem])
def get_favorite_news(
    db: Session = Depends(get_db),
):
    """
    Return only favorited news items for the current user.
    """
    return crud.get_favorites(db, user_id=1)


# -----------------------------
# Categories & stats (static)
# -----------------------------
@router.get("/categories/list")
def get_categories(db: Session = Depends(get_db)):
    """Get all unique categories."""
    categories = (
        db.query(NewsItemModel.category_cluster)
        .distinct()
        .filter(NewsItemModel.category_cluster.isnot(None))
        .all()
    )
    return [cat[0] for cat in categories if cat[0]]


@router.get("/stats/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics."""
    return crud.get_news_stats(db)


# -----------------------------
# Search (static)
# -----------------------------
@router.post("/search", response_model=List[NewsItem])
async def search_news(
    request: NewsSearchRequest,
    db: Session = Depends(get_db),
):
    """
    Semantic search using HuggingFace embeddings + pgvector.
    Falls back to keyword search if embedding fails.
    """
    try:
        query_vector = await hf_service.generate_embedding(request.query)

        if query_vector and any(v != 0.0 for v in query_vector):
            results = (
                db.query(NewsItemModel)
                .order_by(NewsItemModel.embedding.cosine_distance(query_vector))
                .limit(request.limit)
                .all()
            )

            if results:
                logger.info(f"Semantic search returned {len(results)} results")
                return results

        logger.info("Falling back to keyword search")
        results = (
            db.query(NewsItemModel)
            .filter(
                or_(
                    NewsItemModel.title.ilike(f"%{request.query}%"),
                    NewsItemModel.summary.ilike(f"%{request.query}%"),
                )
            )
            .order_by(desc(NewsItemModel.impact_score))
            .limit(request.limit)
            .all()
        )

        return results

    except Exception as e:
        logger.error(f"Search error: {e}")
        return (
            db.query(NewsItemModel)
            .filter(NewsItemModel.impact_score >= 50)
            .order_by(desc(NewsItemModel.published_at))
            .limit(request.limit)
            .all()
        )


# -----------------------------
# Single news item & favorite
# -----------------------------
@router.get("/{news_id}", response_model=NewsItem)
def get_news_item(news_id: int, db: Session = Depends(get_db)):
    """Get a specific news item by ID."""
    news = crud.get_news_by_id(db, news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News item not found")

    # Increment view count
    news.view_count += 1
    db.commit()

    return news


@router.post("/{news_id}/favorite")
def toggle_favorite_news(
    news_id: int,
    db: Session = Depends(get_db),
):
    """
    Toggle favorite status for a news item.
    For now assumes a single user (user_id=1).
    """
    news = crud.get_news_by_id(db, news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News item not found")

    is_favorited = crud.toggle_favorite(db, news_id=news_id, user_id=1)
    return {"news_id": news_id, "is_favorited": is_favorited}
