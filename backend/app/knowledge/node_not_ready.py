from app.knowledge.model import Knowledge


NODE_NOT_READY = Knowledge(
    reason="NodeNotReady",
    issue="NodeNotReady",
    severity="CRITICAL",
    confidence=0.99,
    description=(
        "The Kubernetes node is not in the Ready state and "
        "cannot reliably schedule or run workloads."
    ),
    recommendation=(
        "Inspect the kubelet service, verify node connectivity, "
        "check container runtime health, and review node events."
    ),
)
