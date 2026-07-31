from typing import List, Optional

from pydantic import BaseModel


class NodeEvidence(BaseModel):
    name: str
    roles: List[str]

    kubelet_version: Optional[str] = None
    os_image: Optional[str] = None
    kernel_version: Optional[str] = None
    container_runtime: Optional[str] = None

    internal_ip: Optional[str] = None
    external_ip: Optional[str] = None

    cpu_capacity: Optional[str] = None
    memory_capacity: Optional[str] = None
    pod_capacity: Optional[str] = None

    ready_status: str
