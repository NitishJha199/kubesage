# Sprint 3 - Event Aware Diagnosis

## Goal

Teach the PodDiagnoser to use Kubernetes Events as additional evidence.

Architecture rules:

- Do not change collectors.
- Do not change models.
- Do not modify Knowledge objects.
- Only improve PodDiagnoser.

Task

For each pod:

1. Find all Events belonging to the pod.

2. Add Warning events into DiagnosisResult.evidence.

Format:

Event: <reason> - <message>

Ignore Normal events.

Do not change diagnosis logic yet.

The goal is only to enrich evidence.

Outcome

Diagnosis results now contain Kubernetes Warning events.
