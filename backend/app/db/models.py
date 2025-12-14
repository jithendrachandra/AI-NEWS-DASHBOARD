from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector

from app.db.base import Base


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    url = Column(String)
    source_type = Column(String, default="rss")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_fetched = Column(DateTime(timezone=True), nullable=True)
    fetch_count = Column(Integer, default=0)


class NewsItem(Base):
    __tablename__ = "news_items"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=True)

    title = Column(Text, nullable=False)
    url = Column(Text, unique=True, nullable=False)
    published_at = Column(DateTime(timezone=True))

    summary = Column(Text)
    impact_score = Column(Integer, default=0)
    sentiment = Column(String, default="Neutral")
    category_cluster = Column(String, default="General")

    embedding = Column(Vector(384))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    view_count = Column(Integer, default=0)
    broadcast_count = Column(Integer, default=0)

    source = relationship("Source")


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    news_item_id = Column(Integer, ForeignKey("news_items.id"))
    user_id = Column(Integer, default=1)  # For future multi-user support
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class BroadcastLog(Base):
    __tablename__ = "broadcast_logs"

    id = Column(Integer, primary_key=True)
    news_item_id = Column(Integer, ForeignKey("news_items.id"))
    platform = Column(String, nullable=False)
    status = Column(String, default="success")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
