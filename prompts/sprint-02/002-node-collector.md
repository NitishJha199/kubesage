# Sprint 2 - Node Collector

## Goal

Implement the Node Collector for KubeSage.

You are working on the KubeSage project.

Architecture requirements:

- The collector layer is the only layer allowed to communicate with Kubernetes.
- Never return Kubernetes SDK objects.
- Convert everything into Pydantic models.
- Use dependency injection.
- Use type hints everywhere.
- Keep the code clean, modular and production quality.

Task:

Create the files:

backend/app/models/node.py

backend/app/collector/nodes.py

Requirements:

1. Create a Pydantic model named NodeEvidence.

2. Include at least the following fields:

- name
- roles
- kubelet_version
- os_image
- kernel_version
- container_runtime
- internal_ip
- external_ip
- cpu_capacity
- memory_capacity
- pod_capacity
- ready_status

3. Create a class named NodeCollector.

4. Accept KubernetesClient through the constructor.

5. Query every node from the cluster.

6. Convert every Kubernetes node into NodeEvidence.

7. Return List[NodeEvidence].

8. Never expose Kubernetes SDK objects outside the collector.

9. Add docstrings.

10. Follow PEP8.

Do not implement any diagnosis logic.
Do not calculate health.
Do not calculate confidence.
Only collect and normalize node information.

## Actual Outcome

- NodeEvidence model created
- NodeCollector implemented
- Successfully tested against local Kind cluster
- Returns List[NodeEvidence]
- Reviewed and approved

