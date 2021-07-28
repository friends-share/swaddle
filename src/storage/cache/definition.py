import abc
import pickle
from typing import TypeVar, Generic, List

import redis
from redis import Redis

from src.config import SystemConfig

Type = TypeVar('Type')


class Cache(abc.ABC, Generic[Type]):
    __cache__: Redis

    @staticmethod
    def start():
        Cache.__cache__ = redis.Redis(host=SystemConfig.get_vital("REDIS_HOST"),
                                      port=SystemConfig.get("REDIS_PORT", "6379"),
                                      db=SystemConfig.get("REDIS_DB", "0"),
                                      password=None, socket_timeout=None)

    @staticmethod
    def stop():
        if Cache.__cache__:
            Cache.__cache__.close()

    def put(self, key, value: Type) -> bool:
        return Cache.__cache__.set(self.internal_key(key), pickle.dumps(value)) if value else None

    def get(self, key, default=None) -> Type:
        return Cache._get(self.internal_key(key), default)

    @staticmethod
    def _get(internal_key, default=None):
        value = Cache.__cache__.get(internal_key)
        return pickle.loads(value) if value else default

    def rm(self, key):
        return Cache.__cache__.delete(self.internal_key(key))

    def rm_all(self, partial: str = None) -> int:
        search_key = f'{self.data_prefix()}*{partial}*' if partial else f'{self.data_prefix()}*'
        count = 0
        for key in Cache.__cache__.scan_iter(search_key):
            Cache.__cache__.delete(key)
            count += 1
        return count

    def get_all(self, partial: str = None) -> List[Type]:
        search_key = f'{self.data_prefix()}*{partial}*' if partial else f'{self.data_prefix()}*'
        data = [Cache._get(key) for key in Cache.__cache__.scan_iter(search_key)]
        return data

    def exists(self, key) -> bool:
        return Cache.__cache__.exists(self.internal_key(key))

    def keys(self) -> List[str]:
        return Cache.__cache__.keys(self.data_prefix() + "*")

    @abc.abstractmethod
    def data_prefix(self) -> str:
        pass

    def internal_key(self, key: str):
        return self.data_prefix() + str(key)
