import pymysql

from instructions import Instructions


class Admin(Instructions):
    def __init__(self, db, s_no):
        super().__init__(db)
        self.role_no = 3
        self.s_no = s_no

    # 获取用户信息（管理员）
    def get_user_info_admin_view(self):
        view_name = 'user_info_admin_view'
        # info = '用户信息'
        result = self.show_view(view_name)
        for i in range(len(result)):
            result[i][2] = str(result[i][2])
        return result

    # 重置密码
    def reset_password(self, s_no):
        data = ['s_no', 'user', 'u_password']
        user_sql = 'select %s from %s where %s=\'%s\'' % (data[0], data[1], data[0], s_no)  # 查询用户是否存在
        result = self.get_list(user_sql)
        if not result:
            # print('用户不存在，请重新输入工号：')
            return 0

        defult_password = '123456'
        reset_sql = 'UPDATE %s SET %s=%s WHERE %s LIKE \'%s\'' % (data[1], data[2], defult_password, data[0], s_no)
        # info = '重置完毕。'
        self.execute(reset_sql)
        return 1

    # 注销账户
    def close_account(self, s_no):
        data = ['s_no', 'user']
        user_sql = 'select %s from %s where %s=\'%s\'' % (data[0], data[1], data[0], s_no)  # 查询用户是否存在
        result = self.get_list(user_sql)
        if not result:
            # print('用户不存在，请重新输入工号。')
            return 0

        if s_no == self.s_no:
            # print('不可删除本账户。')
            return -1

        delete_sql = 'DELETE FROM %s where %s=\'%s\'' % (data[1], data[0], s_no)
        # info = '删除完毕。'
        self.execute(delete_sql)
        return 1

    # 更改身份
    def change_role(self, s_no, r_no):
        data = ['s_no', 'user', 'r_no']
        user_sql = 'select %s from %s where %s=\'%s\'' % (data[0], data[1], data[0], s_no)  # 查询用户是否存在
        result = self.get_list(user_sql)
        if not result:
            # print('用户不存在，请重新输入工号。')
            return 0

        if s_no == self.s_no:
            # print('不可更改本账户的身份。')
            return -1

        role_list = ['1', '2', '3']
        if r_no not in role_list:
            # print('身份编号不在给定范围内。')
            return -2

        update_sql = 'UPDATE %s SET %s=%s WHERE %s LIKE \'%s\'' % (data[1], data[2], r_no, data[0], s_no)
        # info = '更改完毕。'
        self.execute(update_sql)
        return 1
