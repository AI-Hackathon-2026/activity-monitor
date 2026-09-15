from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class ClientInfo:
    client_ip: str
    ip_chain: list[str]
    direct_peer: str
    user_agent: str


@dataclass
class WhoamiEntity:
    served_by: str

    request_id: str
    request_type: str
    endpoint: str

    data: dict
    metadata: dict
    client: ClientInfo
    timestamp: datetime

    def to_dict(self) -> dict:
        return asdict(self)
