from app.services.authentication_service import AuthenticationService
from app.services.implementations.user_repository_impl import UserRepositoryImpl
from app.services.implementations.bcrypt_hasher_impl import BcryptHasherImpl
from app.services.implementations.fingerprint_impl import FingerprintImpl
from app.core.exceptions.fingerprint_exceptions import SensorStorageException


class AdminController:
    def __init__(self):
        self.auth_service = AuthenticationService(UserRepositoryImpl(), BcryptHasherImpl())
        self.fingerprint_service = None#FingerprintImpl()

    def create_user(self, firstName, lastName, password, role, fingerprintId):
        return self.auth_service.registerUser(
            firstName=firstName,
            lastName=lastName,
            password=password,
            role=role,
            fingerprintId=fingerprintId)
    
    def capture_fingerprint(self):
        if not self.fingerprint_service.capture_fingerprint():
            raise Exception("Fingerprint sensor not available.")
        
    def store_fingerprint(self):
        id = self.fingerprint_service.match_and_store()
        if id:
            return id
    def delete_user(self, username):
        user = self.auth_service.usersRepositoryInterface.getUserByUsername(username)
        if not user:
            raise Exception(f"User {username} does not exist.")
        
        self.auth_service.usersRepositoryInterface.deleteUser(user.id)
        return True

    