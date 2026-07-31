# Sprint 4 - Knowledge Registry

## Goal

Introduce a registry for Kubernetes troubleshooting knowledge.

## Cursor Prompt

You are working on the KubeSage project.

Architecture rules:

- The registry is the single entry point to the Knowledge Base.
- Diagnosis engines must not import individual knowledge files.
- The registry returns Knowledge objects.
- Use type hints.
- Add docstrings.
- Follow PEP8.

Task:

Create backend/app/knowledge/registry.py.

Requirements:

- Register all available knowledge entries.
- Provide a function:

get_knowledge(issue: str) -> Knowledge | None

Return None if the issue is unknown.

## Outcome

- Centralized Knowledge Registry created.
- Diagnosis engines can retrieve knowledge by issue name.
