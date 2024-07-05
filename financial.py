import pymysql
import time
from instructions import Instructions


class Financial(Instructions):
    def __init__(self, db, s_no):
        super().__init__(db)
        self.role_no = 2
        self.s_no = s_no

    # 获取所有员工的薪资
    def get_staff_scale_view(self):
        view_name = 'staff_latest_scale_view'
        # info = '员工薪资'
        result = self.show_view(view_name)
        for i in range(len(result)):
            result[i][3] = str(result[i][3])
            result[i][4] = str(result[i][4])
            result[i][5] = str(result[i][5])
        return result

    # 更改薪资等级
    def change_scale_no(self, s_no, scale):
        sql = 'select * from staff where %s=\'%s\'' % ('s_no', s_no)
        result = self.get_list(sql)
        if not result:
            # print('该工号不存在，请联系管理员。')
            return 0

        f_time1 = time.strftime("%Y-%m-%d", time.localtime())
        sql = 'insert into staff_scale values (\'%s\', %s, \'%s\')' % (s_no, scale, f_time1)
        # info = '更改完毕。'
        self.execute(sql)
        return 1

    # 查看报表
    def view_statement(self):
        sql = 'select * from statement'
        result = self.query(sql)
        for i in range(len(result)):
            result[i][2] = str(result[i][2])
            result[i][3] = str(result[i][3])
        return result

    # 审批报表
    def delete_statement(self, st_no):
        delete_sql = 'delete from statement where %s=\'%s\'' % ('st_no', st_no)
        self.execute(delete_sql)
