import pandas as pd
import pymysql
import hashlib

class Instructions:
    def __init__(self, db):
        self.db = db
        self.cursor = db.cursor()
        view_list_sql = 'show table status where comment=\'view\';'
        self.view_list = self.get_list(view_list_sql)
        table_list_sql = 'show full tables where Table_type = \'BASE TABLE\';'
        self.table_list = self.get_list(table_list_sql)

    # 获取列表
    def get_list(self, sql):
        list = []
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            for i, row in enumerate(result):
                list.append(row[0])
        except pymysql.Error as e:
            print('Wrong ' + str(e.args[0]) + ':')
            print(e.args[1])

        return list

    # 执行增、删、改操作
    def execute(self, sql, info=None):
        try:
            rows = self.cursor.execute(sql)
            if rows == 0:
                print('未更改任何数据。\n')
                return
            else:
                self.db.commit()
                if info:
                    print(info)
        except pymysql.Error as e:
            print('Wrong ' + str(e.args[0]) + ':')
            print(e.args[1])
            self.db.rollback()
        return

    # 查询操作
    def query(self, sql, info=None):
        try:
            self.cursor.execute(sql)
            headers = [i[0] for i in self.cursor.description]
            result = pd.DataFrame(self.cursor.fetchall(), columns=headers)
            if info:
                print(info)
            # print(result)
            result = result.values.tolist()
            return result
        except pymysql.Error as e:
            print('Wrong ' + str(e.args[0]) + ':')
            print(e.args[1])
            return None

    # 注册
    def signup(self, staff_no, user_name, user_password, confirmed_pwd, user_email, user_phone):
        if not self.table_list:
            return -1

        data = ['staff', 's_no', 'user', 'u_name', 'u_password', 'u_email', 'u_phoneNumber']

        no_sql = 'select * from %s where %s=\'%s\'' % (data[0], data[1], staff_no)  # 查询工号是否存在
        result = self.get_list(no_sql)
        if not result:
            # print('该工号不存在，请联系管理员。')
            return 1

        user_sql = 'select * from %s where %s=\'%s\'' % (data[2], data[1], staff_no)  # 查询用户是否存在
        result = self.get_list(user_sql)
        if result:
            # print('该用户已存在，请直接登录。')
            return 2

        name_sql = 'select * from %s where %s=\'%s\'' % (data[2], data[3], user_name)  # 查询用户名是否存在
        result = self.get_list(name_sql)
        if result:
            # print('该用户名已存在，请重新设置您的用户名。')
            return 3

        if user_password != confirmed_pwd:
            # print('密码不相符。')
            return 4

        user_password = self.encrypt(user_password)  # 加密

        attribute = '(%s, %s, %s, %s, %s)' % (data[3], data[4], data[5], data[6], data[1])
        values = (user_name, user_password, user_email, user_phone, staff_no)
        sql = 'INSERT INTO %s %s VALUES %s' % (data[2], attribute, values)
        self.execute(sql)
        return 0

    # 登录
    def signin(self, user_name, password):
        role_no = 0
        s_no = None

        if not self.table_list:
            return role_no, s_no

        password = self.encrypt(password)  # 加密

        data = ['r_no', 's_no', 'user', 'u_name', 'u_password']
        sql = 'select %s, %s from %s where %s=\'%s\' and %s=\'%s\'' % (
            data[0], data[1], data[2], data[3], user_name, data[4], password)
        result = self.query(sql)
        if result:
            for i, row in enumerate(result):
                role_no = row[0]
                s_no = row[1]

        return role_no, s_no

    # 加密
    def encrypt(self, password):
        sha_signature = hashlib.sha256(password.encode()).hexdigest()
        return sha_signature

    # 查看视图
    def show_view(self, view_name, info=None):
        if not self.view_list:
            return None

        # print('视图列表：', self.view_list)
        if view_name in self.view_list:
            sql = 'select * from %s' % (view_name,)
            result = self.query(sql, info)
            return result

        print('视图名称错误。\n')
        return None

    # 查询薪资
    def query_salary(self, sno):
        sql = 'select scale_no from staff_scale where s_no = %s' % (sno,)
        result = self.get_list(sql)
        result = result[0]
        sql = "select * from scale where scale_no = %s" % (result,)
        result = self.query(sql)
        result = result[0]
        # result[0]为薪资等级，后为工资
        result[1] = int(result[1])
        result.append(result[1]*3)
        result.append(result[1]*12)
        return result

    def personal_information(self, sno):
        sql = 'select * from staff where s_no = %s' % (sno,)
        result = self.query(sql)
        result = result[0]
        information = []
        for i in range(len(result)):
            information.append(result[i])
        sql = 'select * from user where s_no = %s' % (sno,)
        result = self.query(sql)
        result = result[0]
        information.append(result[2])
        information.append(result[3])
        return information

    def password_change(self, sno, password):
        password = self.encrypt(password)  # 加密
        sql = 'update user set u_password = \'%s\' where s_no = %s' % (password, sno)
        self.execute(sql)
        print("修改成功")

