import uuid


from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    server_id: str = Field(str(uuid.uuid4()), description="Unique identifier for the server instance.", example="server-1")