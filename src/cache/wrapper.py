# хотим задекорировать select_dict
# будет запускаться, если в редиске ничего нет,
# если есть, то возьмёт из кэша и ничего искать не будет


# ooiiii aaiii o ii i  iii ooaaooiio

# чё делаем ёпта
# cоздаём функцию, которая принимает параметры подключения к кэшу,
# подключается к нему и имеет в себе декоратор который всё красиво делает

from functools import wraps
from cache.redis_cache import RedisCache

def fetch_from_cache(cache_name: str, cache_config: dict):
    cache_conn = RedisCache(cache_config['redis']) # подключаемся к Redis
    ttl = cache_config['ttl']
    def decorator(f):
        # как оно работает
        # лезем в кэш и смотрим, есть ли там что-то
        # если есть, то возвращаем кэшированную информацию
        # если нет, то запускаем декорируемую функцию
        # достаём оттуда информацию
        # заносим её в кэш
        # возвращаем кэшированную информацию
        @wraps(f)
        def wrapper(*args, **kwargs):
            cached_value = cache_conn.get_value(cache_name)
            #print("cached_value=", cached_value)
            if cached_value:
                return cached_value
            response = f(*args, **kwargs)
            #print("response=", response)
            cache_conn.set_value(cache_name,response,ttl)
            return response
        return wrapper
    return decorator
