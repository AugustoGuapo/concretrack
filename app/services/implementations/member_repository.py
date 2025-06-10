from datetime import datetime
from app.storage import db_connection as db
from app.models.member import Member
class MemberRepository:
    def __init__(self):
        self.db_connection = db.create_connection()
        

    def getMemberById(self, memberId: int):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM members WHERE id = ?", (memberId,))
        row = cursor.fetchone()
        if row:
             return Member(
                id=row[0],
                family_id=row[1],
                date_of_fracture=datetime.strptime(row[2], "%Y-%m-%d"),
                type_frac=row[3],
                result=row[4],
                operative=row[5])
        
        return None
    
    def insertMember(self, member: Member):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO members (family_id, date_of_fracture, result, operative) VALUES (?, ?, ?, ?)",
                       (member.family_id, member.date_of_fracture.strftime("%Y-%m-%d"), member.result, member.operative))
        self.db_connection.commit()

    def insertResult(self, member: Member):
        cursor = self.db_connection.cursor()
        cursor.execute("UPDATE members SET result = ?, operative = ? WHERE id = ?",
                       ( member.result, member.operative, member.id))
        self.db_connection.commit()
    
    
