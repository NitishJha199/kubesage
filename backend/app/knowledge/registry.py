from typing import Optional

from app.knowledge.application_crash import APPLICATION_CRASH
from app.knowledge.crash_loop_backoff import CRASH_LOOP_BACKOFF
from app.knowledge.image_pull_backoff import IMAGE_PULL_BACKOFF
from app.knowledge.model import Knowledge
from app.knowledge.oom_killed import OOM_KILLED
from app.knowledge.node_not_ready import NODE_NOT_READY
from app.knowledge.failed_scheduling import FAILED_SCHEDULING
from app.knowledge.service_without_matching_pods import (
    SERVICE_WITHOUT_MATCHING_PODS,
)
from app.knowledge.persistent_volume_claim_pending import (
    PERSISTENT_VOLUME_CLAIM_PENDING,
)
_REGISTRY: dict[str, Knowledge] = {
    IMAGE_PULL_BACKOFF.reason: IMAGE_PULL_BACKOFF,
    CRASH_LOOP_BACKOFF.reason: CRASH_LOOP_BACKOFF,
    OOM_KILLED.reason: OOM_KILLED,
    APPLICATION_CRASH.reason: APPLICATION_CRASH,
    NODE_NOT_READY.reason: NODE_NOT_READY,
    FAILED_SCHEDULING.reason: FAILED_SCHEDULING,
    SERVICE_WITHOUT_MATCHING_PODS.reason: SERVICE_WITHOUT_MATCHING_PODS,
    PERSISTENT_VOLUME_CLAIM_PENDING.reason:
    PERSISTENT_VOLUME_CLAIM_PENDING,
}


def get_knowledge(reason: Optional[str]) -> Optional[Knowledge]:
    """
    Return the Knowledge object associated with a Kubernetes reason.
    """

    if reason is None:
        return None

    return _REGISTRY.get(reason)
