from app.storage import db_connection as db


class FamilyRepository:
    def __init__(self):
        self.db_connection = db.create_connection()

    def getFamilyNameById(self, familyId: int) -> str:
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT sample_place FROM families WHERE id = ?", (familyId,))
        row = cursor.fetchone()
        if row:
            return row[0]
        return ""
