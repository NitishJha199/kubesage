from app.knowledge.model import Knowledge


CRASH_LOOP_BACKOFF = Knowledge(
    reason="CrashLoopBackOff",
    issue="CrashLoopBackOff",
    severity="CRITICAL",
    confidence=0.95,
    description=(
        "The container repeatedly starts and crashes. "
        "Kubernetes backs off before restarting it again."
    ),
    recommendation=(
        "Inspect the container logs, verify the application startup "
        "configuration, check environment variables, mounted volumes, "
        "and required dependencies."
    ),
)
