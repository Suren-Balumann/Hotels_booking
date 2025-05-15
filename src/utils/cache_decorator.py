import json
from functools import wraps
from src.setup import redis_manager


def my_own_cache(expire: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key_cache = f"cache:{func.__name__}"
            result_from_cache = await redis_manager.get(key_cache)
            if result_from_cache:
                return json.loads(result_from_cache)
            else:
                result = await func(*args, **kwargs)
                result_to_dict = [model.model_dump() for model in result]
                result_to_jason = json.dumps(result_to_dict)
                await redis_manager.set(key_cache, result_to_jason, expire)
                return result

        return wrapper

    return decorator
