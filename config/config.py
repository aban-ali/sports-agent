from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    OpenAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OpenAI_API_BASE = os.getenv("OPENAI_API_BASE")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    GOOGLE_CALENDAR_CREDENTIALS = os.getenv("GOOGLE_CALENDAR_CREDENTIALS")

    LLM_MODEL = "sonar"
    LLM_TEMPERATURE = 0