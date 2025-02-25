from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    OpenAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OpenAI_API_BASE = "https://api.perplexity.ai/"
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    GOOGLE_CALENDAR_CREDENTIALS = 'credentials.json'

    LLM_MODEL = "sonar"
    LLM_TEMPERATURE = 0