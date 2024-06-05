from pathlib import Path

from config.input_verifiers.input_verifier import InputVerifier

class Field:
    def __init__(self, key: str, prompt: str, verifier: InputVerifier):
        self.key = key
        self.prompt = prompt
        self.verifier = verifier
