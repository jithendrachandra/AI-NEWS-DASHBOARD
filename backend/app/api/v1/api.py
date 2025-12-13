from fastapi import APIRouter
from app.api.v1.endpoints import news, broadcast, sources

api_router = APIRouter()

api_router.include_router(news.router, prefix="/news", tags=["News"])
api_router.include_router(broadcast.router, prefix="/broadcast", tags=["Broadcast"])
api_router.include_router(sources.router, prefix="/sources", tags=["Sources"])