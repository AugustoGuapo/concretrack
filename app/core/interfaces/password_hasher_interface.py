from typing import Protocol


class PasswordHasherInterface(Protocol):

    def hash(self, password: str) -> str: ...
    def verify(self, password: str, hashed: str) -> bool: ...
