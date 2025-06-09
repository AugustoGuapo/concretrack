from app.models.user import User

class SessionState:
    _current_user = None

    @classmethod
    def set_user(cls, user):
        cls._current_user = user

    @classmethod
    def get_user(cls)-> User:
        if cls._current_user is None:
            raise ValueError("No user has been set.")
        return cls._current_user

    @classmethod
    def clear_user(cls):
        cls._current_user = None