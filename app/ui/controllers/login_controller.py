from app.services.authentication_service import AuthenticationService
from app.services.implementations.user_repository_impl import UserRepositoryImpl
from app.services.implementations.bcrypt_hasher_impl import BcryptHasherImpl
from app.state.session_state import SessionState  # <- Nuevo


class LoginController:
    def __init__(self):
        self.auth_service = AuthenticationService(
            UserRepositoryImpl(), BcryptHasherImpl()
        )

    def login(self, username: str, password: str):
        user = self.auth_service.authenticateUserCredentials(
            username=username, password=password
        )

        if user:
            SessionState.set_user(user)  # <- Guardar el usuario en estado global
            return True
        return False
