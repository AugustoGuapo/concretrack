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
                id=row[0],
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
        cursor.execute(
            "INSERT INTO users (first_name, last_name, role, username, password, fingerprint_id, is_active) VALUES (?, ?, ?, ?, ?, ?, 1)",
            (user.firstName, user.lastName, user.role.value, user.username, user.passwordHash, user.fingerprintId)
        )
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
        cursor.execute("SELECT id, first_name, last_name, role, username FROM users WHERE is_active = 1")
        rows = cursor.fetchall()
        usuarios = []
        for row in rows:
            usuarios.append({
                "id": row[0],
                "nombre": f"{row[1]} {row[2]}",
                "rol": row[3],
                "username": row[4]
            })
        return usuarios

    def updateUser(self, user_id, first_name, last_name, role, username=None, password_hash=None):
        """
        Actualiza el usuario.
        - role puede ser UserRole o string; aquí lo convertimos a string (role_value).
        - Si username es None, no lo actualizamos.
        - Si password_hash es None, no actualizamos la contraseña.
        """
        cursor = self.db_connection.cursor()

        # Normalizar role a string almacenable
        if hasattr(role, "value"):
            role_value = role.value
        else:
            role_value = role

        # Construir query dinámicamente según lo que venga
        set_parts = ["first_name = ?", "last_name = ?", "role = ?"]
        params = [first_name, last_name, role_value]

        if username is not None:
            set_parts.append("username = ?")
            params.append(username)

        if password_hash is not None:
            set_parts.append("password = ?")  # tu columna en la DB parece llamarse 'password'
            params.append(password_hash)

        set_clause = ", ".join(set_parts)
        query = f"UPDATE users SET {set_clause} WHERE id = ?"
        params.append(user_id)

        cursor.execute(query, tuple(params))
        self.db_connection.commit()



    def logicalDeleteUser(self, user_id):
        cursor = self.db_connection.cursor()
        cursor.execute("UPDATE users SET is_active = 0 WHERE id = ?", (user_id,))
        self.db_connection.commit()
