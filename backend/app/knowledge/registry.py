from app.knowledge.crash_loop_backoff import CRASH_LOOP_BACKOFF
from app.knowledge.image_pull_backoff import IMAGE_PULL_BACKOFF
from app.knowledge.model import Knowledge


_KNOWLEDGE: dict[str, Knowledge] = {
    IMAGE_PULL_BACKOFF.issue: IMAGE_PULL_BACKOFF,
    CRASH_LOOP_BACKOFF.issue: CRASH_LOOP_BACKOFF,
}


def get_knowledge(issue: str) -> Knowledge | None:
    """
    Return knowledge for a Kubernetes issue.
    """
    return _KNOWLEDGE.get(issue)
