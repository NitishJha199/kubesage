from app.knowledge.model import Knowledge


SERVICE_WITHOUT_MATCHING_PODS = Knowledge(
    reason="ServiceWithoutMatchingPods",
    issue="ServiceWithoutMatchingPods",
    severity="WARNING",
    confidence=0.95,
    description=(
        "The Service selector does not match any Pods."
    ),
    recommendation=(
        "Verify the Service selector and ensure the target Pods "
        "have the expected labels."
    ),
)
