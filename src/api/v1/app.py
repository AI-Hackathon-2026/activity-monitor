from typing import Annotated
from datetime import datetime, timezone

from fastapi import Request, Depends, APIRouter, HTTPException
from src.api.v1.schemas import WhoamiRequest, WhoamiResponse, GetServerIdResponse
from src.application.whoami_use_case import WhoamiUseCase
from src.domain.whoami_storage import WhoamiEntity, ClientInfo


def client_ip_info(request: Request) -> dict:
    xff = request.headers.get("x-forwarded-for")
    chain = [ip.strip() for ip in xff.split(",")] if xff else []
    return {
        "client_ip": chain[0]
        if chain
        else (request.client.host if request.client else "unknown"),
        "ip_chain": chain,  # e.g. ["203.0.113.5", "10.0.0.2"] — original client first, each proxy after
        "direct_peer": request.client.host
        if request.client
        else None,  # last hop before this app
    }


def get_whoami_use_case(request: Request) -> WhoamiUseCase:
    return WhoamiUseCase(whoami_repository=request.app.state.whoami_storage_adapter)


WhoamiUseCaseDependency = Annotated[WhoamiUseCase, Depends(get_whoami_use_case)]

router = APIRouter(prefix="/api/v1")
whoami_router = APIRouter(prefix="/whoami", tags=["Whoami API"])


router.include_router(whoami_router)


@whoami_router.post("/log", response_model=WhoamiResponse)
async def post_whoami(
    whoami_request: WhoamiRequest,
    whoami_use_case: WhoamiUseCaseDependency,
    request: Request,
) -> WhoamiResponse:
    whoami_entity = WhoamiEntity(
        request_id=whoami_request.request_id,
        data=whoami_request.data,
        metadata=whoami_request.metadata,
        served_by=request.app.state.server_id,
        request_type="POST",
        endpoint=str(request.url.path),
        client=ClientInfo(
            user_agent=request.headers.get("user-agent", "unknown"),
            **client_ip_info(request),
        ),
        timestamp=datetime.now(timezone.utc),
    )
    status = await whoami_use_case.post_whoami(whoami_entity)
    if not status:
        raise HTTPException(
            status_code=500, detail="Failed to store whoami data in the repository"
        )
    return WhoamiResponse(
        served_by=request.app.state.server_id,
        request_id=whoami_request.request_id,
        data=whoami_request.data,
        client_info=whoami_entity.client,
    )


@whoami_router.get("/log", response_model=WhoamiEntity)
async def get_whoami(
    request_id: str, whoami_use_case: WhoamiUseCaseDependency, request: Request
) -> WhoamiEntity:
    whoami_entity = await whoami_use_case.get_whoami(request_id)
    if whoami_entity is None:
        raise HTTPException(status_code=404, detail="Whoami data not found")
    return whoami_entity


@whoami_router.get("/count", response_model=int)
async def get_whoami_count(whoami_use_case: WhoamiUseCaseDependency) -> int:
    return await whoami_use_case.get_whoami_count()


@router.get("/server-id", response_model=GetServerIdResponse)
async def get_server_id(request: Request) -> GetServerIdResponse:
    return GetServerIdResponse(server_id=request.app.state.server_id)
