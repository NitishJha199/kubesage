from typing import List

from app.diagnosis.result import DiagnosisResult
from app.knowledge.registry import get_knowledge
from app.models.event import EventEvidence
from app.models.pod import PodEvidence


class PodDiagnoser:
    """
    Diagnoses Kubernetes Pods using collected evidence and the Knowledge Base.
    """

    def __init__(
        self,
        pods: List[PodEvidence],
        events: List[EventEvidence],
    ) -> None:
        self._pods = pods
        self._events = events

    def diagnose(self) -> List[DiagnosisResult]:
        """
        Diagnose all collected pods.
        """
        results: List[DiagnosisResult] = []

        for pod in self._pods:
            result = self._diagnose_pod(pod)

            if result is not None:
                results.append(result)

        return results

    def _diagnose_pod(
        self,
        pod: PodEvidence,
    ) -> DiagnosisResult | None:
        """
        Diagnose a single pod.
        """

        for container in pod.containers:

            # Normalize the Kubernetes reason
            reason = container.reason

            # Fallback for CrashLoopBackOff
            if (
                reason is None
                and container.state == "Waiting"
                and container.restart_count > 0
            ):
                reason = "CrashLoopBackOff"

            knowledge = get_knowledge(reason)

            if knowledge is None:
                continue

            return DiagnosisResult(
                resource_type="Pod",
                resource_name=pod.name,
                namespace=pod.namespace,
                diagnosis=knowledge.issue,
                severity=knowledge.severity,
                confidence=knowledge.confidence,
                evidence=[
                    f"Pod phase: {pod.phase}",
                    f"Container state: {container.state}",
                    f"Reason: {reason}",
                    f"Restart count: {container.restart_count}",
                ],
                recommendation=knowledge.recommendation,
            )

        return None
