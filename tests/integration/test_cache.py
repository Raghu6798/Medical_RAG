import os
import sys 

import pytest
from langchain_redis.cache import RedisSemanticCache
from langchain_core.documents import Document
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))
from models.embedding_model.embed_model import Embed_model
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="module")
def redis_cache():
    """Fixture to initialize the RedisSemanticCache."""
    redis_uri = os.getenv("REDIS_URI")
    assert redis_uri is not None, "REDIS_URI not found in environment variables"

    cache = RedisSemanticCache(
        redis_url=redis_uri,
        embeddings=Embed_model,
        distance_threshold=0.9
    )
    return cache

def test_cache_connection(redis_cache):
    """Check that Redis connection is valid."""
    assert redis_cache.redis.ping(), "Cannot connect to Redis"

def test_cache_store_and_retrieve(redis_cache):
    """Test storing and retrieving an embedding-based document."""
    key = "test-key"
    doc = Document(page_content="Redis is a fast in-memory key-value store.")

    # Store document
    redis_cache.set(key, [doc])

    # Retrieve document
    result = redis_cache.get(key)
    
    assert result is not None, "No result retrieved from Redis"
    assert isinstance(result, list), "Returned result is not a list"
    assert any("Redis" in d.page_content for d in result), "Expected content not found"
