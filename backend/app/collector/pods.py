"""Pod collector for gathering normalized pod evidence from Kubernetes."""

from typing import List, Optional, Tuple

from kubernetes.client.models import (
    V1ContainerState,
    V1ContainerStatus,
    V1Pod,
)

from app.collector.client import KubernetesClient
from app.models.pod import ContainerState, PodEvidence


class PodCollector:
    """Collects pod evidence from every namespace in the cluster."""

    def __init__(self, client: KubernetesClient) -> None:
        """Initialize the collector."""
        self._client = client

    def collect(self) -> List[PodEvidence]:
        """Collect evidence for all pods."""
        response = self._client.core.list_pod_for_all_namespaces()
        return [self._to_pod_evidence(pod) for pod in response.items]

    def _to_pod_evidence(self, pod: V1Pod) -> PodEvidence:
        """Convert a Kubernetes Pod into PodEvidence."""
        metadata = pod.metadata
        spec = pod.spec
        status = pod.status

        owner_kind: Optional[str] = None
        owner_name: Optional[str] = None

        if metadata and metadata.owner_references:
            owner = metadata.owner_references[0]
            owner_kind = owner.kind
            owner_name = owner.name

        containers: List[ContainerState] = []

        if status and status.container_statuses:
            for container_status in status.container_statuses:
                containers.append(
                    self._to_container_state(container_status)
                )

        return PodEvidence(
            name=metadata.name if metadata else "",
            namespace=metadata.namespace if metadata else "",
            labels=metadata.labels if metadata and metadata.labels else {},
            phase=status.phase if status and status.phase else "Unknown",
            node=spec.node_name if spec else None,
            owner_kind=owner_kind,
            owner_name=owner_name,
            pod_ip=status.pod_ip if status else None,
            containers=containers,
        )

    def _to_container_state(
        self,
        container_status: V1ContainerStatus,
    ) -> ContainerState:
        """
        Convert Kubernetes container status into ContainerState.
        """

        state, reason = self._resolve_container_state(
            container_status.state
        )

        last_state, last_reason = self._resolve_container_state(
            container_status.last_state
        )

        terminated = (
            container_status.last_state.terminated
            if container_status.last_state
            and container_status.last_state.terminated
            else None
        )

        return ContainerState(
            name=container_status.name,
            state=state,
            reason=reason,
            restart_count=container_status.restart_count or 0,
            ready=container_status.ready,
            last_state=last_state,
            last_reason=last_reason,
            exit_code=terminated.exit_code if terminated else None,
            signal=terminated.signal if terminated else None,
            started_at=str(terminated.started_at) if terminated and terminated.started_at else None,
            finished_at=str(terminated.finished_at) if terminated and terminated.finished_at else None,
        )

    def _resolve_container_state(
        self,
        state: Optional[V1ContainerState],
    ) -> Tuple[str, Optional[str]]:
        """
        Convert Kubernetes state object into a normalized state label.
        """

        if state is None:
            return "Unknown", None

        if state.running is not None:
            return "Running", None

        if state.waiting is not None:
            return "Waiting", state.waiting.reason

        if state.terminated is not None:
            return "Terminated", state.terminated.reason

        return "Unknown", None
