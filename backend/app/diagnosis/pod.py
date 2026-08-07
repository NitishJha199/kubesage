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
        Diagnose a single pod using the best available evidence.
        """

        pod_events = self._get_pod_events(pod)

        # ---------------------------------------------------------
        # Step 1: Scheduling failures (highest priority)
        # ---------------------------------------------------------
        for event in pod_events:
            if event.reason == "FailedScheduling":

                knowledge = get_knowledge("FailedScheduling")

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
                        f"Scheduling event: {event.message}",
                    ],
                    recommendation=knowledge.recommendation,
                )

        # ---------------------------------------------------------
        # Step 2: Container failures
        # ---------------------------------------------------------
        for container in pod.containers:

            reason = self._determine_root_cause(container)

            if reason is None:
                continue

            knowledge = get_knowledge(reason)

            if knowledge is None:
                continue

            evidence = [
                f"Pod phase: {pod.phase}",
                f"Container state: {container.state}",
                f"Current reason: {container.reason}",
                f"Last state: {container.last_state}",
                f"Last reason: {container.last_reason}",
                f"Restart count: {container.restart_count}",
            ]

            if container.exit_code is not None:
                evidence.append(f"Exit code: {container.exit_code}")

            for event in pod_events:
                evidence.append(
                    f"Event: {event.reason} - {event.message}"
                )

            return DiagnosisResult(
                resource_type="Pod",
                resource_name=pod.name,
                namespace=pod.namespace,
                diagnosis=knowledge.issue,
                severity=knowledge.severity,
                confidence=knowledge.confidence,
                evidence=evidence,
                recommendation=knowledge.recommendation,
            )

        return None

    def _determine_root_cause(self, container) -> str | None:
        """
        Determine the most likely root cause for a container.

        Priority:
        1. Last termination reason
        2. Current waiting reason
        3. CrashLoopBackOff fallback
        """

        # Highest priority: previous termination reason
        if container.last_reason:
            return container.last_reason

        # Second priority: current waiting reason
        if container.reason:
            return container.reason

        # Fallback for restarting containers
        if (
            container.state == "Waiting"
            and container.restart_count > 0
        ):
            return "CrashLoopBackOff"

        return None

    def _get_pod_events(
        self,
        pod: PodEvidence,
    ) -> List[EventEvidence]:
        """
        Return events belonging to the given pod.
        """

        return [
            event
            for event in self._events
            if event.involved_object_kind == "Pod"
            and event.involved_object_name == pod.name
            and event.namespace == pod.namespace
            and event.type == "Warning"
        ]
