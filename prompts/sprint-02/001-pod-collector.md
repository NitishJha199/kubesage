
# Sprint 2 - Pod Collector

## Goal

Implement the Pod Collector for KubeSage.

## Cursor Prompt

You are working on the KubeSage project.

Architecture requirements:

- The collector layer is the only layer allowed to communicate with Kubernetes.
- Never return Kubernetes client SDK objects.
- Convert everything into Pydantic models.
- Use type hints everywhere.
- Keep the code modular and production-quality.

Task:

Create backend/app/collector/pods.py.

Requirements:

1. Create a class named PodCollector.
2. Accept a KubernetesClient instance through the constructor (dependency injection).
3. Query every pod from every namespace.
4. Convert every pod into PodEvidence.
5. Convert every container status into ContainerState.
6. Detect:
   - Running
   - Waiting
   - Terminated
7. Populate:
   - namespace
   - pod name
   - node
   - phase
   - pod IP
   - owner reference
   - restart count
   - waiting reason
8. Return List[PodEvidence].
9. Never print anything.
10. No diagnosis logic.
11. Add docstrings and type hints.
12. Follow PEP8.

## Outcome

- PodCollector implemented
- Uses KubernetesClient
- Returns normalized PodEvidence objects
