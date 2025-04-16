import os
from dotenv import load_dotenv

# Load environment variables from .env in local development
if os.getenv("ENVIRONMENT") != "production":
    load_dotenv()

# Neo4j DB 1
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Neo4j DB 2 (optional)
NEO4J_URI_2 = os.getenv("NEO4J_URI_2")
NEO4J_USERNAME_2 = os.getenv("NEO4J_USERNAME_2")
NEO4J_PASSWORD_2 = os.getenv("NEO4J_PASSWORD_2")

# Redis
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_URI = os.getenv("REDIS_URI")

# Langfuse
LANGFUSE_HOST_URL = os.getenv("LANGFUSE_HOST_URL")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")

# OpenRouter
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Chainlit Auth Secret (used for session encryption)
CHAINLIT_AUTH_SECRET = os.getenv("CHAINLIT_AUTH_SECRET")

# GitHub OAuth
OAUTH_GITHUB_CLIENT_ID = os.getenv("OAUTH_GITHUB_CLIENT_ID")
OAUTH_GITHUB_CLIENT_SECRET = os.getenv("OAUTH_GITHUB_CLIENT_SECRET")

# Google OAuth
OAUTH_GOOGLE_CLIENT_ID = os.getenv("OAUTH_GOOGLE_CLIENT_ID")
OAUTH_GOOGLE_CLIENT_SECRET = os.getenv("OAUTH_GOOGLE_CLIENT_SECRET")  should not be pushed into production right ? 
