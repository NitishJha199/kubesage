from typing import List

from kubernetes.client import V1PersistentVolume

from app.collector.client import KubernetesClient
from app.models.persistent_volume import (
    PersistentVolumeEvidence,
)


class PersistentVolumeCollector:
    """
    Collects PersistentVolume evidence.
    """

    def __init__(
        self,
        client: KubernetesClient,
    ) -> None:
        self._client = client

    def collect(self) -> List[PersistentVolumeEvidence]:
        """
        Collect PersistentVolumes from the cluster.
        """

        volumes = (
            self._client
            .list_persistent_volumes()
            .items
        )

        evidence: List[PersistentVolumeEvidence] = []

        for volume in volumes:
            evidence.append(
                self._build(volume)
            )

        return evidence

    def _build(
        self,
        volume: V1PersistentVolume,
    ) -> PersistentVolumeEvidence:

        claim = volume.spec.claim_ref

        return PersistentVolumeEvidence(
            name=volume.metadata.name,
            phase=volume.status.phase,
            storage_class=volume.spec.storage_class_name,
            capacity=(
                volume.spec.capacity.get("storage")
                if volume.spec.capacity
                else None
            ),
            access_modes=volume.spec.access_modes or [],
            reclaim_policy=volume.spec.persistent_volume_reclaim_policy,
            claim_name=(
                claim.name
                if claim
                else None
            ),
            claim_namespace=(
                claim.namespace
                if claim
                else None
            ),
        )
