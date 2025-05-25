from app.services.results_service import ResultsService 

class ResultsController:
    def __init__(self):
        self.results_service = ResultsService()

    def save_results(self, user_id: int, member_id: int, results: float):
        try:
            self.results_service.saveResults(userId=user_id, memberId=member_id, results=results)
            return {"status": "success", "message": "Results saved successfully."}
        except ValueError as e:
            return {"status": "error", "message": str(e)}
