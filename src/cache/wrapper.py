
from functools import wraps
from cache.redis_cache import RedisCache

def fetch_from_cache(cache_name: str, cache_config: dict):
    cache_conn = RedisCache(cache_config['redis']) # подключаемся к Redis
    print(cache_config)
    ttl = cache_config['ttl']  # time to last

    def decorator(f):
        ''' Лезем в кэш и смотрим, есть ли там что-то
        если есть, то возвращаем кэшированную информацию
        если нет, то запускаем декорируемую функцию
        достаём оттуда информацию, заносим её в кэш, возвращаем кэшированную информацию 
        '''
        @wraps(f)
        def wrapper(*args, **kwargs):
            cached_value = cache_conn.get_value(cache_name)
            if cached_value:
                return cached_value
            response = f(*args, **kwargs)
            cache_conn.set_value(cache_name, response, ttl)
            return response
        return wrapper
    return decorator
