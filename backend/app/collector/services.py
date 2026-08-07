from typing import List

from kubernetes.client.models import V1Service

from app.collector.client import KubernetesClient
from app.models.service import ServiceEvidence


class ServiceCollector:
    """
    Collects normalized Service evidence from Kubernetes.
    """

    def __init__(self, client: KubernetesClient) -> None:
        self._client = client

    def collect(self) -> List[ServiceEvidence]:
        """
        Collect all Services in the cluster.
        """
        response = self._client.core.list_service_for_all_namespaces()

        return [
            self._to_service_evidence(service)
            for service in response.items
        ]

    def _to_service_evidence(
        self,
        service: V1Service,
    ) -> ServiceEvidence:
        """
        Convert a Kubernetes Service into ServiceEvidence.
        """

        metadata = service.metadata
        spec = service.spec

        ports: List[int] = []

        if spec and spec.ports:
            ports = [
                port.port
                for port in spec.ports
            ]

        return ServiceEvidence(
            name=metadata.name if metadata else "",
            namespace=metadata.namespace if metadata else "",
            service_type=spec.type if spec and spec.type else "ClusterIP",
            cluster_ip=spec.cluster_ip if spec else None,
            selector=spec.selector if spec and spec.selector else {},
            ports=ports,
        )
