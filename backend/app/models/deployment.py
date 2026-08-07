from typing import Optional

from pydantic import BaseModel


class DeploymentEvidence(BaseModel):
    """
    Normalized representation of a Kubernetes Deployment.
    """

    name: str

    namespace: str

    desired_replicas: int

    available_replicas: int

    ready_replicas: int

    updated_replicas: int

    unavailable_replicas: int

    observed_generation: Optional[int] = None

    generation: Optional[int] = None
