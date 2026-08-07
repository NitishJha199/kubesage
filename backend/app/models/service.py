from typing import Optional

from pydantic import BaseModel


class ServiceEvidence(BaseModel):
    """
    Normalized representation of a Kubernetes Service.
    """

    name: str
    namespace: str

    service_type: str

    cluster_ip: Optional[str]

    selector: dict[str, str]

    ports: list[int]
