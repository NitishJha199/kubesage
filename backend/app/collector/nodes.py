"""Node collector for gathering normalized node evidence from Kubernetes."""

from typing import List, Optional

from kubernetes.client.models import V1Node, V1NodeStatus

from app.collector.client import KubernetesClient
from app.models.node import NodeEvidence


class NodeCollector:
    """Collects node evidence from the cluster."""

    def __init__(self, client: KubernetesClient) -> None:
        """Initialize the collector with an injected Kubernetes client.

        Args:
            client: Client used to query the Kubernetes API.
        """
        self._client = client

    def collect(self) -> List[NodeEvidence]:
        """Return normalized evidence for every node in the cluster.

        Returns:
            A list of NodeEvidence objects, one per cluster node.
        """
        response = self._client.core.list_node()
        return [self._to_node_evidence(node) for node in response.items]

    def _to_node_evidence(self, node: V1Node) -> NodeEvidence:
        """Convert a Kubernetes node into a NodeEvidence model.

        Args:
            node: Raw node object from the Kubernetes API.

        Returns:
            Normalized node evidence.
        """
        metadata = node.metadata
        status = node.status
        node_info = status.node_info if status else None
        capacity = status.capacity if status and status.capacity else {}

        return NodeEvidence(
            name=metadata.name if metadata else "",
            roles=self._extract_roles(node),
            kubelet_version=node_info.kubelet_version if node_info else None,
            os_image=node_info.os_image if node_info else None,
            kernel_version=node_info.kernel_version if node_info else None,
            container_runtime=(
                node_info.container_runtime_version if node_info else None
            ),
            internal_ip=self._resolve_address(status, "InternalIP"),
            external_ip=self._resolve_address(status, "ExternalIP"),
            cpu_capacity=capacity.get("cpu"),
            memory_capacity=capacity.get("memory"),
            pod_capacity=capacity.get("pods"),
            ready_status=self._resolve_ready_status(status),
        )

    def _extract_roles(self, node: V1Node) -> List[str]:
        """Extract node roles from Kubernetes node labels.

        Args:
            node: Raw node object from the Kubernetes API.

        Returns:
            Role names derived from node-role labels, or an empty list if none
            are present.
        """
        roles: List[str] = []
        labels = node.metadata.labels if node.metadata and node.metadata.labels else {}
        for label_key, label_value in labels.items():
            if label_key.startswith("node-role.kubernetes.io/"):
                role = label_key.split("/", 1)[1]
                if role:
                    roles.append(role)
            elif label_key == "kubernetes.io/role" and label_value:
                roles.append(label_value)
        return roles

    def _resolve_address(
        self, status: Optional[V1NodeStatus], address_type: str
    ) -> Optional[str]:
        """Return the first node address matching the given type.

        Args:
            status: Node status object from the Kubernetes API.
            address_type: Address type to match, such as InternalIP or ExternalIP.

        Returns:
            The matching address, or None if not found.
        """
        if status is None or not status.addresses:
            return None
        for address in status.addresses:
            if address.type == address_type:
                return address.address
        return None

    def _resolve_ready_status(self, status: Optional[V1NodeStatus]) -> str:
        """Map the Kubernetes Ready condition to a normalized status label.

        Args:
            status: Node status object from the Kubernetes API.

        Returns:
            Ready when the node reports Ready=True, NotReady when Ready=False,
            and Unknown when the condition is absent.
        """
        if status is None or not status.conditions:
            return "Unknown"
        for condition in status.conditions:
            if condition.type == "Ready":
                if condition.status == "True":
                    return "Ready"
                if condition.status == "False":
                    return "NotReady"
                return "Unknown"
        return "Unknown"
