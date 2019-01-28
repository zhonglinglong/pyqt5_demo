# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont, QColor, QBrush
from PyQt5.QtWidgets import QAbstractItemView, QDialog, QPushButton, QFormLayout, QLineEdit, QComboBox, QLabel, \
    QMessageBox, QHeaderView
from common import base
from sysDemo.sqlite.mySqlite import MySqlite
import datetime


class Ui_Form(object):
    def setupUi(self, Form):
        base.consoleLog('初始化生成系统页面')

        #主窗口
        Form.setObjectName("Form")
        Form.resize(1200, 950)
        Form.setStyleSheet('background:#FFFFFF')
        Form.setFixedSize(self.width(), self.height())

        # 菜单栏
        self.treeWidget = QtWidgets.QTreeWidget(Form)
        self.treeWidget.setGeometry(QtCore.QRect(10, 20, 171, 921))
        self.treeWidget.setStyleSheet('color:black')
        # self.treeWidget.setFont(QFont("Helvetica",12))
        self.treeWidget.setObjectName("treeWidget")
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "test系统"))
        self.treeWidget.headerItem().setText(0, _translate("Form", "菜单栏"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.setSortingEnabled(__sortingEnabled)

        #财务管理菜单栏节点
        self.finance_item = QtWidgets.QTreeWidgetItem(self.treeWidget)
        self.finance_repayment_plan_item = QtWidgets.QTreeWidgetItem(self.finance_item)
        self.finance_bill_flow_item = QtWidgets.QTreeWidgetItem(self.finance_item)
        self.credit_card_item = QtWidgets.QTreeWidgetItem(self.finance_item)
        self.treeWidget.topLevelItem(0).setText(0, _translate("Form", "财务管理"))
        self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("Form", "还款计划"))
        self.treeWidget.topLevelItem(0).child(1).setText(0, _translate("Form", "账单流水"))
        self.treeWidget.topLevelItem(0).child(2).setText(0, _translate("Form", "信用卡"))

        #测试管理菜单栏节点
        self.test_item = QtWidgets.QTreeWidgetItem(self.treeWidget)
        self.project_item = QtWidgets.QTreeWidgetItem(self.test_item)
        self.tool_item = QtWidgets.QTreeWidgetItem(self.test_item)
        self.keyword_item = QtWidgets.QTreeWidgetItem(self.test_item)
        self.testcase_item = QtWidgets.QTreeWidgetItem(self.test_item)
        self.treeWidget.topLevelItem(1).setText(0, _translate("Form", "测试管理"))
        self.treeWidget.topLevelItem(1).child(0).setText(0, _translate("Form", "项目运行"))
        self.treeWidget.topLevelItem(1).child(1).setText(0, _translate("Form", "数据构造"))
        self.treeWidget.topLevelItem(1).child(2).setText(0, _translate("Form", "关键字"))
        self.treeWidget.topLevelItem(1).child(3).setText(0, _translate("Form", "用例库"))


        # 设置总页签
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(190, 20, 1701, 971))
        self.tabWidget.setObjectName("tabWidget")


        # 设置页签的第一个显示窗口  首页
        self.tab_ = QtWidgets.QWidget()
        self.tab_.setObjectName("tab_")
        self.tabWidget.addTab(self.tab_, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_), "首页")
        self.tab_.setStyleSheet('background:#F2F2F2')

    def add_testcase(self,value=False):
        base.consoleLog('新增测试用例页面')
        if value:
            base.consoleLog('已经存在该页面,不在加载!')
            return

        # 新增页签作为关键字的页面
        self.testcase_tab = QtWidgets.QWidget()
        self.testcase_tab.setObjectName("testcase_tab")
        self.testcase_tab.setStyleSheet('background:#F2F2F2')
        self.tabWidget.addTab(self.testcase_tab, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.testcase_tab), "用例库")

        # 搜索条件
        self.testcase_name_lineEdit = QtWidgets.QLineEdit(self.testcase_tab)
        self.testcase_name_lineEdit.setGeometry(QtCore.QRect(10, 10, 90, 22))
        self.testcase_name_lineEdit.setPlaceholderText('用例名称')
        self.testcase_name_lineEdit.setObjectName("testcase_name_lineEdit")

        self.testcase_text_lineEdit = QtWidgets.QLineEdit(self.testcase_tab)
        self.testcase_text_lineEdit.setGeometry(QtCore.QRect(110, 10, 90, 20))
        self.testcase_text_lineEdit.setPlaceholderText('用例描述')
        self.testcase_text_lineEdit.setObjectName("testcase_text_lineEdit")

        # 搜索
        self.testcase_search_pushButton = QtWidgets.QPushButton(self.testcase_tab)
        self.testcase_search_pushButton.setGeometry(QtCore.QRect(772, 10, 75, 28))
        self.testcase_search_pushButton.setObjectName("testcase_search_pushButton")
        self.testcase_search_pushButton.setText("搜索")
        self.testcase_search_pushButton.setStyleSheet('background-color:#20A0FF;color:white')
        self.testcase_search_pushButton.setFont(QFont("Arial", 12, QFont.Bold))

        # # 关闭页面按钮
        # self.testcase_close_pushButton = QtWidgets.QPushButton(self.testcase_tab)
        # self.testcase_close_pushButton.setGeometry(QtCore.QRect(980, 5, 25, 20))
        # self.testcase_close_pushButton.setObjectName("testcase_close_pushButton")
        # self.testcase_close_pushButton.setText("X")
        # self.testcase_close_pushButton.setFont(QFont("Arial",12,QFont.Bold))
        # self.testcase_close_pushButton.setStyleSheet('background-color:white;color:red')

        # self.testcase_close_pushButton.setStyleSheet('color:red;border-radius:3px')ji

        # 表单运行及明细按钮
        self.testcase_PushButton1 = QtWidgets.QPushButton()
        self.testcase_PushButton1.setObjectName("testcase_PushButton1")
        self.testcase_PushButton1.setText("编辑")
        self.testcase_PushButton2 = QtWidgets.QPushButton()
        self.testcase_PushButton2.setObjectName("testcase_PushButton2")
        self.testcase_PushButton2.setText("编辑")
        self.testcase_PushButton3 = QtWidgets.QPushButton()
        self.testcase_PushButton3.setObjectName("testcase_PushButton3")
        self.testcase_PushButton3.setText("编辑")
        self.testcase_PushButton4 = QtWidgets.QPushButton()
        self.testcase_PushButton4.setObjectName("testcase_PushButton4")
        self.testcase_PushButton4.setText("编辑")
        self.testcase_PushButton5 = QtWidgets.QPushButton()
        self.testcase_PushButton5.setObjectName("testcase_PushButton5")
        self.testcase_PushButton5.setText("编辑")
        self.testcase_PushButton6 = QtWidgets.QPushButton()
        self.testcase_PushButton6.setObjectName("testcase_PushButton6")
        self.testcase_PushButton6.setText("编辑")
        self.testcase_PushButton7 = QtWidgets.QPushButton()
        self.testcase_PushButton7.setObjectName("testcase_PushButton7")
        self.testcase_PushButton7.setText("编辑")
        self.testcase_PushButton8 = QtWidgets.QPushButton()
        self.testcase_PushButton8.setObjectName("testcase_PushButton8")
        self.testcase_PushButton8.setText("编辑")
        self.testcase_PushButton9 = QtWidgets.QPushButton()
        self.testcase_PushButton9.setObjectName("testcase_PushButton9")
        self.testcase_PushButton9.setText("编辑")
        self.testcase_PushButton10 = QtWidgets.QPushButton()
        self.testcase_PushButton10.setObjectName("testcase_PushButton10")
        self.testcase_PushButton10.setText("编辑")
        self.testcase_PushButton11 = QtWidgets.QPushButton()
        self.testcase_PushButton11.setObjectName("testcase_PushButton11")
        self.testcase_PushButton11.setText("编辑")
        self.testcase_PushButton12 = QtWidgets.QPushButton()
        self.testcase_PushButton12.setObjectName("testcase_PushButton12")
        self.testcase_PushButton12.setText("编辑")
        self.testcase_PushButton13 = QtWidgets.QPushButton()
        self.testcase_PushButton13.setObjectName("testcase_PushButton13")
        self.testcase_PushButton13.setText("编辑")
        self.testcase_PushButton14 = QtWidgets.QPushButton()
        self.testcase_PushButton14.setObjectName("testcase_PushButton14")
        self.testcase_PushButton14.setText("编辑")
        self.testcase_PushButton15 = QtWidgets.QPushButton()
        self.testcase_PushButton15.setObjectName("testcase_PushButton15")
        self.testcase_PushButton15.setText("编辑")
        self.testcase_PushButton16 = QtWidgets.QPushButton()
        self.testcase_PushButton16.setObjectName("testcase_PushButton16")
        self.testcase_PushButton16.setText("编辑")
        self.testcase_PushButton17 = QtWidgets.QPushButton()
        self.testcase_PushButton17.setObjectName("testcase_PushButton17")
        self.testcase_PushButton17.setText("编辑")
        self.testcase_PushButton18 = QtWidgets.QPushButton()
        self.testcase_PushButton18.setObjectName("testcase_PushButton18")
        self.testcase_PushButton18.setText("编辑")
        self.testcase_PushButton19 = QtWidgets.QPushButton()
        self.testcase_PushButton19.setObjectName("testcase_PushButton19")
        self.testcase_PushButton19.setText("编辑")
        self.testcase_PushButton20 = QtWidgets.QPushButton()
        self.testcase_PushButton20.setObjectName("testcase_PushButton20")
        self.testcase_PushButton20.setText("编辑")
        self.testcase_PushButton21 = QtWidgets.QPushButton()
        self.testcase_PushButton21.setObjectName("testcase_PushButton21")
        self.testcase_PushButton21.setText("编辑")
        self.testcase_PushButton22 = QtWidgets.QPushButton()
        self.testcase_PushButton22.setObjectName("testcase_PushButton22")
        self.testcase_PushButton22.setText("编辑")
        self.testcase_PushButton23 = QtWidgets.QPushButton()
        self.testcase_PushButton23.setObjectName("testcase_PushButton23")
        self.testcase_PushButton23.setText("编辑")
        self.testcase_PushButton24 = QtWidgets.QPushButton()
        self.testcase_PushButton24.setObjectName("testcase_PushButton24")
        self.testcase_PushButton24.setText("编辑")
        self.testcase_PushButton25 = QtWidgets.QPushButton()
        self.testcase_PushButton25.setObjectName("testcase_PushButton25")
        self.testcase_PushButton25.setText("编辑")
        self.testcase_PushButtonAll = {self.testcase_PushButton1: 1,
                                      self.testcase_PushButton2: 2,
                                      self.testcase_PushButton3: 3,
                                      self.testcase_PushButton4: 4,
                                      self.testcase_PushButton5: 5,
                                      self.testcase_PushButton6: 6,
                                      self.testcase_PushButton7: 7,
                                      self.testcase_PushButton8: 8,
                                      self.testcase_PushButton9: 9,
                                      self.testcase_PushButton10: 10,
                                      self.testcase_PushButton11: 11,
                                      self.testcase_PushButton12: 12,
                                      self.testcase_PushButton13: 13,
                                      self.testcase_PushButton14: 14,
                                      self.testcase_PushButton15: 15,
                                      self.testcase_PushButton16: 16,
                                      self.testcase_PushButton17: 17,
                                      self.testcase_PushButton18: 18,
                                      self.testcase_PushButton19: 19,
                                      self.testcase_PushButton20: 20,
                                      self.testcase_PushButton21: 21,
                                      self.testcase_PushButton22: 22,
                                      self.testcase_PushButton23: 23,
                                      self.testcase_PushButton24: 24,
                                      self.testcase_PushButton25: 25
                                      }

        # 列表展示
        self.testcase_tableWidget = QtWidgets.QTableWidget(self.testcase_tab)
        self.testcase_tableWidget.setGeometry(QtCore.QRect(10, 50, 921, 795))
        self.testcase_tableWidget.setObjectName("testcase_tableWidget")
        self.testcase_tableWidget.setColumnCount(7)
        self.testcase_tableWidget.setColumnWidth(0, 150)
        self.testcase_tableWidget.setColumnWidth(1, 150)
        self.testcase_tableWidget.setColumnWidth(2, 500)
        self.testcase_tableWidget.setColumnWidth(3, 500)
        self.testcase_tableWidget.setColumnWidth(4, 300)
        self.testcase_tableWidget.setColumnWidth(5, 200)
        self.testcase_tableWidget.setColumnWidth(6, 80)
        self.testcase_tableWidget.setRowCount(25)
        # 表单插入25*7的格子
        for i in range(25):
            for j in range(7):
                item = QtWidgets.QTableWidgetItem()
                self.testcase_tableWidget.setVerticalHeaderItem(i, item)
                item = QtWidgets.QTableWidgetItem()
                self.testcase_tableWidget.setHorizontalHeaderItem(j, item)
        # 表单首列1-30
        for i in range(25):
            item = self.testcase_tableWidget.verticalHeaderItem(i)
            item.setText(str(i + 1))
        self.testcase_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 列表禁止编辑
        # 表的头部
        item = self.testcase_tableWidget.horizontalHeaderItem(0)
        item.setText("用例名称")
        item = self.testcase_tableWidget.horizontalHeaderItem(1)
        item.setText("用例描述")
        item = self.testcase_tableWidget.horizontalHeaderItem(2)
        item.setText("操作步骤")
        item = self.testcase_tableWidget.horizontalHeaderItem(3)
        item.setText("接口步骤")
        item = self.testcase_tableWidget.horizontalHeaderItem(4)
        item.setText("预期结果")
        item = self.testcase_tableWidget.horizontalHeaderItem(6)
        item.setText("操作-编辑")
        item = self.testcase_tableWidget.horizontalHeaderItem(5)
        item.setText("运行结果")

        # 运行,详情按钮加载到表格中
        key = list(self.testcase_PushButtonAll.keys())
        for i in range(len(key)):
            self.testcase_tableWidget.setCellWidget(i, 6, key[i])
        #
        # key = list(self.testcase_detailed_PushButtonAll.keys())
        # for i in range(len(key)):
        #     self.testcase_tableWidget.setCellWidget(i, 6, key[i])

        # 不显示垂直表头
        # self.testcase_tableWidget.setShowGrid(False)
        self.testcase_tableWidget.verticalHeader().setVisible(False)
        # 表头上颜色
        self.testcase_tableWidget.setStyleSheet(
            "QHeaderView::section{background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgb(46,46,46),stop:1 rgb(66,66,66));color: rgb(210,210,210);;padding-left: 4px;border: 1px solid #383838;}")
        self.testcase_tableWidget.setStyleSheet(

            "background: rgb(221,249,248);alternate-background-color:rgb(48,51,180);selection-background-color:qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgb(56,56,230),stop:1 rgb(174,253,188));"
        )

        # 列表下方搜索
        # 上一页
        self.testcase_previous_page_pushButton = QtWidgets.QPushButton(self.testcase_tab)
        self.testcase_previous_page_pushButton.setGeometry(QtCore.QRect(10, 850, 75, 23))
        self.testcase_previous_page_pushButton.setObjectName("testcase_previous_page_pushButton")
        self.testcase_previous_page_pushButton.setText('上一页')
        self.testcase_previous_page_pushButton.setStyleSheet('background-color:#20A0FF')

        # 当前页
        self.testcase_current_page_label = QtWidgets.QLabel(self.testcase_tab)
        self.testcase_current_page_label.setGeometry(QtCore.QRect(90, 850, 35, 21))
        self.testcase_current_page_label.setObjectName("testcase_current_page_label")
        self.testcase_current_page_label.setText('0/0')
        # 下一页
        self.testcase_next_page_pushButton = QtWidgets.QPushButton(self.testcase_tab)
        self.testcase_next_page_pushButton.setGeometry(QtCore.QRect(120, 850, 75, 23))
        self.testcase_next_page_pushButton.setObjectName("testcase_next_page_pushButton")
        self.testcase_next_page_pushButton.setText('下一页')
        self.testcase_next_page_pushButton.setStyleSheet('background-color:#20A0FF')

        # 项目数量
        self.testcase_total_amount_of_label = QtWidgets.QLabel(self.testcase_tab)
        self.testcase_total_amount_of_label.setGeometry(QtCore.QRect(230, 850, 55, 21))
        self.testcase_total_amount_of_label.setObjectName("testcase_total_amount_of_label")
        self.testcase_total_amount_of_label.setText('项目总数')
        self.testcase_total_amount_of_lineEdit = QtWidgets.QLineEdit(self.testcase_tab)
        self.testcase_total_amount_of_lineEdit.setGeometry(QtCore.QRect(280, 850, 90, 20))
        self.testcase_total_amount_of_lineEdit.setReadOnly(True)
        self.testcase_total_amount_of_lineEdit.setObjectName("testcase_total_amount_of_lineEdit")

    def add_keyword(self,value=False):
        base.consoleLog('新增关键字页面')
        if value:
            base.consoleLog('已经存在该页面,不在加载!')
            return

        # 新增页签作为关键字的页面
        self.keyword_tab = QtWidgets.QWidget()
        self.keyword_tab.setObjectName("keyword_tab")
        self.keyword_tab.setStyleSheet('background:#F2F2F2')
        self.tabWidget.addTab(self.keyword_tab, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.keyword_tab), "关键字")

        # 搜索条件
        self.keyword_name_lineEdit = QtWidgets.QLineEdit(self.keyword_tab)
        self.keyword_name_lineEdit.setGeometry(QtCore.QRect(10, 10, 90, 22))
        self.keyword_name_lineEdit.setPlaceholderText('关键字名称')
        self.keyword_name_lineEdit.setObjectName("keyword_name_lineEdit")

        self.keyword_text_lineEdit = QtWidgets.QLineEdit(self.keyword_tab)
        self.keyword_text_lineEdit.setGeometry(QtCore.QRect(110, 10, 90, 20))
        self.keyword_text_lineEdit.setPlaceholderText('关键字描述')
        self.keyword_text_lineEdit.setObjectName("keyword_text_lineEdit")

        # 搜索
        self.keyword_search_pushButton = QtWidgets.QPushButton(self.keyword_tab)
        self.keyword_search_pushButton.setGeometry(QtCore.QRect(772, 10, 75, 28))
        self.keyword_search_pushButton.setObjectName("keyword_search_pushButton")
        self.keyword_search_pushButton.setText("搜索")
        self.keyword_search_pushButton.setStyleSheet('background-color:#20A0FF;color:white')
        self.keyword_search_pushButton.setFont(QFont("Arial", 12, QFont.Bold))

        # # 关闭页面按钮
        # self.keyword_close_pushButton = QtWidgets.QPushButton(self.keyword_tab)
        # self.keyword_close_pushButton.setGeometry(QtCore.QRect(980, 5, 25, 20))
        # self.keyword_close_pushButton.setObjectName("keyword_close_pushButton")
        # self.keyword_close_pushButton.setText("X")
        # self.keyword_close_pushButton.setFont(QFont("Arial",12,QFont.Bold))
        # self.keyword_close_pushButton.setStyleSheet('background-color:white;color:red')

        # self.keyword_close_pushButton.setStyleSheet('color:red;border-radius:3px')ji

        # 表单运行及明细按钮
        self.keyword_PushButton1 = QtWidgets.QPushButton()
        self.keyword_PushButton1.setObjectName("keyword_PushButton1")
        self.keyword_PushButton1.setText("编辑")
        self.keyword_PushButton2 = QtWidgets.QPushButton()
        self.keyword_PushButton2.setObjectName("keyword_PushButton2")
        self.keyword_PushButton2.setText("编辑")
        self.keyword_PushButton3 = QtWidgets.QPushButton()
        self.keyword_PushButton3.setObjectName("keyword_PushButton3")
        self.keyword_PushButton3.setText("编辑")
        self.keyword_PushButton4 = QtWidgets.QPushButton()
        self.keyword_PushButton4.setObjectName("keyword_PushButton4")
        self.keyword_PushButton4.setText("编辑")
        self.keyword_PushButton5 = QtWidgets.QPushButton()
        self.keyword_PushButton5.setObjectName("keyword_PushButton5")
        self.keyword_PushButton5.setText("编辑")
        self.keyword_PushButton6 = QtWidgets.QPushButton()
        self.keyword_PushButton6.setObjectName("keyword_PushButton6")
        self.keyword_PushButton6.setText("编辑")
        self.keyword_PushButton7 = QtWidgets.QPushButton()
        self.keyword_PushButton7.setObjectName("keyword_PushButton7")
        self.keyword_PushButton7.setText("编辑")
        self.keyword_PushButton8 = QtWidgets.QPushButton()
        self.keyword_PushButton8.setObjectName("keyword_PushButton8")
        self.keyword_PushButton8.setText("编辑")
        self.keyword_PushButton9 = QtWidgets.QPushButton()
        self.keyword_PushButton9.setObjectName("keyword_PushButton9")
        self.keyword_PushButton9.setText("编辑")
        self.keyword_PushButton10 = QtWidgets.QPushButton()
        self.keyword_PushButton10.setObjectName("keyword_PushButton10")
        self.keyword_PushButton10.setText("编辑")
        self.keyword_PushButton11 = QtWidgets.QPushButton()
        self.keyword_PushButton11.setObjectName("keyword_PushButton11")
        self.keyword_PushButton11.setText("编辑")
        self.keyword_PushButton12 = QtWidgets.QPushButton()
        self.keyword_PushButton12.setObjectName("keyword_PushButton12")
        self.keyword_PushButton12.setText("编辑")
        self.keyword_PushButton13 = QtWidgets.QPushButton()
        self.keyword_PushButton13.setObjectName("keyword_PushButton13")
        self.keyword_PushButton13.setText("编辑")
        self.keyword_PushButton14 = QtWidgets.QPushButton()
        self.keyword_PushButton14.setObjectName("keyword_PushButton14")
        self.keyword_PushButton14.setText("编辑")
        self.keyword_PushButton15 = QtWidgets.QPushButton()
        self.keyword_PushButton15.setObjectName("keyword_PushButton15")
        self.keyword_PushButton15.setText("编辑")
        self.keyword_PushButton16 = QtWidgets.QPushButton()
        self.keyword_PushButton16.setObjectName("keyword_PushButton16")
        self.keyword_PushButton16.setText("编辑")
        self.keyword_PushButton17 = QtWidgets.QPushButton()
        self.keyword_PushButton17.setObjectName("keyword_PushButton17")
        self.keyword_PushButton17.setText("编辑")
        self.keyword_PushButton18 = QtWidgets.QPushButton()
        self.keyword_PushButton18.setObjectName("keyword_PushButton18")
        self.keyword_PushButton18.setText("编辑")
        self.keyword_PushButton19 = QtWidgets.QPushButton()
        self.keyword_PushButton19.setObjectName("keyword_PushButton19")
        self.keyword_PushButton19.setText("编辑")
        self.keyword_PushButton20 = QtWidgets.QPushButton()
        self.keyword_PushButton20.setObjectName("keyword_PushButton20")
        self.keyword_PushButton20.setText("编辑")
        self.keyword_PushButton21 = QtWidgets.QPushButton()
        self.keyword_PushButton21.setObjectName("keyword_PushButton21")
        self.keyword_PushButton21.setText("编辑")
        self.keyword_PushButton22 = QtWidgets.QPushButton()
        self.keyword_PushButton22.setObjectName("keyword_PushButton22")
        self.keyword_PushButton22.setText("编辑")
        self.keyword_PushButton23 = QtWidgets.QPushButton()
        self.keyword_PushButton23.setObjectName("keyword_PushButton23")
        self.keyword_PushButton23.setText("编辑")
        self.keyword_PushButton24 = QtWidgets.QPushButton()
        self.keyword_PushButton24.setObjectName("keyword_PushButton24")
        self.keyword_PushButton24.setText("编辑")
        self.keyword_PushButton25 = QtWidgets.QPushButton()
        self.keyword_PushButton25.setObjectName("keyword_PushButton25")
        self.keyword_PushButton25.setText("编辑")
        self.keyword_PushButtonAll = {self.keyword_PushButton1: 1,
                                      self.keyword_PushButton2: 2,
                                      self.keyword_PushButton3: 3,
                                      self.keyword_PushButton4: 4,
                                      self.keyword_PushButton5: 5,
                                      self.keyword_PushButton6: 6,
                                      self.keyword_PushButton7: 7,
                                      self.keyword_PushButton8: 8,
                                      self.keyword_PushButton9: 9,
                                      self.keyword_PushButton10: 10,
                                      self.keyword_PushButton11: 11,
                                      self.keyword_PushButton12: 12,
                                      self.keyword_PushButton13: 13,
                                      self.keyword_PushButton14: 14,
                                      self.keyword_PushButton15: 15,
                                      self.keyword_PushButton16: 16,
                                      self.keyword_PushButton17: 17,
                                      self.keyword_PushButton18: 18,
                                      self.keyword_PushButton19: 19,
                                      self.keyword_PushButton20: 20,
                                      self.keyword_PushButton21: 21,
                                      self.keyword_PushButton22: 22,
                                      self.keyword_PushButton23: 23,
                                      self.keyword_PushButton24: 24,
                                      self.keyword_PushButton25: 25
                                      }

        # 列表展示
        self.keyword_tableWidget = QtWidgets.QTableWidget(self.keyword_tab)
        self.keyword_tableWidget.setGeometry(QtCore.QRect(10, 50, 921, 795))
        self.keyword_tableWidget.setObjectName("keyword_tableWidget")
        self.keyword_tableWidget.setColumnCount(7)
        self.keyword_tableWidget.setColumnWidth(0, 150)
        self.keyword_tableWidget.setColumnWidth(1, 150)
        self.keyword_tableWidget.setColumnWidth(2, 500)
        self.keyword_tableWidget.setColumnWidth(3, 500)
        self.keyword_tableWidget.setColumnWidth(4, 300)
        self.keyword_tableWidget.setColumnWidth(5, 200)
        self.keyword_tableWidget.setColumnWidth(6, 80)
        self.keyword_tableWidget.setRowCount(25)
        # 表单插入25*7的格子
        for i in range(25):
            for j in range(7):
                item = QtWidgets.QTableWidgetItem()
                self.keyword_tableWidget.setVerticalHeaderItem(i, item)
                item = QtWidgets.QTableWidgetItem()
                self.keyword_tableWidget.setHorizontalHeaderItem(j, item)
        # 表单首列1-30
        for i in range(25):
            item = self.keyword_tableWidget.verticalHeaderItem(i)
            item.setText(str(i + 1))
        self.keyword_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 列表禁止编辑
        # 表的头部
        item = self.keyword_tableWidget.horizontalHeaderItem(0)
        item.setText("关键字名称")
        item = self.keyword_tableWidget.horizontalHeaderItem(1)
        item.setText("关键字描述")
        item = self.keyword_tableWidget.horizontalHeaderItem(2)
        item.setText("参数")
        item = self.keyword_tableWidget.horizontalHeaderItem(3)
        item.setText("参数解释")
        item = self.keyword_tableWidget.horizontalHeaderItem(4)
        item.setText("demo")
        item = self.keyword_tableWidget.horizontalHeaderItem(6)
        item.setText("操作-编辑")
        item = self.keyword_tableWidget.horizontalHeaderItem(5)
        item.setText("待定")

        # 运行,详情按钮加载到表格中
        key = list(self.keyword_PushButtonAll.keys())
        for i in range(len(key)):
            self.keyword_tableWidget.setCellWidget(i, 6, key[i])
        #
        # key = list(self.keyword_detailed_PushButtonAll.keys())
        # for i in range(len(key)):
        #     self.keyword_tableWidget.setCellWidget(i, 6, key[i])

        # 不显示垂直表头
        # self.keyword_tableWidget.setShowGrid(False)
        self.keyword_tableWidget.verticalHeader().setVisible(False)
        # 表头上颜色
        self.keyword_tableWidget.setStyleSheet(
            "QHeaderView::section{background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgb(46,46,46),stop:1 rgb(66,66,66));color: rgb(210,210,210);;padding-left: 4px;border: 1px solid #383838;}")
        self.keyword_tableWidget.setStyleSheet(

            "background: rgb(221,249,248);alternate-background-color:rgb(48,51,180);selection-background-color:qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgb(56,56,230),stop:1 rgb(174,253,188));"
        )

        # 列表下方搜索
        # 上一页
        self.keyword_previous_page_pushButton = QtWidgets.QPushButton(self.keyword_tab)
        self.keyword_previous_page_pushButton.setGeometry(QtCore.QRect(10, 850, 75, 23))
        self.keyword_previous_page_pushButton.setObjectName("keyword_previous_page_pushButton")
        self.keyword_previous_page_pushButton.setText('上一页')
        self.keyword_previous_page_pushButton.setStyleSheet('background-color:#20A0FF')

        # 当前页
        self.keyword_current_page_label = QtWidgets.QLabel(self.keyword_tab)
        self.keyword_current_page_label.setGeometry(QtCore.QRect(90, 850, 35, 21))
        self.keyword_current_page_label.setObjectName("keyword_current_page_label")
        self.keyword_current_page_label.setText('0/0')
        # 下一页
        self.keyword_next_page_pushButton = QtWidgets.QPushButton(self.keyword_tab)
        self.keyword_next_page_pushButton.setGeometry(QtCore.QRect(120, 850, 75, 23))
        self.keyword_next_page_pushButton.setObjectName("keyword_next_page_pushButton")
        self.keyword_next_page_pushButton.setText('下一页')
        self.keyword_next_page_pushButton.setStyleSheet('background-color:#20A0FF')

        # 项目数量
        self.keyword_total_amount_of_label = QtWidgets.QLabel(self.keyword_tab)
        self.keyword_total_amount_of_label.setGeometry(QtCore.QRect(230, 850, 55, 21))
        self.keyword_total_amount_of_label.setObjectName("keyword_total_amount_of_label")
        self.keyword_total_amount_of_label.setText('项目总数')
        self.keyword_total_amount_of_lineEdit = QtWidgets.QLineEdit(self.keyword_tab)
        self.keyword_total_amount_of_lineEdit.setGeometry(QtCore.QRect(280, 850, 90, 20))
        self.keyword_total_amount_of_lineEdit.setReadOnly(True)
        self.keyword_total_amount_of_lineEdit.setObjectName("keyword_total_amount_of_lineEdit")

    def add_test_data(self,value=False):
        base.consoleLog('新增数据构造页面')
        if value:
            return
        # 新增页签作为测试工具构造的页面
        self.add_data_tab = QtWidgets.QWidget()
        self.add_data_tab.setObjectName("add_data_tab")
        self.add_data_tab.setStyleSheet('background:#F2F2F2')
        self.tabWidget.addTab(self.add_data_tab, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.add_data_tab), "数据构造")
        #
        # # 关闭页面按钮
        # self.data_tab_close_pushButton = QtWidgets.QPushButton(self.add_data_tab)
        # self.data_tab_close_pushButton.setGeometry(QtCore.QRect(980, 5, 25, 20))
        # self.data_tab_close_pushButton.setObjectName("data_tab_close_pushButton")
        # self.data_tab_close_pushButton.setText("X")
        # self.data_tab_close_pushButton.setFont(QFont("Arial", 12, QFont.Bold))
        # self.data_tab_close_pushButton.setStyleSheet('background-color:white;color:red')

        #新增一个容器在标签里面。所有的内容只能显示在这个容器范围内
        self.ground_widget = QtWidgets.QWidget(self.add_data_tab)
        self.ground_widget.setStyleSheet('background:#DDF9F8')
        self.ground_widget.setGeometry(QtCore.QRect(30, 40, 660, 800))

        #新增一个容器专门放测试工具控件，移动栏控制这个容器
        self.data_all_widget = QtWidgets.QWidget(self.ground_widget)
        self.data_all_widget.setGeometry(QtCore.QRect(0,0,850, 1987))
        self.data_all_widget.setStyleSheet('background:#FFFFFF')
        self.data_all_widget.setObjectName('data_all_widget')

        #每个新增数据的区域分别用一个新窗口
        self.widget = QtWidgets.QWidget(self.data_all_widget)
        self.widget.setGeometry(QtCore.QRect(30, 40, 731, 111))
        self.widget.setObjectName("widget")
        self.widget.setStyleSheet('background: #DDF9F8')
        self.widget.resize(600,170)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(20, 5, 94, 18))
        self.label.setObjectName("label")
        self.label.setText('新增楼盘111111')
        self.label.setFont(QFont("Roman times",12,QFont.Bold))
        self.label.setStyleSheet('color:#E23F57')
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 40, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText('文字颜色颜色啊')
        self.lineEdit.setStyleSheet('color:#4B53DC')
        self.comboBox = QtWidgets.QComboBox(self.widget)
        self.comboBox.setGeometry(QtCore.QRect(160, 40, 111, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox_2 = QtWidgets.QComboBox(self.widget)
        self.comboBox_2.setGeometry(QtCore.QRect(300, 40, 111, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_3 = QtWidgets.QComboBox(self.widget)
        self.comboBox_3.setGeometry(QtCore.QRect(20, 70, 111, 22))
        self.comboBox_3.setObjectName("comboBox_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setGeometry(QtCore.QRect(440, 40, 113, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_3.setGeometry(QtCore.QRect(160, 70, 113, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(480, 130, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText('新增')
        self.pushButton.setStyleSheet('background:#FA5138')

        self.widget_2 = QtWidgets.QWidget(self.data_all_widget)
        self.widget_2.setGeometry(QtCore.QRect(30, 240, 731, 111))
        self.widget_2.setObjectName("widget_2")
        self.widget_2.setStyleSheet('background: #DDF9F8')
        self.widget_2.resize(600,170)
        self.label_2 = QtWidgets.QLabel(self.widget_2)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 54, 12))
        self.label_2.setObjectName("label_2")
        self.label_2.setText('新增22222222')
        self.lineEdit_4 = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_4.setGeometry(QtCore.QRect(20, 40, 113, 20))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.comboBox_4 = QtWidgets.QComboBox(self.widget_2)
        self.comboBox_4.setGeometry(QtCore.QRect(160, 40, 111, 22))
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_5 = QtWidgets.QComboBox(self.widget_2)
        self.comboBox_5.setGeometry(QtCore.QRect(300, 40, 111, 22))
        self.comboBox_5.setObjectName("comboBox_5")
        self.comboBox_6 = QtWidgets.QComboBox(self.widget_2)
        self.comboBox_6.setGeometry(QtCore.QRect(20, 70, 111, 22))
        self.comboBox_6.setObjectName("comboBox_6")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_5.setGeometry(QtCore.QRect(440, 40, 113, 20))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_6.setGeometry(QtCore.QRect(160, 70, 113, 20))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.pushButton_2 = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_2.setGeometry(QtCore.QRect(480, 130, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText('22222')

        self.widget_3 = QtWidgets.QWidget(self.data_all_widget)
        self.widget_3.setGeometry(QtCore.QRect(30, 440, 731, 111))
        self.widget_3.setObjectName("widget_3")
        self.widget_3.setStyleSheet('background: #DDF9F8')
        self.widget_3.resize(600, 170)
        self.label_3 = QtWidgets.QLabel(self.widget_3)
        self.label_3.setGeometry(QtCore.QRect(20, 10, 54, 12))
        self.label_3.setObjectName("label_3")
        self.label_3.setText('新增3333333333')
        self.lineEdit_7 = QtWidgets.QLineEdit(self.widget_3)
        self.lineEdit_7.setGeometry(QtCore.QRect(20, 40, 113, 20))
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.comboBox_7 = QtWidgets.QComboBox(self.widget_3)
        self.comboBox_7.setGeometry(QtCore.QRect(160, 40, 111, 22))
        self.comboBox_7.setObjectName("comboBox_7")
        self.comboBox_8 = QtWidgets.QComboBox(self.widget_3)
        self.comboBox_8.setGeometry(QtCore.QRect(300, 40, 111, 22))
        self.comboBox_8.setObjectName("comboBox_8")
        self.comboBox_9 = QtWidgets.QComboBox(self.widget_3)
        self.comboBox_9.setGeometry(QtCore.QRect(20, 70, 111, 22))
        self.comboBox_9.setObjectName("comboBox_9")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.widget_3)
        self.lineEdit_8.setGeometry(QtCore.QRect(440, 40, 113, 20))
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.lineEdit_9 = QtWidgets.QLineEdit(self.widget_3)
        self.lineEdit_9.setGeometry(QtCore.QRect(160, 70, 113, 20))
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.pushButton_3 = QtWidgets.QPushButton(self.widget_3)
        self.pushButton_3.setGeometry(QtCore.QRect(480, 130, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setText('33333')

        self.widget_4 = QtWidgets.QWidget(self.data_all_widget)
        self.widget_4.setGeometry(QtCore.QRect(30, 640, 600, 160))
        self.widget_4.setObjectName("widget_4")
        self.widget_4.setStyleSheet('background: #DDF9F8')
        self.label_4 = QtWidgets.QLabel(self.widget_4)
        self.label_4.setGeometry(QtCore.QRect(20, 10, 54, 12))
        self.label_4.setObjectName("label_4")
        self.label_4.setText('新增4444444')
        self.lineEdit_10 = QtWidgets.QLineEdit(self.widget_4)
        self.lineEdit_10.setGeometry(QtCore.QRect(20, 40, 113, 20))
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.comboBox_10 = QtWidgets.QComboBox(self.widget_4)
        self.comboBox_10.setGeometry(QtCore.QRect(160, 40, 111, 22))
        self.comboBox_10.setObjectName("comboBox_10")
        self.comboBox_11 = QtWidgets.QComboBox(self.widget_4)
        self.comboBox_11.setGeometry(QtCore.QRect(300, 40, 111, 22))
        self.comboBox_11.setObjectName("comboBox_11")
        self.comboBox_12 = QtWidgets.QComboBox(self.widget_4)
        self.comboBox_12.setGeometry(QtCore.QRect(20, 70, 111, 22))
        self.comboBox_12.setObjectName("comboBox_12")
        self.lineEdit_11 = QtWidgets.QLineEdit(self.widget_4)
        self.lineEdit_11.setGeometry(QtCore.QRect(440, 40, 113, 20))
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.lineEdit_12 = QtWidgets.QLineEdit(self.widget_4)
        self.lineEdit_12.setGeometry(QtCore.QRect(160, 70, 113, 20))
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.pushButton_4 = QtWidgets.QPushButton(self.widget_4)
        self.pushButton_4.setGeometry(QtCore.QRect(480, 130, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setText('444444444444')

        self.widget_5 = QtWidgets.QWidget(self.data_all_widget)
        self.widget_5.setGeometry(QtCore.QRect(30, 840, 600, 160))
        self.widget_5.setObjectName("widget_5")
        self.widget_5.setStyleSheet('background: #DDF9F8')
        self.label_5 = QtWidgets.QLabel(self.widget_5)
        self.label_5.setGeometry(QtCore.QRect(20, 10, 54, 12))
        self.label_5.setObjectName("label_5")
        self.label_5.setText('新增55555')
        self.lineEdit_13 = QtWidgets.QLineEdit(self.widget_5)
        self.lineEdit_13.setGeometry(QtCore.QRect(20, 40, 113, 20))
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.comboBox_13 = QtWidgets.QComboBox(self.widget_5)
        self.comboBox_13.setGeometry(QtCore.QRect(160, 40, 111, 22))
        self.comboBox_13.setObjectName("comboBox_13")
        self.comboBox_14 = QtWidgets.QComboBox(self.widget_5)
        self.comboBox_14.setGeometry(QtCore.QRect(300, 40, 111, 22))
        self.comboBox_14.setObjectName("comboBox_14")
        self.comboBox_15 = QtWidgets.QComboBox(self.widget_5)
        self.comboBox_15.setGeometry(QtCore.QRect(20, 70, 111, 22))
        self.comboBox_15.setObjectName("comboBox_15")
        self.lineEdit_14 = QtWidgets.QLineEdit(self.widget_5)
        self.lineEdit_14.setGeometry(QtCore.QRect(440, 40, 113, 20))
        self.lineEdit_14.setObjectName("lineEdit_14")
        self.lineEdit_15 = QtWidgets.QLineEdit(self.widget_5)
        self.lineEdit_15.setGeometry(QtCore.QRect(160, 70, 113, 20))
        self.lineEdit_15.setObjectName("lineEdit_15")
        self.pushButton_5 = QtWidgets.QPushButton(self.widget_5)
        self.pushButton_5.setGeometry(QtCore.QRect(480, 130, 75, 23))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setText('55555555555')

        self.verticalScrollBar = QtWidgets.QScrollBar(self.add_data_tab)
        self.verticalScrollBar.setMinimum(0)
        self.verticalScrollBar.setMaximum(10)
        self.verticalScrollBar.setGeometry(QtCore.QRect(680, 40, 20, 800))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")


    def add_project_page(self, value=False):
        base.consoleLog('新增项目运行界面')
        if value:
            return

        # 新增页签作为项目运行的页面
        self.project_tab = QtWidgets.QWidget()
        self.project_tab.setObjectName("project_tab")
        self.tabWidget.addTab(self.project_tab, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.project_tab), "项目运行")
        self.project_tab.setStyleSheet('background:#F2F2F2')

        #搜索条件
        self.project_name_lineEdit = QtWidgets.QLineEdit(self.project_tab)
        self.project_name_lineEdit.setGeometry(QtCore.QRect(10, 10, 90, 22))
        self.project_name_lineEdit.setPlaceholderText('项目名称')
        self.project_name_lineEdit.setObjectName("project_name_lineEdit")

        self.project_text_lineEdit = QtWidgets.QLineEdit(self.project_tab)
        self.project_text_lineEdit.setGeometry(QtCore.QRect(110, 10, 90, 20))
        self.project_text_lineEdit.setPlaceholderText('项目描述')
        self.project_text_lineEdit.setObjectName("project_text_lineEdit")

        self.project_executor_lineEdit = QtWidgets.QLineEdit(self.project_tab)
        self.project_executor_lineEdit.setGeometry(QtCore.QRect(210, 10, 90, 20))
        self.project_executor_lineEdit.setPlaceholderText('项目负责人')
        self.project_executor_lineEdit.setObjectName("project_executor_lineEdit")

        # 搜索
        self.project_search_pushButton = QtWidgets.QPushButton(self.project_tab)
        self.project_search_pushButton.setGeometry(QtCore.QRect(772, 10, 75, 28))
        self.project_search_pushButton.setObjectName("project_search_pushButton")
        self.project_search_pushButton.setText("搜索")
        self.project_search_pushButton.setStyleSheet('background-color:#20A0FF;color:white')
        self.project_search_pushButton.setFont(QFont("Arial",12,QFont.Bold))

        # # 关闭页面按钮
        # self.project_close_pushButton = QtWidgets.QPushButton(self.project_tab)
        # self.project_close_pushButton.setGeometry(QtCore.QRect(980, 5, 25, 20))
        # self.project_close_pushButton.setObjectName("project_close_pushButton")
        # self.project_close_pushButton.setText("X")
        # self.project_close_pushButton.setFont(QFont("Arial",12,QFont.Bold))
        # self.project_close_pushButton.setStyleSheet('background-color:white;color:red')

        # self.project_close_pushButton.setStyleSheet('color:red;border-radius:3px')ji


        # 表单运行及明细按钮
        self.project_PushButton1 = QtWidgets.QPushButton()
        self.project_PushButton1.setObjectName("project_PushButton1")
        self.project_PushButton1.setText("运行")
        self.project_PushButton2 = QtWidgets.QPushButton()
        self.project_PushButton2.setObjectName("project_PushButton2")
        self.project_PushButton2.setText("运行")
        self.project_PushButton3 = QtWidgets.QPushButton()
        self.project_PushButton3.setObjectName("project_PushButton3")
        self.project_PushButton3.setText("运行")
        self.project_PushButton4 = QtWidgets.QPushButton()
        self.project_PushButton4.setObjectName("project_PushButton4")
        self.project_PushButton4.setText("运行")
        self.project_PushButton5 = QtWidgets.QPushButton()
        self.project_PushButton5.setObjectName("project_PushButton5")
        self.project_PushButton5.setText("运行")
        self.project_PushButton6 = QtWidgets.QPushButton()
        self.project_PushButton6.setObjectName("project_PushButton6")
        self.project_PushButton6.setText("运行")
        self.project_PushButton7 = QtWidgets.QPushButton()
        self.project_PushButton7.setObjectName("project_PushButton7")
        self.project_PushButton7.setText("运行")
        self.project_PushButton8 = QtWidgets.QPushButton()
        self.project_PushButton8.setObjectName("project_PushButton8")
        self.project_PushButton8.setText("运行")
        self.project_PushButton9 = QtWidgets.QPushButton()
        self.project_PushButton9.setObjectName("project_PushButton9")
        self.project_PushButton9.setText("运行")
        self.project_PushButton10 = QtWidgets.QPushButton()
        self.project_PushButton10.setObjectName("project_PushButton10")
        self.project_PushButton10.setText("运行")
        self.project_PushButton11 = QtWidgets.QPushButton()
        self.project_PushButton11.setObjectName("project_PushButton11")
        self.project_PushButton11.setText("运行")
        self.project_PushButton12 = QtWidgets.QPushButton()
        self.project_PushButton12.setObjectName("project_PushButton12")
        self.project_PushButton12.setText("运行")
        self.project_PushButton13 = QtWidgets.QPushButton()
        self.project_PushButton13.setObjectName("project_PushButton13")
        self.project_PushButton13.setText("运行")
        self.project_PushButton14 = QtWidgets.QPushButton()
        self.project_PushButton14.setObjectName("project_PushButton14")
        self.project_PushButton14.setText("运行")
        self.project_PushButton15 = QtWidgets.QPushButton()
        self.project_PushButton15.setObjectName("project_PushButton15")
        self.project_PushButton15.setText("运行")
        self.project_PushButton16 = QtWidgets.QPushButton()
        self.project_PushButton16.setObjectName("project_PushButton16")
        self.project_PushButton16.setText("运行")
        self.project_PushButton17 = QtWidgets.QPushButton()
        self.project_PushButton17.setObjectName("project_PushButton17")
        self.project_PushButton17.setText("运行")
        self.project_PushButton18 = QtWidgets.QPushButton()
        self.project_PushButton18.setObjectName("project_PushButton18")
        self.project_PushButton18.setText("运行")
        self.project_PushButton19 = QtWidgets.QPushButton()
        self.project_PushButton19.setObjectName("project_PushButton19")
        self.project_PushButton19.setText("运行")
        self.project_PushButton20 = QtWidgets.QPushButton()
        self.project_PushButton20.setObjectName("project_PushButton20")
        self.project_PushButton20.setText("运行")
        self.project_PushButton21 = QtWidgets.QPushButton()
        self.project_PushButton21.setObjectName("project_PushButton21")
        self.project_PushButton21.setText("运行")
        self.project_PushButton22 = QtWidgets.QPushButton()
        self.project_PushButton22.setObjectName("project_PushButton22")
        self.project_PushButton22.setText("运行")
        self.project_PushButton23 = QtWidgets.QPushButton()
        self.project_PushButton23.setObjectName("project_PushButton23")
        self.project_PushButton23.setText("运行")
        self.project_PushButton24 = QtWidgets.QPushButton()
        self.project_PushButton24.setObjectName("project_PushButton24")
        self.project_PushButton24.setText("运行")
        self.project_PushButton25 = QtWidgets.QPushButton()
        self.project_PushButton25.setObjectName("project_PushButton25")
        self.project_PushButton25.setText("运行")
        self.project_PushButtonAll = {self.project_PushButton1: 1,
                                      self.project_PushButton2: 2,
                                      self.project_PushButton3: 3,
                                      self.project_PushButton4: 4,
                                      self.project_PushButton5: 5,
                                      self.project_PushButton6: 6,
                                      self.project_PushButton7: 7,
                                      self.project_PushButton8: 8,
                                      self.project_PushButton9: 9,
                                      self.project_PushButton10: 10,
                                      self.project_PushButton11: 11,
                                      self.project_PushButton12: 12,
                                      self.project_PushButton13: 13,
                                      self.project_PushButton14: 14,
                                      self.project_PushButton15: 15,
                                      self.project_PushButton16: 16,
                                      self.project_PushButton17: 17,
                                      self.project_PushButton18: 18,
                                      self.project_PushButton19: 19,
                                      self.project_PushButton20: 20,
                                      self.project_PushButton21: 21,
                                      self.project_PushButton22: 22,
                                      self.project_PushButton23: 23,
                                      self.project_PushButton24: 24,
                                      self.project_PushButton25: 25
                                      }

        self.project_detailed_PushButton1 = QtWidgets.QPushButton()
        self.project_detailed_PushButton1.setObjectName("project_detailed_PushButton1")
        self.project_detailed_PushButton1.setText("明细")
        self.project_detailed_PushButton2 = QtWidgets.QPushButton()
        self.project_detailed_PushButton2.setObjectName("project_detailed_PushButton2")
        self.project_detailed_PushButton2.setText("明细")
        self.project_detailed_PushButton3 = QtWidgets.QPushButton()
        self.project_detailed_PushButton3.setObjectName("project_detailed_PushButton3")
        self.project_detailed_PushButton3.setText("明细")
        self.project_detailed_PushButton4 = QtWidgets.QPushButton()
        self.project_detailed_PushButton4.setObjectName("project_detailed_PushButton4")
        self.project_detailed_PushButton4.setText("明细")
        self.project_detailed_PushButton5 = QtWidgets.QPushButton()
        self.project_detailed_PushButton5.setObjectName("project_detailed_PushButton5")
        self.project_detailed_PushButton5.setText("明细")
        self.project_detailed_PushButton6 = QtWidgets.QPushButton()
        self.project_detailed_PushButton6.setObjectName("project_detailed_PushButton6")
        self.project_detailed_PushButton6.setText("明细")
        self.project_detailed_PushButton7 = QtWidgets.QPushButton()
        self.project_detailed_PushButton7.setObjectName("project_detailed_PushButton7")
        self.project_detailed_PushButton7.setText("明细")
        self.project_detailed_PushButton8 = QtWidgets.QPushButton()
        self.project_detailed_PushButton8.setObjectName("project_detailed_PushButton8")
        self.project_detailed_PushButton8.setText("明细")
        self.project_detailed_PushButton9 = QtWidgets.QPushButton()
        self.project_detailed_PushButton9.setObjectName("project_detailed_PushButton9")
        self.project_detailed_PushButton9.setText("明细")
        self.project_detailed_PushButton10 = QtWidgets.QPushButton()
        self.project_detailed_PushButton10.setObjectName("project_detailed_PushButton10")
        self.project_detailed_PushButton10.setText("明细")
        self.project_detailed_PushButton11 = QtWidgets.QPushButton()
        self.project_detailed_PushButton11.setObjectName("project_detailed_PushButton11")
        self.project_detailed_PushButton11.setText("明细")
        self.project_detailed_PushButton12 = QtWidgets.QPushButton()
        self.project_detailed_PushButton12.setObjectName("project_detailed_PushButton12")
        self.project_detailed_PushButton12.setText("明细")
        self.project_detailed_PushButton13 = QtWidgets.QPushButton()
        self.project_detailed_PushButton13.setObjectName("project_detailed_PushButton13")
        self.project_detailed_PushButton13.setText("明细")
        self.project_detailed_PushButton14 = QtWidgets.QPushButton()
        self.project_detailed_PushButton14.setObjectName("project_detailed_PushButton14")
        self.project_detailed_PushButton14.setText("明细")
        self.project_detailed_PushButton15 = QtWidgets.QPushButton()
        self.project_detailed_PushButton15.setObjectName("project_detailed_PushButton15")
        self.project_detailed_PushButton15.setText("明细")
        self.project_detailed_PushButton16 = QtWidgets.QPushButton()
        self.project_detailed_PushButton16.setObjectName("project_detailed_PushButton16")
        self.project_detailed_PushButton16.setText("明细")
        self.project_detailed_PushButton17 = QtWidgets.QPushButton()
        self.project_detailed_PushButton17.setObjectName("project_detailed_PushButton17")
        self.project_detailed_PushButton17.setText("明细")
        self.project_detailed_PushButton18 = QtWidgets.QPushButton()
        self.project_detailed_PushButton18.setObjectName("project_detailed_PushButton18")
        self.project_detailed_PushButton18.setText("明细")
        self.project_detailed_PushButton19 = QtWidgets.QPushButton()
        self.project_detailed_PushButton19.setObjectName("project_detailed_PushButton19")
        self.project_detailed_PushButton19.setText("明细")
        self.project_detailed_PushButton20 = QtWidgets.QPushButton()
        self.project_detailed_PushButton20.setObjectName("project_detailed_PushButton20")
        self.project_detailed_PushButton20.setText("明细")
        self.project_detailed_PushButton21 = QtWidgets.QPushButton()
        self.project_detailed_PushButton21.setObjectName("project_detailed_PushButton21")
        self.project_detailed_PushButton21.setText("明细")
        self.project_detailed_PushButton22 = QtWidgets.QPushButton()
        self.project_detailed_PushButton22.setObjectName("project_detailed_PushButton22")
        self.project_detailed_PushButton22.setText("明细")
        self.project_detailed_PushButton23 = QtWidgets.QPushButton()
        self.project_detailed_PushButton23.setObjectName("project_detailed_PushButton23")
        self.project_detailed_PushButton23.setText("明细")
        self.project_detailed_PushButton24 = QtWidgets.QPushButton()
        self.project_detailed_PushButton24.setObjectName("project_detailed_PushButton24")
        self.project_detailed_PushButton24.setText("明细")
        self.project_detailed_PushButton25 = QtWidgets.QPushButton()
        self.project_detailed_PushButton25.setObjectName("project_detailed_PushButton25")
        self.project_detailed_PushButton25.setText("明细")
        self.project_detailed_PushButtonAll = {self.project_detailed_PushButton1: 1,
                                               self.project_detailed_PushButton2: 2,
                                               self.project_detailed_PushButton3: 3,
                                               self.project_detailed_PushButton4: 4,
                                               self.project_detailed_PushButton5: 5,
                                               self.project_detailed_PushButton6: 6,
                                               self.project_detailed_PushButton7: 7,
                                               self.project_detailed_PushButton8: 8,
                                               self.project_detailed_PushButton9: 9,
                                               self.project_detailed_PushButton10: 10,
                                               self.project_detailed_PushButton11: 11,
                                               self.project_detailed_PushButton12: 12,
                                               self.project_detailed_PushButton13: 13,
                                               self.project_detailed_PushButton14: 14,
                                               self.project_detailed_PushButton15: 15,
                                               self.project_detailed_PushButton16: 16,
                                               self.project_detailed_PushButton17: 17,
                                               self.project_detailed_PushButton18: 18,
                                               self.project_detailed_PushButton19: 19,
                                               self.project_detailed_PushButton20: 20,
                                               self.project_detailed_PushButton21: 21,
                                               self.project_detailed_PushButton22: 22,
                                               self.project_detailed_PushButton23: 23,
                                               self.project_detailed_PushButton24: 24,
                                               self.project_detailed_PushButton25: 25
                                               }

        # 列表展示
        self.project_tableWidget = QtWidgets.QTableWidget(self.project_tab)
        self.project_tableWidget.setGeometry(QtCore.QRect(10, 50, 921, 795))
        self.project_tableWidget.setObjectName("project_tableWidget")
        self.project_tableWidget.setColumnCount(7)
        self.project_tableWidget.setColumnWidth(0, 100)
        self.project_tableWidget.setColumnWidth(1, 350)
        self.project_tableWidget.setColumnWidth(2, 150)
        self.project_tableWidget.setColumnWidth(3, 80)
        self.project_tableWidget.setColumnWidth(4, 80)
        self.project_tableWidget.setColumnWidth(5, 80)
        self.project_tableWidget.setColumnWidth(6, 80)
        self.project_tableWidget.setRowCount(25)
        # 表单插入25*7的格子
        for i in range(25):
            for j in range(7):
                item = QtWidgets.QTableWidgetItem()
                self.project_tableWidget.setVerticalHeaderItem(i, item)
                item = QtWidgets.QTableWidgetItem()
                self.project_tableWidget.setHorizontalHeaderItem(j, item)
        # 表单首列1-30
        for i in range(25):
            item = self.project_tableWidget.verticalHeaderItem(i)
            item.setText(str(i + 1))
        self.project_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 列表禁止编辑
        # 表的头部
        item = self.project_tableWidget.horizontalHeaderItem(0)
        item.setText("项目名称")
        item = self.project_tableWidget.horizontalHeaderItem(1)
        item.setText("项目描述")
        item = self.project_tableWidget.horizontalHeaderItem(2)
        item.setText("最近执行时间")
        item = self.project_tableWidget.horizontalHeaderItem(3)
        item.setText("最近执行结果")
        item = self.project_tableWidget.horizontalHeaderItem(4)
        item.setText("项目负责人")
        item = self.project_tableWidget.horizontalHeaderItem(5)
        item.setText("操作-运行")
        item = self.project_tableWidget.horizontalHeaderItem(6)
        item.setText("操作-明细")

        # 运行,详情按钮加载到表格中
        key = list(self.project_PushButtonAll.keys())
        for i in range(len(key)):
            self.project_tableWidget.setCellWidget(i, 5, key[i])

        key = list(self.project_detailed_PushButtonAll.keys())
        for i in range(len(key)):
            self.project_tableWidget.setCellWidget(i, 6, key[i])

        # 不显示垂直表头
        # self.project_tableWidget.setShowGrid(False)
        self.project_tableWidget.verticalHeader().setVisible(False)
        # 表头上颜色
        self.project_tableWidget.setStyleSheet(
            "QHeaderView::section{background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgb(46,46,46),stop:1 rgb(66,66,66));color: rgb(210,210,210);;padding-left: 4px;border: 1px solid #383838;}")
        self.project_tableWidget.setStyleSheet(

            "background: rgb(221,249,248);alternate-background-color:rgb(48,51,180);selection-background-color:qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgb(56,56,230),stop:1 rgb(174,253,188));"
        )

        # 列表下方搜索
        # 上一页
        self.project_previous_page_pushButton = QtWidgets.QPushButton(self.project_tab)
        self.project_previous_page_pushButton.setGeometry(QtCore.QRect(10, 850, 75, 23))
        self.project_previous_page_pushButton.setObjectName("project_previous_page_pushButton")
        self.project_previous_page_pushButton.setText('上一页')
        self.project_previous_page_pushButton.setStyleSheet('background-color:#20A0FF')

        # 当前页
        self.project_current_page_label = QtWidgets.QLabel(self.project_tab)
        self.project_current_page_label.setGeometry(QtCore.QRect(90, 850, 35, 21))
        self.project_current_page_label.setObjectName("project_current_page_label")
        self.project_current_page_label.setText('0/0')
        # 下一页
        self.project_next_page_pushButton = QtWidgets.QPushButton(self.project_tab)
        self.project_next_page_pushButton.setGeometry(QtCore.QRect(120, 850, 75, 23))
        self.project_next_page_pushButton.setObjectName("project_next_page_pushButton")
        self.project_next_page_pushButton.setText('下一页')
        self.project_next_page_pushButton.setStyleSheet('background-color:#20A0FF')

        # 项目数量
        self.project_total_amount_of_label = QtWidgets.QLabel(self.project_tab)
        self.project_total_amount_of_label.setGeometry(QtCore.QRect(230, 850, 55, 21))
        self.project_total_amount_of_label.setObjectName("project_total_amount_of_label")
        self.project_total_amount_of_label.setText('项目总数')
        self.project_total_amount_of_lineEdit = QtWidgets.QLineEdit(self.project_tab)
        self.project_total_amount_of_lineEdit.setGeometry(QtCore.QRect(280, 850, 90, 20))
        self.project_total_amount_of_lineEdit.setReadOnly(True)
        self.project_total_amount_of_lineEdit.setObjectName("project_total_amount_of_lineEdit")

    def add_financial_repayment_page(self, value=False):
        """
        生成还款计划页面
        :param:value = False 才可以生成页面
        :return:
        """
        base.consoleLog('生成还款计划页面')
        if value:
            return

        # 新增页签作为还款计划的页面
        self.financial_repayment_tab = QtWidgets.QWidget()
        self.financial_repayment_tab.setObjectName("financial_repayment_tab")
        self.tabWidget.addTab(self.financial_repayment_tab, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.financial_repayment_tab), "还款计划")

        # 搜索条件
        # 银行类型
        self.financial_repayment_bank_comboBox = QtWidgets.QComboBox(self.financial_repayment_tab)
        self.financial_repayment_bank_comboBox.setGeometry(QtCore.QRect(10, 10, 90, 22))
        self.financial_repayment_bank_comboBox.setObjectName("financial_repayment_bank_comboBox")
        self.financial_repayment_bank_comboBox.addItem("")
        self.financial_repayment_bank_comboBox.addItem("")
        self.financial_repayment_bank_comboBox.addItem("")
        self.financial_repayment_bank_comboBox.addItem("")
        self.financial_repayment_bank_comboBox.addItem("")
        self.financial_repayment_bank_comboBox.addItem("")
        self.financial_repayment_bank_comboBox.addItem("")
        self.financial_repayment_bank_comboBox.addItem("")
        self.financial_repayment_bank_comboBox.setItemText(0, "全部还款")
        self.financial_repayment_bank_comboBox.setItemText(1, "借呗")
        self.financial_repayment_bank_comboBox.setItemText(2, "花旗")
        self.financial_repayment_bank_comboBox.setItemText(3, "招行e")
        self.financial_repayment_bank_comboBox.setItemText(4, "房贷")
        self.financial_repayment_bank_comboBox.setItemText(5, "农村信用社")
        self.financial_repayment_bank_comboBox.setItemText(6, "花旗")
        self.financial_repayment_bank_comboBox.setItemText(7, "微粒贷")
        # 账单开始日、结束日
        self.financial_repayment_bill_starting_date_lineEdit = QtWidgets.QLineEdit(self.financial_repayment_tab)
        self.financial_repayment_bill_starting_date_lineEdit.setGeometry(QtCore.QRect(110, 10, 90, 20))
        self.financial_repayment_bill_starting_date_lineEdit.setPlaceholderText('账单开始日')
        self.financial_repayment_bill_starting_date_lineEdit.setObjectName(
            "financial_repayment_bill_starting_date_lineEdit")
        self.financial_repayment_bill_closing_date_lineEdit = QtWidgets.QLineEdit(self.financial_repayment_tab)
        self.financial_repayment_bill_closing_date_lineEdit.setGeometry(QtCore.QRect(210, 10, 90, 20))
        self.financial_repayment_bill_closing_date_lineEdit.setPlaceholderText('账单结束日')
        self.financial_repayment_bill_closing_date_lineEdit.setObjectName(
            "financial_repayment_bill_closing_date_lineEdit")
        # 还款开始日、结束日
        self.financial_repayment_starting_date_lineEdit = QtWidgets.QLineEdit(self.financial_repayment_tab)
        self.financial_repayment_starting_date_lineEdit.setGeometry(QtCore.QRect(310, 10, 90, 20))
        self.financial_repayment_starting_date_lineEdit.setPlaceholderText('还款开始日')
        self.financial_repayment_starting_date_lineEdit.setObjectName("financial_repayment_starting_date_lineEdit")
        self.financial_repayment_closing_date_lineEdit = QtWidgets.QLineEdit(self.financial_repayment_tab)
        self.financial_repayment_closing_date_lineEdit.setGeometry(QtCore.QRect(410, 10, 90, 20))
        self.financial_repayment_closing_date_lineEdit.setPlaceholderText('还款结束日')
        self.financial_repayment_closing_date_lineEdit.setObjectName("financial_repayment_closing_date_lineEdit")
        # 搜索，新增按钮
        self.financial_repayment_search_pushButton = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.financial_repayment_search_pushButton.setGeometry(QtCore.QRect(532, 10, 75, 23))
        self.financial_repayment_search_pushButton.setObjectName("financial_repayment_search_pushButton")
        self.financial_repayment_search_pushButton.setText("搜索")
        self.financial_repayment_add_pushButton = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.financial_repayment_add_pushButton.setGeometry(QtCore.QRect(632, 10, 75, 23))
        self.financial_repayment_add_pushButton.setObjectName("financial_repayment_add_pushButton")
        self.financial_repayment_add_pushButton.setText("新增")

        self.financial_repayment_czl_label = QtWidgets.QLabel(self.financial_repayment_tab)
        self.financial_repayment_czl_label.setGeometry(QtCore.QRect(520, 50, 75, 23))
        self.financial_repayment_czl_label.setObjectName("financial_repayment_czl_label")
        self.financial_repayment_czl_label.setText('    操作栏   ')
        self.inancial_repayment_PushButton1 = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.inancial_repayment_PushButton1.setGeometry(QtCore.QRect(530, 74, 75, 33))
        self.inancial_repayment_PushButton1.setObjectName("inancial_repayment_PushButton1")
        self.inancial_repayment_PushButton1.setText("详情")
        self.inancial_repayment_PushButton2 = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.inancial_repayment_PushButton2.setGeometry(QtCore.QRect(530, 104, 75, 33))
        self.inancial_repayment_PushButton2.setObjectName("inancial_repayment_PushButton2")
        self.inancial_repayment_PushButton2.setText("详情")
        self.inancial_repayment_PushButton3 = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.inancial_repayment_PushButton3.setGeometry(QtCore.QRect(530, 134, 75, 33))
        self.inancial_repayment_PushButton3.setObjectName("inancial_repayment_PushButton3")
        self.inancial_repayment_PushButton3.setText("详情")
        self.inancial_repayment_PushButton4 = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.inancial_repayment_PushButton4.setGeometry(QtCore.QRect(530, 164, 75, 33))
        self.inancial_repayment_PushButton4.setObjectName("inancial_repayment_PushButton4")
        self.inancial_repayment_PushButton4.setText("详情")
        self.inancial_repayment_PushButton5 = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.inancial_repayment_PushButton5.setGeometry(QtCore.QRect(530, 194, 75, 33))
        self.inancial_repayment_PushButton5.setObjectName("inancial_repayment_PushButton5")
        self.inancial_repayment_PushButton5.setText("详情")
        self.inancial_repayment_PushButton6 = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.inancial_repayment_PushButton6.setGeometry(QtCore.QRect(530, 224, 75, 33))
        self.inancial_repayment_PushButton6.setObjectName("inancial_repayment_PushButton6")
        self.inancial_repayment_PushButton6.setText("详情")
        self.inancial_repayment_PushButton7 = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.inancial_repayment_PushButton7.setGeometry(QtCore.QRect(530, 254, 75, 33))
        self.inancial_repayment_PushButton7.setObjectName("inancial_repayment_PushButton7")
        self.inancial_repayment_PushButton7.setText("详情")
        self.inancial_repayment_PushButton8 = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.inancial_repayment_PushButton8.setGeometry(QtCore.QRect(530, 284, 75, 33))
        self.inancial_repayment_PushButton8.setObjectName("inancial_repayment_PushButton8")
        self.inancial_repayment_PushButton8.setText("详情")
        self.inancial_repayment_PushButton9 = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.inancial_repayment_PushButton9.setGeometry(QtCore.QRect(530, 314, 75, 33))
        self.inancial_repayment_PushButton9.setObjectName("inancial_repayment_PushButton9")
        self.inancial_repayment_PushButton9.setText("详情")
        self.inancial_repayment_PushButton10 = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.inancial_repayment_PushButton10.setGeometry(QtCore.QRect(530, 344, 75, 33))
        self.inancial_repayment_PushButton10.setObjectName("inancial_repayment_PushButton10")
        self.inancial_repayment_PushButton10.setText("详情")
        self.inancial_repayment_PushButton11 = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.inancial_repayment_PushButton11.setGeometry(QtCore.QRect(530, 374, 75, 33))
        self.inancial_repayment_PushButton11.setObjectName("inancial_repayment_PushButton11")
        self.inancial_repayment_PushButton11.setText("详情")
        self.inancial_repayment_PushButton12 = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.inancial_repayment_PushButton12.setGeometry(QtCore.QRect(530, 404, 75, 33))
        self.inancial_repayment_PushButton12.setObjectName("inancial_repayment_PushButton12")
        self.inancial_repayment_PushButton12.setText("详情")
        self.inancial_repayment_PushButton13 = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.inancial_repayment_PushButton13.setGeometry(QtCore.QRect(530, 434, 75, 33))
        self.inancial_repayment_PushButton13.setObjectName("inancial_repayment_PushButton13")
        self.inancial_repayment_PushButton13.setText("详情")
        self.inancial_repayment_PushButton14 = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.inancial_repayment_PushButton14.setGeometry(QtCore.QRect(530, 464, 75, 33))
        self.inancial_repayment_PushButton14.setObjectName("inancial_repayment_PushButton14")
        self.inancial_repayment_PushButton14.setText("详情")
        self.inancial_repayment_PushButton15 = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.inancial_repayment_PushButton15.setGeometry(QtCore.QRect(530, 494, 75, 33))
        self.inancial_repayment_PushButton15.setObjectName("inancial_repayment_PushButton15")
        self.inancial_repayment_PushButton15.setText("详情")
        self.inancial_repayment_PushButton16 = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.inancial_repayment_PushButton16.setGeometry(QtCore.QRect(530, 524, 75, 33))
        self.inancial_repayment_PushButton16.setObjectName("inancial_repayment_PushButton16")
        self.inancial_repayment_PushButton16.setText("详情")
        self.inancial_repayment_PushButton17 = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.inancial_repayment_PushButton17.setGeometry(QtCore.QRect(530, 554, 75, 33))
        self.inancial_repayment_PushButton17.setObjectName("inancial_repayment_PushButton17")
        self.inancial_repayment_PushButton17.setText("详情")
        self.inancial_repayment_PushButton18 = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.inancial_repayment_PushButton18.setGeometry(QtCore.QRect(530, 584, 75, 33))
        self.inancial_repayment_PushButton18.setObjectName("inancial_repayment_PushButton18")
        self.inancial_repayment_PushButton18.setText("详情")
        self.inancial_repayment_PushButton19 = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.inancial_repayment_PushButton19.setGeometry(QtCore.QRect(530, 614, 75, 33))
        self.inancial_repayment_PushButton19.setObjectName("inancial_repayment_PushButton19")
        self.inancial_repayment_PushButton19.setText("详情")
        self.inancial_repayment_PushButton20 = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.inancial_repayment_PushButton20.setGeometry(QtCore.QRect(530, 644, 75, 33))
        self.inancial_repayment_PushButton20.setObjectName("inancial_repayment_PushButton20")
        self.inancial_repayment_PushButton20.setText("详情")
        self.inancial_repayment_PushButton21 = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.inancial_repayment_PushButton21.setGeometry(QtCore.QRect(530, 674, 75, 33))
        self.inancial_repayment_PushButton21.setObjectName("inancial_repayment_PushButton21")
        self.inancial_repayment_PushButton21.setText("详情")
        self.inancial_repayment_PushButton22 = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.inancial_repayment_PushButton22.setGeometry(QtCore.QRect(530, 704, 75, 33))
        self.inancial_repayment_PushButton22.setObjectName("inancial_repayment_PushButton22")
        self.inancial_repayment_PushButton22.setText("详情")
        self.inancial_repayment_PushButton23 = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.inancial_repayment_PushButton23.setGeometry(QtCore.QRect(530, 734, 75, 33))
        self.inancial_repayment_PushButton23.setObjectName("inancial_repayment_PushButton23")
        self.inancial_repayment_PushButton23.setText("详情")
        self.inancial_repayment_PushButton24 = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.inancial_repayment_PushButton24.setGeometry(QtCore.QRect(530, 764, 75, 33))
        self.inancial_repayment_PushButton24.setObjectName("inancial_repayment_PushButton24")
        self.inancial_repayment_PushButton24.setText("详情")
        self.inancial_repayment_PushButton25 = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.inancial_repayment_PushButton25.setGeometry(QtCore.QRect(530, 794, 75, 33))
        self.inancial_repayment_PushButton25.setObjectName("inancial_repayment_PushButton25")
        self.inancial_repayment_PushButton25.setText("详情")
        self.inancial_repayment_PushButtonAll = {self.inancial_repayment_PushButton1: 1,
                                                 self.inancial_repayment_PushButton2: 2,
                                                 self.inancial_repayment_PushButton3: 3,
                                                 self.inancial_repayment_PushButton4: 4,
                                                 self.inancial_repayment_PushButton5: 5,
                                                 self.inancial_repayment_PushButton6: 6,
                                                 self.inancial_repayment_PushButton7: 7,
                                                 self.inancial_repayment_PushButton8: 8,
                                                 self.inancial_repayment_PushButton9: 9,
                                                 self.inancial_repayment_PushButton10: 10,
                                                 self.inancial_repayment_PushButton11: 11,
                                                 self.inancial_repayment_PushButton12: 12,
                                                 self.inancial_repayment_PushButton13: 13,
                                                 self.inancial_repayment_PushButton14: 14,
                                                 self.inancial_repayment_PushButton15: 15,
                                                 self.inancial_repayment_PushButton16: 16,
                                                 self.inancial_repayment_PushButton17: 17,
                                                 self.inancial_repayment_PushButton18: 18,
                                                 self.inancial_repayment_PushButton19: 19,
                                                 self.inancial_repayment_PushButton20: 20,
                                                 self.inancial_repayment_PushButton21: 21,
                                                 self.inancial_repayment_PushButton22: 22,
                                                 self.inancial_repayment_PushButton23: 23,
                                                 self.inancial_repayment_PushButton24: 24,
                                                 self.inancial_repayment_PushButton25: 25
                                                 }

        # 列表展示
        self.financial_repayment_tableWidget = QtWidgets.QTableWidget(self.financial_repayment_tab)
        self.financial_repayment_tableWidget.setGeometry(QtCore.QRect(10, 50, 521, 795))
        self.financial_repayment_tableWidget.setObjectName("financial_repayment_tableWidget")
        self.financial_repayment_tableWidget.setColumnCount(5)
        self.financial_repayment_tableWidget.setRowCount(25)
        # 表单插入25*5的格子
        for i in range(25):
            for j in range(5):
                item = QtWidgets.QTableWidgetItem()
                self.financial_repayment_tableWidget.setVerticalHeaderItem(i, item)
                item = QtWidgets.QTableWidgetItem()
                self.financial_repayment_tableWidget.setHorizontalHeaderItem(j, item)
        # 表单首列1-30
        for i in range(25):
            item = self.financial_repayment_tableWidget.verticalHeaderItem(i)
            item.setText(str(i + 1))
        self.financial_repayment_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 列表禁止编辑
        # 表的头部
        item = self.financial_repayment_tableWidget.horizontalHeaderItem(0)
        item.setText("还款类型")
        item = self.financial_repayment_tableWidget.horizontalHeaderItem(1)
        item.setText("账单日")
        item = self.financial_repayment_tableWidget.horizontalHeaderItem(2)
        item.setText("还款日")
        item = self.financial_repayment_tableWidget.horizontalHeaderItem(3)
        item.setText("还款期数")
        item = self.financial_repayment_tableWidget.horizontalHeaderItem(4)
        item.setText("金额")

        # 列表下方搜索
        # 上一页
        self.financial_repayment_previous_page_pushButton = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.financial_repayment_previous_page_pushButton.setGeometry(QtCore.QRect(10, 850, 75, 23))
        self.financial_repayment_previous_page_pushButton.setObjectName("financial_repayment_previous_page_pushButton")
        self.financial_repayment_previous_page_pushButton.setText('上一页')
        # 当前页
        self.financial_repayment_current_page_label = QtWidgets.QLabel(self.financial_repayment_tab)
        self.financial_repayment_current_page_label.setGeometry(QtCore.QRect(90, 850, 35, 21))
        self.financial_repayment_current_page_label.setObjectName("financial_repayment_current_page_label")
        self.financial_repayment_current_page_label.setText('0/0')
        # 下一页
        self.financial_repayment_next_page_pushButton = QtWidgets.QPushButton(self.financial_repayment_tab)
        self.financial_repayment_next_page_pushButton.setGeometry(QtCore.QRect(120, 850, 75, 23))
        self.financial_repayment_next_page_pushButton.setObjectName("financial_repayment_next_page_pushButton")
        self.financial_repayment_next_page_pushButton.setText('下一页')
        # 还款金额总和
        self.financial_repayment_total_amount_of_repayment_label = QtWidgets.QLabel(self.financial_repayment_tab)
        self.financial_repayment_total_amount_of_repayment_label.setGeometry(QtCore.QRect(230, 850, 55, 21))
        self.financial_repayment_total_amount_of_repayment_label.setObjectName(
            "financial_repayment_total_amount_of_repayment_label")
        self.financial_repayment_total_amount_of_repayment_label.setText('金额总和')
        self.financial_repayment_total_amount_of_repayment_lineEdit = QtWidgets.QLineEdit(self.financial_repayment_tab)
        self.financial_repayment_total_amount_of_repayment_lineEdit.setGeometry(QtCore.QRect(280, 850, 90, 20))
        self.financial_repayment_total_amount_of_repayment_lineEdit.setReadOnly(True)
        self.financial_repayment_total_amount_of_repayment_lineEdit.setObjectName(
            "financial_repayment_total_amount_of_repayment_lineEdit")
        # 还款笔数
        self.financial_repayment_amount_label = QtWidgets.QLabel(self.financial_repayment_tab)
        self.financial_repayment_amount_label.setGeometry(QtCore.QRect(410, 850, 55, 21))
        self.financial_repayment_amount_label.setObjectName("financial_repayment_amount_label")
        self.financial_repayment_amount_label.setText('笔数')
        self.financial_repayment_amount_lineEdit = QtWidgets.QLineEdit(self.financial_repayment_tab)
        self.financial_repayment_amount_lineEdit.setGeometry(QtCore.QRect(440, 850, 90, 20))
        self.financial_repayment_amount_lineEdit.setReadOnly(True)
        self.financial_repayment_amount_lineEdit.setObjectName("financial_repayment_amount_lineEdit")

    def add_financial_repayment_datapage(self):
        """
        :return:
        """
        base.consoleLog('新增财务还款计划数据')
        self.financial_repayment_datapage = QDialog(self)
        self.financial_repayment_datapage.setWindowTitle('新增财务还款计划数据')
        self.financial_repayment_datapage.resize(400, 300)
        self.add_financial_repayment_button = QPushButton("保存", self.financial_repayment_datapage)
        self.add_financial_repayment_button.setGeometry(QtCore.QRect(250, 230, 75, 23))
        self.add_financial_repayment_button.show()
        self.add_financial_repayment_button.clicked.connect(self.get_financial_repayment_datapage)
        self.add_financial_repayment_button.clicked.connect(self.select_financial_repayment_list)
        flo = QFormLayout(self.financial_repayment_datapage)
        flo.addRow(QLabel())
        flo.addRow(QLabel())
        flo.addRow(QLabel())

        self.add_assetType = QComboBox(self.financial_repayment_datapage)
        self.add_assetType.addItems(['房贷', '借呗', '招行e', '华夏', '农村信用社', '花旗银行', '微粒贷'])
        flo.addRow("    还款类型", self.add_assetType)

        self.add_statementDateLineEdit = QLineEdit(self.financial_repayment_datapage)
        self.add_statementDateLineEdit.setPlaceholderText('请输入账单日')
        flo.addRow("      账单日", self.add_statementDateLineEdit)

        self.add_repaymentDateLineEdit = QLineEdit(self.financial_repayment_datapage)
        self.add_repaymentDateLineEdit.setPlaceholderText('请输入还款日')
        flo.addRow("      还款日", self.add_repaymentDateLineEdit)

        self.add_repaymentPeriodLineEdit = QLineEdit(self.financial_repayment_datapage)
        self.add_repaymentPeriodLineEdit.setPlaceholderText('请输入期数')
        flo.addRow("        期数", self.add_repaymentPeriodLineEdit)

        self.add_repaymentAmountLineEdit = QLineEdit(self.financial_repayment_datapage)
        self.add_repaymentAmountLineEdit.setPlaceholderText('请输入每期金额')
        flo.addRow("        金额", self.add_repaymentAmountLineEdit)

        self.financial_repayment_datapage.setLayout(flo)
        self.financial_repayment_datapage.show()

    def get_financial_repayment_datapage(self):
        """
        :return:
        """
        base.consoleLog('获取新增的还款计划的数据')
        assetTypeData = QComboBox.currentText(self.add_assetType)
        statementDateData = QLineEdit.displayText(self.add_statementDateLineEdit)
        repaymentDateData = QLineEdit.displayText(self.add_repaymentDateLineEdit)
        repaymentPeriodDateData = QLineEdit.displayText(self.add_repaymentPeriodLineEdit)
        repaymentAmountDate = QLineEdit.displayText(self.add_repaymentAmountLineEdit)

        if statementDateData == '' or repaymentDateData == '' or repaymentPeriodDateData == '' or repaymentAmountDate == '':
            QMessageBox.about(self, "提示", "您有部分数据为空，请输入完整信息之后再点击保存!")
            return

        # 每次新增相同类型的贷款,要把现有的数据逻辑删除
        sql = """UPDATE financial_repayment_data set deleted=1,update_time='%s' where asset_type='%s' and deleted=0;""" % (
        base.time_time(), assetTypeData)
        MySqlite(sql).update_sql()

        day = statementDateData[8:10]
        days = repaymentDateData[8:10]
        for i in range(int(repaymentPeriodDateData)):
            statementDateDatas = str(
                datetime.datetime.strptime(statementDateData, '%Y-%m-%d') + datetime.timedelta(days=(30 * i)))[
                                 0:8] + day
            repaymentDateDatas = str(
                datetime.datetime.strptime(repaymentDateData, '%Y-%m-%d') + datetime.timedelta(days=(30 * i)))[
                                 0:8] + days

            sql = """select statement_date from financial_repayment_data where asset_type = "%s" and deleted=0 and statement_date ="%s" """ % (
            assetTypeData, statementDateDatas)
            statement_date_ = MySqlite(sql).select_sql()
            try:
                if statement_date_[0][0]:
                    statementDateDatas = str(
                        datetime.datetime.strptime(statementDateData, '%Y-%m-%d') + datetime.timedelta(
                            days=(30 * (i + 1))))[
                                         0:8] + day
            except:
                pass

            sql = """select repayment_date from financial_repayment_data where asset_type = "%s" and deleted=0 and repayment_date ="%s" """ % (
                assetTypeData, repaymentDateDatas)
            repaymentDateDatas_ = MySqlite(sql).select_sql()
            try:
                if repaymentDateDatas_[0][0]:
                    repaymentDateDatas = str(
                        datetime.datetime.strptime(repaymentDateData, '%Y-%m-%d') + datetime.timedelta(
                            days=(30 * (i + 1))))[
                                         0:8] + days
            except:
                pass

            sql = """INSERT INTO financial_repayment_data VALUES (null,'%s', '%s', '%s', '%s','待还款','%s','%s','%s',0 );
        """ % (assetTypeData, statementDateDatas, repaymentDateDatas, str(i + 1), repaymentAmountDate, base.time_time(),
               base.time_time())
            MySqlite(sql).insert_sql()
        QMessageBox.about(self, "提示", "您的还款计划生成成功!")
        self.financial_repayment_datapage.close()
        return

    def add_financial_flow_page(self, value=False):
        """
        生成财务流水页面
        :param value:
        :return:
        """
        base.consoleLog('生成财务流水页面')
        if value:
            return
        # 新增页签作为财务流水的页面
        self.financial_flow_tab = QtWidgets.QWidget()
        self.financial_flow_tab.setObjectName("financial_flow_tab")
        self.tabWidget.addTab(self.financial_flow_tab, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.financial_flow_tab), "财务流水")

        # 搜索条件
        # 流水类型
        self.financial_flow_type_comboBox = QtWidgets.QComboBox(self.financial_flow_tab)
        self.financial_flow_type_comboBox.setGeometry(QtCore.QRect(10, 10, 90, 22))
        self.financial_flow_type_comboBox.setObjectName("financial_flow_type_comboBox")
        self.financial_flow_type_comboBox.addItem("")
        self.financial_flow_type_comboBox.addItem("")
        self.financial_flow_type_comboBox.addItem("")
        self.financial_flow_type_comboBox.addItem("")
        self.financial_flow_type_comboBox.addItem("")
        self.financial_flow_type_comboBox.addItem("")
        self.financial_flow_type_comboBox.addItem("")
        self.financial_flow_type_comboBox.addItem("")
        self.financial_flow_type_comboBox.setItemText(0, "全部消费")
        self.financial_flow_type_comboBox.setItemText(1, "房租水电")
        self.financial_flow_type_comboBox.setItemText(2, "外出玩乐")
        self.financial_flow_type_comboBox.setItemText(3, "交通费")
        self.financial_flow_type_comboBox.setItemText(4, "还信用卡")
        self.financial_flow_type_comboBox.setItemText(5, "生活用品")
        self.financial_flow_type_comboBox.setItemText(6, "其他")
        self.financial_flow_type_comboBox.setItemText(7, "吃饭")
        # 消费开始日、结束日
        self.financial_flow_consumption_starting_date_lineEdit = QtWidgets.QLineEdit(self.financial_flow_tab)
        self.financial_flow_consumption_starting_date_lineEdit.setGeometry(QtCore.QRect(110, 10, 90, 20))
        self.financial_flow_consumption_starting_date_lineEdit.setPlaceholderText('消费开始日')
        self.financial_flow_consumption_starting_date_lineEdit.setObjectName(
            "financial_flow_consumption_starting_date_lineEdit")
        self.financial_flow_consumption_closing_date_lineEdit = QtWidgets.QLineEdit(self.financial_flow_tab)
        self.financial_flow_consumption_closing_date_lineEdit.setGeometry(QtCore.QRect(210, 10, 90, 20))
        self.financial_flow_consumption_closing_date_lineEdit.setPlaceholderText('消费结束日')
        self.financial_flow_consumption_closing_date_lineEdit.setObjectName(
            "financial_flow_consumption_closing_date_lineEdit")
        # 账单最小金额、最大金额
        self.financial_flow_min_date_lineEdit = QtWidgets.QLineEdit(self.financial_flow_tab)
        self.financial_flow_min_date_lineEdit.setGeometry(QtCore.QRect(310, 10, 90, 20))
        self.financial_flow_min_date_lineEdit.setPlaceholderText('账单最小金额')
        self.financial_flow_min_date_lineEdit.setObjectName("financial_flow_min_date_lineEdit")
        self.financial_flow_max_date_lineEdit = QtWidgets.QLineEdit(self.financial_flow_tab)
        self.financial_flow_max_date_lineEdit.setGeometry(QtCore.QRect(410, 10, 90, 20))
        self.financial_flow_max_date_lineEdit.setPlaceholderText('账单最大金额')
        self.financial_flow_max_date_lineEdit.setObjectName("financial_flow_max_date_lineEdit")
        # 消费人
        self.financial_flow_consumer_comboBox = QtWidgets.QComboBox(self.financial_flow_tab)
        self.financial_flow_consumer_comboBox.setGeometry(QtCore.QRect(532, 10, 75, 23))
        self.financial_flow_consumer_comboBox.setObjectName("financial_flow_consumer_comboBox")
        self.financial_flow_consumer_comboBox.addItem("")
        self.financial_flow_consumer_comboBox.addItem("")
        self.financial_flow_consumer_comboBox.addItem("")
        self.financial_flow_consumer_comboBox.setItemText(0, "全部消费人")
        self.financial_flow_consumer_comboBox.setItemText(1, "陈小珍")
        self.financial_flow_consumer_comboBox.setItemText(2, "钟玲龙")
        # 搜索，新增按钮
        self.financial_flow_search_pushButton = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_search_pushButton.setGeometry(QtCore.QRect(632, 10, 75, 23))
        self.financial_flow_search_pushButton.setObjectName("financial_flow_search_pushButton")
        self.financial_flow_search_pushButton.setText("搜索")
        self.financial_flow_add_pushButton = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_add_pushButton.setGeometry(QtCore.QRect(732, 10, 75, 23))
        self.financial_flow_add_pushButton.setObjectName("financial_flow_add_pushButton")
        self.financial_flow_add_pushButton.setText("新增")

        # 列表展示
        self.financial_flow_tableWidget = QtWidgets.QTableWidget(self.financial_flow_tab)
        self.financial_flow_tableWidget.setGeometry(QtCore.QRect(10, 50, 521, 795))
        self.financial_flow_tableWidget.setObjectName("financial_flow_tableWidget")
        self.financial_flow_tableWidget.setColumnCount(5)
        self.financial_flow_tableWidget.setColumnWidth(0, 150)
        self.financial_flow_tableWidget.setColumnWidth(1, 80)
        self.financial_flow_tableWidget.setColumnWidth(3, 80)
        self.financial_flow_tableWidget.setRowCount(25)
        # 表单插入25*5的格子
        for i in range(25):
            for j in range(5):
                item = QtWidgets.QTableWidgetItem()
                self.financial_flow_tableWidget.setVerticalHeaderItem(i, item)
                item = QtWidgets.QTableWidgetItem()
                self.financial_flow_tableWidget.setHorizontalHeaderItem(j, item)
        # 表单首列1-25
        for i in range(25):
            item = self.financial_flow_tableWidget.verticalHeaderItem(i)
            item.setText(str(i + 1))
        self.financial_flow_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 列表禁止编辑
        # 表的头部
        item = self.financial_flow_tableWidget.horizontalHeaderItem(0)
        item.setText("消费描述")
        item = self.financial_flow_tableWidget.horizontalHeaderItem(1)
        item.setText("消费分类")
        item = self.financial_flow_tableWidget.horizontalHeaderItem(2)
        item.setText("消费日期")
        item = self.financial_flow_tableWidget.horizontalHeaderItem(3)
        item.setText("消费金额")
        item = self.financial_flow_tableWidget.horizontalHeaderItem(4)
        item.setText("消费人")

        self.financial_flow_czl_label = QtWidgets.QLabel(self.financial_flow_tab)
        self.financial_flow_czl_label.setGeometry(QtCore.QRect(520, 50, 75, 23))
        self.financial_flow_czl_label.setObjectName("ffinancial_flow_czl_label")
        self.financial_flow_czl_label.setText('    操作栏   ')
        self.financial_flow_PushButton1 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_PushButton1.setGeometry(QtCore.QRect(530, 74, 75, 33))
        self.financial_flow_PushButton1.setObjectName("financial_flow_PushButton1")
        self.financial_flow_PushButton1.setText("详情")
        self.financial_flow_PushButton2 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_PushButton2.setGeometry(QtCore.QRect(530, 104, 75, 33))
        self.financial_flow_PushButton2.setObjectName("financial_flow_PushButton2")
        self.financial_flow_PushButton2.setText("详情")
        self.financial_flow_PushButton3 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_PushButton3.setGeometry(QtCore.QRect(530, 134, 75, 33))
        self.financial_flow_PushButton3.setObjectName("financial_flow_PushButton3")
        self.financial_flow_PushButton3.setText("详情")
        self.financial_flow_PushButton4 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_PushButton4.setGeometry(QtCore.QRect(530, 164, 75, 33))
        self.financial_flow_PushButton4.setObjectName("financial_flow_PushButton4")
        self.financial_flow_PushButton4.setText("详情")
        self.financial_flow_PushButton5 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_PushButton5.setGeometry(QtCore.QRect(530, 194, 75, 33))
        self.financial_flow_PushButton5.setObjectName("financial_flow_PushButton5")
        self.financial_flow_PushButton5.setText("详情")
        self.financial_flow_PushButton6 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_PushButton6.setGeometry(QtCore.QRect(530, 224, 75, 33))
        self.financial_flow_PushButton6.setObjectName("financial_flow_PushButton6")
        self.financial_flow_PushButton6.setText("详情")
        self.financial_flow_PushButton7 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_PushButton7.setGeometry(QtCore.QRect(530, 254, 75, 33))
        self.financial_flow_PushButton7.setObjectName("financial_flow_PushButton7")
        self.financial_flow_PushButton7.setText("详情")
        self.financial_flow_PushButton8 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_PushButton8.setGeometry(QtCore.QRect(530, 284, 75, 33))
        self.financial_flow_PushButton8.setObjectName("financial_flow_PushButton8")
        self.financial_flow_PushButton8.setText("详情")
        self.financial_flow_PushButton9 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_PushButton9.setGeometry(QtCore.QRect(530, 314, 75, 33))
        self.financial_flow_PushButton9.setObjectName("financial_flow_PushButton9")
        self.financial_flow_PushButton9.setText("详情")
        self.financial_flow_PushButton10 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_PushButton10.setGeometry(QtCore.QRect(530, 344, 75, 33))
        self.financial_flow_PushButton10.setObjectName("financial_flow_PushButton10")
        self.financial_flow_PushButton10.setText("详情")
        self.financial_flow_PushButton11 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_PushButton11.setGeometry(QtCore.QRect(530, 374, 75, 33))
        self.financial_flow_PushButton11.setObjectName("financial_flow_PushButton11")
        self.financial_flow_PushButton11.setText("详情")
        self.financial_flow_PushButton12 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_PushButton12.setGeometry(QtCore.QRect(530, 404, 75, 33))
        self.financial_flow_PushButton12.setObjectName("financial_flow_PushButton12")
        self.financial_flow_PushButton12.setText("详情")
        self.financial_flow_PushButton13 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_PushButton13.setGeometry(QtCore.QRect(530, 434, 75, 33))
        self.financial_flow_PushButton13.setObjectName("financial_flow_PushButton13")
        self.financial_flow_PushButton13.setText("详情")
        self.financial_flow_PushButton14 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_PushButton14.setGeometry(QtCore.QRect(530, 464, 75, 33))
        self.financial_flow_PushButton14.setObjectName("financial_flow_PushButton14")
        self.financial_flow_PushButton14.setText("详情")
        self.financial_flow_PushButton15 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_PushButton15.setGeometry(QtCore.QRect(530, 494, 75, 33))
        self.financial_flow_PushButton15.setObjectName("financial_flow_PushButton15")
        self.financial_flow_PushButton15.setText("详情")
        self.financial_flow_PushButton16 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_PushButton16.setGeometry(QtCore.QRect(530, 524, 75, 33))
        self.financial_flow_PushButton16.setObjectName("financial_flow_PushButton16")
        self.financial_flow_PushButton16.setText("详情")
        self.financial_flow_PushButton17 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_PushButton17.setGeometry(QtCore.QRect(530, 554, 75, 33))
        self.financial_flow_PushButton17.setObjectName("financial_flow_PushButton17")
        self.financial_flow_PushButton17.setText("详情")
        self.financial_flow_PushButton18 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_PushButton18.setGeometry(QtCore.QRect(530, 584, 75, 33))
        self.financial_flow_PushButton18.setObjectName("financial_flow_PushButton18")
        self.financial_flow_PushButton18.setText("详情")
        self.financial_flow_PushButton19 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_PushButton19.setGeometry(QtCore.QRect(530, 614, 75, 33))
        self.financial_flow_PushButton19.setObjectName("financial_flow_PushButton19")
        self.financial_flow_PushButton19.setText("详情")
        self.financial_flow_PushButton20 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_PushButton20.setGeometry(QtCore.QRect(530, 644, 75, 33))
        self.financial_flow_PushButton20.setObjectName("financial_flow_PushButton20")
        self.financial_flow_PushButton20.setText("详情")
        self.financial_flow_PushButton21 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_PushButton21.setGeometry(QtCore.QRect(530, 674, 75, 33))
        self.financial_flow_PushButton21.setObjectName("financial_flow_PushButton21")
        self.financial_flow_PushButton21.setText("详情")
        self.financial_flow_PushButton22 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_PushButton22.setGeometry(QtCore.QRect(530, 704, 75, 33))
        self.financial_flow_PushButton22.setObjectName("financial_flow_PushButton22")
        self.financial_flow_PushButton22.setText("详情")
        self.financial_flow_PushButton23 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_PushButton23.setGeometry(QtCore.QRect(530, 734, 75, 33))
        self.financial_flow_PushButton23.setObjectName("financial_flow_PushButton23")
        self.financial_flow_PushButton23.setText("详情")
        self.financial_flow_PushButton24 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_PushButton24.setGeometry(QtCore.QRect(530, 764, 75, 33))
        self.financial_flow_PushButton24.setObjectName("financial_flow_PushButton24")
        self.financial_flow_PushButton24.setText("详情")
        self.financial_flow_PushButton25 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_PushButton25.setGeometry(QtCore.QRect(530, 794, 75, 33))
        self.financial_flow_PushButton25.setObjectName("financial_flow_PushButton25")
        self.financial_flow_PushButton25.setText("详情")
        self.financial_flow_PushButtonAll = {self.financial_flow_PushButton1: 1,
                                             self.financial_flow_PushButton2: 2,
                                             self.financial_flow_PushButton3: 3,
                                             self.financial_flow_PushButton4: 4,
                                             self.financial_flow_PushButton5: 5,
                                             self.financial_flow_PushButton6: 6,
                                             self.financial_flow_PushButton7: 7,
                                             self.financial_flow_PushButton8: 8,
                                             self.financial_flow_PushButton9: 9,
                                             self.financial_flow_PushButton10: 10,
                                             self.financial_flow_PushButton11: 11,
                                             self.financial_flow_PushButton12: 12,
                                             self.financial_flow_PushButton13: 13,
                                             self.financial_flow_PushButton14: 14,
                                             self.financial_flow_PushButton15: 15,
                                             self.financial_flow_PushButton16: 16,
                                             self.financial_flow_PushButton17: 17,
                                             self.financial_flow_PushButton18: 18,
                                             self.financial_flow_PushButton19: 19,
                                             self.financial_flow_PushButton20: 20,
                                             self.financial_flow_PushButton21: 21,
                                             self.financial_flow_PushButton22: 22,
                                             self.financial_flow_PushButton23: 23,
                                             self.financial_flow_PushButton24: 24,
                                             self.financial_flow_PushButton25: 25
                                             }

        self.financial_flow_delete_PushButton1 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_delete_PushButton1.setGeometry(QtCore.QRect(603, 74, 75, 33))
        self.financial_flow_delete_PushButton1.setObjectName("financial_flow_PushButton1")
        self.financial_flow_delete_PushButton1.setText("删除")
        self.financial_flow_delete_PushButton2 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_delete_PushButton2.setGeometry(QtCore.QRect(603, 104, 75, 33))
        self.financial_flow_delete_PushButton2.setObjectName("financial_flow_PushButton2")
        self.financial_flow_delete_PushButton2.setText("删除")
        self.financial_flow_delete_PushButton3 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_delete_PushButton3.setGeometry(QtCore.QRect(603, 134, 75, 33))
        self.financial_flow_delete_PushButton3.setObjectName("financial_flow_PushButton3")
        self.financial_flow_delete_PushButton3.setText("删除")
        self.financial_flow_delete_PushButton4 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_delete_PushButton4.setGeometry(QtCore.QRect(603, 164, 75, 33))
        self.financial_flow_delete_PushButton4.setObjectName("financial_flow_PushButton4")
        self.financial_flow_delete_PushButton4.setText("删除")
        self.financial_flow_delete_PushButton5 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_delete_PushButton5.setGeometry(QtCore.QRect(603, 194, 75, 33))
        self.financial_flow_delete_PushButton5.setObjectName("financial_flow_PushButton5")
        self.financial_flow_delete_PushButton5.setText("删除")
        self.financial_flow_delete_PushButton6 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_delete_PushButton6.setGeometry(QtCore.QRect(603, 224, 75, 33))
        self.financial_flow_delete_PushButton6.setObjectName("financial_flow_PushButton6")
        self.financial_flow_delete_PushButton6.setText("删除")
        self.financial_flow_delete_PushButton7 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_delete_PushButton7.setGeometry(QtCore.QRect(603, 254, 75, 33))
        self.financial_flow_delete_PushButton7.setObjectName("financial_flow_PushButton7")
        self.financial_flow_delete_PushButton7.setText("删除")
        self.financial_flow_delete_PushButton8 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_delete_PushButton8.setGeometry(QtCore.QRect(603, 284, 75, 33))
        self.financial_flow_delete_PushButton8.setObjectName("financial_flow_PushButton8")
        self.financial_flow_delete_PushButton8.setText("删除")
        self.financial_flow_delete_PushButton9 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_delete_PushButton9.setGeometry(QtCore.QRect(603, 314, 75, 33))
        self.financial_flow_delete_PushButton9.setObjectName("financial_flow_PushButton9")
        self.financial_flow_delete_PushButton9.setText("删除")
        self.financial_flow_delete_PushButton10 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_delete_PushButton10.setGeometry(QtCore.QRect(603, 344, 75, 33))
        self.financial_flow_delete_PushButton10.setObjectName("financial_flow_PushButton10")
        self.financial_flow_delete_PushButton10.setText("删除")
        self.financial_flow_delete_PushButton11 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_delete_PushButton11.setGeometry(QtCore.QRect(603, 374, 75, 33))
        self.financial_flow_delete_PushButton11.setObjectName("financial_flow_PushButton11")
        self.financial_flow_delete_PushButton11.setText("删除")
        self.financial_flow_delete_PushButton12 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_delete_PushButton12.setGeometry(QtCore.QRect(603, 404, 75, 33))
        self.financial_flow_delete_PushButton12.setObjectName("financial_flow_PushButton12")
        self.financial_flow_delete_PushButton12.setText("删除")
        self.financial_flow_delete_PushButton13 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_delete_PushButton13.setGeometry(QtCore.QRect(603, 434, 75, 33))
        self.financial_flow_delete_PushButton13.setObjectName("financial_flow_PushButton13")
        self.financial_flow_delete_PushButton13.setText("删除")
        self.financial_flow_delete_PushButton14 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_delete_PushButton14.setGeometry(QtCore.QRect(603, 464, 75, 33))
        self.financial_flow_delete_PushButton14.setObjectName("financial_flow_PushButton14")
        self.financial_flow_delete_PushButton14.setText("删除")
        self.financial_flow_delete_PushButton15 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_delete_PushButton15.setGeometry(QtCore.QRect(603, 494, 75, 33))
        self.financial_flow_delete_PushButton15.setObjectName("financial_flow_PushButton15")
        self.financial_flow_delete_PushButton15.setText("删除")
        self.financial_flow_delete_PushButton16 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_delete_PushButton16.setGeometry(QtCore.QRect(603, 524, 75, 33))
        self.financial_flow_delete_PushButton16.setObjectName("financial_flow_PushButton16")
        self.financial_flow_delete_PushButton16.setText("删除")
        self.financial_flow_delete_PushButton17 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_delete_PushButton17.setGeometry(QtCore.QRect(603, 554, 75, 33))
        self.financial_flow_delete_PushButton17.setObjectName("financial_flow_PushButton17")
        self.financial_flow_delete_PushButton17.setText("删除")
        self.financial_flow_delete_PushButton18 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_delete_PushButton18.setGeometry(QtCore.QRect(603, 584, 75, 33))
        self.financial_flow_delete_PushButton18.setObjectName("financial_flow_PushButton18")
        self.financial_flow_delete_PushButton18.setText("删除")
        self.financial_flow_delete_PushButton19 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_delete_PushButton19.setGeometry(QtCore.QRect(603, 614, 75, 33))
        self.financial_flow_delete_PushButton19.setObjectName("financial_flow_PushButton19")
        self.financial_flow_delete_PushButton19.setText("删除")
        self.financial_flow_delete_PushButton20 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_delete_PushButton20.setGeometry(QtCore.QRect(603, 644, 75, 33))
        self.financial_flow_delete_PushButton20.setObjectName("financial_flow_PushButton20")
        self.financial_flow_delete_PushButton20.setText("删除")
        self.financial_flow_delete_PushButton21 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_delete_PushButton21.setGeometry(QtCore.QRect(603, 674, 75, 33))
        self.financial_flow_delete_PushButton21.setObjectName("financial_flow_PushButton21")
        self.financial_flow_delete_PushButton21.setText("删除")
        self.financial_flow_delete_PushButton22 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_delete_PushButton22.setGeometry(QtCore.QRect(603, 704, 75, 33))
        self.financial_flow_delete_PushButton22.setObjectName("financial_flow_PushButton22")
        self.financial_flow_delete_PushButton22.setText("删除")
        self.financial_flow_delete_PushButton23 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_delete_PushButton23.setGeometry(QtCore.QRect(603, 734, 75, 33))
        self.financial_flow_delete_PushButton23.setObjectName("financial_flow_PushButton23")
        self.financial_flow_delete_PushButton23.setText("删除")
        self.financial_flow_delete_PushButton24 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_delete_PushButton24.setGeometry(QtCore.QRect(603, 764, 75, 33))
        self.financial_flow_delete_PushButton24.setObjectName("financial_flow_PushButton24")
        self.financial_flow_delete_PushButton24.setText("删除")
        self.financial_flow_delete_PushButton25 = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_delete_PushButton25.setGeometry(QtCore.QRect(603, 794, 75, 33))
        self.financial_flow_delete_PushButton25.setObjectName("financial_flow_PushButton25")
        self.financial_flow_delete_PushButton25.setText("删除")
        self.financial_flow_delete_PushButtonAll = {self.financial_flow_delete_PushButton1: 1,
                                                    self.financial_flow_delete_PushButton2: 2,
                                                    self.financial_flow_delete_PushButton3: 3,
                                                    self.financial_flow_delete_PushButton4: 4,
                                                    self.financial_flow_delete_PushButton5: 5,
                                                    self.financial_flow_delete_PushButton6: 6,
                                                    self.financial_flow_delete_PushButton7: 7,
                                                    self.financial_flow_delete_PushButton8: 8,
                                                    self.financial_flow_delete_PushButton9: 9,
                                                    self.financial_flow_delete_PushButton10: 10,
                                                    self.financial_flow_delete_PushButton11: 11,
                                                    self.financial_flow_delete_PushButton12: 12,
                                                    self.financial_flow_delete_PushButton13: 13,
                                                    self.financial_flow_delete_PushButton14: 14,
                                                    self.financial_flow_delete_PushButton15: 15,
                                                    self.financial_flow_delete_PushButton16: 16,
                                                    self.financial_flow_delete_PushButton17: 17,
                                                    self.financial_flow_delete_PushButton18: 18,
                                                    self.financial_flow_delete_PushButton19: 19,
                                                    self.financial_flow_delete_PushButton20: 20,
                                                    self.financial_flow_delete_PushButton21: 21,
                                                    self.financial_flow_delete_PushButton22: 22,
                                                    self.financial_flow_delete_PushButton23: 23,
                                                    self.financial_flow_delete_PushButton24: 24,
                                                    self.financial_flow_delete_PushButton25: 25
                                                    }

        # 列表下方搜索
        # 上一页
        self.financial_flow_previous_page_pushButton = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_previous_page_pushButton.setGeometry(QtCore.QRect(10, 850, 75, 23))
        self.financial_flow_previous_page_pushButton.setObjectName("financial_flow_previous_page_pushButton")
        self.financial_flow_previous_page_pushButton.setText('上一页')
        # 当前页
        self.financial_flow_current_page_label = QtWidgets.QLabel(self.financial_flow_tab)
        self.financial_flow_current_page_label.setGeometry(QtCore.QRect(90, 850, 35, 21))
        self.financial_flow_current_page_label.setObjectName("financial_flow_current_page_label")
        self.financial_flow_current_page_label.setText('0/0')
        # 下一页
        self.financial_flow_next_page_pushButton = QtWidgets.QPushButton(self.financial_flow_tab)
        self.financial_flow_next_page_pushButton.setGeometry(QtCore.QRect(120, 850, 75, 23))
        self.financial_flow_next_page_pushButton.setObjectName("financial_flow_next_page_pushButton")
        self.financial_flow_next_page_pushButton.setText('下一页')
        # 还款金额总和
        self.financial_flow_total_amount_of_flow_label = QtWidgets.QLabel(self.financial_flow_tab)
        self.financial_flow_total_amount_of_flow_label.setGeometry(QtCore.QRect(230, 850, 55, 21))
        self.financial_flow_total_amount_of_flow_label.setObjectName(
            "financial_flow_total_amount_of_flow_label")
        self.financial_flow_total_amount_of_flow_label.setText('金额总和')
        self.financial_flow_total_amount_of_flow_lineEdit = QtWidgets.QLineEdit(self.financial_flow_tab)
        self.financial_flow_total_amount_of_flow_lineEdit.setGeometry(QtCore.QRect(280, 850, 90, 20))
        self.financial_flow_total_amount_of_flow_lineEdit.setReadOnly(True)
        self.financial_flow_total_amount_of_flow_lineEdit.setObjectName(
            "financial_flow_total_amount_of_flow_lineEdit")
        # 还款笔数
        self.financial_flow_amount_label = QtWidgets.QLabel(self.financial_flow_tab)
        self.financial_flow_amount_label.setGeometry(QtCore.QRect(410, 850, 55, 21))
        self.financial_flow_amount_label.setObjectName("financial_flow_amount_label")
        self.financial_flow_amount_label.setText('笔数')
        self.financial_flow_amount_lineEdit = QtWidgets.QLineEdit(self.financial_flow_tab)
        self.financial_flow_amount_lineEdit.setGeometry(QtCore.QRect(440, 850, 90, 20))
        self.financial_flow_amount_lineEdit.setReadOnly(True)
        self.financial_flow_amount_lineEdit.setObjectName("financial_flow_amount_lineEdit")

    def add_financial_flow_datapage(self):
        """
        :return:
        """
        base.consoleLog('新增财务流水')
        self.financial_flow_datapage = QDialog(self)
        self.financial_flow_datapage.setWindowTitle('新增财务流水')
        self.financial_flow_datapage.resize(400, 250)
        self.add_financial_flow_databutton = QPushButton("保存", self.financial_flow_datapage)
        self.add_financial_flow_databutton.setGeometry(QtCore.QRect(300, 200, 75, 23))
        self.add_financial_flow_databutton.show()
        self.add_financial_flow_databutton.clicked.connect(self.get_financial_flow_datapage)
        self.add_financial_flow_databutton.clicked.connect(self.select_financial_flow_list)
        self.add_financial_flow_dataflo = QFormLayout(self.financial_flow_datapage)
        self.add_financial_flow_dataflo.addRow(QLabel())
        self.add_financial_flow_dataflo.addRow(QLabel())
        self.add_financial_flow_dataflo.addRow(QLabel())
        self.addeventLineEdit = QLineEdit(self.financial_flow_datapage)
        self.adddateLineEdit = QLineEdit(self.financial_flow_datapage)
        self.addclassificationComboBox = QComboBox(self.financial_flow_datapage)
        self.addclassificationComboBox.addItems(['生活用品', '吃饭', '房租水电', '外出玩乐', '交通费', '还信用卡', '亲戚送礼', '其他'])
        self.addmoneyLineEdit = QLineEdit(self.financial_flow_datapage)
        self.addcreateNameComboBox = QComboBox(self.financial_flow_datapage)
        self.addcreateNameComboBox.addItems(['钟玲龙', '陈小珍'])
        self.add_financial_flow_dataflo.addRow("消费事件", self.addeventLineEdit)
        self.add_financial_flow_dataflo.addRow("消费日期", self.adddateLineEdit)
        self.add_financial_flow_dataflo.addRow("消费类型", self.addclassificationComboBox)
        self.add_financial_flow_dataflo.addRow("消费金额", self.addmoneyLineEdit)
        self.add_financial_flow_dataflo.addRow("   消费者", self.addcreateNameComboBox)

        self.addeventLineEdit.setPlaceholderText("请输入该笔流水的消费情况")
        self.adddateLineEdit.setPlaceholderText("请输入该事件发生的日期")
        self.addmoneyLineEdit.setPlaceholderText("请输入该笔消费的金额")
        self.financial_flow_datapage.setLayout(self.add_financial_flow_dataflo)
        self.financial_flow_datapage.show()

    def get_financial_flow_datapage(self):
        """
        :return:
        """
        base.consoleLog('获取新增财务流水页面数据')
        classificationData = QComboBox.currentText(self.addclassificationComboBox)
        eventData = QLineEdit.displayText(self.addeventLineEdit)
        dateData = QLineEdit.displayText(self.adddateLineEdit)
        moneyData = QLineEdit.displayText(self.addmoneyLineEdit)
        createName = QComboBox.currentText(self.addcreateNameComboBox)

        if eventData == '' or dateData == '' or moneyData == '':
            QMessageBox.about(self.financial_flow_datapage, "提示", "您有部分数据为空，请输入完整信息之后再点击保存!")
            return

        sql = """INSERT INTO financial_flow VALUES (null,'%s', '%s', '%s', '%s','%s','%s','%s',0 );
               """ % (
        eventData, dateData, classificationData, moneyData, createName, base.time_time(), base.time_time())
        MySqlite(sql).insert_sql()
        QMessageBox.about(self.financial_flow_datapage, "提示", "您的账单生成成功!")
        self.financial_flow_datapage.close()
        return

    def add_credit_card_page(self, value=False):
        base.consoleLog('生成信用卡页面')

        if value:
            return

        # 新增页签作为还款计划的页面
        self.credit_card_tab = QtWidgets.QWidget()
        self.credit_card_tab.setObjectName("credit_card_tab")
        self.tabWidget.addTab(self.credit_card_tab, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.credit_card_tab), "信用卡")

        # 刷新，新增按钮
        self.credit_card_search_pushButton = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_search_pushButton.setGeometry(QtCore.QRect(832, 10, 75, 33))
        self.credit_card_search_pushButton.setObjectName("credit_card_search_pushButton")
        self.credit_card_search_pushButton.setText("刷新")
        self.credit_card_add_pushButton = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_add_pushButton.setGeometry(QtCore.QRect(922, 10, 75, 33))
        self.credit_card_add_pushButton.setObjectName("credit_card_add_pushButton")
        self.credit_card_add_pushButton.setText("新增")

        self.credit_card_czl_label = QtWidgets.QLabel(self.credit_card_tab)
        self.credit_card_czl_label.setGeometry(QtCore.QRect(830, 50, 75, 23))
        self.credit_card_czl_label.setObjectName("credit_card_czl_label")
        self.credit_card_czl_label.setText('    操作栏   ')
        self.credit_card_PushButton1 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_PushButton1.setGeometry(QtCore.QRect(830, 74, 75, 33))
        self.credit_card_PushButton1.setObjectName("credit_card_PushButton1")
        self.credit_card_PushButton1.setText("详情")
        self.credit_card_PushButton2 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_PushButton2.setGeometry(QtCore.QRect(830, 104, 75, 33))
        self.credit_card_PushButton2.setObjectName("credit_card_PushButton2")
        self.credit_card_PushButton2.setText("详情")
        self.credit_card_PushButton3 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_PushButton3.setGeometry(QtCore.QRect(830, 134, 75, 33))
        self.credit_card_PushButton3.setObjectName("credit_card_PushButton3")
        self.credit_card_PushButton3.setText("详情")
        self.credit_card_PushButton4 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_PushButton4.setGeometry(QtCore.QRect(830, 164, 75, 33))
        self.credit_card_PushButton4.setObjectName("credit_card_PushButton4")
        self.credit_card_PushButton4.setText("详情")
        self.credit_card_PushButton5 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_PushButton5.setGeometry(QtCore.QRect(830, 194, 75, 33))
        self.credit_card_PushButton5.setObjectName("credit_card_PushButton5")
        self.credit_card_PushButton5.setText("详情")
        self.credit_card_PushButton6 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_PushButton6.setGeometry(QtCore.QRect(830, 224, 75, 33))
        self.credit_card_PushButton6.setObjectName("credit_card_PushButton6")
        self.credit_card_PushButton6.setText("详情")
        self.credit_card_PushButton7 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_PushButton7.setGeometry(QtCore.QRect(830, 254, 75, 33))
        self.credit_card_PushButton7.setObjectName("credit_card_PushButton7")
        self.credit_card_PushButton7.setText("详情")
        self.credit_card_PushButton8 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_PushButton8.setGeometry(QtCore.QRect(830, 284, 75, 33))
        self.credit_card_PushButton8.setObjectName("credit_card_PushButton8")
        self.credit_card_PushButton8.setText("详情")
        self.credit_card_PushButton9 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_PushButton9.setGeometry(QtCore.QRect(830, 314, 75, 33))
        self.credit_card_PushButton9.setObjectName("credit_card_PushButton9")
        self.credit_card_PushButton9.setText("详情")
        self.credit_card_PushButton10 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_PushButton10.setGeometry(QtCore.QRect(830, 344, 75, 33))
        self.credit_card_PushButton10.setObjectName("credit_card_PushButton10")
        self.credit_card_PushButton10.setText("详情")
        self.credit_card_PushButton11 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_PushButton11.setGeometry(QtCore.QRect(830, 374, 75, 33))
        self.credit_card_PushButton11.setObjectName("credit_card_PushButton11")
        self.credit_card_PushButton11.setText("详情")
        self.credit_card_PushButton12 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_PushButton12.setGeometry(QtCore.QRect(830, 404, 75, 33))
        self.credit_card_PushButton12.setObjectName("credit_card_PushButton12")
        self.credit_card_PushButton12.setText("详情")
        self.credit_card_PushButton13 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_PushButton13.setGeometry(QtCore.QRect(830, 434, 75, 33))
        self.credit_card_PushButton13.setObjectName("credit_card_PushButton13")
        self.credit_card_PushButton13.setText("详情")
        self.credit_card_PushButton14 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_PushButton14.setGeometry(QtCore.QRect(830, 464, 75, 33))
        self.credit_card_PushButton14.setObjectName("credit_card_PushButton14")
        self.credit_card_PushButton14.setText("详情")
        self.credit_card_PushButton15 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_PushButton15.setGeometry(QtCore.QRect(830, 494, 75, 33))
        self.credit_card_PushButton15.setObjectName("credit_card_PushButton15")
        self.credit_card_PushButton15.setText("详情")
        self.credit_card_PushButton16 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_PushButton16.setGeometry(QtCore.QRect(830, 524, 75, 33))
        self.credit_card_PushButton16.setObjectName("credit_card_PushButton16")
        self.credit_card_PushButton16.setText("详情")
        self.credit_card_PushButton17 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_PushButton17.setGeometry(QtCore.QRect(830, 554, 75, 33))
        self.credit_card_PushButton17.setObjectName("credit_card_PushButton17")
        self.credit_card_PushButton17.setText("详情")
        self.credit_card_PushButton18 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_PushButton18.setGeometry(QtCore.QRect(830, 584, 75, 33))
        self.credit_card_PushButton18.setObjectName("credit_card_PushButton18")
        self.credit_card_PushButton18.setText("详情")
        self.credit_card_PushButton19 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_PushButton19.setGeometry(QtCore.QRect(830, 614, 75, 33))
        self.credit_card_PushButton19.setObjectName("credit_card_PushButton19")
        self.credit_card_PushButton19.setText("详情")
        self.credit_card_PushButton20 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_PushButton20.setGeometry(QtCore.QRect(830, 644, 75, 33))
        self.credit_card_PushButton20.setObjectName("credit_card_PushButton20")
        self.credit_card_PushButton20.setText("详情")
        self.credit_card_PushButton21 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_PushButton21.setGeometry(QtCore.QRect(830, 674, 75, 33))
        self.credit_card_PushButton21.setObjectName("credit_card_PushButton21")
        self.credit_card_PushButton21.setText("详情")
        self.credit_card_PushButton22 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_PushButton22.setGeometry(QtCore.QRect(830, 704, 75, 33))
        self.credit_card_PushButton22.setObjectName("credit_card_PushButton22")
        self.credit_card_PushButton22.setText("详情")
        self.credit_card_PushButton23 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_PushButton23.setGeometry(QtCore.QRect(830, 734, 75, 33))
        self.credit_card_PushButton23.setObjectName("credit_card_PushButton23")
        self.credit_card_PushButton23.setText("详情")
        self.credit_card_PushButton24 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_PushButton24.setGeometry(QtCore.QRect(830, 764, 75, 33))
        self.credit_card_PushButton24.setObjectName("credit_card_PushButton24")
        self.credit_card_PushButton24.setText("详情")
        self.credit_card_PushButton25 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_PushButton25.setGeometry(QtCore.QRect(830, 794, 75, 33))
        self.credit_card_PushButton25.setObjectName("credit_card_PushButton25")
        self.credit_card_PushButton25.setText("详情")
        self.credit_card_PushButtonAll = {self.credit_card_PushButton1: 1,
                                          self.credit_card_PushButton2: 2,
                                          self.credit_card_PushButton3: 3,
                                          self.credit_card_PushButton4: 4,
                                          self.credit_card_PushButton5: 5,
                                          self.credit_card_PushButton6: 6,
                                          self.credit_card_PushButton7: 7,
                                          self.credit_card_PushButton8: 8,
                                          self.credit_card_PushButton9: 9,
                                          self.credit_card_PushButton10: 10,
                                          self.credit_card_PushButton11: 11,
                                          self.credit_card_PushButton12: 12,
                                          self.credit_card_PushButton13: 13,
                                          self.credit_card_PushButton14: 14,
                                          self.credit_card_PushButton15: 15,
                                          self.credit_card_PushButton16: 16,
                                          self.credit_card_PushButton17: 17,
                                          self.credit_card_PushButton18: 18,
                                          self.credit_card_PushButton19: 19,
                                          self.credit_card_PushButton20: 20,
                                          self.credit_card_PushButton21: 21,
                                          self.credit_card_PushButton22: 22,
                                          self.credit_card_PushButton23: 23,
                                          self.credit_card_PushButton24: 24,
                                          self.credit_card_PushButton25: 25
                                          }
        self.credit_card_deletePushButton1 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_deletePushButton1.setGeometry(QtCore.QRect(903, 74, 75, 33))
        self.credit_card_deletePushButton1.setObjectName("credit_card_deletePushButton1")
        self.credit_card_deletePushButton1.setText("删除")
        self.credit_card_deletePushButton2 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_deletePushButton2.setGeometry(QtCore.QRect(903, 104, 75, 33))
        self.credit_card_deletePushButton2.setObjectName("credit_card_deletePushButton2")
        self.credit_card_deletePushButton2.setText("删除")
        self.credit_card_deletePushButton3 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_deletePushButton3.setGeometry(QtCore.QRect(903, 134, 75, 33))
        self.credit_card_deletePushButton3.setObjectName("credit_card_deletePushButton3")
        self.credit_card_deletePushButton3.setText("删除")
        self.credit_card_deletePushButton4 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_deletePushButton4.setGeometry(QtCore.QRect(903, 164, 75, 33))
        self.credit_card_deletePushButton4.setObjectName("credit_card_deletePushButton4")
        self.credit_card_deletePushButton4.setText("删除")
        self.credit_card_deletePushButton5 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_deletePushButton5.setGeometry(QtCore.QRect(903, 194, 75, 33))
        self.credit_card_deletePushButton5.setObjectName("credit_card_deletePushButton5")
        self.credit_card_deletePushButton5.setText("删除")
        self.credit_card_deletePushButton6 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_deletePushButton6.setGeometry(QtCore.QRect(903, 224, 75, 33))
        self.credit_card_deletePushButton6.setObjectName("credit_card_deletePushButton6")
        self.credit_card_deletePushButton6.setText("删除")
        self.credit_card_deletePushButton7 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_deletePushButton7.setGeometry(QtCore.QRect(903, 254, 75, 33))
        self.credit_card_deletePushButton7.setObjectName("credit_card_deletePushButton7")
        self.credit_card_deletePushButton7.setText("删除")
        self.credit_card_deletePushButton8 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_deletePushButton8.setGeometry(QtCore.QRect(903, 284, 75, 33))
        self.credit_card_deletePushButton8.setObjectName("credit_card_deletePushButton8")
        self.credit_card_deletePushButton8.setText("删除")
        self.credit_card_deletePushButton9 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_deletePushButton9.setGeometry(QtCore.QRect(903, 314, 75, 33))
        self.credit_card_deletePushButton9.setObjectName("credit_card_deletePushButton9")
        self.credit_card_deletePushButton9.setText("删除")
        self.credit_card_deletePushButton10 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_deletePushButton10.setGeometry(QtCore.QRect(903, 344, 75, 33))
        self.credit_card_deletePushButton10.setObjectName("credit_card_deletePushButton10")
        self.credit_card_deletePushButton10.setText("删除")
        self.credit_card_deletePushButton11 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_deletePushButton11.setGeometry(QtCore.QRect(903, 374, 75, 33))
        self.credit_card_deletePushButton11.setObjectName("credit_card_deletePushButton11")
        self.credit_card_deletePushButton11.setText("删除")
        self.credit_card_deletePushButton12 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_deletePushButton12.setGeometry(QtCore.QRect(903, 404, 75, 33))
        self.credit_card_deletePushButton12.setObjectName("credit_card_deletePushButton12")
        self.credit_card_deletePushButton12.setText("删除")
        self.credit_card_deletePushButton13 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_deletePushButton13.setGeometry(QtCore.QRect(903, 434, 75, 33))
        self.credit_card_deletePushButton13.setObjectName("credit_card_deletePushButton13")
        self.credit_card_deletePushButton13.setText("删除")
        self.credit_card_deletePushButton14 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_deletePushButton14.setGeometry(QtCore.QRect(903, 464, 75, 33))
        self.credit_card_deletePushButton14.setObjectName("credit_card_deletePushButton14")
        self.credit_card_deletePushButton14.setText("删除")
        self.credit_card_deletePushButton15 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_deletePushButton15.setGeometry(QtCore.QRect(903, 494, 75, 33))
        self.credit_card_deletePushButton15.setObjectName("credit_card_deletePushButton15")
        self.credit_card_deletePushButton15.setText("删除")
        self.credit_card_deletePushButton16 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_deletePushButton16.setGeometry(QtCore.QRect(903, 524, 75, 33))
        self.credit_card_deletePushButton16.setObjectName("credit_card_deletePushButton16")
        self.credit_card_deletePushButton16.setText("删除")
        self.credit_card_deletePushButton17 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_deletePushButton17.setGeometry(QtCore.QRect(903, 554, 75, 33))
        self.credit_card_deletePushButton17.setObjectName("credit_card_deletePushButton17")
        self.credit_card_deletePushButton17.setText("删除")
        self.credit_card_deletePushButton18 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_deletePushButton18.setGeometry(QtCore.QRect(903, 584, 75, 33))
        self.credit_card_deletePushButton18.setObjectName("credit_card_deletePushButton18")
        self.credit_card_deletePushButton18.setText("删除")
        self.credit_card_deletePushButton19 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_deletePushButton19.setGeometry(QtCore.QRect(903, 614, 75, 33))
        self.credit_card_deletePushButton19.setObjectName("credit_card_deletePushButton19")
        self.credit_card_deletePushButton19.setText("删除")
        self.credit_card_deletePushButton20 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_deletePushButton20.setGeometry(QtCore.QRect(903, 644, 75, 33))
        self.credit_card_deletePushButton20.setObjectName("credit_card_deletePushButton20")
        self.credit_card_deletePushButton20.setText("删除")
        self.credit_card_deletePushButton21 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_deletePushButton21.setGeometry(QtCore.QRect(903, 674, 75, 33))
        self.credit_card_deletePushButton21.setObjectName("credit_card_deletePushButton21")
        self.credit_card_deletePushButton21.setText("删除")
        self.credit_card_deletePushButton22 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_deletePushButton22.setGeometry(QtCore.QRect(903, 704, 75, 33))
        self.credit_card_deletePushButton22.setObjectName("credit_card_deletePushButton22")
        self.credit_card_deletePushButton22.setText("删除")
        self.credit_card_deletePushButton23 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_deletePushButton23.setGeometry(QtCore.QRect(903, 734, 75, 33))
        self.credit_card_deletePushButton23.setObjectName("credit_card_deletePushButton23")
        self.credit_card_deletePushButton23.setText("删除")
        self.credit_card_deletePushButton24 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_deletePushButton24.setGeometry(QtCore.QRect(903, 764, 75, 33))
        self.credit_card_deletePushButton24.setObjectName("credit_card_deletePushButton24")
        self.credit_card_deletePushButton24.setText("删除")
        self.credit_card_deletePushButton25 = QtWidgets.QPushButton(self.credit_card_tab)
        self.credit_card_deletePushButton25.setGeometry(QtCore.QRect(903, 794, 75, 33))
        self.credit_card_deletePushButton25.setObjectName("credit_card_deletePushButton25")
        self.credit_card_deletePushButton25.setText("删除")
        self.credit_card_deletePushButtonAll = {self.credit_card_deletePushButton1: 1,
                                                self.credit_card_deletePushButton2: 2,
                                                self.credit_card_deletePushButton3: 3,
                                                self.credit_card_deletePushButton4: 4,
                                                self.credit_card_deletePushButton5: 5,
                                                self.credit_card_deletePushButton6: 6,
                                                self.credit_card_deletePushButton7: 7,
                                                self.credit_card_deletePushButton8: 8,
                                                self.credit_card_deletePushButton9: 9,
                                                self.credit_card_deletePushButton10: 10,
                                                self.credit_card_deletePushButton11: 11,
                                                self.credit_card_deletePushButton12: 12,
                                                self.credit_card_deletePushButton13: 13,
                                                self.credit_card_deletePushButton14: 14,
                                                self.credit_card_deletePushButton15: 15,
                                                self.credit_card_deletePushButton16: 16,
                                                self.credit_card_deletePushButton17: 17,
                                                self.credit_card_deletePushButton18: 18,
                                                self.credit_card_deletePushButton19: 19,
                                                self.credit_card_deletePushButton20: 20,
                                                self.credit_card_deletePushButton21: 21,
                                                self.credit_card_deletePushButton22: 22,
                                                self.credit_card_deletePushButton23: 23,
                                                self.credit_card_deletePushButton24: 24,
                                                self.credit_card_deletePushButton25: 25
                                                }

        # 列表展示
        self.credit_card_tableWidget = QtWidgets.QTableWidget(self.credit_card_tab)
        self.credit_card_tableWidget.setGeometry(QtCore.QRect(10, 50, 821, 795))
        self.credit_card_tableWidget.setObjectName("credit_card_tableWidget")
        self.credit_card_tableWidget.setColumnCount(8)
        self.credit_card_tableWidget.setColumnWidth(0, 150)
        self.credit_card_tableWidget.setColumnWidth(1, 150)
        self.credit_card_tableWidget.setColumnWidth(2, 80)
        self.credit_card_tableWidget.setColumnWidth(3, 80)
        self.credit_card_tableWidget.setColumnWidth(4, 80)
        self.credit_card_tableWidget.setColumnWidth(5, 80)
        self.credit_card_tableWidget.setColumnWidth(6, 400)
        self.credit_card_tableWidget.setColumnWidth(7, 400)
        self.credit_card_tableWidget.setRowCount(25)

        # 表单插入25*5的格子
        for i in range(25):
            for j in range(8):
                item = QtWidgets.QTableWidgetItem()
                self.credit_card_tableWidget.setVerticalHeaderItem(i, item)
                item = QtWidgets.QTableWidgetItem()
                self.credit_card_tableWidget.setHorizontalHeaderItem(j, item)
        # 表单首列1-25
        for i in range(25):
            item = self.credit_card_tableWidget.verticalHeaderItem(i)
            item.setText(str(i + 1))
        self.credit_card_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 列表禁止编辑
        # 表的头部
        item = self.credit_card_tableWidget.horizontalHeaderItem(0)
        item.setText("信用卡名称")
        item = self.credit_card_tableWidget.horizontalHeaderItem(1)
        item.setText("卡号")
        item = self.credit_card_tableWidget.horizontalHeaderItem(2)
        item.setText("额度")
        item = self.credit_card_tableWidget.horizontalHeaderItem(3)
        item.setText("出账日")
        item = self.credit_card_tableWidget.horizontalHeaderItem(4)
        item.setText("还款日")
        item = self.credit_card_tableWidget.horizontalHeaderItem(5)
        item.setText("支付绑定APP")
        item = self.credit_card_tableWidget.horizontalHeaderItem(6)
        item.setText("福利")
        item = self.credit_card_tableWidget.horizontalHeaderItem(7)
        item.setText("备注")
        self.credit_card_tableWidget.setStyleSheet("QHeaderView::section {background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,\
                                                         stop:0 #00007f, stop: 0.5 #00007f,stop: 0.6 #00007f, stop:1 #00007f);color: red;}")

        # self.credit_card_tableWidget.setFont(QFont("Helvetica"))
        # self.credit_card_tableWidget.setHorizontalHeaderLabels(Qt.AlignHCenter)

    def add_credit_card_datapage(self):
        base.consoleLog('打开新增信用卡数据页面')

        self.credit_card_datapage = QDialog(self)
        self.credit_card_datapage.resize(360, 296)
        self.credit_card_datapage.setWindowTitle('新增信用卡信息')
        self.credit_card_name_label = QLabel(self.credit_card_datapage)
        self.credit_card_name_label.setGeometry(QtCore.QRect(22, 22, 66, 16))
        self.credit_card_name_label.setObjectName("credit_card_name_label")
        self.credit_card_name_label.setText('信用卡名称')
        self.credit_card_name_lineEdit = QLineEdit(self.credit_card_datapage)
        self.credit_card_name_lineEdit.setGeometry(QtCore.QRect(94, 22, 231, 20))
        self.credit_card_name_lineEdit.setObjectName("credit_card_name_lineEdit")
        self.credit_card_name_lineEdit.setPlaceholderText('请输入信用卡名称')

        self.credit_card_number_label = QLabel(self.credit_card_datapage)
        self.credit_card_number_label.setGeometry(QtCore.QRect(22, 51, 66, 16))
        self.credit_card_number_label.setObjectName("credit_card_number_label")
        self.credit_card_number_label.setText('卡号')
        self.credit_card_number_lineEdit = QLineEdit(self.credit_card_datapage)
        self.credit_card_number_lineEdit.setGeometry(QtCore.QRect(94, 51, 231, 20))
        self.credit_card_number_lineEdit.setObjectName("credit_card_number_lineEdit")
        self.credit_card_number_lineEdit.setPlaceholderText('请输入信用卡卡号')

        self.credit_card_quota_label = QLabel(self.credit_card_datapage)
        self.credit_card_quota_label.setGeometry(QtCore.QRect(22, 81, 66, 16))
        self.credit_card_quota_label.setObjectName("credit_card_quota_label")
        self.credit_card_quota_label.setText('额度')
        self.credit_card_quota_lineEdit = QLineEdit(self.credit_card_datapage)
        self.credit_card_quota_lineEdit.setGeometry(QtCore.QRect(94, 81, 231, 20))
        self.credit_card_quota_lineEdit.setObjectName("credit_card_quota_lineEdit")
        self.credit_card_quota_lineEdit.setPlaceholderText('请输入信用卡额度')

        self.credit_card_account_date_label = QLabel(self.credit_card_datapage)
        self.credit_card_account_date_label.setGeometry(QtCore.QRect(22, 111, 66, 16))
        self.credit_card_account_date_label.setObjectName("credit_card_account_date_label")
        self.credit_card_account_date_label.setText('出账日')
        self.credit_card_account_date_lineEdit = QLineEdit(self.credit_card_datapage)
        self.credit_card_account_date_lineEdit.setGeometry(QtCore.QRect(94, 111, 231, 20))
        self.credit_card_account_date_lineEdit.setObjectName("credit_card_account_date_lineEdit")
        self.credit_card_account_date_lineEdit.setPlaceholderText('请输入信用卡账单日')

        self.credit_card_repayment_date_label = QLabel(self.credit_card_datapage)
        self.credit_card_repayment_date_label.setGeometry(QtCore.QRect(22, 141, 66, 16))
        self.credit_card_repayment_date_label.setObjectName("credit_card_repayment_date_label")
        self.credit_card_repayment_date_label.setText('还款日')
        self.credit_card_repayment_date_lineEdit = QLineEdit(self.credit_card_datapage)
        self.credit_card_repayment_date_lineEdit.setGeometry(QtCore.QRect(94, 141, 231, 20))
        self.credit_card_repayment_date_lineEdit.setObjectName("credit_card_repayment_date_lineEdit")
        self.credit_card_repayment_date_lineEdit.setPlaceholderText('请输入信用卡还款日')

        self.credit_card_binding_payment_name_label = QLabel(self.credit_card_datapage)
        self.credit_card_binding_payment_name_label.setGeometry(QtCore.QRect(22, 171, 66, 16))
        self.credit_card_binding_payment_name_label.setObjectName("credit_card_binding_payment_name_label")
        self.credit_card_binding_payment_name_label.setText('支付绑定App')
        self.credit_card_binding_payment_name_lineEdit = QLineEdit(self.credit_card_datapage)
        self.credit_card_binding_payment_name_lineEdit.setGeometry(QtCore.QRect(94, 171, 231, 20))
        self.credit_card_binding_payment_name_lineEdit.setObjectName("credit_card_binding_payment_name_lineEdit")
        self.credit_card_binding_payment_name_lineEdit.setPlaceholderText('请输入信用卡绑定的付款APP名称')

        self.credit_card_welfare_label = QLabel(self.credit_card_datapage)
        self.credit_card_welfare_label.setGeometry(QtCore.QRect(22, 201, 66, 16))
        self.credit_card_welfare_label.setObjectName("credit_card_welfare_label")
        self.credit_card_welfare_label.setText('福利')
        self.credit_card_welfare_lineEdit = QLineEdit(self.credit_card_datapage)
        self.credit_card_welfare_lineEdit.setGeometry(QtCore.QRect(94, 201, 231, 20))
        self.credit_card_welfare_lineEdit.setObjectName("credit_card_welfare_lineEdit")
        self.credit_card_welfare_lineEdit.setPlaceholderText('请输入信用卡福利')

        self.credit_card_welfare_data_label = QLabel(self.credit_card_datapage)
        self.credit_card_welfare_data_label.setGeometry(QtCore.QRect(22, 231, 66, 16))
        self.credit_card_welfare_data_label.setObjectName("credit_card_welfare_data_label")
        self.credit_card_welfare_data_label.setText('备注')
        self.credit_card_welfare_data_lineEdit = QLineEdit(self.credit_card_datapage)
        self.credit_card_welfare_data_lineEdit.setGeometry(QtCore.QRect(94, 231, 231, 20))
        self.credit_card_welfare_data_lineEdit.setObjectName("credit_card_welfare_data_lineEdit")
        self.credit_card_welfare_data_lineEdit.setPlaceholderText('请输入信用卡使用福利时的日期')

        self.credit_card_datapagepushButton = QPushButton(self.credit_card_datapage)
        self.credit_card_datapagepushButton.setGeometry(QtCore.QRect(260, 260, 71, 23))
        self.credit_card_datapagepushButton.setObjectName("credit_card_datapagepushButton")
        self.credit_card_datapagepushButton.setText('保存')
        self.credit_card_datapagepushButton.clicked.connect(self.get_credit_card_datapage)
        self.credit_card_datapagepushButton.clicked.connect(self.select_credit_card_list)
        self.credit_card_datapage.show()

    def get_credit_card_datapage(self):
        base.consoleLog('获取新增信用卡界面的输入信息并保存到数据库')
        card_name = QLineEdit.displayText(self.credit_card_name_lineEdit)
        card_number = QLineEdit.displayText(self.credit_card_number_lineEdit)
        card_quota = QLineEdit.displayText(self.credit_card_quota_lineEdit)
        account_date = QLineEdit.displayText(self.credit_card_account_date_lineEdit)
        repayment_date = QLineEdit.displayText(self.credit_card_repayment_date_lineEdit)
        binding_payment_name = QLineEdit.displayText(self.credit_card_binding_payment_name_lineEdit)
        welfare = QLineEdit.displayText(self.credit_card_welfare_lineEdit)
        welfare_data = QLineEdit.displayText(self.credit_card_welfare_data_lineEdit)

        if card_name == '' or card_number == '' or card_quota == '' or account_date == '' or repayment_date == '' or binding_payment_name == '' or welfare == '' or welfare_data == '':
            QMessageBox.about(self.credit_card_datapage, "提示", "您有部分数据为空，请输入完整信息之后再点击保存!")
            return
        sql = """INSERT INTO credit_card VALUES (null,'%s', '%s', '%s','%s', '%s', '%s', '%s','%s','%s','%s',0 );
                       """ % (
        card_name, card_quota, account_date, repayment_date, binding_payment_name, welfare, welfare_data, card_number,
        base.time_time(), base.time_time())
        MySqlite(sql).insert_sql()
        QMessageBox.about(self.credit_card_datapage, "提示", "您的信用卡录入成功!")
        self.credit_card_datapage.close()
        return





