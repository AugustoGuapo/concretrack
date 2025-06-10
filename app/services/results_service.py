from app.services.implementations.member_repository import MemberRepository
from app.models.member import Member
class ResultsService:
    def __init__(self):
        self.member_repository = MemberRepository()  # This should be set to an instance of MemberRepository
    def saveResults(self, userId: int, memberId: int, results: float, type_frac: int):
        member = self.member_repository.getMemberById(memberId)
        if not member:
            raise ValueError(f"Member with ID {memberId} not found.")
        
        member.result = results
        member.operative = userId
        member.type = type_frac

        self.member_repository.insertResult(member)

