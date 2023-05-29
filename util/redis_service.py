import redis
import yaml

with open("config/config.yml", "r") as f:
    config = yaml.safe_load(f)
    redis_config = config["redis"]

pool = redis.ConnectionPool(
    host=redis_config["host"],
    port=redis_config["port"],
    password=redis_config["password"],
    db=redis_config["db"]
)


def get_redis_connection():
    return redis.Redis(connection_pool=pool)
