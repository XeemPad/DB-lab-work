import json
from redis import Redis, DataError


class RedisCache:
    def __init__(self, config: dict):
        self.config = config
        self.conn = self._connect()

    def _connect(self):
        conn = Redis(**self.config)
        return conn

    def set_value(self, name: str, value_dict: dict, ttl: int):
        value_js = json.dumps(value_dict)
        try:
            self.conn.set(name=name, value=value_js)
            if ttl > 0:
                self.conn.expire(name, ttl)
                return True
        except DataError as err:
            print(err)
            return False

    def get_value(self, name: str):
        value_js = self.conn.get(name)
        if value_js:
            value_dict = json.loads(value_js)
            print(value_dict)
            return value_dict
        else:
            return None
