from datetime import datetime
from app.storage import db_connection as db
from app.models.member import Member
class MemberRepository:
    def __init__(self):
        self.db_connection = db.create_connection()
        

    def getMemberById(self, memberId: int):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id, family_id, date_of_fracture, result, operative, fracture_days FROM members WHERE id = ?", (memberId,))
        row = cursor.fetchone()
        if row:
             return Member(
                id=row[0],
                family_id=row[1],
                date_of_fracture=datetime.strptime(row[2][0:10], "%Y-%m-%d"),
                result=row[3],
                operative=row[4],
                fracture_days=row[5])
        
        return None
    
    def insertMember(self, member: Member):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO members (family_id, date_of_fracture, result, operative) VALUES (?, ?, ?, ?)",
                       (member.family_id, member.date_of_fracture.strftime("%Y-%m-%d"), member.result, member.operative))
        self.db_connection.commit()

    def insertResult(self, member: Member, fracture_type: str):
        cursor = self.db_connection.cursor()
        cursor.execute("UPDATE members SET result = ?, operative = ?, fractured_at = DATE('now', 'localtime'), fracture_type = ? WHERE id = ?",
                       (member.result, member.operative, fracture_type, member.id))
        self.db_connection.commit()

    def getMembersForTheDay(self) -> list[Member]:
        """Fetches all members whose fracture date is between 01/01/1970 and today."""
        cursor = self.db_connection.cursor()
        cursor.execute(
            "SELECT id, family_id, date_of_Fracture, result, operative, fracture_days FROM members WHERE (date_of_fracture BETWEEN '1970-01-01' AND DATE('now', 'localtime') and (result is null or result = \"\")) OR (result is not null and result != \"\") AND is_reported is null;"
        )
        rows = cursor.fetchall()
        members = []
        for row in rows:
            members.append(Member(
                id=row[0],
                family_id=row[1],
                date_of_fracture=datetime.strptime(row[2][0:10], "%Y-%m-%d"),
                result=row[3],
                operative=row[4],
                fracture_days=row[5]
            ))
        return members
    
    def signWork(self):
        cursor = self.db_connection.cursor()
        cursor.execute(
            "UPDATE members SET is_reported = 1 WHERE result IS NOT NULL AND is_reported IS NULL;"
        )
        self.db_connection.commit()

    
    
