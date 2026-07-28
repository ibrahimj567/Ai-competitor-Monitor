import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME = "AI Competitor Monitor"
    VERSION = "1.0.0"

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./competitor.db"
    )

settings = Settings()