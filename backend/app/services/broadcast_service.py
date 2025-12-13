import logging
from app.db.models import NewsItem

logger = logging.getLogger(__name__)

async def broadcast_news(news_item: NewsItem, platform: str, custom_message: str = None):
    """
    Simulates sending data to external APIs.
    In a real app, this would use sendgrid, linkedin-api, or twilio.
    """
    # Simulate API Latency
    logger.info(f"Broadcasting to {platform}...")
    
    content = custom_message if custom_message else news_item.summary
    
    # Mock Success Logic
    response = {
        "status": "success",
        "platform": platform,
        "payload_sent": content,
        "timestamp": "now"
    }
    
    if platform == "linkedin":
        logger.info(f"✅ [LINKEDIN] Posted: {news_item.title}")
    elif platform == "email":
        logger.info(f"✅ [EMAIL] Sent to subscribers: {news_item.title}")
    elif platform == "whatsapp":
        logger.info(f"✅ [WHATSAPP] Shared: {news_item.title}")
    else:
        return {"status": "failed", "message": "Unknown platform"}
        
    return response