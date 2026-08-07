We are implementing the Deployment Diagnoser for Kubesage.

Project rules:

- Python 3.11
- Pydantic models
- Clean Architecture
- SOLID
- No Kubernetes API calls inside diagnosers
- Diagnosers only consume normalized evidence
- Small methods
- Strong typing
- Google-style docstrings

Current architecture:

DeploymentCollector
        ↓
DeploymentEvidence
        ↓
DeploymentDiagnoser
        ↓
DiagnosisResult

Implement:

app/diagnosis/deployment.py

Requirements:

Create a DeploymentDiagnoser class.

Constructor:

DeploymentDiagnoser(
    deployments: List[DeploymentEvidence]
)

Public method:

diagnose() -> List[DiagnosisResult]

For every deployment:

If

available_replicas < desired_replicas

produce a DiagnosisResult.

Diagnosis:

DeploymentUnavailable

Severity:

WARNING

Confidence:

0.90

Evidence should include:

Deployment name
Desired replicas
Available replicas
Ready replicas
Unavailable replicas

Recommendation:

Some replicas are unavailable.
Inspect the Pods belonging to this Deployment
to determine the underlying cause.

If deployment is healthy,
return nothing.

The diagnoser must not call Kubernetes APIs.

Use clean helper methods where appropriate.
