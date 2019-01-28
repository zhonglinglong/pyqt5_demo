# -*- coding: utf-8 -*-

'''
 更新财务流水的窗口
'''
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget, QFormLayout, QLabel, QPushButton, QDialog, QComboBox, \
    QMessageBox
from common import base
from sysDemo.sqlite.mySqlite import MySqlite


class UpdateFinancialFlow(QDialog):
    def __init__(self, parent=None):
        super(UpdateFinancialFlow, self).__init__(parent)
        base.consoleLog('更新财务流水')
        self.setWindowTitle("更新财务流水")
        self.resize(400,200)
        self.update_financial_flow_button = QPushButton("保存", self)
        self.update_financial_flow_button.setGeometry(QtCore.QRect(300, 150, 75, 23))
        self.update_financial_flow_button.show()
        self.update_financial_flow_button.clicked.connect(self.update_financial_flow_info)

        flo = QFormLayout()
        flo.addRow(QLabel())
        self.updateeventLineEdit = QLineEdit()
        self.updatedataLineEdit = QLineEdit()
        self.updateclassificationComboBox = QComboBox()
        self.updatevalueLineEdit = QLineEdit()
        flo.addRow("消费事件", self.updateeventLineEdit)
        flo.addRow("消费分类", self.updateclassificationComboBox)
        flo.addRow("消费日期", self.updatedataLineEdit)
        flo.addRow("消费金额", self.updatevalueLineEdit)
        self.setLayout(flo)

    def update_financial_flow_info(self):
        """
        更新账单流水
        :return:
        """
        base.consoleLog('更新账单流水详情的值')

        updateevent = QLineEdit.displayText(self.updateeventLineEdit)
        updatedata = QLineEdit.displayText(self.updatedataLineEdit)
        updatevalue = QLineEdit.displayText(self.updatevalueLineEdit)
        ID = int(self.windowTitle().split('财务流水信息')[1])

        if updateevent == '' or updatedata == '' or updatevalue == '':
            QMessageBox.about(self, "提示", "您有部分数据为空，请输入完整信息之后再点击保存!")
            return

        sql = """update financial_flow set event='%s',datas='%s',money='%s',update_time='%s' where ID='%s';
            """ % (updateevent, updatedata, updatevalue, base.time_time(),ID)
        MySqlite(sql).update_sql()
        QMessageBox.about(self, "提示", "您的财务流水信息更新成功!")
        self.close()
        return

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     win = UpdateFinancialFlow()
#     win.show()
#     sys.exit(app.exec_())
