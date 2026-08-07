from app.ai.batch import BatchAIResponse
from app.ai.ollama_provider import OllamaProvider
from app.diagnosis.result import DiagnosisResult


class AIExplanationService:
    """
    Generates AI explanations using a single Ollama request.
    """

    def __init__(self) -> None:
        self.provider = OllamaProvider()

    def explain_batch(
        self,
        diagnoses: list[DiagnosisResult],
    ) -> BatchAIResponse:

        return self.provider.explain_batch(diagnoses)
