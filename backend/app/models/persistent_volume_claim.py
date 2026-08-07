from typing import Optional

from pydantic import BaseModel


class PersistentVolumeClaimEvidence(BaseModel):
    """
    Normalized evidence collected for a Kubernetes PersistentVolumeClaim.
    """

    name: str
    namespace: str

    phase: str

    volume_name: Optional[str] = None

    storage_class: Optional[str] = None

    requested_storage: Optional[str] = None

    access_modes: list[str]
