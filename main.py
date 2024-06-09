# -*- coding:gbk -*-
import pymysql
import GUI
import sys
from instructions import Instructions

if __name__ == '__main__':
    try:
        db = pymysql.connect(host="localhost", user="root", password="hujiaer2216", database="financial_management")
    except:
        print('连接数据库失败\n')
        exit(0)

    ins = Instructions(db)

    app = GUI.QApplication(sys.argv)
    win = GUI.LoginWindow(ins)
    sys.exit(app.exec_())
