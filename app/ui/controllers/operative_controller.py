from app.services.samples_service import SamplesService
from app.services.implementations.member_repository import MemberRepository
from app.models.member import Member

class OperativeController:
    def __init__(self):
        self.samples_service = SamplesService(MemberRepository())

    def get_samples(self) -> list[Member]:
        """Fetches the list of samples from the service."""
        return self.samples_service.get_samples()