import os

from redis import Redis
from structlog import get_logger

log = get_logger()

REDIS_EXPIRATION_TIME: int = os.getenv("REDIS_EXPIRATION_TIME")


class RedisService:

    def __init__(self):
        self.redis_host = "redis-orders"
        self.redis_port = 6379
        self.redis = self.connect()

    def connect(self):
        try:
            return Redis(host=self.redis_host, port=self.redis_port, db=0)
        except Exception as exc:
            log.error(
                f"Could not connect to Redis with "
                f"REDIS_HOST: {str(self.redis_host)}" 
                f"REDIS_PORT: {str(self.redis_port)}"
            )
            raise exc

    def get_value(self, key):
        log.info(f"[CACHE] GET value: {key}")
        return self.redis.get(key)

    def set_value(self, key, value):
        log.info(f"[CACHE] SET value: {key}")
        return self.redis.set(key, value, ex=REDIS_EXPIRATION_TIME)

    def delete_value(self, key):
        log.info(f"[CACHE] DELETE value: {key}")
        self.redis.delete(key)
