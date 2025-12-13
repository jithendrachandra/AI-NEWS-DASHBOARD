from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.broadcast import BroadcastRequest, BroadcastResponse
from app.services import broadcast_service
from app.db import crud

router = APIRouter()

@router.post("/", response_model=BroadcastResponse)
async def broadcast_item(
    request: BroadcastRequest, 
    db: Session = Depends(get_db)
):
    news_item = crud.get_news_by_id(db, request.news_item_id)
    if not news_item:
        raise HTTPException(status_code=404, detail="News item not found")
        
    result = await broadcast_service.broadcast_news(
        news_item, 
        request.platform, 
        request.custom_message
    )
    
    return {
        "status": result["status"], 
        "platform": request.platform, 
        "message": "Broadcast executed successfully"
    }