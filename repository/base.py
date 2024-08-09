import abc
from abc import abstractmethod


class BaseRepository(abc.ABC):
    @abstractmethod
    def read(self, *args, **kwargs):
        ...

    @abstractmethod
    def read_all(self, *args, **kwargs):
        ...

    @abstractmethod
    def create(self, *args, **kwargs):
        ...

    @abstractmethod
    def update(self, *args, **kwargs):
        ...

    @abstractmethod
    def delete(self, *args, **kwargs):
        ...
