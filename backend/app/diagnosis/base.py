from abc import ABC, abstractmethod

from app.diagnosis.result import DiagnosisResult


class Diagnoser(ABC):
    """
    Base interface for every Kubernetes diagnoser.
    """

    @abstractmethod
    def diagnose(self) -> list[DiagnosisResult]:
        """
        Return every diagnosis found by this diagnoser.
        """
        raise NotImplementedError
