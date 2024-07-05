from LoginUi import *
from User_Interface import *
from Finance_interface import *
from Register import *
from Admin_Interface import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from admin import Admin
from employee import Employee
from financial import Financial


class LoginWindow(QMainWindow):  ##加载界面
    def __init__(self, ins):
        super().__init__()
        self.ins = ins
        self.db = ins.db
        self.ui = Ui_LoginWindow()  ##注意调用的是哪个函数
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)  ##阴影
        self.shadow.setOffset(0, 0)
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QtCore.Qt.black)
        self.ui.frame.setGraphicsEffect(self.shadow)
        self.ui.pushButton_Register.clicked.connect(self.signup)
        self.ui.pushButton_L_sure.clicked.connect(self.signin)
        self.show()

    # 注册
    def signup(self):
        self.win = RegisterWindow(self.ins)
        self.close()

    # 登录
    def signin(self):
        user_name = self.ui.lineEdit_L_account.text()
        password = self.ui.lineEdit_L_password.text()

        role_no, s_no = self.ins.signin(user_name, password)

        if role_no == 1:
            self.win = UserWindow(self.db, s_no)
            self.close()
        elif role_no == 2:
            self.win = FinanceWindow(self.db, s_no)
            self.close()
        elif role_no == 3:
            self.win = AdminWindow(self.db, s_no)
            self.close()
        else:
            self.ui.stackedWidget.setCurrentIndex(1)


class RegisterWindow(QMainWindow):  # 注册界面
    def __init__(self, ins):
        super().__init__()
        self.ins = ins
        self.ui = Ui_RegisterWindow()  ##注意调用的是哪个函数
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.pushButton_R.clicked.connect(self.signup)
        self.ui.pushButton_L.clicked.connect(self.login)
        self.show()

    # 注册
    def signup(self):
        staff_no = self.ui.lineEdit.text()  # 工号
        user_name = self.ui.lineEdit_2.text()  # 用户名
        user_password = self.ui.lineEdit_3.text()  # 密码
        confirmed_pwd = self.ui.lineEdit_4.text()  # 确认密码
        user_email = self.ui.lineEdit_5.text()  # 邮箱
        user_phone = self.ui.lineEdit_6.text()  # 电话
        flag = self.ins.signup(staff_no, user_name, user_password, confirmed_pwd, user_email, user_phone)
        if flag == 1:
            self.ui.stackedWidget.setCurrentIndex(2)  # 工号不存在
        else:
            if not user_name:
                self.ui.stackedWidget.setCurrentIndex(4)  # 用户名不能为空
            if flag == 2:
                self.ui.stackedWidget.setCurrentIndex(5) # 该用户已存在，请直接登录。
            elif flag == 3:
                self.ui.stackedWidget.setCurrentIndex(6)  # 用户名已存在
            elif flag == 4:
                self.ui.stackedWidget.setCurrentIndex(3)  # 密码不相符
            elif flag == 0:
                self.ui.stackedWidget.setCurrentIndex(1)  # 注册成功

    def login(self):
        self.win =LoginWindow(self.ins)
        self.close()


