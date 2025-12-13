"""
Test HuggingFace service to ensure it's working
"""
import sys
sys.path.append('/app')

import asyncio
from app.services.huggingface_service import hf_service
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_service():
    logger.info("🧪 Testing HuggingFace Service...")
    
    # Test 1: Embedding Generation
    logger.info("\n1️⃣ Testing embedding generation...")
    test_text = "OpenAI releases GPT-5 with revolutionary capabilities"
    embedding = await hf_service.generate_embedding(test_text)
    
    if embedding:
        logger.info(f"✅ Embedding generated: {len(embedding)} dimensions")
        logger.info(f"   First 5 values: {embedding[:5]}")
    else:
        logger.error("❌ Embedding generation failed")
    
    # Test 2: News Analysis
    logger.info("\n2️⃣ Testing news analysis...")
    title = "OpenAI Announces GPT-5"
    content = """OpenAI has announced the release of GPT-5, their latest 
    language model with unprecedented capabilities in reasoning and understanding. 
    The model shows significant improvements over GPT-4."""
    
    analysis = await hf_service.analyze_news_item(title, content)
    
    if analysis:
        logger.info("✅ Analysis complete:")
        logger.info(f"   Summary: {analysis.get('summary', 'N/A')[:100]}...")
        logger.info(f"   Impact Score: {analysis.get('impact_score')}")
        logger.info(f"   Sentiment: {analysis.get('sentiment')}")
        logger.info(f"   Category: {analysis.get('category_cluster')}")
    else:
        logger.error("❌ Analysis failed")
    
    logger.info("\n✅ All tests completed!")

if __name__ == "__main__":
    asyncio.run(test_service())