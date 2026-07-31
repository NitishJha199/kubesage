from typing import List, Optional

from kubernetes.client.models import CoreV1Event

from app.collector.client import KubernetesClient
from app.models.event import EventEvidence


class EventCollector:
    """
    Collects Kubernetes events and converts them into EventEvidence models.
    """

    def __init__(self, client: KubernetesClient) -> None:
        self._client = client

    def collect(self) -> List[EventEvidence]:
        """
        Collect all events from every namespace.
        """
        event_list = self._client.list_events()

        return [
            self._to_event_evidence(event)
            for event in event_list.items
        ]

    def _to_event_evidence(self, event: CoreV1Event) -> EventEvidence:
        """
        Convert a Kubernetes Event into EventEvidence.
        """

        involved = event.involved_object
        source = event.source

        first_timestamp = (
            event.first_timestamp.isoformat()
            if event.first_timestamp
            else None
        )

        last_timestamp = (
            event.last_timestamp.isoformat()
            if event.last_timestamp
            else None
        )

        return EventEvidence(
            namespace=event.metadata.namespace if event.metadata else None,
            involved_object_kind=involved.kind if involved else "Unknown",
            involved_object_name=involved.name if involved else "Unknown",
            type=event.type or "Unknown",
            reason=event.reason or "Unknown",
            message=event.message or "",
            source_component=source.component if source else None,
            first_timestamp=first_timestamp,
            last_timestamp=last_timestamp,
            count=event.count,
        )
