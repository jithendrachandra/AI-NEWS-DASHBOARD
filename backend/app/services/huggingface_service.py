import logging
import asyncio
import time
from typing import List, Optional, Dict, Any
from functools import wraps

import requests
from sentence_transformers import SentenceTransformer

from app.core.config import settings

logger = logging.getLogger(__name__)


# --------------------------------------------------
# Rate limiting decorator
# --------------------------------------------------
def rate_limit(max_calls_per_minute: int):
    min_interval = 60.0 / max_calls_per_minute
    last_called = [0.0]

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            wait_for = min_interval - elapsed
            if wait_for > 0:
                await asyncio.sleep(wait_for)
            result = await func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator


# --------------------------------------------------
# Hugging Face Service
# --------------------------------------------------
class HuggingFaceService:
    def __init__(self):
        self.api_key = settings.HUGGINGFACE_API_KEY
        self.model_id = settings.HUGGINGFACE_MODEL_ID
        self.embedding_model_name = settings.HUGGINGFACE_EMBEDDING_MODEL

        # ✅ NEW official HF endpoint (old one is deprecated)
        self.api_url = (
            f"https://router.huggingface.co/hf-inference/models/{self.model_id}"
        )
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # --------------------------------------------------
        # Load local embedding model (preferred path)
        # --------------------------------------------------
        self.use_local_embeddings = False
        self.embedding_model: Optional[SentenceTransformer] = None

        try:
            logger.info(
                f"Loading local embedding model: {self.embedding_model_name}"
            )
            self.embedding_model = SentenceTransformer(
                self.embedding_model_name
            )
            self.use_local_embeddings = True
            logger.info("✅ Local embedding model loaded successfully")
        except Exception as e:
            logger.error(
                f"❌ Failed to load local embedding model: {e}"
            )
            logger.warning("Embeddings will be skipped if generation fails")

    # --------------------------------------------------
    # News analysis (HF Inference API)
    # --------------------------------------------------
    @rate_limit(settings.MAX_REQUESTS_PER_MINUTE)
    async def analyze_news_item(
        self, title: str, content: str
    ) -> Dict[str, Any]:
        """
        Uses Hugging Face text-generation model to analyze news.
        """

        prompt = f"""
Analyze the following AI news article.

Title:
{title}

Content:
{content[:1200]}

Return STRICTLY in this format:

SUMMARY: <2 sentence summary>
IMPACT: <0-100>
SENTIMENT: Positive | Neutral | Negative
CATEGORY: Research | Product | Business | Policy | Other
"""

        try:
            response = await asyncio.to_thread(
                requests.post,
                self.api_url,
                headers=self.headers,
                json={
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": 200,
                        "temperature": 0.3,
                    },
                },
                timeout=30,
            )

            if response.status_code != 200:
                logger.error(
                    f"HF API error {response.status_code}: {response.text}"
                )
                return self._fallback_analysis(title, content)

            data = response.json()

            if isinstance(data, list) and data:
                generated = data[0].get("generated_text", "")
            else:
                generated = data.get("generated_text", "")

            return self._parse_analysis_response(
                generated, title, content
            )

        except Exception as e:
            logger.error(f"HF analysis failed: {e}")
            return self._fallback_analysis(title, content)

    # --------------------------------------------------
    # Parse structured LLM output
    # --------------------------------------------------
    def _parse_analysis_response(
        self, text: str, title: str, content: str
    ) -> Dict[str, Any]:
        result = {
            "summary": "",
            "impact_score": 50,
            "sentiment": "Neutral",
            "category_cluster": "General",
        }

        try:
            for line in text.splitlines():
                line = line.strip()

                if line.startswith("SUMMARY:"):
                    result["summary"] = line.replace(
                        "SUMMARY:", ""
                    ).strip()

                elif line.startswith("IMPACT:"):
                    score = "".join(filter(str.isdigit, line))
                    if score:
                        result["impact_score"] = min(
                            int(score), 100
                        )

                elif line.startswith("SENTIMENT:"):
                    result["sentiment"] = line.replace(
                        "SENTIMENT:", ""
                    ).strip()

                elif line.startswith("CATEGORY:"):
                    result["category_cluster"] = line.replace(
                        "CATEGORY:", ""
                    ).strip()

            if not result["summary"]:
                result["summary"] = (
                    content[:250] + "..."
                    if len(content) > 250
                    else content
                )

            return result

        except Exception as e:
            logger.error(f"Response parse failed: {e}")
            return self._fallback_analysis(title, content)

    # --------------------------------------------------
    # Fallback analysis (NO hallucinations)
    # --------------------------------------------------
    def _fallback_analysis(
        self, title: str, content: str
    ) -> Dict[str, Any]:
        text = f"{title} {content}".lower()

        impact = 40
        if any(k in text for k in ["breakthrough", "major", "significant"]):
            impact += 25
        if any(k in text for k in ["policy", "law", "regulation"]):
            impact += 15

        impact = min(impact, 100)

        sentiment = "Neutral"
        if any(k in text for k in ["success", "advance", "improve"]):
            sentiment = "Positive"
        elif any(k in text for k in ["risk", "problem", "concern"]):
            sentiment = "Negative"

        category = "General"
        if any(k in text for k in ["paper", "research", "arxiv"]):
            category = "Research"
        elif any(k in text for k in ["launch", "product", "release"]):
            category = "Product"
        elif any(k in text for k in ["funding", "startup", "market"]):
            category = "Business"
        elif any(k in text for k in ["policy", "law", "government"]):
            category = "Policy"

        return {
            "summary": content[:300] + "..."
            if len(content) > 300
            else content,
            "impact_score": impact,
            "sentiment": sentiment,
            "category_cluster": category,
        }

    # --------------------------------------------------
    # Embedding generation (LOCAL ONLY)
    # --------------------------------------------------
    async def generate_embedding(
        self, text: str
    ) -> Optional[List[float]]:
        """
        Generates embeddings locally.
        Returns None on failure (DO NOT store junk vectors).
        """

        if not self.use_local_embeddings or not self.embedding_model:
            logger.warning("Local embedding model not available")
            return None

        try:
            vector = await asyncio.to_thread(
                self.embedding_model.encode,
                text,
                convert_to_tensor=False,
                normalize_embeddings=True,
            )
            return vector.tolist()

        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            return None


# --------------------------------------------------
# Singleton instance
# --------------------------------------------------
hf_service = HuggingFaceService()
