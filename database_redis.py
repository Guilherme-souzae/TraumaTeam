import redis

class DatabaseRedis:
    def __init__(self):
        self.client = redis.Redis(host='redis', port=6379, decode_responses=True)