# src/services/classification_service.py

import json
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import settings


CLASSIFICATION_PROMPT = """
You are an expert document classifier for a Host Country Services relocation platform.

Classify into:
Service: Host Country
Sub-services:
- Property Visit
- City Orientation
- Local Area Exploration
- Hotel Stay
- Service Apartment
- Short-Term Rental
- Guest House

Return ONLY JSON:
{
  "service": "Host Country",
  "sub_service": "...",
  "confidence": "High|Medium|Low",
  "reason": "...",
  "email": "..." or null
}
"""


class ClassificationService:
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.1,
        )

    def _safe_json(self, text):
        try:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                return json.loads(match.group())
        except:
            pass
        return {}

    def classify(self, filename: str, text: str):
        prompt = f"""
{CLASSIFICATION_PROMPT}

Document filename:
{filename}

Text:
{text}
"""

        resp = self.model.invoke(prompt)
        return self._safe_json(resp.content)


classification_service = ClassificationService()