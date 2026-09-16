from abc import ABC, abstractmethod


class LifeCycle(ABC):
    @abstractmethod
    async def start(self) -> None: ...

    @abstractmethod
    async def stop(self) -> None: ...
