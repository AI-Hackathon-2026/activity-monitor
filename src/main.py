from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import Settings
from src.infrastructure.whoami_storage_adapter_mock import WhoamiStorageAdapterMock
from src.api.v1.app import router as whoami_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings: Settings = app.state.settings

    whoami_storage_adapter = WhoamiStorageAdapterMock()
    await whoami_storage_adapter.start()

    app.state.whoami_storage_adapter = whoami_storage_adapter
    app.state.server_id = settings.server_id

    yield

    await whoami_storage_adapter.stop()


def create_app() -> FastAPI:
    settings = Settings()
    app = FastAPI(lifespan=lifespan)
    app.state.settings = settings
    app.include_router(whoami_router)
    return app
