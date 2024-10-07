from abc import ABCMeta, abstractmethod
from typing import AsyncGenerator


class BaseDBAccessor(metaclass=ABCMeta):

    @abstractmethod
    async def lifespan_connections(self, *args, **kwargs) -> AsyncGenerator:
        pass

    @abstractmethod
    async def ping(self, *args, **kwargs) -> bool:
        pass
