from app.services.authentication_service import AuthenticationService
from app.services.implementations.user_repository_impl import UserRepositoryImpl
from app.services.implementations.bcrypt_hasher_impl import BcryptHasherImpl

class LoginController:
    def __init__(self):
        self.auth_service = AuthenticationService(UserRepositoryImpl(), BcryptHasherImpl())


        
    def login(self, username: str, password: str):
        return self.auth_service.authenticateUser(
            username=username,
            password=password
        )