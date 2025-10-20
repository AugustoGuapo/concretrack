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

    # Autenticación normal (usuario y contraseña)
    def authenticateUserCredentials(self, username, password) -> User:
        fetchedUser = self.usersRepositoryInterface.getUserByUsername(username)

        if not fetchedUser:
            logging.error(f"User {username} not found.")
            return None

        if self.passwordHasherInterface.verify(password, fetchedUser.passwordHash):
            return fetchedUser
        return None

    # Autenticación por huella dactilar
    def authenticateUserByFingerprintId(self, fingerprintId) -> User:
        fetchedUser = self.usersRepositoryInterface.getUserByFingerprintId(fingerprintId)

        if not fetchedUser:
            logging.error(f"User with fingerprint ID {fingerprintId} not found.")
            return None

        return fetchedUser

    # Registrar un nuevo usuario (con o sin huella)
    def registerUser(self, firstName, lastName, password, role, fingerprintId=None) -> bool:
        username = self.generateUsername(firstName, lastName)

        # Verificar si el nombre de usuario ya existe
        if self.usersRepositoryInterface.getUserByUsername(username):
            logging.error(f"Username {username} already exists.")
            return False

        hashedPassword = self.passwordHasherInterface.hash(password)

        # Convertir role a UserRole si viene como string
        if isinstance(role, str):
            try:
                role_enum = UserRole[role.upper()]
            except KeyError:
                logging.error(f"Invalid role '{role}' provided.")
                return False
        else:
            role_enum = role

        # Crear el objeto User
        user = User(
            id=None,
            username=username,
            firstName=firstName,
            lastName=lastName,
            passwordHash=hashedPassword,
            role=role_enum,
            fingerprintId=fingerprintId
        )

        # Insertar en la base de datos
        self.usersRepositoryInterface.insertUser(user)
        return True

    # Generar nombre de usuario único automáticamente
    def generateUsername(self, firstName: str, lastName: str) -> str:
        username = f"{firstName.lower()}.{lastName.lower()}.{random.randint(100, 999)}"

        if self.usersRepositoryInterface.existsUsername(username):
            logging.warning(f"Username {username} already exists. Regenerating...")
            return self.generateUsername(firstName, lastName)

        return username


# Ejemplo de prueba directa
if __name__ == "__main__":
    service = AuthenticationService(UserRepositoryImpl(), BcryptHasherImpl())
    service.registerUser("Augusto", "Diaz", "12345678", UserRole.ADMIN)
    service.registerUser("Oscar", "Padilla", "12345678", UserRole.OPERATIVE)
