from app.models.user import User
from app.models.user_role import UserRole
import random
import logging
from app.core.interfaces.users_repository_interface import UsersRepositoryInterface
from app.core.interfaces.password_hasher_interface import PasswordHasherInterface
from app.services.implementations.user_repository_impl import UserRepositoryImpl
from app.services.implementations.bcrypt_hasher_impl import BcryptHasherImpl


class AuthenticationService:
    def __init__(
        self,
        usersRepositoryInterface: UsersRepositoryInterface,
        passwordHasherInterface: PasswordHasherInterface,
    ):
        self.usersRepositoryInterface = usersRepositoryInterface
        self.passwordHasherInterface = passwordHasherInterface

    def authenticateUserCredentials(self, username, password) -> User:
        fetchedUser = self.usersRepositoryInterface.getUserByUsername(username)

        if not fetchedUser:
            logging.error(f"User {username} not found.")
            return None
        if self.passwordHasherInterface.verify(password, fetchedUser.passwordHash):
            return fetchedUser
        return None

    def authenticateUserByFingerprintId(self, fingerprintId) -> User:
        fetchedUser = self.usersRepositoryInterface.getUserByFingerprintId(
            fingerprintId
        )

        if not fetchedUser:
            logging.error(f"User with fingerprint ID {fingerprintId} not found.")
            return None
        return fetchedUser

    def registerUser(self, firstName, lastName, password, role, fingerprintId) -> bool:
        username = self.generateUsername(firstName, lastName)
        if self.usersRepositoryInterface.getUserByUsername(username):
            logging.error(f"Username {username} already exists.")
            return False
        hashedPassword = self.passwordHasherInterface.hash(password)
        user = User(username, firstName, lastName, hashedPassword, role, fingerprintId)
        self.usersRepositoryInterface.insertUser(user)
        return True

    def generateUsername(self, firstName: str, lastName: str) -> str:
        username = f"{firstName.lower()}.{lastName.lower()}"
        username += f".{random.randint(100, 999)}"
        if self.usersRepositoryInterface.existsUsername(username):
            logging.error(f"Username {username} already exists.")
            return self.generateUsername(firstName, lastName)
        return username
    
if __name__ == "__main__":
    service = AuthenticationService(
        UserRepositoryImpl(), BcryptHasherImpl()
    )
    service.registerUser("Augusto", "Diaz", "12345678", UserRole.ADMIN)
    service.registerUser("Oscar", "Padilla", "12345678", UserRole.OPERATIVE)