
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config.settings import settings


def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0,
        google_api_key=settings.GEMINI_API_KEY,
        timeout=30,
        max_retries=1,
    )
