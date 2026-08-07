from app.knowledge.model import Knowledge


PERSISTENT_VOLUME_CLAIM_PENDING = Knowledge(
    reason="PersistentVolumeClaimPending",
    issue="PersistentVolumeClaimPending",
    severity="WARNING",
    confidence=0.95,
    description=(
        "The PersistentVolumeClaim is Pending because Kubernetes "
        "could not bind it to a suitable PersistentVolume."
    ),
    recommendation=(
        "Verify the StorageClass exists, ensure a matching "
        "PersistentVolume is available, and inspect the "
        "PersistentVolumeClaim events."
    ),
)
