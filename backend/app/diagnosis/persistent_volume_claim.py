from typing import List

from app.diagnosis.result import DiagnosisResult
from app.knowledge.registry import get_knowledge
from app.models.persistent_volume_claim import (
    PersistentVolumeClaimEvidence,
)


class PersistentVolumeClaimDiagnoser:
    """
    Diagnoses Kubernetes PersistentVolumeClaims.
    """

    def __init__(
        self,
        persistent_volume_claims: List[PersistentVolumeClaimEvidence],
    ) -> None:
        self._persistent_volume_claims = persistent_volume_claims

    def diagnose(self) -> List[DiagnosisResult]:
        results: List[DiagnosisResult] = []

        for pvc in self._persistent_volume_claims:
            result = self._diagnose_pvc(pvc)

            if result is not None:
                results.append(result)

        return results

    def _diagnose_pvc(
        self,
        pvc: PersistentVolumeClaimEvidence,
    ) -> DiagnosisResult | None:

        if pvc.phase != "Pending":
            return None

        knowledge = get_knowledge(
            "PersistentVolumeClaimPending"
        )

        if knowledge is None:
            return None

        return DiagnosisResult(
            resource_type="PersistentVolumeClaim",
            resource_name=pvc.name,
            namespace=pvc.namespace,
            diagnosis=knowledge.issue,
            severity=knowledge.severity,
            confidence=knowledge.confidence,
            evidence=[
                f"Phase: {pvc.phase}",
                f"StorageClass: {pvc.storage_class}",
                f"Requested Storage: {pvc.requested_storage}",
                f"Volume: {pvc.volume_name}",
            ],
            recommendation=knowledge.recommendation,
        )
