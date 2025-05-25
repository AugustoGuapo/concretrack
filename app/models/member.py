
import datetime

class Member:

    def __init__(self, id: int, family_id: int, date_of_fracture: datetime, result: float, operative: int):
        self.id = id
        self.family_id = family_id
        self.date_of_fracture = date_of_fracture
        self.result = result
        self.operative = operative