import bcrypt
from app.core.interfaces.password_hasher_interface import (
    PasswordHasherInterface
)


class BcryptHasherImpl(PasswordHasherInterface):
    def hash(self, password: str) -> str:
        hashedPass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashedPass.decode('utf-8')

    def verify(self, password: str, hash: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))
