from app.storage import db_connection as db
from app.core.interfaces.users_repository_interface import (
    UsersRepositoryInterface
)
from app.models.user import User
from typing import Optional
from app.models.user_role import UserRole


class UserRepositoryImpl(UsersRepositoryInterface):
    def __init__(self):
        self.db_connection = db.create_connection()

    def getUserByUsername(self, username) -> Optional[User]:
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row:
            return User(
                id= row[0],
                firstName=row[1],
                lastName=row[2],
                role=UserRole(row[3]),
                username=row[4],
                passwordHash=row[5]
            )
        return None

    def insertUser(self, user: User):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO users (username, first_name, last_name," +
                       "password, role) VALUES (?, ?, ?, ?, ?)",
                       (user.username, user.firstName, user.lastName,
                        user.passwordHash, user.role.value))
        self.db_connection.commit()

    def existsUsername(self, username: str) -> bool:
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        return row is not None
    
    def getUserByFingerprintId(self, fingerprintId) -> User:
        return User("Augusto", "a", "", "", UserRole.ADMIN)
