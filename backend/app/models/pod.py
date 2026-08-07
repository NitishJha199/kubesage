from typing import List, Optional

from pydantic import BaseModel


class ContainerState(BaseModel):
    """
    Runtime state of a single container within a Kubernetes Pod.
    """

    name: str

    state: str
    reason: Optional[str] = None

    restart_count: int

    ready: bool

    last_state: Optional[str] = None
    last_reason: Optional[str] = None

    exit_code: Optional[int] = None
    signal: Optional[int] = None

    started_at: Optional[str] = None
    finished_at: Optional[str] = None


class PodEvidence(BaseModel):
    """
    Evidence collected for a Kubernetes Pod.
    """

    name: str
    namespace: str

    labels: dict[str, str]

    phase: str

    node: Optional[str] = None

    owner_kind: Optional[str] = None
    owner_name: Optional[str] = None

    pod_ip: Optional[str] = None

    containers: List[ContainerState]
