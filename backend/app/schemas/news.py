from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NewsItemBase(BaseModel):
    title: str
    url: str
    source_id: Optional[int] = None
    published_at: Optional[datetime] = None
    summary: Optional[str] = None
    impact_score: int = 0
    sentiment: str = "Neutral"
    category_cluster: Optional[str] = None


class NewsItemCreate(NewsItemBase):
    embedding: list[float]


class NewsItem(NewsItemBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class NewsSearchRequest(BaseModel):
    query: str
    limit: int = 10
