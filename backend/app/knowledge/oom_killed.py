from app.knowledge.model import Knowledge


OOM_KILLED = Knowledge(
    reason="OOMKilled",
    issue="OOMKilled",
    severity="CRITICAL",
    confidence=0.98,
    description=(
        "The container exceeded its configured memory limit and was terminated "
        "by the Linux Out-Of-Memory (OOM) killer."
    ),
    recommendation=(
        "Increase the container memory limit, reduce application memory usage, "
        "or investigate possible memory leaks."
    ),
)
