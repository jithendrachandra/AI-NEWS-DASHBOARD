import sys
sys.path.append('/app')

from app.core.database import SessionLocal
from app.db import crud
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INITIAL_SOURCES = [
    ("OpenAI Blog", "https://openai.com/blog/rss.xml"),
    ("Google AI Blog", "https://blog.google/technology/ai/rss/"),
    ("Anthropic News", "https://www.anthropic.com/news/rss.xml"),
    ("DeepMind Blog", "https://deepmind.google/blog/rss.xml"),
    ("Hugging Face Blog", "https://huggingface.co/blog/feed.xml"),
    ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("The Verge AI", "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml"),
    ("MIT Tech Review AI", "https://www.technologyreview.com/topic/artificial-intelligence/feed"),
    ("VentureBeat AI", "https://venturebeat.com/category/ai/feed/"),
    ("Wired AI", "https://www.wired.com/tag/artificial-intelligence/feed/"),
    ("AI News", "https://www.artificialintelligence-news.com/feed/"),
    ("Meta AI Research", "https://ai.facebook.com/blog/rss/"),
    ("Microsoft AI", "https://blogs.microsoft.com/ai/feed/"),
    ("NVIDIA AI", "https://blogs.nvidia.com/blog/category/deep-learning/feed/"),
    ("Stanford HAI", "https://hai.stanford.edu/news/rss.xml"),
    ("Berkeley AI Research", "https://bair.berkeley.edu/blog/feed.xml"),
    ("AI Alignment Forum", "https://www.alignmentforum.org/feed.xml"),
    ("Papers With Code", "https://paperswithcode.com/rss.xml"),
    ("Reddit r/MachineLearning", "https://www.reddit.com/r/MachineLearning/.rss"),
    ("Towards Data Science AI", "https://towardsdatascience.com/feed/tagged/artificial-intelligence"),
]

def seed_sources():
    db = SessionLocal()
    try:
        logger.info("🌱 Starting source seeding...")
        
        for name, url in INITIAL_SOURCES:
            try:
                source = crud.create_source(db, name, url)
                logger.info(f"✓ {name}")
            except Exception as e:
                logger.error(f"✗ {name}: {e}")
        
        logger.info(f"\n✅ Successfully seeded {len(INITIAL_SOURCES)} sources")
        
    except Exception as e:
        logger.error(f"❌ Seeding failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_sources()