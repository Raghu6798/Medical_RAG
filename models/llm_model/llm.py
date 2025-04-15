import os 

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

LLM= ChatOpenAI(
    base_url=os.getenv("OPENROUTER_BASE_URL"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="meta-llama/llama-4-maverick:free"
)