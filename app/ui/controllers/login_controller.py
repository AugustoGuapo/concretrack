from app.services.authentication_service import AuthenticationService
from app.services.implementations.user_repository_impl import UserRepositoryImpl
from app.services.implementations.bcrypt_hasher_impl import BcryptHasherImpl
from app.state.session_state import SessionState
from app.hardware.fingerprint_sensor import FingerprintSensor


class LoginController:
    def __init__(self):
        self.auth_service = AuthenticationService(
            UserRepositoryImpl(), BcryptHasherImpl()
        )
        # Instanciamos el sensor real (solo debe usarse en device)
        self.fingerprintSensor = FingerprintSensor()

    def login(self, username: str, password: str):
        user = self.auth_service.authenticateUserCredentials(
            username=username, password=password
        )
        if user:
            SessionState.set_user(user)
            print(f"User {user.username} logged in successfully.")
            return True
        return False

    def fingerPrintLogin(self):
        """
        Intenta autenticar por huella. Devuelve True si éxito.
        """
        try:
            fingerprintId = self.fingerprintSensor.check_fingerprint()
            if fingerprintId == -1:
                return False

            user = self.auth_service.authenticateUserByFingerprintId(fingerprintId)
            if user:
                SessionState.set_user(user)
                return True
            return False
        except Exception as e:
            print(f"Error en autenticación biométrica: {e}")
            return False