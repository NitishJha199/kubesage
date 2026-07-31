from pydantic import BaseModel, Field


class Knowledge(BaseModel):
    """
    Represents structured knowledge about a Kubernetes issue.
    """

    issue: str = Field(..., description="Unique issue name.")
    severity: str = Field(..., description="Severity level.")
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Default confidence score."
    )
    description: str = Field(
        ...,
        description="Explanation of the issue."
    )
    recommendation: str = Field(
        ...,
        description="Recommended remediation."
    )
