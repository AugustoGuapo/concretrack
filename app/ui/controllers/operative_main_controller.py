from app.models.user import User

class OperativeMainController:
    def __init__(self, user: User):
        self.user = user

    def load_samples(self):