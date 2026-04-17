
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    EXTRACTION_CONFIDENCE_THRESHOLD: float = float(
        os.getenv("EXTRACTION_CONFIDENCE_THRESHOLD", 95.0)
    )

settings = Settings()