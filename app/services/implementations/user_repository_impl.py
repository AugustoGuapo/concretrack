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
                username=row[1],
                firstName=row[2],
                lastName=row[3],
                passwordHash=row[4],
                role=UserRole(row[5])
            )
        return None

    def insertUser(self, user: User):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO users (username, firstName, lastName," +
                       "passwordHash, role) VALUES (?, ?, ?, ?, ?)",
                       (user.username, user.firstName, user.lastName,
                        user.passwordHash, user.role.value))
        self.db_connection.commit()

    def existsUsername(self, username: str) -> bool:
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        return row is not None
