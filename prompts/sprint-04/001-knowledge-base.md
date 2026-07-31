# Sprint 4 - Knowledge Base

## Goal

Introduce the Knowledge Base for KubeSage.

## Cursor Prompt

You are working on the KubeSage project.

Architecture rules:

- The knowledge layer stores Kubernetes troubleshooting knowledge.
- It must not communicate with Kubernetes.
- It must not contain diagnosis logic.
- It only provides structured information about known Kubernetes issues.
- Use Pydantic models.
- Add docstrings and type hints.
- Follow PEP8.

Task:

Create a knowledge model that represents a Kubernetes issue.

The model should contain:

- issue
- severity
- confidence
- description
- recommendation

Then create the first knowledge entry for:

ImagePullBackOff

Populate it with production-quality descriptions and recommendations.

## Outcome

- Knowledge model created.
- First knowledge entry added.
- Diagnosis engine will consume this knowledge in later steps.
