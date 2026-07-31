# Sprint 3 - Pod Diagnoser

## Goal

Implement the first diagnosis engine for KubeSage.

The Pod Diagnoser is responsible for analyzing normalized PodEvidence objects
and producing structured DiagnosisResult objects.

---

## Cursor Prompt

You are working on the KubeSage project.

Architecture rules:

- The diagnosis layer must never communicate with Kubernetes directly.
- Only consume normalized Pydantic models from the collector layer.
- Never import the Kubernetes SDK.
- Return DiagnosisResult objects only.
- Use type hints everywhere.
- Add docstrings.
- Keep the implementation modular and production-quality.
- Follow PEP8.

---

## Task

Create:

backend/app/diagnosis/pod.py

Implement a class named:

PodDiagnoser

Requirements:

1. Accept the following through the constructor:

   - List[PodEvidence]
   - List[EventEvidence]

2. Implement a public method:

   diagnose() -> List[DiagnosisResult]

3. For every PodEvidence:

   Detect the following conditions:

   - ImagePullBackOff
   - ErrImagePull
   - CrashLoopBackOff

4. Use EventEvidence to strengthen the diagnosis whenever matching events
   exist for the same Pod.

5. Populate DiagnosisResult with:

   - resource_type
   - resource_name
   - namespace
   - diagnosis
   - severity
   - confidence
   - evidence
   - recommendation

6. Confidence values:

   - 0.95 when both Pod status and Events agree
   - 0.80 when only Pod status indicates the issue
   - 0.70 when only Events indicate the issue

7. Ignore healthy Pods.

8. Never print anything.

9. Keep helper methods private.

10. Add docstrings and type hints.

---

## Outcome

The diagnosis layer can now detect common Pod failures using collected
evidence and return structured DiagnosisResult objects.
