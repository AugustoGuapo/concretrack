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
                passwordHash=row[5],
                fingerprintId=row[6]
            )
        return None

    def insertUser(self, user: User):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO users (username, first_name, last_name," +
                       "password, role, fingerprint_id) VALUES (?, ?, ?, ?, ?, ?)",
                       (user.username, user.firstName, user.lastName,
                        user.passwordHash, user.role.value, user.fingerprintId))
        self.db_connection.commit()

    def existsUsername(self, username: str) -> bool:
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        return row is not None
    
    def getUserByFingerprintId(self, fingerprintId) -> User:
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM users WHERE fingerprint_id = ?", (fingerprintId,))
        row = cursor.fetchone()
        if row:
            return User(
                id=row[0],
                firstName=row[1],
                lastName=row[2],
                role=UserRole(row[3]),
                username=row[4],
                passwordHash=row[5],
                fingerprintId=int(row[6])
            )
        return None
    
    def getAllActiveUsers(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id, first_name, last_name, role FROM users WHERE is_active = 1")
        rows = cursor.fetchall()
        usuarios = []
        for row in rows:
            usuarios.append({
                "id": row[0],
                "nombre": f"{row[1]} {row[2]}",
                "rol": row[3]
            })
        return usuarios

    def updateUser(self, user_id, first_name, last_name, role, password_hash=None):
        cursor = self.db_connection.cursor()

        if password_hash:
            query = "UPDATE users SET first_name=?, last_name=?, role=?, password=? WHERE id=?"
            params = (first_name, last_name, role, password_hash, user_id)
        else:
            query = "UPDATE users SET first_name=?, last_name=?, role=? WHERE id=?"
            params = (first_name, last_name, role, user_id)

        cursor.execute(query, params)
        self.db_connection.commit()
    


    def logicalDeleteUser(self, user_id):
        cursor = self.db_connection.cursor()
        cursor.execute("UPDATE users SET is_active = 0 WHERE id = ?", (user_id,))
        self.db_connection.commit()

