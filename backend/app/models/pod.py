from typing import List, Optional
from pydantic import BaseModel


class ContainerState(BaseModel):
    name: str
    state: str
    reason: Optional[str] = None
    restart_count: int


class PodEvidence(BaseModel):
    name: str
    namespace: str

    phase: str

    node: Optional[str] = None

    owner_kind: Optional[str] = None
    owner_name: Optional[str] = None

    pod_ip: Optional[str] = None

    containers: List[ContainerState]
