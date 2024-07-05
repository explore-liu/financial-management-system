import pymysql
import os
import pandas as pd
from instructions import Instructions


class Employee(Instructions):
    def __init__(self, db, s_no):
        super().__init__(db)
        self.role_no = 1
        self.s_no = s_no

    def submit_statement(self, s_no, file_path):
        if not os.path.exists(file_path):
            return -1  # 文件名不存在

        df = pd.read_csv(file_path)
        if df.empty:
            return 0  # 表为空

        for index, row in df.iterrows():
            row_dict = row.to_dict()
            data = (row_dict['项目号'], row_dict['开销名'], row_dict['金额'], row_dict['日期'], s_no)
            submit_sql = 'INSERT INTO %s VALUES %s' % ('statement', data)
            self.execute(submit_sql)

        return 1
