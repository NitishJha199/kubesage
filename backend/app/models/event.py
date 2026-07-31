from typing import Optional

from pydantic import BaseModel, Field


class EventEvidence(BaseModel):
    """
    Normalized representation of a Kubernetes Event.
    """

    namespace: Optional[str] = Field(
        default=None,
        description="Namespace where the event occurred."
    )

    involved_object_kind: str = Field(
        ...,
        description="Kind of the involved Kubernetes object."
    )

    involved_object_name: str = Field(
        ...,
        description="Name of the involved Kubernetes object."
    )

    type: str = Field(
        ...,
        description="Event type (Normal or Warning)."
    )

    reason: str = Field(
        ...,
        description="Short reason for the event."
    )

    message: str = Field(
        ...,
        description="Detailed event message."
    )

    source_component: Optional[str] = Field(
        default=None,
        description="Component that generated the event."
    )

    first_timestamp: Optional[str] = Field(
        default=None,
        description="First occurrence timestamp."
    )

    last_timestamp: Optional[str] = Field(
        default=None,
        description="Last occurrence timestamp."
    )

    count: Optional[int] = Field(
        default=None,
        description="Number of times the event occurred."
    )
