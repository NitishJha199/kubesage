# Sprint 3 - Container State Enhancement

## Goal

Extend the container evidence model to capture richer runtime information for diagnosis.

## Cursor Prompt

You are working on the KubeSage project.

Architecture rules:

- Use Pydantic.
- Production-quality code.
- No diagnosis logic.
- No Kubernetes SDK changes outside the collector.

Task

Enhance the ContainerState model in:

backend/app/models/pod.py

Add the following optional fields:

- last_state
- last_reason
- exit_code
- signal
- started_at
- finished_at
- ready

Update the PodCollector so these fields are collected from the Kubernetes API when available.

Do not modify the diagnosis engine.

## Outcome

The Pod collector now captures richer runtime evidence for every container.
