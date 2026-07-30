"""Pod collector for gathering normalized pod evidence from Kubernetes."""

from typing import List, Optional, Tuple

from kubernetes.client.models import V1ContainerState, V1ContainerStatus, V1Pod

from app.collector.client import KubernetesClient
from app.models.pod import ContainerState, PodEvidence


class PodCollector:
    """Collects pod evidence from every namespace in the cluster."""

    def __init__(self, client: KubernetesClient) -> None:
        """Initialize the collector with an injected Kubernetes client.

        Args:
            client: Client used to query the Kubernetes API.
        """
        self._client = client

    def collect(self) -> List[PodEvidence]:
        """Return normalized evidence for every pod in the cluster.

        Returns:
            A list of PodEvidence objects, one per pod across all namespaces.
        """
        response = self._client.core.list_pod_for_all_namespaces()
        return [self._to_pod_evidence(pod) for pod in response.items]

    def _to_pod_evidence(self, pod: V1Pod) -> PodEvidence:
        """Convert a Kubernetes pod into a PodEvidence model.

        Args:
            pod: Raw pod object from the Kubernetes API.

        Returns:
            Normalized pod evidence.
        """
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
                containers.append(self._to_container_state(container_status))

        return PodEvidence(
            name=metadata.name if metadata else "",
            namespace=metadata.namespace if metadata else "",
            phase=status.phase if status and status.phase else "Unknown",
            node=spec.node_name if spec else None,
            owner_kind=owner_kind,
            owner_name=owner_name,
            pod_ip=status.pod_ip if status else None,
            containers=containers,
        )

    def _to_container_state(self, container_status: V1ContainerStatus) -> ContainerState:
        """Convert a Kubernetes container status into a ContainerState model.

        Args:
            container_status: Raw container status from the Kubernetes API.

        Returns:
            Normalized container state evidence.
        """
        state, reason = self._resolve_container_state(container_status.state)
        return ContainerState(
            name=container_status.name,
            state=state,
            reason=reason,
            restart_count=container_status.restart_count or 0,
        )

    def _resolve_container_state(
        self, state: Optional[V1ContainerState]
    ) -> Tuple[str, Optional[str]]:
        """Map a Kubernetes container state to a normalized state label.

        Args:
            state: Raw container state from the Kubernetes API.

        Returns:
            A tuple of (state_label, reason) where state_label is one of
            Running, Waiting, Terminated, or Unknown.
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
