from config.input_verifiers.input_verifier import InputVerifier


class NoCheckInputVerifier(InputVerifier):
    def verify_input(self, input: str) -> str | None:
        return None

    def format_input(self, input: str) -> str:
        return input
