# -*- coding: utf-8 -*-

from datetime import datetime
from PyQt5.QtWidgets import QDialog, QPushButton, QFormLayout, QLabel, QComboBox, QLineEdit, QMessageBox
from PyQt5 import QtCore
from common import base
from sysDemo.sqlite.mySqlite import MySqlite


class UpdateCreditCard(QDialog):
    def __init__(self, parent=None):
        super(UpdateCreditCard, self).__init__(parent)
        base.consoleLog('信用卡详情')
        self.setWindowTitle("信用卡详情")

        self.resize(360, 296)
        self.setWindowTitle('新增信用卡信息')
        self.credit_card_name_label = QLabel(self)
        self.credit_card_name_label.setGeometry(QtCore.QRect(22, 22, 66, 16))
        self.credit_card_name_label.setObjectName("credit_card_name_label")
        self.credit_card_name_label.setText('信用卡名称')
        self.credit_card_name_lineEdit = QLineEdit(self)
        self.credit_card_name_lineEdit.setGeometry(QtCore.QRect(94, 22, 231, 20))
        self.credit_card_name_lineEdit.setObjectName("credit_card_name_lineEdit")
        self.credit_card_name_lineEdit.setPlaceholderText('请输入信用卡名称')

        self.credit_card_number_label = QLabel(self)
        self.credit_card_number_label.setGeometry(QtCore.QRect(22, 51, 66, 16))
        self.credit_card_number_label.setObjectName("credit_card_number_label")
        self.credit_card_number_label.setText('卡号')
        self.credit_card_number_lineEdit = QLineEdit(self)
        self.credit_card_number_lineEdit.setGeometry(QtCore.QRect(94, 51, 231, 20))
        self.credit_card_number_lineEdit.setObjectName("credit_card_number_lineEdit")
        self.credit_card_number_lineEdit.setPlaceholderText('请输入信用卡卡号')

        self.credit_card_quota_label = QLabel(self)
        self.credit_card_quota_label.setGeometry(QtCore.QRect(22, 81, 66, 16))
        self.credit_card_quota_label.setObjectName("credit_card_quota_label")
        self.credit_card_quota_label.setText('额度')
        self.credit_card_quota_lineEdit = QLineEdit(self)
        self.credit_card_quota_lineEdit.setGeometry(QtCore.QRect(94, 81, 231, 20))
        self.credit_card_quota_lineEdit.setObjectName("credit_card_quota_lineEdit")
        self.credit_card_quota_lineEdit.setPlaceholderText('请输入信用卡额度')

        self.credit_card_account_date_label = QLabel(self)
        self.credit_card_account_date_label.setGeometry(QtCore.QRect(22, 111, 66, 16))
        self.credit_card_account_date_label.setObjectName("credit_card_account_date_label")
        self.credit_card_account_date_label.setText('出账日')
        self.credit_card_account_date_lineEdit = QLineEdit(self)
        self.credit_card_account_date_lineEdit.setGeometry(QtCore.QRect(94, 111, 231, 20))
        self.credit_card_account_date_lineEdit.setObjectName("credit_card_account_date_lineEdit")
        self.credit_card_account_date_lineEdit.setPlaceholderText('请输入信用卡账单日')

        self.credit_card_repayment_date_label = QLabel(self)
        self.credit_card_repayment_date_label.setGeometry(QtCore.QRect(22, 141, 66, 16))
        self.credit_card_repayment_date_label.setObjectName("credit_card_repayment_date_label")
        self.credit_card_repayment_date_label.setText('还款日')
        self.credit_card_repayment_date_lineEdit = QLineEdit(self)
        self.credit_card_repayment_date_lineEdit.setGeometry(QtCore.QRect(94, 141, 231, 20))
        self.credit_card_repayment_date_lineEdit.setObjectName("credit_card_repayment_date_lineEdit")
        self.credit_card_repayment_date_lineEdit.setPlaceholderText('请输入信用卡还款日')

        self.credit_card_binding_payment_name_label = QLabel(self)
        self.credit_card_binding_payment_name_label.setGeometry(QtCore.QRect(22, 171, 66, 16))
        self.credit_card_binding_payment_name_label.setObjectName("credit_card_binding_payment_name_label")
        self.credit_card_binding_payment_name_label.setText('支付绑定App')
        self.credit_card_binding_payment_name_lineEdit = QLineEdit(self)
        self.credit_card_binding_payment_name_lineEdit.setGeometry(QtCore.QRect(94, 171, 231, 20))
        self.credit_card_binding_payment_name_lineEdit.setObjectName("credit_card_binding_payment_name_lineEdit")
        self.credit_card_binding_payment_name_lineEdit.setPlaceholderText('请输入信用卡绑定的付款APP名称')

        self.credit_card_welfare_label = QLabel(self)
        self.credit_card_welfare_label.setGeometry(QtCore.QRect(22, 201, 66, 16))
        self.credit_card_welfare_label.setObjectName("credit_card_welfare_label")
        self.credit_card_welfare_label.setText('福利')
        self.credit_card_welfare_lineEdit = QLineEdit(self)
        self.credit_card_welfare_lineEdit.setGeometry(QtCore.QRect(94, 201, 231, 20))
        self.credit_card_welfare_lineEdit.setObjectName("credit_card_welfare_lineEdit")
        self.credit_card_welfare_lineEdit.setPlaceholderText('请输入信用卡福利')

        self.credit_card_welfare_data_label = QLabel(self)
        self.credit_card_welfare_data_label.setGeometry(QtCore.QRect(22, 231, 66, 16))
        self.credit_card_welfare_data_label.setObjectName("credit_card_welfare_data_label")
        self.credit_card_welfare_data_label.setText('备注')
        self.credit_card_welfare_data_lineEdit = QLineEdit(self)
        self.credit_card_welfare_data_lineEdit.setGeometry(QtCore.QRect(94, 231, 231, 20))
        self.credit_card_welfare_data_lineEdit.setObjectName("credit_card_welfare_data_lineEdit")
        self.credit_card_welfare_data_lineEdit.setPlaceholderText('请输入信用卡使用福利时的日期')

        self.credit_card_datapagepushButton = QPushButton(self)
        self.credit_card_datapagepushButton.setGeometry(QtCore.QRect(260, 260, 71, 23))
        self.credit_card_datapagepushButton.setObjectName("credit_card_datapagepushButton")
        self.credit_card_datapagepushButton.setText('保存')
        self.credit_card_datapagepushButton.clicked.connect(self.update_credit_card)

    def update_credit_card(self):
        base.consoleLog('获取新增信用卡详情的内容，如果修改了重新保存')
        card_name = QLineEdit.displayText(self.credit_card_name_lineEdit)
        card_number = QLineEdit.displayText(self.credit_card_number_lineEdit)
        card_quota = QLineEdit.displayText(self.credit_card_quota_lineEdit)
        account_date = QLineEdit.displayText(self.credit_card_account_date_lineEdit)
        repayment_date = QLineEdit.displayText(self.credit_card_repayment_date_lineEdit)
        binding_payment_name = QLineEdit.displayText(self.credit_card_binding_payment_name_lineEdit)
        welfare = QLineEdit.displayText(self.credit_card_welfare_lineEdit)
        welfare_data = QLineEdit.displayText(self.credit_card_welfare_data_lineEdit)
        ID = int(self.windowTitle().split('信用卡详情')[1])

        if card_name == '' or card_number == '' or card_quota == '' or account_date == '' or repayment_date == '' or binding_payment_name == '' or welfare == '' or welfare_data == '':
            QMessageBox.about(self, "提示", "您有部分数据为空，请输入完整信息之后再点击保存!")
            return
        sql = """update credit_card set card_name='%s',card_number='%s',card_quota='%s',account_date='%s',repayment_date='%s',binding_payment_name='%s',welfare='%s',welfare_data='%s',update_time='%s' where card_id = '%s' ;
                              """ % (
        card_name, card_number,card_quota, account_date, repayment_date, binding_payment_name, welfare, welfare_data, base.time_time(),ID)
        MySqlite(sql).update_sql()
        QMessageBox.about(self, "提示", "您的信用卡信息更新成功!")
        self.close()
        return


