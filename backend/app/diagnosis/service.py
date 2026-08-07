from typing import List

from app.collector.client import KubernetesClient
from app.collector.deployments import DeploymentCollector
from app.collector.events import EventCollector
from app.collector.nodes import NodeCollector
from app.collector.persistent_volume_claims import (
    PersistentVolumeClaimCollector,
)
from app.collector.pods import PodCollector
from app.collector.services import ServiceCollector

from app.ai.response import DiagnosisWithAI
from app.ai.service import AIExplanationService

from app.diagnosis.deployment import DeploymentDiagnoser
from app.diagnosis.k8s_service import ServiceDiagnoser
from app.diagnosis.node import NodeDiagnoser
from app.diagnosis.persistent_volume_claim import (
    PersistentVolumeClaimDiagnoser,
)
from app.diagnosis.pod import PodDiagnoser
from app.diagnosis.result import DiagnosisResult


class DiagnosisService:
    """
    Coordinates evidence collection and diagnosis execution.
    """

    def __init__(
        self,
        client: KubernetesClient,
    ) -> None:
        self._client = client

    def diagnose(self) -> List[DiagnosisWithAI]:
        """
        Collect evidence and execute all registered diagnosers.
        """

        pods = PodCollector(self._client).collect()
        deployments = DeploymentCollector(self._client).collect()
        events = EventCollector(self._client).collect()
        nodes = NodeCollector(self._client).collect()
        services = ServiceCollector(self._client).collect()

        persistent_volume_claims = (
            PersistentVolumeClaimCollector(self._client).collect()
        )

        diagnosers = [
            PodDiagnoser(
                pods=pods,
                events=events,
            ),
            NodeDiagnoser(
                nodes=nodes,
            ),
            ServiceDiagnoser(
                services=services,
                pods=pods,
            ),
            DeploymentDiagnoser(
                deployments=deployments,
            ),
            PersistentVolumeClaimDiagnoser(
                persistent_volume_claims=persistent_volume_claims,
            ),
        ]

        results: List[DiagnosisResult] = []

        for diagnoser in diagnosers:
            results.extend(diagnoser.diagnose())

        ai_service = AIExplanationService()


        batch = ai_service.explain_batch(results)

        enriched_results: List[DiagnosisWithAI] = []

        for result, explanation in zip(results, batch.explanations):
            enriched_results.append(
                DiagnosisWithAI(
                    **result.model_dump(),
                    ai=explanation,
                )
            )

        return enriched_results
