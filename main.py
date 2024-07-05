# -*- coding:gbk -*-
import pymysql
import GUI
import sys
from instructions import Instructions

if __name__ == '__main__':
    try:
        db = pymysql.connect(host="rm-bp134czkc4vi5a9517o.mysql.rds.aliyuncs.com", user="ad", password="@tao123456", database="financial_system")
    except:
        print('连接数据库失败\n')
        exit(0)

    ins = Instructions(db)

    app = GUI.QApplication(sys.argv)
    win = GUI.LoginWindow(ins)
    sys.exit(app.exec_())
