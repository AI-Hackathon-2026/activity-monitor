from src.domain.whoami_storage import WhoamiEntity
from src.application.whoami_storage_port import WhoamiRepository
from src.infrastructure.lifecycle import LifeCycle



class WhoamiStorageAdapterMock(WhoamiRepository, LifeCycle):
    def __init__(self):
        self.repository = {}

    async def post_whoami(self, whoami_entity: WhoamiEntity) -> bool:
        self.repository[whoami_entity.request_id] = whoami_entity
        return True

    async def get_whoami_count(self) -> int:
        return len(self.repository)

    async def start(self):
        ...

    async def stop(self):
        ...
