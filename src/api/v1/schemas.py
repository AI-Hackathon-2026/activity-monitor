from pydantic import BaseModel, Field

from src.domain.whoami_storage import ClientInfo


class WhoamiRequest(BaseModel):
    request_id: str = Field(..., description="Unique identifier for the request.", example="123e4567-e89b-12d3-a456-426614174000")
    data: dict = Field(..., description="The data to be processed by the API.", example={"key": "value"})
    metadata: dict = Field(dict(), description="Metadata associated with the request.", example={"source": "test"})


class WhoamiResponse(BaseModel):
    served_by: str = Field(..., description="Identifier of the server that processed the request.", example="server-1")
    request_id: str = Field(..., description="Unique identifier for the request.", example="123e4567-e89b-12d3-a456-426614174000")
    data: dict = Field(..., description="The data returned by the API.", example={"key": "value"})
    client_info: ClientInfo = Field(..., description="Information about the client making the request.")


class GetServerIdResponse(BaseModel):
    server_id: str = Field(..., description="Unique identifier for the server instance.", example="server-1")