from app.services.authentication_service import AuthenticationService
from app.services.implementations.user_repository_impl import UserRepositoryImpl
from app.services.implementations.bcrypt_hasher_impl import BcryptHasherImpl
from app.state.session_state import SessionState  # <- Nuevo
from app.hardware.fingerprint_sensor import FingerprintSensor


class LoginController:
    def __init__(self):
        self.auth_service = AuthenticationService(
            UserRepositoryImpl(), BcryptHasherImpl()
        )
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
        if self.fingerprintSensor is None:
            return False  # Sensor no disponible → login por huella no posible
        fingerprintId = self.fingerprintSensor.check_fingerprint()
        if fingerprintId == -1:
            return False
        
        user = self.auth_service.authenticateUserByFingerprintId(fingerprintId)
        if user:
            SessionState.set_user(user)
            return True
        return False