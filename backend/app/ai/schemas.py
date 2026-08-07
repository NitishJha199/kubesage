from pydantic import BaseModel

class AIExplanation(BaseModel):
    summary: str

    root_cause: str

    impact: str

    verification_steps: list[str]

    kubectl_commands: list[str]

    prevention: str
