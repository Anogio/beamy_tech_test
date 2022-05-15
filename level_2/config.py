import os

import redis

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")

# No connection is established at declaration time
redis_client = redis.Redis(host=REDIS_HOST, port=6379)
