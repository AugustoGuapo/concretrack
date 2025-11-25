from app.services.implementations.family_repository import FamilyRepository
from app.services.implementations.member_repository import MemberRepository
from app.models.member import Member
class ResultsService:
    def __init__(self):
        self.member_repository = MemberRepository()  # This should be set to an instance of MemberRepository
        self.family_repository = FamilyRepository()  # Instance of FamilyRepository
    def saveResults(self, userId: int, memberId: int, results: float, fracture_type: str):
        member = self.member_repository.getMemberById(memberId)
        if not member:
            raise ValueError(f"Member with ID {memberId} not found.")
        
        member.result = results
        member.operative = userId

        self.member_repository.insertResult(member, fracture_type)
    def getFamilyNameById(self, familyId: int) -> str:
        return self.family_repository.getFamilyNameById(familyId)

