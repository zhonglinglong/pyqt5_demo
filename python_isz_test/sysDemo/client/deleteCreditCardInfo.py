# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox
from sysDemo.sqlite.mySqlite import MySqlite
from common import  base

class DeleteCreditCardInfo(QDialog):
    def __init__(self, parent=None):
        super(DeleteCreditCardInfo, self).__init__(parent)
        self.resize(376, 207)
        self.setWindowTitle("警告")
        self.delete_credit_card_label = QtWidgets.QLabel(self)
        self.delete_credit_card_label.setGeometry(QtCore.QRect(120, 40, 151, 41))
        self.delete_credit_card_label.setObjectName("delete_credit_card_label")
        self.delete_credit_card_label.setText("您确定删除该条流水？")

        self.delete_credit_card_YESpushButton = QtWidgets.QPushButton(self)
        self.delete_credit_card_YESpushButton.setGeometry(QtCore.QRect(100, 130, 75, 23))
        self.delete_credit_card_YESpushButton.setObjectName("delete_credit_card_YESpushButton")
        self.delete_credit_card_YESpushButton.setText("确定")
        self.delete_credit_card_YESpushButton.clicked.connect(self.get_yes)

        self.delete_credit_card_NOpushButton = QtWidgets.QPushButton(self)
        self.delete_credit_card_NOpushButton.setGeometry(QtCore.QRect(210, 130, 75, 23))
        self.delete_credit_card_NOpushButton.setObjectName("delete_credit_card_NOpushButton")
        self.delete_credit_card_NOpushButton.setText("取消")
        self.delete_credit_card_NOpushButton.clicked.connect(self.get_no)

    def get_yes(self):
        """
        点击确定
        :return:
        """
        base.consoleLog('删除信用卡点击确定按钮')
        ID = int(self.windowTitle().split('警告')[1])

        #先判断是否被删除
        sql = """select deleted from credit_card where card_id='%s'""" % ID
        deleted = MySqlite(sql).select_sql()[0][0]
        if deleted=='1':
            self.close()
            QMessageBox.about(self, "警告", "该条数据已被删除，请刷新列表！")
            return

        sql = """update credit_card set deleted=1,update_time='%s' where card_id='%s';""" % (base.time_time(),ID)
        MySqlite(sql).update_sql()
        self.close()
        QMessageBox.about(self, "提示", "该条数据删除成功！")
        return

    def get_no(self):
        """
        点进取消
        :return:
        """
        base.consoleLog('删除信用卡点击取消按钮')
        self.close()
        return




