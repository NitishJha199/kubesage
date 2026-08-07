from typing import List

from app.diagnosis.result import DiagnosisResult
from app.knowledge.registry import get_knowledge
from app.models.node import NodeEvidence


class NodeDiagnoser:
    """
    Diagnoses Kubernetes Nodes.
    """

    def __init__(
        self,
        nodes: List[NodeEvidence],
    ) -> None:
        self._nodes = nodes

    def diagnose(self) -> List[DiagnosisResult]:
        results: List[DiagnosisResult] = []

        for node in self._nodes:
            result = self._diagnose_node(node)

            if result is not None:
                results.append(result)

        return results

    def _diagnose_node(
        self,
        node: NodeEvidence,
    ) -> DiagnosisResult | None:

        if node.ready_status == "Ready":
            return None

        knowledge = get_knowledge("NodeNotReady")

        if knowledge is None:
            return None

        evidence = [
            f"Ready Status: {node.ready_status}",
            f"Kubelet Version: {node.kubelet_version}",
            f"Container Runtime: {node.container_runtime}",
            f"OS Image: {node.os_image}",
        ]

        return DiagnosisResult(
            resource_type="Node",
            resource_name=node.name,
            namespace="-",
            diagnosis=knowledge.issue,
            severity=knowledge.severity,
            confidence=knowledge.confidence,
            evidence=evidence,
            recommendation=knowledge.recommendation,
        )
