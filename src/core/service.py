import abc
from typing import Generic, TypeVar

from src.storage.cache.definition import Cache

Managed = TypeVar('Managed')
Id = TypeVar('Id')


class AService(abc.ABC, Generic[Managed, Id]):
    store: Cache[Managed]

    def __init__(self, store: Cache[Managed]):
        self.store = store

    def save_obj(self, obj: Managed) -> bool:
        return self.store.put(self.get_id(obj), obj)

    def get_by_id(self, saved_id: Id, default=None):
        return self.store.get(saved_id, default)

    def exists(self, saved_id: Id) -> bool:
        return self.store.exists(saved_id)

    @abc.abstractmethod
    def get_id(self, obj: Managed) -> Id:
        pass
