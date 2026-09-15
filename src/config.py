import uuid


from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class IgniteHost(BaseModel):
    host: str = Field(
        ..., description="The hostname or IP address of the Ignite server."
    )
    port: int = Field(..., description="The port number of the Ignite server.")


class IgniteSettings(BaseSettings):
    cache_name: str = Field(
        "whoami_cache",
        description="The name of the cache used for storing whoami data.",
    )
    replication_factor: int = Field(
        1, description="The replication factor for the Ignite cache."
    )

    nodes: list[IgniteHost] = Field(..., description="A list of Ignite server nodes.")


class Settings(BaseSettings):
    server_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for the server instance.",
        examples=["server-1"],
    )

    ignite_settings: IgniteSettings = Field(
        default_factory=IgniteSettings,
        description="Configuration settings for the Ignite server.",
    )

    model_config = SettingsConfigDict(
        env_file=None,
        env_nested_delimiter="__",
    )
