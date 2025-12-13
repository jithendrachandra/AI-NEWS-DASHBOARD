from pydantic import BaseModel
from typing import Optional

class BroadcastRequest(BaseModel):
    news_item_id: int
    platform: str # "linkedin", "email", "whatsapp"
    custom_message: Optional[str] = None

class BroadcastResponse(BaseModel):
    status: str
    platform: str
    message: str