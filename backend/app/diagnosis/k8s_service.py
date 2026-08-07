from typing import List

from app.diagnosis.result import DiagnosisResult
from app.knowledge.registry import get_knowledge
from app.models.pod import PodEvidence
from app.models.service import ServiceEvidence


class ServiceDiagnoser:
    """
    Diagnoses Kubernetes Services by correlating them with Pods.
    """

    def __init__(
        self,
        services: List[ServiceEvidence],
        pods: List[PodEvidence],
    ) -> None:
        self._services = services
        self._pods = pods

    def diagnose(self) -> List[DiagnosisResult]:
        results: List[DiagnosisResult] = []

        for service in self._services:
            result = self._diagnose_service(service)

            if result is not None:
                results.append(result)

        return results

    def _diagnose_service(
        self,
        service: ServiceEvidence,
    ) -> DiagnosisResult | None:

        if not service.selector:
            return None

        matching_pods = [
            pod
            for pod in self._pods
            if (
                pod.namespace == service.namespace
                and self._matches_selector(
                    service.selector,
                    pod.labels,
                )
            )
        ]

        if matching_pods:
            return None

        knowledge = get_knowledge(
            "ServiceWithoutMatchingPods"
        )

        if knowledge is None:
            return None

        return DiagnosisResult(
            resource_type="Service",
            resource_name=service.name,
            namespace=service.namespace,
            diagnosis=knowledge.issue,
            severity=knowledge.severity,
            confidence=knowledge.confidence,
            evidence=[
                f"Selector: {service.selector}",
                "Matching Pods: 0",
            ],
            recommendation=knowledge.recommendation,
        )

    def _matches_selector(
        self,
        selector: dict[str, str],
        labels: dict[str, str],
    ) -> bool:
        for key, value in selector.items():
            if labels.get(key) != value:
                return False

        return True
