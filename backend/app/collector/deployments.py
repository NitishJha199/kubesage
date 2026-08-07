from typing import List

from kubernetes.client.models import V1Deployment

from app.collector.client import KubernetesClient
from app.models.deployment import DeploymentEvidence


class DeploymentCollector:
    """
    Collects Deployment evidence from every namespace.
    """

    def __init__(self, client: KubernetesClient) -> None:
        self._client = client

    def collect(self) -> List[DeploymentEvidence]:

        response = self._client.apps.list_deployment_for_all_namespaces()

        return [
            self._to_evidence(deployment)
            for deployment in response.items
        ]

    def _to_evidence(
        self,
        deployment: V1Deployment,
    ) -> DeploymentEvidence:

        metadata = deployment.metadata
        spec = deployment.spec
        status = deployment.status

        return DeploymentEvidence(
            name=metadata.name,
            namespace=metadata.namespace,

            desired_replicas=spec.replicas or 0,

            available_replicas=status.available_replicas or 0,
            ready_replicas=status.ready_replicas or 0,
            updated_replicas=status.updated_replicas or 0,
            unavailable_replicas=status.unavailable_replicas or 0,

            generation=metadata.generation,
            observed_generation=status.observed_generation,
        )
