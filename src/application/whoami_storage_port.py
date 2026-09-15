from abc import ABC, abstractmethod
from src.domain.whoami_storage import WhoamiEntity


class WhoamiRepository(ABC):
    @abstractmethod
    async def post_whoami(self, whoami_entity: WhoamiEntity) -> bool:
        ...

    @abstractmethod
    async def get_whoami_count(self) -> int:
        ...