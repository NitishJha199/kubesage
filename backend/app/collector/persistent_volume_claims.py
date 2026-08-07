from typing import List

from kubernetes.client.models import V1PersistentVolumeClaim

from app.collector.client import KubernetesClient
from app.models.persistent_volume_claim import (
    PersistentVolumeClaimEvidence,
)


class PersistentVolumeClaimCollector:
    """
    Collects normalized PersistentVolumeClaim evidence.
    """

    def __init__(
        self,
        client: KubernetesClient,
    ) -> None:
        self._client = client

    def collect(self) -> List[PersistentVolumeClaimEvidence]:

        response = (
            self._client.core.list_persistent_volume_claim_for_all_namespaces()
        )

        return [
            self._to_evidence(pvc)
            for pvc in response.items
        ]

    def _to_evidence(
        self,
        pvc: V1PersistentVolumeClaim,
    ) -> PersistentVolumeClaimEvidence:

        spec = pvc.spec
        status = pvc.status
        metadata = pvc.metadata

        return PersistentVolumeClaimEvidence(
            name=metadata.name,
            namespace=metadata.namespace,
            phase=status.phase or "Unknown",
            volume_name=spec.volume_name,
            storage_class=spec.storage_class_name,
            requested_storage=(
                spec.resources.requests.get("storage")
                if spec.resources
                and spec.resources.requests
                else None
            ),
            access_modes=spec.access_modes or [],
        )