class UserWindow(QMainWindow):  ##普通用户界面
    def __init__(self, db, s_no):
        super().__init__()
        self.s_no = s_no
        self.em = Employee(db, s_no)
        self.ui = Ui_UserWindow()  ##注意调用的是哪个函数
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        salary = self.em.query_salary(s_no)
        information = self.em.personal_information(s_no)

        self.ui.label_25.setText(str(salary[0]))  # 薪资等级
        self.ui.label_26.setText(str(salary[1]))  # 月工资
        self.ui.label_27.setText(str(salary[2]))  # 季度工资
        self.ui.label_50.setText(str(salary[3]))  # 年工资
        self.ui.label_14.setText(str(information[0]))  # 工号
        self.ui.label_16.setText(str(information[1]))  # 姓名
        self.ui.label_18.setText(str(information[2]))  # 性别
        self.ui.label_20.setText(str(information[3]))  # 入职年份
        self.ui.label_22.setText(str(information[4]))  # 邮箱
        self.ui.label_24.setText(str(information[5]))  # 电话
        self.ui.pushButton_Seach.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.pushButton_My.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.pushButton_Edit.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))  ##要进行处理
        self.ui.pushButton_Table.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))
        self.ui.pushButton_4.clicked.connect(self.submit_statement)
        self.ui.pushButton_change_sure.clicked.connect(self.change)
        self.show()

    # 修改密码
    def change(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        change_password = self.ui.lineEdit_change_password.text()
        change_Rpassword = self.ui.lineEdit_Rchange_password.text()
        if change_password == change_Rpassword:
            self.ui.stackedWidget_2.setCurrentIndex(1)
            ##在数据库里操作，修改这个人的密码
            self.em.password_change(self.s_no, change_password)
        else:
            self.ui.stackedWidget_2.setCurrentIndex(2)

    # 提交报表
    def submit_statement(self):
        # 需要在这里加入提交报表的窗口
        ##self.ui.stackedWidget.setCurrentIndex(3)
        # 需要：“请输入文件名”
        file_path = self.ui.lineEdit_file.text()  # 这里应接收用户输入
        flag = self.em.submit_statement(self.s_no, file_path)
        if flag == -1:
            self.ui.stackedWidget_3.setCurrentIndex(1)  # 这里需要弹窗 文件名不存在
        elif flag == 0:
            self.ui.stackedWidget_3.setCurrentIndex(2)  # 这里需要弹窗 表为空



class FinanceWindow(QMainWindow):  ##财务管理界面
    def __init__(self, db, s_no):
        super().__init__()
        self.s_no = s_no
        self.fin = Financial(db, s_no)
        self.ui = Ui_FinanceWindow()  ##注意调用的是哪个函数
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        salary = self.fin.query_salary(s_no)
        information = self.fin.personal_information(s_no)

        self.ui.label_25.setText(str(salary[0]))  # 薪资等级
        self.ui.label_26.setText(str(salary[1]))  # 月工资
        self.ui.label_27.setText(str(salary[2]))  # 季度工资
        self.ui.label_50.setText(str(salary[3]))  # 年工资
        self.ui.label_14.setText(str(information[0]))  # 工号
        self.ui.label_16.setText(str(information[1]))  # 姓名
        self.ui.label_18.setText(str(information[2]))  # 性别
        self.ui.label_20.setText(str(information[3]))  # 入职年份
        self.ui.label_22.setText(str(information[4]))  # 邮箱
        self.ui.label_24.setText(str(information[5]))  # 电话
        self.table1 = self.ui.tableWidget

        # 假设这是数据库中的后端数据，一个表格
        backend_data = self.fin.get_staff_scale_view()##
        # 通过后端数据填充
        self.fill_table_with_data(backend_data)

        self.table2 = self.ui.tableWidget_2##审批报表的表格
        # 假设这是数据库中的后端数据，一个表格
        backend_data = self.fin.view_statement()
        # 通过后端数据填充
        self.fill_table_with_data_2(backend_data)

        self.ui.pushButton_Seach.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.pushButton_My.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.pushButton_Edit.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.pushButton_Find.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))
        self.ui.pushButton_Change.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))
        self.ui.pushButton_Check.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(5))
        self.ui.pushButton_change_sure.clicked.connect(self.change)
        self.ui.pushButton_change_money_sure.clicked.connect(self.change_money)
        self.ui.pushButton_4.clicked.connect(self.delete_statement)

        self.show()

    def change(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        change_password = self.ui.lineEdit_change_password.text()
        change_Rpassword = self.ui.lineEdit_Rchange_password.text()
        if change_password == change_Rpassword:
            self.ui.stackedWidget_2.setCurrentIndex(1)
            ##在数据库里操作，修改这个人的密码
            self.fin.password_change(self.s_no, change_password)
        else:
            self.ui.stackedWidget_2.setCurrentIndex(2)

    def change_money(self):
        s_no = self.ui.lineEdit_num.text()
        scale = self.ui.lineEdit_grade.text()
        # 找工号，正确的话返回check=1
        check = self.fin.change_scale_no(s_no, scale)
        if check == 1:  ##找到了正确的工号，数据库中的操作，或许可以用遍历寻找
            # 数据库中的操作修改相关工号的等级
            self.ui.stackedWidget_3.setCurrentIndex(1)
        else:
            self.ui.stackedWidget_3.setCurrentIndex(2)

    def fill_table_with_data(self, data):
        # 设置表格的行数和列数
        self.table1.setRowCount(len(data))
        self.table1.setColumnCount(len(data[0]))
        # 填充数据到表格中
        for row, row_data in enumerate(data):
            for column, value in enumerate(row_data):
                # 创建一个 QTableWidgetItem 并设置到表格的对应位置
                item = QtWidgets.QTableWidgetItem(value)
                self.table1.setItem(row, column, item)

    # 审批报表
    def delete_statement(self):
        ##result = self.fin.view_statement()
        # 需要显示出表格
        # 需要：“请输入要审批的项目号”
        st_no = self.ui.lineEdit_num_2.text()  # 这里需读入项目号
        self.fin.delete_statement(st_no)

        ##result = self.fin.view_statement()
        self.table3 = self.ui.tableWidget_2
        # 假设这是数据库中的后端数据，一个表格
        backend_data = self.fin.view_statement()
        # 通过后端数据填充
        self.fill_table_with_data_3(backend_data)
        # 需要显示出表格

    def fill_table_with_data_2(self, data):
        # 设置表格的行数和列数
        self.table2.setRowCount(len(data))
        self.table2.setColumnCount(len(data[0]))
        # 填充数据到表格中
        for row, row_data in enumerate(data):
            for column, value in enumerate(row_data):
                # 创建一个 QTableWidgetItem 并设置到表格的对应位置
                item = QtWidgets.QTableWidgetItem(value)
                self.table2.setItem(row, column, item)

    def fill_table_with_data_3(self, data):
        # 设置表格的行数和列数
        self.table3.setRowCount(len(data))
        self.table3.setColumnCount(len(data[0]))
        # 填充数据到表格中
        for row, row_data in enumerate(data):
            for column, value in enumerate(row_data):
                # 创建一个 QTableWidgetItem 并设置到表格的对应位置
                item = QtWidgets.QTableWidgetItem(value)
                self.table3.setItem(row, column, item)


class AdminWindow(QMainWindow):
    def __init__(self, db, s_no):
        super().__init__()
        self.ad = Admin(db, s_no)
        self.ui = Ui_AdminWindow()  ##注意调用的是哪个函数
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # 传表格数据进来
        self.table2 = self.ui.tableWidget_2

        # 重置密码
        backend_data = self.ad.get_user_info_admin_view()

        # 通过后端数据填充
        self.fill_table_with_data_2(backend_data)

        # 注销账户
        self.table1 = self.ui.tableWidget
        # 通过后端数据填充
        self.fill_table_with_data(backend_data)

        # 更改身份
        self.table3 = self.ui.tableWidget_3
        # 通过后端数据填充
        self.fill_table_with_data_3(backend_data)

        self.ui.pushButton_Delete.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.pushButton_Edit.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.pushButton_New_identity.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))  ##要进行处理
        self.ui.pushButton_close.clicked.connect(self.close_account)
        self.ui.pushButton_change_sure.clicked.connect(self.change_sure)
        self.ui.pushButton_identity_sure.clicked.connect(self.new_identity)
        self.show()

    # 注销账户
    def close_account(self):
        self.ui.stackedWidget_3.setCurrentIndex(0)
        backend_data = self.ad.get_user_info_admin_view()
        self.table1 = self.ui.tableWidget
        self.fill_table_with_data(backend_data)

        s_no = self.ui.lineEdit.text()  # 工号
        # 数据库中找工号，找到check=1,or=0
        check = self.ad.close_account(s_no)
        if check == 1:
            # 数据库操作，删除相关数据
            # 重新传入一次表格数据，方法一样这里不再重复
            backend_data = self.ad.get_user_info_admin_view()
            self.table1 = self.ui.tableWidget
            self.fill_table_with_data(backend_data)

            self.ui.stackedWidget_3.setCurrentIndex(2)
        else:
            self.ui.stackedWidget_3.setCurrentIndex(1)

    def fill_table_with_data(self, data):
        # 设置表格的行数和列数
        self.table1.setRowCount(len(data))
        self.table1.setColumnCount(len(data[0]))
        # 填充数据到表格中
        for row, row_data in enumerate(data):
            for column, value in enumerate(row_data):
                # 创建一个 QTableWidgetItem 并设置到表格的对应位置
                item = QtWidgets.QTableWidgetItem(value)
                self.table1.setItem(row, column, item)

    def fill_table_with_data_2(self, data):
        # 设置表格的行数和列数
        self.table2.setRowCount(len(data))
        self.table2.setColumnCount(len(data[0]))
        # 填充数据到表格中
        for row, row_data in enumerate(data):
            for column, value in enumerate(row_data):
                # 创建一个 QTableWidgetItem 并设置到表格的对应位置
                item = QtWidgets.QTableWidgetItem(value)
                self.table2.setItem(row, column, item)

    def fill_table_with_data_3(self, data):
        # 设置表格的行数和列数
        self.table3.setRowCount(len(data))
        self.table3.setColumnCount(len(data[0]))
        # 填充数据到表格中
        for row, row_data in enumerate(data):
            for column, value in enumerate(row_data):
                # 创建一个 QTableWidgetItem 并设置到表格的对应位置
                item = QtWidgets.QTableWidgetItem(value)
                self.table3.setItem(row, column, item)

    # 重置密码
    def change_sure(self):
        self.ui.stackedWidget_2.setCurrentIndex(0)
        backend_data = self.ad.get_user_info_admin_view()
        self.table2 = self.ui.tableWidget_2
        self.fill_table_with_data_2(backend_data)

        s_no = self.ui.lineEdit_num.text()  # 工号
        check = self.ad.reset_password(s_no)
        if check == 1:
            self.ui.stackedWidget_2.setCurrentIndex(3)
        else:
            self.ui.stackedWidget_2.setCurrentIndex(1)

    # 更改身份
    def new_identity(self):
        self.ui.stackedWidget_4.setCurrentIndex(0)
        backend_data = self.ad.get_user_info_admin_view()
        self.table3 = self.ui.tableWidget_3
        self.fill_table_with_data_3(backend_data)

        s_no = self.ui.lineEdit_2.text()  # 工号
        r_no = self.ui.lineEdit_3.text()  # 等级
        # 查找工号，check1同理
        check1 = self.ad.change_role(s_no, r_no)
        if check1 == 1:
            # 数据库操作，修改这个工号员工对应的rank值
            # 修改数据库，更新表，同上
            backend_data = self.ad.get_user_info_admin_view()
            self.table3 = self.ui.tableWidget_3
            self.fill_table_with_data_3(backend_data)
            self.ui.stackedWidget_4.setCurrentIndex(3)
        elif check1 == -2:  # 身份编号不在给定范围内
            self.ui.stackedWidget_4.setCurrentIndex(2)
        else:
            self.ui.stackedWidget_4.setCurrentIndex(1)
