import redis
import json
import os

r = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))

def get_cached(key: str):
    data = r.get(key)
    if data:
        print(f"✅ CACHE HIT — {key}")
        return json.loads(data)
    print(f"❌ CACHE MISS — {key}")
    return None

def set_cache(key: str, value: dict, ttl: int = 60):
    r.setex(key, ttl, json.dumps(value))