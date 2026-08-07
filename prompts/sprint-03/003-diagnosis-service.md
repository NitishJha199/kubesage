# Sprint 3 - Diagnosis Service

## Goal

Create a reusable DiagnosisService that orchestrates evidence collection and diagnosis.

## Cursor Prompt

You are working on the KubeSage project.

Architecture rules:

- Keep orchestration outside the API and playground.
- Use dependency injection.
- Reuse existing collectors and diagnosers.
- No printing.
- Return structured DiagnosisResult objects.
- Production-quality code.
- Add docstrings.

Task:

Create backend/app/diagnosis/service.py.

The service should:

1. Accept a KubernetesClient.

2. Collect:
   - Pods
   - Events
   - Nodes

3. Run:
   - PodDiagnoser

4. Return List[DiagnosisResult].

The service should become the single entry point for diagnosis.

## Outcome

DiagnosisService created.
