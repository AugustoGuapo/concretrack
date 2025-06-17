from app.models.user_role import UserRole


class User:

    def __init__(self, id: int, username: str, firstName: str,
                 lastName: str, passwordHash: str, role: UserRole, fingerprintId: int):
        self.username = username
        self.firstName = firstName
        self.lastName = lastName
        self.passwordHash = passwordHash
        self.role = role
        self.fingerprintId = fingerprintId

    def __repr__(self):
        return f"""User(username={self.username},
        firstName={self.firstName},
        lastName={self.lastName},
        passwordHash={self.passwordHash},
        role={self.role})"""
    
    def getFullName(self) -> str:
        return f"{self.firstName} {self.lastName}"
