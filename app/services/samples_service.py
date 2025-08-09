from app.services.implementations.member_repository import MemberRepository
from app.models.member import Member

class SamplesService:
    def __init__(self, members_repository: MemberRepository):
        self.members_repository = members_repository

    def get_samples(self) -> list[Member]:
        """Fetches the list of samples from the repository for today's work."""
        return self.members_repository.getMembersForTheDay()
    
    def sign_work(self, user_id: int) -> bool:
        """Signs the work for the specified user."""
        return self.members_repository.signWork(user_id)