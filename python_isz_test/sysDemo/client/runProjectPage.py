#-*- coding: utf-8 -*-
# @Time   : 2019/1/15 14:06
# @Author : linglong
# @File   : runProjectPage.py
import subprocess
from time import sleep

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox
from sysDemo.sqlite.mySqlite import MySqlite
from common import  base

class RunProject(QDialog):
    def __init__(self, parent=None):
        super(RunProject, self).__init__(parent)
        self.project_run_page = QDialog(self)
        self.project_run_page.setObjectName('project_run_page')
        self.project_run_page.resize(376, 207)
        self.project_run_page.setWindowTitle("项目执行")

        self.project_run_label = QtWidgets.QLabel('您确定执行项目?', self)
        self.project_run_label.setObjectName('project_run_label')
        self.project_run_label.setGeometry(QtCore.QRect(120, 40, 151, 41))

        self.project_run_YESpushButton = QtWidgets.QPushButton('确定', self)
        self.project_run_YESpushButton.setGeometry(QtCore.QRect(100, 130, 75, 23))
        self.project_run_YESpushButton.setObjectName("project_run_YESpushButton")
        self.project_run_YESpushButton.clicked.connect(self.get_yes)

        self.project_run_NOpushButton = QtWidgets.QPushButton('取消', self)
        self.project_run_NOpushButton.setGeometry(QtCore.QRect(210, 130, 75, 23))
        self.project_run_NOpushButton.setObjectName("project_run_NOpushButton")
        self.project_run_NOpushButton.clicked.connect(self.get_no)

    def get_yes(self):
        """
        点击确定
        :return:
        """
        base.consoleLog('运行项目界面点击确定按钮')

        ID = int(self.windowTitle().split('项目执行')[1])

        #先判断是否被删除
        sql = """select script from test_demo where ID='%s'""" % ID
        script = MySqlite(sql).select_sql()[0][0]
        subprocess.Popen('python3 %s' % script)
        print(script)
        QMessageBox.about(self, "提示", "项目正在后台执行中,稍后查看邮件测试报告或者查看明细")

        self.close()


        return

    def get_no(self):
        """
        点进取消
        :return:
        """
        base.consoleLog('运行项目界面点击取消按钮')
        self.close()
        return

