from abc import ABC, abstractmethod


class InputVerifier(ABC):
    @abstractmethod
    def verify_input(self, input: str) -> str | None:
        pass

    @abstractmethod
    def format_input(self, input: str) -> str:
        pass
