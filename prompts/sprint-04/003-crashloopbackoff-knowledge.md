# Sprint 4 - CrashLoopBackOff Knowledge

## Goal

Teach KubeSage how to diagnose CrashLoopBackOff pods.

## Cursor Prompt

You are working on the KubeSage project.

Architecture rules:

- Do not modify collectors.
- Use the existing Knowledge model.
- Follow the same pattern as ImagePullBackOff.
- Use type hints.
- Add docstrings.
- Follow PEP8.

Task:

Create backend/app/knowledge/crash_loop_backoff.py.

Create a Knowledge object for the Kubernetes issue:

CrashLoopBackOff

Populate:

- issue
- description
- severity
- confidence
- recommendation

Do not change the diagnosis engine.

## Outcome

CrashLoopBackOff knowledge added to the Knowledge Base.
