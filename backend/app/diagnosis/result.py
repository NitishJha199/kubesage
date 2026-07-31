from typing import List, Optional
from pydantic import BaseModel, Field


class DiagnosisResult(BaseModel):
    """
    Represents the output of the KubeSage diagnosis engine after evaluating 
    cluster evidence against predefined rules or models.
    """

    resource_type: str = Field(
        ...,
        description="Kind/type of the target resource analyzed (e.g., Pod, Node, Deployment)."
    )
    resource_name: str = Field(
        ...,
        description="Name of the resource being diagnosed."
    )
    namespace: Optional[str] = Field(
        default=None,
        description="Namespace of the resource, or None if cluster-scoped (e.g., Node)."
    )
    diagnosis: str = Field(
        ...,
        description="Concise summary or classification of the identified issue or status."
    )
    severity: str = Field(
        ...,
        description="Severity level of the diagnosis (e.g., CRITICAL, WARNING, INFO)."
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score of the diagnosis ranging from 0.0 to 1.0."
    )
    evidence: List[str] = Field(
        default_factory=list,
        description="List of raw or formatted supporting evidence strings used to reach this diagnosis."
    )
    recommendation: str = Field(
        ...,
        description="Actionable guidance or steps to resolve or mitigate the diagnosed issue."
    )
