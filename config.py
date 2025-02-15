import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env if it exists

class Config:
    # Example environment variables
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    LINKEDIN_ACCESS_TOKEN: str = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
    LINKEDIN_USER_ID: str = os.getenv("LINKEDIN_USER_ID", "")
    NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "")
    
    # Additional constants
    LLM_MODEL_NAME: str = "Gemma2-9b-It"  # or any default
    LINKEDIN_CHAR_LIMIT: int = 3000
    LINKEDIN_SAFE_LIMIT: int = 2800
