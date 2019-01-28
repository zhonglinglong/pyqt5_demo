# -*- coding: utf-8 -*-

from datetime import datetime
from PyQt5.QtWidgets import QDialog, QPushButton, QFormLayout, QLabel, QComboBox, QLineEdit, QMessageBox
from PyQt5 import QtCore
from common import base
from sysDemo.sqlite.mySqlite import MySqlite


class UpdateCapital(QDialog):
    def __init__(self, parent=None):
        super(UpdateCapital, self).__init__(parent)
        base.consoleLog('还款计划信息')
        self.setWindowTitle("还款计划信息")
        self.resize(400, 300)
        self.update_capital_button = QPushButton("保存", self)
        self.update_capital_button.setGeometry(QtCore.QRect(250, 230, 75, 23))
        self.update_capital_button.show()
        self.update_capital_button.clicked.connect(self.update_capital_info)

        flo = QFormLayout()
        flo.addRow(QLabel())
        flo.addRow(QLabel())
        flo.addRow(QLabel())
        self.assetTypeInfo = QComboBox()
        flo.addRow("    还款类型", self.assetTypeInfo)
        self.statementDateInfoLineEdit = QLineEdit()
        self.statementDateInfoLineEdit.setPlaceholderText('请输入账单日')
        flo.addRow("      账单日", self.statementDateInfoLineEdit)
        self.repaymentDateInfoLineEdit = QLineEdit()
        self.repaymentDateInfoLineEdit.setPlaceholderText('请输入还款日')
        flo.addRow("      还款日", self.repaymentDateInfoLineEdit)
        self.repaymentPeriodInfoLineEdit = QLineEdit()
        self.repaymentPeriodInfoLineEdit.setPlaceholderText('请输入期数')
        flo.addRow("    还款期数", self.repaymentPeriodInfoLineEdit)
        self.repaymentAmountInfoLineEdit = QLineEdit()
        self.repaymentAmountInfoLineEdit.setPlaceholderText('请输入每期金额')
        flo.addRow("        金额", self.repaymentAmountInfoLineEdit)
        self.setLayout(flo)

    def update_capital_info(self):
        """
        详情更新还款计划的信息
        :return:
        """
        base.consoleLog('详情更新还款计划的信息')
        statementDateData = QLineEdit.displayText(self.statementDateInfoLineEdit)
        repaymentDateData = QLineEdit.displayText(self.repaymentDateInfoLineEdit)
        repaymentPeriodDateData = QLineEdit.displayText(self.repaymentPeriodInfoLineEdit)
        repaymentAmountDate = QLineEdit.displayText(self.repaymentAmountInfoLineEdit)
        ID = int(self.windowTitle().split('还款计划信息')[1])

        if statementDateData == '' or repaymentDateData == '' or repaymentPeriodDateData == '' or repaymentAmountDate == '':
            QMessageBox.about(self, "提示", "您有部分数据为空，请输入完整信息之后再点击保存!")
            return

        sql = """update financial_repayment_data set statement_date='%s',repayment_date='%s',repayment_period='%s',repayment_amount='%s',update_time='%s' where ID='%s';
    """ % (statementDateData, repaymentDateData, repaymentPeriodDateData,repaymentAmountDate,base.time_time(),ID)
        MySqlite(sql).update_sql()
        QMessageBox.about(self, "提示", "您的还款计划内容更新成功!")
        self.close()
        return
