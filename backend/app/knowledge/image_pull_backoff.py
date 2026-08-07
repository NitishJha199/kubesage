from app.knowledge.model import Knowledge


IMAGE_PULL_BACKOFF = Knowledge(
    reason="ImagePullBackOff",
    issue="ImagePullBackOff",
    severity="CRITICAL",
    confidence=0.95,
    description=(
        "The kubelet is unable to pull the requested container image. "
        "The image may not exist, the tag may be incorrect, or registry "
        "authentication may have failed."
    ),
    recommendation=(
        "Verify the image name and tag, check registry connectivity, "
        "confirm imagePullSecrets, and ensure the registry is accessible."
    ),
)
