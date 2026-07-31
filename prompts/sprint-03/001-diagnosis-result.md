# Sprint 3 - Diagnosis Result Model

## Goal

Create the DiagnosisResult model for KubeSage.

## Cursor Prompt

You are working on the KubeSage project.

Architecture rules:

- Use Pydantic.
- Use type hints.
- Production-quality code.
- Add docstrings.
- No Kubernetes SDK imports.
- No diagnosis logic.

Task:

Create backend/app/diagnosis/result.py.

Create a DiagnosisResult model with the following fields:

- resource_type
- resource_name
- namespace
- diagnosis
- severity
- confidence
- evidence (List[str])
- recommendation

The model represents the output of the diagnosis engine.

## Outcome

DiagnosisResult model created.
