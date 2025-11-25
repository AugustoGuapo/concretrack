from app.services.implementations.family_repository import FamilyRepository
from app.services.implementations.member_repository import MemberRepository
from app.models.member import Member

class SamplesService:
    def __init__(self, members_repository: MemberRepository, family_repository: FamilyRepository):
        self.members_repository = members_repository
        self.family_repository = family_repository

    def get_samples(self) -> list[Member]:
        """Fetches the list of samples from the repository for today's work."""
        return self.members_repository.getMembersForTheDay()
    
    def sign_work(self) -> bool:
        """Signs the work for the specified user."""
        return self.members_repository.signWork()
    
    def getFamilyNameById(self, familyId: int) -> str:
        return self.family_repository.getFamilyNameById(familyId)