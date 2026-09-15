from src.application.whoami_storage_port import WhoamiRepository
from src.domain.whoami_storage import WhoamiEntity


class WhoamiUseCase:
    def __init__(self, whoami_repository: WhoamiRepository):
        self.whoami_repository = whoami_repository

    async def post_whoami(self, whoami_entity: WhoamiEntity) -> bool:
        return await self.whoami_repository.post_whoami(whoami_entity)

    async def get_whoami_count(self) -> int:
        return await self.whoami_repository.get_whoami_count()

    async def get_whoami(self, request_id: str) -> WhoamiEntity:
        return await self.whoami_repository.get_whoami(request_id)
