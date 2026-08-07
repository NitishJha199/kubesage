from typing import Optional

from pydantic import BaseModel


class PersistentVolumeEvidence(BaseModel):
    """
    Normalized evidence collected for a Kubernetes PersistentVolume.
    """

    name: str

    phase: str

    storage_class: Optional[str] = None

    capacity: Optional[str] = None

    access_modes: list[str]

    reclaim_policy: Optional[str] = None

    claim_name: Optional[str] = None

    claim_namespace: Optional[str] = None
