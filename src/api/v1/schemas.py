from pydantic import BaseModel, Field

from src.domain.whoami_storage import ClientInfo


class WhoamiRequest(BaseModel):
    request_id: str = Field(
        ...,
        description="Unique identifier for the request.",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )
    data: dict = Field(
        ...,
        description="The data to be processed by the API.",
        examples=[{"key": "value"}],
    )
    metadata: dict = Field(
        dict(),
        description="Metadata associated with the request.",
        examples=[{"source": "test"}],
    )


class WhoamiResponse(BaseModel):
    served_by: str = Field(
        ...,
        description="Identifier of the server that processed the request.",
        examples=["server-1"],
    )
    request_id: str = Field(
        ...,
        description="Unique identifier for the request.",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )
    data: dict = Field(
        ..., description="The data returned by the API.", examples=[{"key": "value"}]
    )
    client_info: ClientInfo = Field(
        ..., description="Information about the client making the request."
    )


class GetServerIdResponse(BaseModel):
    server_id: str = Field(
        ...,
        description="Unique identifier for the server instance.",
        examples=["server-1"],
    )
