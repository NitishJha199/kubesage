from pydantic import BaseModel

from app.ai.schemas import AIExplanation


class BatchAIResponse(BaseModel):
    explanations: list[AIExplanation]
