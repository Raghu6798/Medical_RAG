import os 
import sys 

import redis
from dotenv import load_dotenv
from langchain_redis.cache import RedisSemanticCache

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from agent2agent.models.embedding_model.embed_model import Embed_model

load_dotenv()



semantic_cache = RedisSemanticCache(
    redis_url=os.getenv("REDIS_URI"), embeddings=Embed_model, distance_threshold=0.2
)
print(semantic_cache)

