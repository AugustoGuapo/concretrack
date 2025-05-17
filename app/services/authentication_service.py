from app.models.user import User
import random
import logging
from app.core.interfaces.users_repository_interface import (
    UsersRepositoryInterface
)
from app.core.interfaces.password_hasher_interface import (
    PasswordHasherInterface
)
from app.services.implementations.user_repository_impl import (
    UserRepositoryImpl
)
from app.services.implementations.bcrypt_hasher_impl import (
    BcryptHasherImpl
)


class AuthenticationService:
    def __init__(self, usersRepositoryInterface: UsersRepositoryInterface,
                 passwordHasherInterface: PasswordHasherInterface):
        self.usersRepositoryInterface = usersRepositoryInterface
        self.passwordHasherInterface = passwordHasherInterface

    def authenticateUser(self, username, password) -> User:
        fetchedUser = self.usersRepositoryInterface.getUserByUsername(username)

        if not fetchedUser:
            logging.error(f"User {username} not found.")
            return None
        if self.passwordHasherInterface.verify(password,
                                                   fetchedUser.passwordHash):
            return fetchedUser
        return None

    def registerUser(self, firstName, lastName, password, role) -> bool:
        username = self.generateUsername(firstName, lastName)
        if self.usersRepositoryInterface.getUserByUsername(username):
            logging.error(f"Username {username} already exists.")
            return False
        hashedPassword = self.passwordHasherInterface.hash(password)
        user = User(username, firstName, lastName, hashedPassword, role)
        self.usersRepositoryInterface.insertUser(user)
        return True

    def generateUsername(self, firstName: str, lastName: int) -> str:
        username = f"{firstName.lower()}.{lastName.lower()}"
        username += f".{random.randint(100, 999)}"
        if self.usersRepositoryInterface.existsUsername(username):
            logging.error(f"Username {username} already exists.")
            return self.generateUsername(firstName, lastName)
        return username

if __name__ == "__main__":
    userRepository = UserRepositoryImpl()
    passwordHasher = BcryptHasherImpl()
    auth_service = AuthenticationService(userRepository, passwordHasher)
    auth_service.registerUser("Guillermo", "Castaño", "password123", "admin")
    auth_service.registerUser("Maryi", "Brieva", "password123", "operative")
