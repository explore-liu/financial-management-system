import pymysql

from instructions import Instructions


class Employee(Instructions):
    def __init__(self, db, s_no):
        super().__init__(db)
        self.role_no = 1
        self.s_no = s_no
