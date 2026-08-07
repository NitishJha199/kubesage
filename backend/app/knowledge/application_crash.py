from app.knowledge.model import Knowledge


APPLICATION_CRASH = Knowledge(
    reason="Error",
    issue="ApplicationCrash",
    severity="CRITICAL",
    confidence=0.90,
    description=(
        "The container terminated because the application exited with an error."
    ),
    recommendation=(
        "Inspect the container logs, verify the application startup "
        "configuration, validate environment variables, check mounted "
        "volumes, and ensure all required dependencies are available."
    ),
)
