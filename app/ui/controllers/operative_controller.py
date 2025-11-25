import logging
from app.hardware.fingerprint_sensor import FingerprintSensor
from app.services.implementations.family_repository import FamilyRepository
from app.services.samples_service import SamplesService
from app.services.implementations.member_repository import MemberRepository
from app.models.member import Member
from app.state.session_state import SessionState

class OperativeController:
    def __init__(self):
        self.samples_service = SamplesService(MemberRepository(), FamilyRepository())
        self.fingerprintSensor = None #FingerprintSensor()

    def get_samples(self) -> list[Member]:
        """Fetches the list of samples from the service."""
        return self.samples_service.get_samples()
    
    def getFamilyNameById(self, familyId: int) -> str:
        return self.samples_service.getFamilyNameById(familyId)
    
    def sign_work(self) -> bool:
        """Signs the work for the current user."""
        
        user = SessionState.get_user()
        if not user:
            logging.error("No user is currently logged in.")
            return False
        working_user = self.fingerprintSensor.check_fingerprint()
        print(f'El usuario que intenta cerrar sesión tiene la huella #{working_user}')
        if working_user == -1:
            return False
        if working_user == user.fingerprintId:
            self.samples_service.sign_work()
            logging.info(f"User {user.username} signed work successfully.")
            return True
        return False