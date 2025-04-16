import os 


import redis
from dotenv import load_dotenv
from langchain_redis.cache import RedisSemanticCache

from models.embedding_model.embed_model import Embed_model

load_dotenv()

semantic_cache = RedisSemanticCache(
    redis_url=os.getenv("REDIS_URI"), embeddings=Embed_model, distance_threshold=0.2
)
print(semantic_cache)

