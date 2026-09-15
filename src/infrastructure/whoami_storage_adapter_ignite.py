import json
from datetime import datetime

from pyignite import AioClient
from pyignite.exceptions import CacheError
from pyignite.datatypes.prop_codes import PROP_NAME, PROP_BACKUPS_NUMBER


from src.domain.whoami_storage import WhoamiEntity, ClientInfo
from src.application.whoami_storage_port import WhoamiRepository
from src.infrastructure.lifecycle import LifeCycle
from src.config import IgniteSettings


class WhoamiStorageAdapterIgnite(WhoamiRepository, LifeCycle):
    def __init__(self, ignite_settings: IgniteSettings):
        self.ignite_settings = ignite_settings
        self._nodes = [(node.host, node.port) for node in ignite_settings.nodes]
        self.client = AioClient(partition_aware=True)
        self._cache = None
        self.cache_name = ignite_settings.cache_name

    async def post_whoami(self, whoami_entity: WhoamiEntity) -> bool:
        try:
            if self._cache is None:
                raise CacheError(
                    "Cache is not initialized. Ensure that the start method has been called."
                )
            await self._cache.put(
                whoami_entity.request_id,
                json.dumps(whoami_entity.to_dict(), default=str),
            )
            return True
        except CacheError as e:
            print(f"Error storing whoami data: {e}")
            return False

    async def get_whoami_count(self) -> int:
        try:
            if self._cache is None:
                raise CacheError(
                    "Cache is not initialized. Ensure that the start method has been called."
                )
            async with self._cache.scan() as cursor:
                return len([entry async for entry in cursor])
        except CacheError as e:
            print(f"Error retrieving whoami count: {e}")
            return 0

    async def get_whoami(self, request_id: str) -> WhoamiEntity:
        try:
            if self._cache is None:
                raise CacheError(
                    "Cache is not initialized. Ensure that the start method has been called."
                )
            data = await self._cache.get(request_id)
            if data is None:
                raise CacheError("Whoami data not found.")
            data = json.loads(data)
            client_info = data.pop("client")
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])
            return WhoamiEntity(client=ClientInfo(**client_info), **data)
        except CacheError as e:
            print(f"Error retrieving whoami data: {e}")
            raise

    async def start(self):
        await self.client.connect(self._nodes)
        self._cache = await self.client.get_or_create_cache(
            {
                PROP_NAME: self.cache_name,
                PROP_BACKUPS_NUMBER: self.ignite_settings.replication_factor,
            }
        )

    async def stop(self):
        await self.client.close()
