from typing import List

from app.diagnosis.result import DiagnosisResult
from app.models.deployment import DeploymentEvidence


class DeploymentDiagnoser:
    """
    Diagnoses Kubernetes Deployments using normalized deployment evidence.
    """

    def __init__(self, deployments: List[DeploymentEvidence]) -> None:
        """
        Initialize the deployment diagnoser.

        Args:
            deployments: Collected deployment evidence.
        """
        self._deployments = deployments

    def diagnose(self) -> List[DiagnosisResult]:
        """
        Diagnose all deployments.

        Returns:
            List of deployment diagnosis results.
        """
        results: List[DiagnosisResult] = []

        for deployment in self._deployments:
            result = self._diagnose_deployment(deployment)

            if result is not None:
                results.append(result)

        return results

    def _diagnose_deployment(
        self,
        deployment: DeploymentEvidence,
    ) -> DiagnosisResult | None:
        """
        Diagnose a single deployment.

        Args:
            deployment: Deployment evidence.

        Returns:
            DiagnosisResult if an issue is found, otherwise None.
        """
        if self._is_healthy(deployment):
            return None

        return DiagnosisResult(
            resource_type="Deployment",
            resource_name=deployment.name,
            namespace=deployment.namespace,
            diagnosis="DeploymentUnavailable",
            severity="WARNING",
            confidence=0.90,
            evidence=[
                f"Desired replicas: {deployment.desired_replicas}",
                f"Available replicas: {deployment.available_replicas}",
                f"Ready replicas: {deployment.ready_replicas}",
                f"Unavailable replicas: {deployment.unavailable_replicas}",
            ],
            recommendation=(
                "Some replicas are unavailable. "
                "Inspect the Pods belonging to this Deployment "
                "to determine the underlying cause."
            ),
        )

    def _is_healthy(
        self,
        deployment: DeploymentEvidence,
    ) -> bool:
        """
        Determine whether the deployment is healthy.

        Args:
            deployment: Deployment evidence.

        Returns:
            True if all desired replicas are available.
        """
        return (
            deployment.available_replicas
            >= deployment.desired_replicas
        )
