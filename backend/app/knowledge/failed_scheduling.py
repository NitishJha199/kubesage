from app.knowledge.model import Knowledge


FAILED_SCHEDULING = Knowledge(
    reason="FailedScheduling",
    issue="FailedScheduling",
    severity="CRITICAL",
    confidence=0.95,
    description=(
        "The Kubernetes scheduler could not assign the pod to any node."
    ),
    recommendation=(
        "Check available cluster resources, node selectors, taints, "
        "tolerations, affinity rules, and PersistentVolumeClaims."
    ),
)
