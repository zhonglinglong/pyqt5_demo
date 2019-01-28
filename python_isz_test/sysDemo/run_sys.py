# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QComboBox, QLineEdit
from sysDemo.client.allUi import Ui_Form
from sysDemo.client.deleteCreditCardInfo import DeleteCreditCardInfo
from sysDemo.client.deleteFinancialFlowInfo import DeleteFinancialFlowInfo
from sysDemo.client.updateFinancialFlowPage import UpdateFinancialFlow
from sysDemo.client.updateCreditCardPage import UpdateCreditCard
from sysDemo.client.runProjectPage import RunProject
from sysDemo.service.financialRepaymentRequest import FinancialRepayment
from sysDemo.service.financialFlowRequest import FinancialFlowData
from sysDemo.service.creditCardRequest import CreditCardData
from sysDemo.service.testDemoRequest import TestDemoData
from sysDemo.service.keywordRequest import KeywordData
from sysDemo.client.updateCapitalInfoPage import UpdateCapital
from common import base


class MyMainWindow(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        super(Ui_Form, self).__init__()

        self.setupUi(self)
        self.treeWidget.clicked.connect(self.display_page)  # 点击菜单栏选择对应展示的页面
        self.add_financial_flow_page_value = False
        self.add_financial_repayment_page_value = False
        self.add_credit_card_page_value = False
        self.add_project_page_value = False
        self.add_test_value = False
        self.add_keyword_value = False


    def display_page(self):
        """
        点击菜单栏选择对应展示的页面
        :return:
        """
        base.consoleLog('点击菜单栏')
        item = self.treeWidget.currentItem()
        base.consoleLog('被点击的菜单栏的值：' + str(item.text(0)))

        if item.text(0) == '还款计划':
            try:
                self.add_financial_repayment_page(self.add_financial_repayment_page_value)  # 生成该页面
                self.tabWidget.setCurrentWidget(self.financial_repayment_tab)  # 切换展示当前页面
                self.select_financial_repayment_list()  # 按照当前条件加载还款计划数据
                self.financial_repayment_search_pushButton.clicked.connect(
                    self.select_financial_repayment_list)  # 还款计划搜索按钮点击事件
                self.financial_repayment_previous_page_pushButton.clicked.connect(
                    self.select_financial_repayment_data_previous_page)  # 还款计划上一页按钮点击事件
                self.financial_repayment_next_page_pushButton.clicked.connect(
                    self.select_financial_repayment_data_next_page)  # 还款计划上一页按钮点击事件
                self.financial_repayment_add_pushButton.clicked.connect(self.add_financial_repayment_datapage)
                self.add_financial_repayment_page_value = True
            except Exception as e:
                base.consoleLog(str(e), 'e')
        elif item.text(0) == '账单流水':
            try:
                self.add_financial_flow_page(self.add_financial_flow_page_value)  # 生成该页面
                self.tabWidget.setCurrentWidget(self.financial_flow_tab)  # 切换展示当前页面
                self.select_financial_flow_list()  # 按照当前条件加载还款计划数据
                self.financial_flow_search_pushButton.clicked.connect(
                    self.select_financial_flow_list)  # 还款计划搜索按钮点击事件
                self.financial_flow_previous_page_pushButton.clicked.connect(
                    self.select_financial_flow_data_previous_page)  # 还款计划上一页按钮点击事件
                self.financial_flow_next_page_pushButton.clicked.connect(
                    self.select_financial_flow_data_next_page)  # 还款计划上一页按钮点击事件
                # 新增还款计划按钮
                self.financial_flow_add_pushButton.clicked.connect(self.add_financial_flow_datapage)
                self.add_financial_flow_page_value = True
            except Exception as e:
                base.consoleLog(str(e), 'e')
        elif item.text(0) == '信用卡':
            try:
                self.add_credit_card_page(self.add_credit_card_page_value)  # 生成该页面
                self.tabWidget.setCurrentWidget(self.credit_card_tab)  # 切换展示当前页面
                self.select_credit_card_list()  # 加载当前页面数据
                self.credit_card_search_pushButton.clicked.connect(self.select_credit_card_list)
                # 新增信用卡
                self.credit_card_add_pushButton.clicked.connect(self.add_credit_card_datapage)
                self.add_credit_card_page_value = True
            except Exception as e:
                base.consoleLog(str(e), 'e')
        elif item.text(0) == '项目运行':
            try:
                self.add_project_page(self.add_project_page_value)
                self.tabWidget.setCurrentWidget(self.project_tab)  # 切换展示当前页面
                self.select_project_list()  # 加载页面数据
                self.project_search_pushButton.clicked.connect(self.select_project_list) # 搜索按钮
                self.add_project_page_value = True
                self.project_previous_page_pushButton.clicked.connect(self.select_project_previous_page) #上一页按钮
                self.project_next_page_pushButton.clicked.connect(self.select_project_next_page) #下一页按钮
                # self.tabWidget.currentChanged.connect(self.select_project_list) #切换页面的时候重新加载当前页面数据
                # self.project_close_pushButton.clicked.connect(self.close_project_list) #点击关闭按钮

            except Exception as e:
                base.consoleLog(str(e), 'e')
        elif item.text(0) == '数据构造':
            try:
                self.add_test_data(self.add_test_value)
                self.tabWidget.setCurrentWidget(self.add_data_tab)  # 切换展示当前页面
                self.verticalScrollBar.valueChanged.connect(self.add_data_tab_click_cll) # 滑块
                self.add_test_value = True
                # self.data_tab_close_pushButton.clicked.connect(self.close_add_data_tab_list) #点击关闭按钮
            except Exception as e:
                base.consoleLog(str(e), 'e')

        elif item.text(0) == '关键字':
            try:
                self.add_keyword(self.add_keyword_value)
                self.tabWidget.setCurrentWidget(self.keyword_tab)  # 切换展示当前页面
                self.add_keyword_value = True
                self.keyword_search_pushButton.clicked.connect(self.select_keyword_list) # 搜索按钮
            except Exception as e:
                base.consoleLog(str(e), 'e')

        return



    def select_keyword_list(self):
        base.consoleLog('加载关键字页面数据')
        # 只要点击了搜索,第一件事情就是把当前页面的数据填充为空字符串，然后把运行和明细按钮全部加载出来
        for i in range(25):
            for k in range(5):
                self.keyword_tableWidget.setItem(i, k, QTableWidgetItem(''))
        for keys in self.keyword_PushButtonAll:
            keys.setText('运行')
            keys.show()
            keys.setStyleSheet("background-color:#E1E1E1;color:rgb(47,24,248);")


        # 根据搜索条件返回数据库数据
        dict_data = self.get_keyword_select_data()
        result = KeywordData().return_list_data(dict_data)

        #如果返回的数据大于25,只要把前25条数据展示即可
        leng = result['count']
        if leng >= 25:
            for i in range(25):
                datas = result['data'][i]
                for k in range(5):
                    self.keyword_tableWidget.setItem(i, k, QTableWidgetItem(str(datas[k])))

        #如果返回的数据小于25,数据全部展示，然后多余的运行和明细按钮隐藏起来
        try:
            # 把没有数据的按钮和背景设置一样
            if leng < 25:
                for i in range(leng):
                    datas = result['data'][i]
                    for k in range(5):
                        self.keyword_tableWidget.setItem(i, k, QTableWidgetItem(str(datas[k])))

                key = list(self.keyword_PushButtonAll.keys())
                for i in range(25 - leng):
                    key[i + leng].setText('')
                    key[i + leng].hide()
                    # key[i + leng].setStyleSheet("background-color:#DDF9F8;border-radius:3px")


        except Exception as e:
            print(str(e))

        # 更新右下角总数和当前页签显示数
        self.keyword_total_amount_of_lineEdit.setText(str(result['count']))
        self.keyword_current_page_label.setText(str(result['page_number']))
        # 页面数据加载完毕，运行和详情按钮的数据重新加载
        self.get_keyword_info(result['data'])
        return

    def get_keyword_info(self, result):
        base.consoleLog('关键字操作栏按钮赋值')

        try:

            self.run_project_page_1 = RunProject()
            self.project_PushButton1.clicked.connect(self.run_project_page_1.show)
            self.run_project_page_1.setWindowTitle('项目执行' + str(result[0][6]))

            self.run_project_page_2 = RunProject()
            self.project_PushButton2.clicked.connect(self.run_project_page_2.show)
            self.run_project_page_2.setWindowTitle('项目执行' + str(result[1][6]))

            self.run_project_page_3 = RunProject()
            self.project_PushButton3.clicked.connect(self.run_project_page_3.show)
            self.run_project_page_3.setWindowTitle('项目执行' + str(result[2][6]))

            self.run_project_page_4 = RunProject()
            self.project_PushButton4.clicked.connect(self.run_project_page_4.show)
            self.run_project_page_4.setWindowTitle('项目执行' + str(result[3][6]))

            self.run_project_page_5 = RunProject()
            self.project_PushButton5.clicked.connect(self.run_project_page_5.show)
            self.run_project_page_5.setWindowTitle('项目执行' + str(result[4][6]))

            self.run_project_page_6 = RunProject()
            self.project_PushButton6.clicked.connect(self.run_project_page_6.show)
            self.run_project_page_6.setWindowTitle('项目执行' + str(result[5][6]))

            self.run_project_page_7 = RunProject()
            self.project_PushButton7.clicked.connect(self.run_project_page_7.show)
            self.run_project_page_7.setWindowTitle('项目执行' + str(result[6][6]))

            self.run_project_page_8 = RunProject()
            self.project_PushButton8.clicked.connect(self.run_project_page_8.show)
            self.run_project_page_8.setWindowTitle('项目执行' + str(result[7][6]))

            self.run_project_page_9 = RunProject()
            self.project_PushButton9.clicked.connect(self.run_project_page_9.show)
            self.run_project_page_9.setWindowTitle('项目执行' + str(result[8][6]))

            self.run_project_page_10 = RunProject()
            self.project_PushButton10.clicked.connect(self.run_project_page_10.show)
            self.run_project_page_10.setWindowTitle('项目执行' + str(result[9][6]))

            self.run_project_page_11 = RunProject()
            self.project_PushButton11.clicked.connect(self.run_project_page_11.show)
            self.run_project_page_11.setWindowTitle('项目执行' + str(result[10][6]))

            self.run_project_page_12 = RunProject()
            self.project_PushButton12.clicked.connect(self.run_project_page_12.show)
            self.run_project_page_12.setWindowTitle('项目执行' + str(result[11][6]))

            self.run_project_page_13 = RunProject()
            self.project_PushButton13.clicked.connect(self.run_project_page_13.show)
            self.run_project_page_13.setWindowTitle('项目执行' + str(result[12][6]))

            self.run_project_page_14 = RunProject()
            self.project_PushButton14.clicked.connect(self.run_project_page_14.show)
            self.run_project_page_14.setWindowTitle('项目执行' + str(result[13][6]))

            self.run_project_page_15 = RunProject()
            self.project_PushButton15.clicked.connect(self.run_project_page_15.show)
            self.run_project_page_15.setWindowTitle('项目执行' + str(result[14][6]))

            self.run_project_page_16 = RunProject()
            self.project_PushButton16.clicked.connect(self.run_project_page_16.show)
            self.run_project_page_16.setWindowTitle('项目执行' + str(result[15][6]))

            self.run_project_page_17 = RunProject()
            self.project_PushButton17.clicked.connect(self.run_project_page_17.show)
            self.run_project_page_17.setWindowTitle('项目执行' + str(result[16][6]))

            self.run_project_page_18 = RunProject()
            self.project_PushButton18.clicked.connect(self.run_project_page_18.show)
            self.run_project_page_18.setWindowTitle('项目执行' + str(result[17][6]))

            self.run_project_page_19 = RunProject()
            self.project_PushButton19.clicked.connect(self.run_project_page_19.show)
            self.run_project_page_19.setWindowTitle('项目执行' + str(result[18][6]))

            self.run_project_page_20 = RunProject()
            self.project_PushButton20.clicked.connect(self.run_project_page_20.show)
            self.run_project_page_20.setWindowTitle('项目执行' + str(result[19][6]))

            self.run_project_page_21 = RunProject()
            self.project_PushButton21.clicked.connect(self.run_project_page_21.show)
            self.run_project_page_21.setWindowTitle('项目执行' + str(result[20][6]))

            self.run_project_page_22 = RunProject()
            self.project_PushButton22.clicked.connect(self.run_project_page_22.show)
            self.run_project_page_22.setWindowTitle('项目执行' + str(result[21][6]))

            self.run_project_page_23 = RunProject()
            self.project_PushButton23.clicked.connect(self.run_project_page_23.show)
            self.run_project_page_23.setWindowTitle('项目执行' + str(result[22][6]))

            self.run_project_page_24 = RunProject()
            self.project_PushButton24.clicked.connect(self.run_project_page_24.show)
            self.run_project_page_24.setWindowTitle('项目执行' + str(result[23][6]))

            self.run_project_page_25 = RunProject()
            self.project_PushButton25.clicked.connect(self.run_project_page_25.show)
            self.run_project_page_25.setWindowTitle('项目执行' + str(result[24][6]))
        except BaseException as e:
            pass

        return

    def get_keyword_select_data(self):
        base.consoleLog('获取关键字搜索条件的数据')
        keyword_name = QLineEdit.displayText(self.keyword_name_lineEdit)
        keyword_text = QLineEdit.displayText(self.keyword_text_lineEdit)
        dict_select = {}
        dict_select['keyword_name'] = keyword_name
        dict_select['keyword_text'] = keyword_text
        dict_select['one'] = '0'
        base.consoleLog(str(dict_select))

        return dict_select

    def add_data_tab_click_cll(self):
        base.consoleLog('滑动新增数据界面')
        if self.verticalScrollBar.value() == 0:
            self.data_all_widget.setGeometry(QtCore.QRect(0, 0, 850, 1987))
        else:
            self.data_all_widget.setGeometry(QtCore.QRect(0, -200*self.verticalScrollBar.value(), 850, 1987))


    def select_project_list(self):
        base.consoleLog('加载项目运行页面数据')
        # 只要点击了搜索,第一件事情就是把当前页面的数据填充为空字符串，然后把运行和明细按钮全部加载出来
        for i in range(25):
            for k in range(5):
                self.project_tableWidget.setItem(i, k, QTableWidgetItem(''))
        for keys in self.project_PushButtonAll:
            keys.setText('运行')
            keys.show()
            keys.setStyleSheet("background-color:#E1E1E1;color:rgb(47,24,248);")
        for key in self.project_detailed_PushButtonAll.keys():
            key.setText('明细')
            key.show()
            key.setStyleSheet("background-color:#E1E1E1;color:rgb(47,24,248);")

        # 根据搜索条件返回数据库数据
        dict_data = self.get_project_select_data()
        result = TestDemoData().return_list_data(dict_data)

        #如果返回的数据大于25,只要把前25条数据展示即可
        leng = result['count']
        if leng >= 25:
            for i in range(25):
                datas = result['data'][i]
                for k in range(5):
                    self.project_tableWidget.setItem(i, k, QTableWidgetItem(str(datas[k])))

        #如果返回的数据小于25,数据全部展示，然后多余的运行和明细按钮隐藏起来
        try:
            # 把没有数据的按钮和背景设置一样
            if leng < 25:
                for i in range(leng):
                    datas = result['data'][i]
                    for k in range(5):
                        self.project_tableWidget.setItem(i, k, QTableWidgetItem(str(datas[k])))

                key = list(self.project_detailed_PushButtonAll.keys())
                keys = list(self.project_PushButtonAll.keys())
                for i in range(25 - leng):
                    key[i + leng].setText('')
                    key[i + leng].hide()
                    # key[i + leng].setStyleSheet("background-color:#DDF9F8;border-radius:3px")
                for i in range(25 - leng):
                    keys[i + leng].setText('')
                    keys[i + leng].hide()
                    # keys[i + leng].setStyleSheet("background-color:#DDF9F8;border-radius:3px")

        except Exception as e:
            print(str(e))

        # 更新右下角总数和当前页签显示数
        self.project_total_amount_of_lineEdit.setText(str(result['count']))
        self.project_current_page_label.setText(str(result['page_number']))
        # 页面数据加载完毕，运行和详情按钮的数据重新加载
        self.get_project_info(result['data'])
        return

    def get_project_info(self,result):
        """
        获取 运行和明细按钮的对应的值
        :param:result 当前列表展示的值
        :return:
        """
        base.consoleLog('项目运行操作栏按钮赋值')

        try:

            self.run_project_page_1 = RunProject()
            self.project_PushButton1.clicked.connect(self.run_project_page_1.show)
            self.run_project_page_1.setWindowTitle('项目执行' + str(result[0][6]))

            self.run_project_page_2 = RunProject()
            self.project_PushButton2.clicked.connect(self.run_project_page_2.show)
            self.run_project_page_2.setWindowTitle('项目执行' + str(result[1][6]))

            self.run_project_page_3 = RunProject()
            self.project_PushButton3.clicked.connect(self.run_project_page_3.show)
            self.run_project_page_3.setWindowTitle('项目执行' + str(result[2][6]))

            self.run_project_page_4 = RunProject()
            self.project_PushButton4.clicked.connect(self.run_project_page_4.show)
            self.run_project_page_4.setWindowTitle('项目执行' + str(result[3][6]))

            self.run_project_page_5 = RunProject()
            self.project_PushButton5.clicked.connect(self.run_project_page_5.show)
            self.run_project_page_5.setWindowTitle('项目执行' + str(result[4][6]))

            self.run_project_page_6 = RunProject()
            self.project_PushButton6.clicked.connect(self.run_project_page_6.show)
            self.run_project_page_6.setWindowTitle('项目执行' + str(result[5][6]))

            self.run_project_page_7 = RunProject()
            self.project_PushButton7.clicked.connect(self.run_project_page_7.show)
            self.run_project_page_7.setWindowTitle('项目执行' + str(result[6][6]))

            self.run_project_page_8 = RunProject()
            self.project_PushButton8.clicked.connect(self.run_project_page_8.show)
            self.run_project_page_8.setWindowTitle('项目执行' + str(result[7][6]))

            self.run_project_page_9 = RunProject()
            self.project_PushButton9.clicked.connect(self.run_project_page_9.show)
            self.run_project_page_9.setWindowTitle('项目执行' + str(result[8][6]))

            self.run_project_page_10 = RunProject()
            self.project_PushButton10.clicked.connect(self.run_project_page_10.show)
            self.run_project_page_10.setWindowTitle('项目执行' + str(result[9][6]))

            self.run_project_page_11 = RunProject()
            self.project_PushButton11.clicked.connect(self.run_project_page_11.show)
            self.run_project_page_11.setWindowTitle('项目执行' + str(result[10][6]))

            self.run_project_page_12 = RunProject()
            self.project_PushButton12.clicked.connect(self.run_project_page_12.show)
            self.run_project_page_12.setWindowTitle('项目执行' + str(result[11][6]))

            self.run_project_page_13 = RunProject()
            self.project_PushButton13.clicked.connect(self.run_project_page_13.show)
            self.run_project_page_13.setWindowTitle('项目执行' + str(result[12][6]))

            self.run_project_page_14 = RunProject()
            self.project_PushButton14.clicked.connect(self.run_project_page_14.show)
            self.run_project_page_14.setWindowTitle('项目执行' + str(result[13][6]))

            self.run_project_page_15 = RunProject()
            self.project_PushButton15.clicked.connect(self.run_project_page_15.show)
            self.run_project_page_15.setWindowTitle('项目执行' + str(result[14][6]))

            self.run_project_page_16 = RunProject()
            self.project_PushButton16.clicked.connect(self.run_project_page_16.show)
            self.run_project_page_16.setWindowTitle('项目执行' + str(result[15][6]))

            self.run_project_page_17 = RunProject()
            self.project_PushButton17.clicked.connect(self.run_project_page_17.show)
            self.run_project_page_17.setWindowTitle('项目执行' + str(result[16][6]))

            self.run_project_page_18 = RunProject()
            self.project_PushButton18.clicked.connect(self.run_project_page_18.show)
            self.run_project_page_18.setWindowTitle('项目执行' + str(result[17][6]))

            self.run_project_page_19 = RunProject()
            self.project_PushButton19.clicked.connect(self.run_project_page_19.show)
            self.run_project_page_19.setWindowTitle('项目执行' + str(result[18][6]))

            self.run_project_page_20 = RunProject()
            self.project_PushButton20.clicked.connect(self.run_project_page_20.show)
            self.run_project_page_20.setWindowTitle('项目执行' + str(result[19][6]))

            self.run_project_page_21 = RunProject()
            self.project_PushButton21.clicked.connect(self.run_project_page_21.show)
            self.run_project_page_21.setWindowTitle('项目执行' + str(result[20][6]))

            self.run_project_page_22 = RunProject()
            self.project_PushButton22.clicked.connect(self.run_project_page_22.show)
            self.run_project_page_22.setWindowTitle('项目执行' + str(result[21][6]))

            self.run_project_page_23 = RunProject()
            self.project_PushButton23.clicked.connect(self.run_project_page_23.show)
            self.run_project_page_23.setWindowTitle('项目执行' + str(result[22][6]))

            self.run_project_page_24 = RunProject()
            self.project_PushButton24.clicked.connect(self.run_project_page_24.show)
            self.run_project_page_24.setWindowTitle('项目执行' + str(result[23][6]))

            self.run_project_page_25 = RunProject()
            self.project_PushButton25.clicked.connect(self.run_project_page_25.show)
            self.run_project_page_25.setWindowTitle('项目执行' + str(result[24][6]))
        except BaseException as e:
            pass

        return

    def get_project_select_data(self):
        """
        获取项目运行页面的搜索条件
        :return:
        """
        base.consoleLog('获取项目运行搜索条件的数据')
        project = QLineEdit.displayText(self.project_name_lineEdit)
        project_text = QLineEdit.displayText(self.project_text_lineEdit)
        executor = QLineEdit.displayText(self.project_executor_lineEdit)
        dict_select = {}
        dict_select['project'] = project
        dict_select['project_text'] = project_text
        dict_select['executor'] = executor
        dict_select['one'] = '0'
        base.consoleLog(str(dict_select))

        return dict_select

    def select_project_previous_page(self):
        """
        项目运行上一页按钮
        :return:
        """
        base.consoleLog('点击项目运行上一页按钮')

        # 如果就在当前第一个页面，点击上一页之后就不搜索了
        label_page_number = self.project_current_page_label.text().split('/')
        if label_page_number[0] == '1':
            return
        else:
            #如果不是在第一个页面,那就往上加载数据,运行和明细按钮先全部加载出来
            label_page_number = label_page_number[0]
            for key in self.project_PushButtonAll:
                key.show()
            for keys in self.project_detailed_PushButtonAll.keys():
                keys.show()

            #根据查询条件返回上一页的数据，重新填充上一页的数据
            dict_select = self.get_project_select_data()
            dict_select['one'] = str((int(label_page_number) -2) * 25)
            result = TestDemoData().return_list_data(dict_select)
            if len(result['data']) < 25:
                leng = len(result['data'])
                for key in self.project_PushButtonAll:
                    if self.project_PushButtonAll[key] > leng:
                        key.hide()
                for keys in self.project_detailed_PushButtonAll:
                    if self.project_detailed_PushButtonAll[keys] > leng:
                        keys.hide()
            else:
                leng = 25
            for i in range(leng):
                datas = result['data'][i]
                for k in range(5):
                    self.project_tableWidget.setItem(i, k, QTableWidgetItem(datas[k]))
            #数据填充完毕，更新下放的当前页标签
            self.project_current_page_label.setText(
                str(int(label_page_number) - 1) + '/' + result['page_number'].split('/')[1])
            #更新运行和明细按钮的数据
            self.get_project_info(result)
            return

    def select_project_next_page(self):
        """
        项目运行下一页按钮
        :return:
        """
        base.consoleLog('点击项目运行下一页按钮')

        # 如果就在当前最后页面，点击下一页之后就不搜索了
        label_page_number = self.project_current_page_label.text().split('/')
        if  label_page_number[0] == label_page_number[1]:
            return
        else:
            label_page_number = label_page_number[0]
            for i in range(25):
                for k in range(5):
                    self.project_tableWidget.setItem(i, k, QTableWidgetItem(''))
            for key in self.project_PushButtonAll:
                key.show()

            dict_select = self.get_project_select_data()
            dict_select['one'] = str((int(label_page_number)) * 25)
            result = TestDemoData().return_list_data(dict_select)
            if len(result['data']) < 25:
                leng = len(result['data'])
                for key in self.project_PushButtonAll:
                    if self.project_PushButtonAll[key] > leng:
                        key.hide()
                for keys in self.project_detailed_PushButtonAll:
                    if self.project_detailed_PushButtonAll[keys] > leng:
                        keys.hide()
            else:
                leng = 25

            for i in range(leng):
                datas = result['data'][i]
                for k in range(5):
                    self.project_tableWidget.setItem(i, k, QTableWidgetItem(datas[k]))
            self.project_current_page_label.setText(
                str(int(label_page_number) + 1) + '/' + result['page_number'].split('/')[1])
            self.get_project_info(result)
            return

    def get_financial_repayment_select_data(self):
        """
        获取财务还款计划页面搜索数据
        :return:
        """
        base.consoleLog('获取财务还款计划页面搜索数据')
        # 收集搜索条件数据
        assetTypeData = QComboBox.currentText(self.financial_repayment_bank_comboBox)
        if assetTypeData == '全部还款':
            assetTypeData = ''
        statementStartData = QLineEdit.displayText(self.financial_repayment_bill_starting_date_lineEdit)
        if statementStartData == '':
            statementStartData = '1971-01-01'
        statementEndData = QLineEdit.displayText(self.financial_repayment_bill_closing_date_lineEdit)
        if statementEndData == '':
            statementEndData = '2099-12-31'
        repaymentStartData = QLineEdit.displayText(self.financial_repayment_starting_date_lineEdit)
        if repaymentStartData == '':
            repaymentStartData = '1971-01-01'
        repaymentEndData = QLineEdit.displayText(self.financial_repayment_closing_date_lineEdit)
        if repaymentEndData == '':
            repaymentEndData = '2099-12-31'
        dict_select = {}
        dict_select['assetTypeData'] = assetTypeData
        dict_select['statementStartData'] = statementStartData
        dict_select['statementEndData'] = statementEndData
        dict_select['repaymentStartData'] = repaymentStartData
        dict_select['repaymentEndData'] = repaymentEndData
        dict_select['one'] = '0'
        base.consoleLog(str(dict_select))
        return dict_select

    def get_financial_repayment_info(self, result):
        """
        财务还款计划详情按钮赋值
        :param: result  列表的值
        :return:
        """
        base.consoleLog('财务还款计划详情按钮赋值')
        self.financial_repayment_page_info = result
        try:
            # 详情按钮点击事件获取当前行的信息
            if self.financial_repayment_page_info:
                self.upadte_page1 = UpdateCapital()
                self.inancial_repayment_PushButton1.clicked.connect(self.upadte_page1.show)
                self.upadte_page1.assetTypeInfo.addItems([self.financial_repayment_page_info['data'][0][0]])
                self.upadte_page1.statementDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][0][1])
                self.upadte_page1.repaymentDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][0][2])
                self.upadte_page1.repaymentPeriodInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][0][3])
                self.upadte_page1.repaymentAmountInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][0][4])
                self.upadte_page1.setWindowTitle('还款计划信息' + str(self.financial_repayment_page_info['data'][0][5]))

                self.upadte_page2 = UpdateCapital()
                self.inancial_repayment_PushButton2.clicked.connect(self.upadte_page2.show)
                self.upadte_page2.assetTypeInfo.addItems([self.financial_repayment_page_info['data'][1][0]])
                self.upadte_page2.statementDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][1][1])
                self.upadte_page2.repaymentDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][1][2])
                self.upadte_page2.repaymentPeriodInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][1][3])
                self.upadte_page2.repaymentAmountInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][1][4])
                self.upadte_page2.setWindowTitle('还款计划信息' + str(self.financial_repayment_page_info['data'][1][5]))

                self.upadte_page3 = UpdateCapital()
                self.inancial_repayment_PushButton3.clicked.connect(self.upadte_page3.show)
                self.upadte_page3.assetTypeInfo.addItems([self.financial_repayment_page_info['data'][2][0]])
                self.upadte_page3.statementDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][2][1])
                self.upadte_page3.repaymentDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][2][2])
                self.upadte_page3.repaymentPeriodInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][2][3])
                self.upadte_page3.repaymentAmountInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][2][4])
                self.upadte_page3.setWindowTitle('还款计划信息' + str(self.financial_repayment_page_info['data'][2][5]))

                self.upadte_page4 = UpdateCapital()
                self.inancial_repayment_PushButton4.clicked.connect(self.upadte_page4.show)
                self.upadte_page4.assetTypeInfo.addItems([self.financial_repayment_page_info['data'][3][0]])
                self.upadte_page4.statementDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][3][1])
                self.upadte_page4.repaymentDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][3][2])
                self.upadte_page4.repaymentPeriodInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][3][3])
                self.upadte_page4.repaymentAmountInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][3][4])
                self.upadte_page4.setWindowTitle('还款计划信息' + str(self.financial_repayment_page_info['data'][3][5]))

                self.upadte_page5 = UpdateCapital()
                self.inancial_repayment_PushButton5.clicked.connect(self.upadte_page5.show)
                self.upadte_page5.assetTypeInfo.addItems([self.financial_repayment_page_info['data'][4][0]])
                self.upadte_page5.statementDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][4][1])
                self.upadte_page5.repaymentDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][4][2])
                self.upadte_page5.repaymentPeriodInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][4][3])
                self.upadte_page5.repaymentAmountInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][4][4])
                self.upadte_page5.setWindowTitle('还款计划信息' + str(self.financial_repayment_page_info['data'][4][5]))

                self.upadte_page6 = UpdateCapital()
                self.inancial_repayment_PushButton6.clicked.connect(self.upadte_page6.show)
                self.upadte_page6.assetTypeInfo.addItems([self.financial_repayment_page_info['data'][5][0]])
                self.upadte_page6.statementDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][5][1])
                self.upadte_page6.repaymentDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][5][2])
                self.upadte_page6.repaymentPeriodInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][5][3])
                self.upadte_page6.repaymentAmountInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][5][4])
                self.upadte_page6.setWindowTitle('还款计划信息' + str(self.financial_repayment_page_info['data'][5][5]))

                self.upadte_page7 = UpdateCapital()
                self.inancial_repayment_PushButton7.clicked.connect(self.upadte_page7.show)
                self.upadte_page7.assetTypeInfo.addItems([self.financial_repayment_page_info['data'][6][0]])
                self.upadte_page7.statementDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][6][1])
                self.upadte_page7.repaymentDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][6][2])
                self.upadte_page7.repaymentPeriodInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][6][3])
                self.upadte_page7.repaymentAmountInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][6][4])
                self.upadte_page7.setWindowTitle('还款计划信息' + str(self.financial_repayment_page_info['data'][6][5]))

                self.upadte_page8 = UpdateCapital()
                self.inancial_repayment_PushButton8.clicked.connect(self.upadte_page8.show)
                self.upadte_page8.assetTypeInfo.addItems([self.financial_repayment_page_info['data'][7][0]])
                self.upadte_page8.statementDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][7][1])
                self.upadte_page8.repaymentDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][7][2])
                self.upadte_page8.repaymentPeriodInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][7][3])
                self.upadte_page8.repaymentAmountInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][7][4])
                self.upadte_page8.setWindowTitle('还款计划信息' + str(self.financial_repayment_page_info['data'][7][5]))

                self.upadte_page9 = UpdateCapital()
                self.inancial_repayment_PushButton9.clicked.connect(self.upadte_page9.show)
                self.upadte_page9.assetTypeInfo.addItems([self.financial_repayment_page_info['data'][8][0]])
                self.upadte_page9.statementDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][8][1])
                self.upadte_page9.repaymentDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][8][2])
                self.upadte_page9.repaymentPeriodInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][8][3])
                self.upadte_page9.repaymentAmountInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][8][4])
                self.upadte_page9.setWindowTitle('还款计划信息' + str(self.financial_repayment_page_info['data'][8][5]))

                self.upadte_page10 = UpdateCapital()
                self.inancial_repayment_PushButton10.clicked.connect(self.upadte_page10.show)
                self.upadte_page10.assetTypeInfo.addItems([self.financial_repayment_page_info['data'][9][0]])
                self.upadte_page10.statementDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][9][1])
                self.upadte_page10.repaymentDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][9][2])
                self.upadte_page10.repaymentPeriodInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][9][3])
                self.upadte_page10.repaymentAmountInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][9][4])
                self.upadte_page10.setWindowTitle('还款计划信息' + str(self.financial_repayment_page_info['data'][9][5]))

                self.upadte_page11 = UpdateCapital()
                self.inancial_repayment_PushButton11.clicked.connect(self.upadte_page11.show)
                self.upadte_page11.assetTypeInfo.addItems([self.financial_repayment_page_info['data'][10][0]])
                self.upadte_page11.statementDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][10][1])
                self.upadte_page11.repaymentDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][10][2])
                self.upadte_page11.repaymentPeriodInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][10][3])
                self.upadte_page11.repaymentAmountInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][10][4])
                self.upadte_page11.setWindowTitle('还款计划信息' + str(self.financial_repayment_page_info['data'][10][5]))

                self.upadte_page12 = UpdateCapital()
                self.inancial_repayment_PushButton12.clicked.connect(self.upadte_page12.show)
                self.upadte_page12.assetTypeInfo.addItems([self.financial_repayment_page_info['data'][11][0]])
                self.upadte_page12.statementDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][11][1])
                self.upadte_page12.repaymentDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][11][2])
                self.upadte_page12.repaymentPeriodInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][11][3])
                self.upadte_page12.repaymentAmountInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][11][4])
                self.upadte_page12.setWindowTitle('还款计划信息' + str(self.financial_repayment_page_info['data'][11][5]))

                self.upadte_page13 = UpdateCapital()
                self.inancial_repayment_PushButton13.clicked.connect(self.upadte_page13.show)
                self.upadte_page13.assetTypeInfo.addItems([self.financial_repayment_page_info['data'][12][0]])
                self.upadte_page13.statementDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][12][1])
                self.upadte_page13.repaymentDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][12][2])
                self.upadte_page13.repaymentPeriodInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][12][3])
                self.upadte_page13.repaymentAmountInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][12][4])
                self.upadte_page13.setWindowTitle('还款计划信息' + str(self.financial_repayment_page_info['data'][12][5]))

                self.upadte_page14 = UpdateCapital()
                self.inancial_repayment_PushButton14.clicked.connect(self.upadte_page14.show)
                self.upadte_page14.assetTypeInfo.addItems([self.financial_repayment_page_info['data'][13][0]])
                self.upadte_page14.statementDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][13][1])
                self.upadte_page14.repaymentDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][13][2])
                self.upadte_page14.repaymentPeriodInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][13][3])
                self.upadte_page14.repaymentAmountInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][13][4])
                self.upadte_page14.setWindowTitle('还款计划信息' + str(self.financial_repayment_page_info['data'][13][5]))

                self.upadte_page15 = UpdateCapital()
                self.inancial_repayment_PushButton15.clicked.connect(self.upadte_page15.show)
                self.upadte_page15.assetTypeInfo.addItems([self.financial_repayment_page_info['data'][14][0]])
                self.upadte_page15.statementDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][14][1])
                self.upadte_page15.repaymentDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][14][2])
                self.upadte_page15.repaymentPeriodInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][14][3])
                self.upadte_page15.repaymentAmountInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][14][4])
                self.upadte_page15.setWindowTitle('还款计划信息' + str(self.financial_repayment_page_info['data'][14][5]))

                self.upadte_page16 = UpdateCapital()
                self.inancial_repayment_PushButton16.clicked.connect(self.upadte_page16.show)
                self.upadte_page16.assetTypeInfo.addItems([self.financial_repayment_page_info['data'][15][0]])
                self.upadte_page16.statementDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][15][1])
                self.upadte_page16.repaymentDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][15][2])
                self.upadte_page16.repaymentPeriodInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][15][3])
                self.upadte_page16.repaymentAmountInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][15][4])
                self.upadte_page16.setWindowTitle('还款计划信息' + str(self.financial_repayment_page_info['data'][15][5]))

                self.upadte_page17 = UpdateCapital()
                self.inancial_repayment_PushButton17.clicked.connect(self.upadte_page17.show)
                self.upadte_page17.assetTypeInfo.addItems([self.financial_repayment_page_info['data'][16][0]])
                self.upadte_page3.statementDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][16][1])
                self.upadte_page17.repaymentDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][16][2])
                self.upadte_page17.repaymentPeriodInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][16][3])
                self.upadte_page17.repaymentAmountInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][16][4])
                self.upadte_page17.setWindowTitle('还款计划信息' + str(self.financial_repayment_page_info['data'][16][5]))

                self.upadte_page18 = UpdateCapital()
                self.inancial_repayment_PushButton18.clicked.connect(self.upadte_page18.show)
                self.upadte_page18.assetTypeInfo.addItems([self.financial_repayment_page_info['data'][17][0]])
                self.upadte_page18.statementDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][17][1])
                self.upadte_page18.repaymentDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][17][2])
                self.upadte_page18.repaymentPeriodInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][17][3])
                self.upadte_page18.repaymentAmountInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][17][4])
                self.upadte_page18.setWindowTitle('还款计划信息' + str(self.financial_repayment_page_info['data'][17][5]))

                self.upadte_page19 = UpdateCapital()
                self.inancial_repayment_PushButton19.clicked.connect(self.upadte_page19.show)
                self.upadte_page19.assetTypeInfo.addItems([self.financial_repayment_page_info['data'][18][0]])
                self.upadte_page19.statementDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][18][1])
                self.upadte_page19.repaymentDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][18][2])
                self.upadte_page19.repaymentPeriodInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][18][3])
                self.upadte_page19.repaymentAmountInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][18][4])
                self.upadte_page19.setWindowTitle('还款计划信息' + str(self.financial_repayment_page_info['data'][18][5]))

                self.upadte_page20 = UpdateCapital()
                self.inancial_repayment_PushButton20.clicked.connect(self.upadte_page20.show)
                self.upadte_page20.assetTypeInfo.addItems([self.financial_repayment_page_info['data'][19][0]])
                self.upadte_page20.statementDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][19][1])
                self.upadte_page20.repaymentDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][19][2])
                self.upadte_page20.repaymentPeriodInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][19][3])
                self.upadte_page20.repaymentAmountInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][19][4])
                self.upadte_page20.setWindowTitle('还款计划信息' + str(self.financial_repayment_page_info['data'][19][5]))

                self.upadte_page21 = UpdateCapital()
                self.inancial_repayment_PushButton21.clicked.connect(self.upadte_page21.show)
                self.upadte_page21.assetTypeInfo.addItems([self.financial_repayment_page_info['data'][20][0]])
                self.upadte_page21.statementDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][20][1])
                self.upadte_page21.repaymentDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][20][2])
                self.upadte_page21.repaymentPeriodInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][20][3])
                self.upadte_page21.repaymentAmountInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][20][4])
                self.upadte_page21.setWindowTitle('还款计划信息' + str(self.financial_repayment_page_info['data'][20][5]))

                self.upadte_page22 = UpdateCapital()
                self.inancial_repayment_PushButton22.clicked.connect(self.upadte_page22.show)
                self.upadte_page22.assetTypeInfo.addItems([self.financial_repayment_page_info['data'][21][0]])
                self.upadte_page22.statementDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][21][1])
                self.upadte_page22.repaymentDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][21][2])
                self.upadte_page22.repaymentPeriodInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][21][3])
                self.upadte_page22.repaymentAmountInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][21][4])
                self.upadte_page22.setWindowTitle('还款计划信息' + str(self.financial_repayment_page_info['data'][21][5]))

                self.upadte_page23 = UpdateCapital()
                self.inancial_repayment_PushButton23.clicked.connect(self.upadte_page23.show)
                self.upadte_page23.assetTypeInfo.addItems([self.financial_repayment_page_info['data'][22][0]])
                self.upadte_page23.statementDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][22][1])
                self.upadte_page23.repaymentDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][22][2])
                self.upadte_page23.repaymentPeriodInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][22][3])
                self.upadte_page23.repaymentAmountInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][22][4])
                self.upadte_page23.setWindowTitle('还款计划信息' + str(self.financial_repayment_page_info['data'][22][5]))

                self.upadte_page24 = UpdateCapital()
                self.inancial_repayment_PushButton24.clicked.connect(self.upadte_page24.show)
                self.upadte_page24.assetTypeInfo.addItems([self.financial_repayment_page_info['data'][23][0]])
                self.upadte_page24.statementDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][23][1])
                self.upadte_page24.repaymentDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][23][2])
                self.upadte_page24.repaymentPeriodInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][23][3])
                self.upadte_page24.repaymentAmountInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][23][4])
                self.upadte_page24.setWindowTitle('还款计划信息' + str(self.financial_repayment_page_info['data'][23][5]))

                self.upadte_page25 = UpdateCapital()
                self.inancial_repayment_PushButton25.clicked.connect(self.upadte_page25.show)
                self.upadte_page25.assetTypeInfo.addItems([self.financial_repayment_page_info['data'][24][0]])
                self.upadte_page25.statementDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][24][1])
                self.upadte_page25.repaymentDateInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][24][2])
                self.upadte_page25.repaymentPeriodInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][24][3])
                self.upadte_page25.repaymentAmountInfoLineEdit.setText(
                    self.financial_repayment_page_info['data'][24][4])
                self.upadte_page25.setWindowTitle('还款计划信息' + str(self.financial_repayment_page_info['data'][24][5]))
        except BaseException as e:
            base.consoleLog(str(e), 'e')

    def select_financial_repayment_list(self):
        """
        查询财务还款计划页面
        :return:
        """
        base.consoleLog('查询财务还款计划页面')
        # 给当前页面注入空白字符
        for i in range(25):
            for k in range(5):
                self.financial_repayment_tableWidget.setItem(i, k, QTableWidgetItem(''))
        for key in self.inancial_repayment_PushButtonAll:
            key.show()

        dict_select = self.get_financial_repayment_select_data()
        result = FinancialRepayment().return_list_data(dict_select)
        if result['count'] == 0:
            self.financial_repayment_current_page_label.setText(result['page_number'])
            self.financial_repayment_total_amount_of_repayment_lineEdit.setText(str(result['repayment_amount']))
            self.financial_repayment_amount_lineEdit.setText(str(result['count']))
            return
        elif result['count'] < 25:
            leng = result['count']
            for key in self.inancial_repayment_PushButtonAll:
                if self.inancial_repayment_PushButtonAll[key] > leng:
                    key.hide()
        else:
            leng = 25
        for i in range(leng):
            datas = result['data'][i]
            for k in range(5):
                self.financial_repayment_tableWidget.setItem(i, k, QTableWidgetItem(datas[k]))
        self.financial_repayment_current_page_label.setText(result['page_number'])
        self.financial_repayment_total_amount_of_repayment_lineEdit.setText(str(result['repayment_amount']))
        self.financial_repayment_amount_lineEdit.setText(str(result['count']))
        self.get_financial_repayment_info(result)
        return

    def select_financial_repayment_data_previous_page(self):
        """
        还款计划上一页按钮
        :return:
        """
        base.consoleLog('点击还款计划上一页按钮')
        # 如果就在当前第一个页面，点击上一页之后就不搜索了
        label_page_number = self.financial_repayment_current_page_label.text().split('/')
        if label_page_number[0] == '1':
            return
        else:
            label_page_number = label_page_number[0]
        for key in self.inancial_repayment_PushButtonAll:
            key.show()
        dict_select = self.get_financial_repayment_select_data()
        dict_select['one'] = str((int(label_page_number) - 2) * 25)
        dict_select['two'] = str((int(label_page_number) - 1) * 25)
        result = FinancialRepayment().return_list_data(dict_select)
        if len(result['data']) < 25:
            leng = len(result['data'])
            for key in self.inancial_repayment_PushButtonAll:
                if self.inancial_repayment_PushButtonAll[key] > leng:
                    key.hide()
        else:
            leng = 25
        for i in range(leng):
            datas = result['data'][i]
            for k in range(5):
                self.financial_repayment_tableWidget.setItem(i, k, QTableWidgetItem(datas[k]))
        self.financial_repayment_current_page_label.setText(
            str(int(label_page_number) - 1) + '/' + result['page_number'].split('/')[1])
        self.financial_repayment_total_amount_of_repayment_lineEdit.setText(result['repayment_amount'])
        self.financial_repayment_amount_lineEdit.setText(str(result['count']))
        self.get_financial_repayment_info(result)
        return

    def select_financial_repayment_data_next_page(self):
        """
        还款计划下一页按钮
        :return:
        """
        base.consoleLog('点击还款计划下一页按钮')
        # 如果就在当前最后页面，点击下一页之后就不搜索了
        label_page_number = self.financial_repayment_current_page_label.text().split('/')
        if  label_page_number[0] == label_page_number[1]:
            return
        else:
            label_page_number = label_page_number[0]
            for i in range(25):
                for k in range(5):
                    self.financial_repayment_tableWidget.setItem(i, k, QTableWidgetItem(''))
        for key in self.inancial_repayment_PushButtonAll:
            key.show()
        dict_select = self.get_financial_repayment_select_data()
        dict_select['two'] = str((int(label_page_number) + 1) * 25)
        dict_select['one'] = str((int(label_page_number)) * 25)
        result = FinancialRepayment().return_list_data(dict_select)
        if len(result['data']) < 25:
            leng = len(result['data'])
            for key in self.inancial_repayment_PushButtonAll:
                if self.inancial_repayment_PushButtonAll[key] > leng:
                    key.hide()
        else:
            leng = 25
        for i in range(leng):
            datas = result['data'][i]
            for k in range(5):
                self.financial_repayment_tableWidget.setItem(i, k, QTableWidgetItem(datas[k]))
        self.financial_repayment_current_page_label.setText(
            str(int(label_page_number) + 1) + '/' + result['page_number'].split('/')[1])
        self.financial_repayment_total_amount_of_repayment_lineEdit.setText(result['repayment_amount'])
        self.financial_repayment_amount_lineEdit.setText(str(result['count']))
        self.get_financial_repayment_info(result)
        return

    def get_financial_flow_select_data(self):
        """
        获取财务账单流水页面搜索数据
        :return:
        """
        base.consoleLog('获取财务账单流水页面搜索数据')
        # 收集搜索条件数据
        classificationtData = QComboBox.currentText(self.financial_flow_type_comboBox)
        if classificationtData == '全部消费':
            classificationtData = ''
        dataStartData = QLineEdit.displayText(self.financial_flow_consumption_starting_date_lineEdit)
        if dataStartData == '':
            dataStartData = '1971-01-01'
        dataEndData = QLineEdit.displayText(self.financial_flow_consumption_closing_date_lineEdit)
        if dataEndData == '':
            dataEndData = '2099-12-31'

        createNameData = QComboBox.currentText(self.financial_flow_consumer_comboBox)
        if createNameData == '全部消费人':
            createNameData = ''

        moneyMinData = QLineEdit.displayText(self.financial_flow_min_date_lineEdit)
        if moneyMinData == '':
            moneyMinData = 0.00
        moneyMaxData = QLineEdit.displayText(self.financial_flow_max_date_lineEdit)
        if moneyMaxData == '':
            moneyMaxData = 999999.99

        dict_select = {}
        dict_select['classificationtData'] = classificationtData
        dict_select['dataStartData'] = dataStartData
        dict_select['dataEndData'] = dataEndData
        dict_select['createNameData'] = createNameData
        dict_select['moneyMinData'] = '%.2f' % float(moneyMinData)
        dict_select['moneyMaxData'] = '%.2f' % float(moneyMaxData)
        dict_select['one'] = '0'
        dict_select['two'] = '25'
        base.consoleLog(str(dict_select))
        return dict_select

    def get_financial_flow_info(self, result):
        """
        财务流水详情按钮赋值
        :param: result  列表的值
        :return:
        """
        base.consoleLog('财务流水详情按钮赋值')
        self.financial_flow_page_info = result
        try:
            # 详情按钮点击事件获取当前行的信息
            if self.financial_flow_page_info:
                self.financial_flow_delete_page1 = DeleteFinancialFlowInfo()
                self.financial_flow_delete_PushButton1.clicked.connect(self.financial_flow_delete_page1.show)
                self.financial_flow_delete_page1.setWindowTitle('警告' + str(self.financial_flow_page_info['data'][0][5]))
                self.update_financial_flow_page1 = UpdateFinancialFlow()
                self.financial_flow_PushButton1.clicked.connect(self.update_financial_flow_page1.show)
                self.update_financial_flow_page1.updateeventLineEdit.setText(
                    self.financial_flow_page_info['data'][0][0])
                self.update_financial_flow_page1.updatedataLineEdit.setText(
                    self.financial_flow_page_info['data'][0][2])
                self.update_financial_flow_page1.updateclassificationComboBox.addItems([
                    self.financial_flow_page_info['data'][0][1]])
                self.update_financial_flow_page1.updatevalueLineEdit.setText(
                    str(self.financial_flow_page_info['data'][0][3]))
                self.update_financial_flow_page1.setWindowTitle(
                    '财务流水信息' + str(self.financial_flow_page_info['data'][0][5]))

                self.financial_flow_delete_page2 = DeleteFinancialFlowInfo()
                self.financial_flow_delete_PushButton2.clicked.connect(self.financial_flow_delete_page2.show)
                self.financial_flow_delete_page2.setWindowTitle('警告' + str(self.financial_flow_page_info['data'][1][5]))
                self.update_financial_flow_page2 = UpdateFinancialFlow()
                self.financial_flow_PushButton2.clicked.connect(self.update_financial_flow_page2.show)
                self.update_financial_flow_page2.updateeventLineEdit.setText(
                    self.financial_flow_page_info['data'][1][0])
                self.update_financial_flow_page2.updatedataLineEdit.setText(
                    self.financial_flow_page_info['data'][1][2])
                self.update_financial_flow_page2.updateclassificationComboBox.addItems([
                    self.financial_flow_page_info['data'][1][1]])
                self.update_financial_flow_page2.updatevalueLineEdit.setText(
                    str(self.financial_flow_page_info['data'][1][3]))
                self.update_financial_flow_page2.setWindowTitle(
                    '财务流水信息' + str(self.financial_flow_page_info['data'][1][5]))

                self.financial_flow_delete_page3 = DeleteFinancialFlowInfo()
                self.financial_flow_delete_PushButton3.clicked.connect(self.financial_flow_delete_page3.show)
                self.financial_flow_delete_page3.setWindowTitle('警告' + str(self.financial_flow_page_info['data'][2][5]))
                self.update_financial_flow_page3 = UpdateFinancialFlow()
                self.financial_flow_PushButton3.clicked.connect(self.update_financial_flow_page3.show)
                self.update_financial_flow_page3.updateeventLineEdit.setText(
                    self.financial_flow_page_info['data'][2][0])
                self.update_financial_flow_page3.updatedataLineEdit.setText(
                    self.financial_flow_page_info['data'][2][2])
                self.update_financial_flow_page3.updateclassificationComboBox.addItems([
                    self.financial_flow_page_info['data'][2][1]])
                self.update_financial_flow_page3.updatevalueLineEdit.setText(
                    str(self.financial_flow_page_info['data'][2][3]))
                self.update_financial_flow_page3.setWindowTitle(
                    '财务流水信息' + str(self.financial_flow_page_info['data'][2][5]))

                self.financial_flow_delete_page4 = DeleteFinancialFlowInfo()
                self.financial_flow_delete_PushButton4.clicked.connect(self.financial_flow_delete_page4.show)
                self.financial_flow_delete_page4.setWindowTitle('警告' + str(self.financial_flow_page_info['data'][3][5]))
                self.update_financial_flow_page4 = UpdateFinancialFlow()
                self.financial_flow_PushButton4.clicked.connect(self.update_financial_flow_page4.show)
                self.update_financial_flow_page4.updateeventLineEdit.setText(
                    self.financial_flow_page_info['data'][3][0])
                self.update_financial_flow_page4.updatedataLineEdit.setText(
                    self.financial_flow_page_info['data'][3][2])
                self.update_financial_flow_page4.updateclassificationComboBox.addItems([
                    self.financial_flow_page_info['data'][3][1]])
                self.update_financial_flow_page4.updatevalueLineEdit.setText(
                    str(self.financial_flow_page_info['data'][3][3]))
                self.update_financial_flow_page4.setWindowTitle(
                    '财务流水信息' + str(self.financial_flow_page_info['data'][3][5]))

                self.financial_flow_delete_page5 = DeleteFinancialFlowInfo()
                self.financial_flow_delete_PushButton5.clicked.connect(self.financial_flow_delete_page5.show)
                self.financial_flow_delete_page5.setWindowTitle('警告' + str(self.financial_flow_page_info['data'][4][5]))
                self.update_financial_flow_page5 = UpdateFinancialFlow()
                self.financial_flow_PushButton5.clicked.connect(self.update_financial_flow_page5.show)
                self.update_financial_flow_page5.updateeventLineEdit.setText(
                    self.financial_flow_page_info['data'][4][0])
                self.update_financial_flow_page5.updatedataLineEdit.setText(
                    self.financial_flow_page_info['data'][4][2])
                self.update_financial_flow_page5.updateclassificationComboBox.addItems([
                    self.financial_flow_page_info['data'][4][1]])
                self.update_financial_flow_page5.updatevalueLineEdit.setText(
                    str(self.financial_flow_page_info['data'][4][3]))
                self.update_financial_flow_page5.setWindowTitle(
                    '财务流水信息' + str(self.financial_flow_page_info['data'][4][5]))

                self.financial_flow_delete_page6 = DeleteFinancialFlowInfo()
                self.financial_flow_delete_PushButton6.clicked.connect(self.financial_flow_delete_page6.show)
                self.financial_flow_delete_page6.setWindowTitle('警告' + str(self.financial_flow_page_info['data'][5][5]))
                self.update_financial_flow_page6 = UpdateFinancialFlow()
                self.financial_flow_PushButton6.clicked.connect(self.update_financial_flow_page6.show)
                self.update_financial_flow_page6.updateeventLineEdit.setText(
                    self.financial_flow_page_info['data'][5][0])
                self.update_financial_flow_page6.updatedataLineEdit.setText(
                    self.financial_flow_page_info['data'][5][2])
                self.update_financial_flow_page6.updateclassificationComboBox.addItems([
                    self.financial_flow_page_info['data'][5][1]])
                self.update_financial_flow_page6.updatevalueLineEdit.setText(
                    str(self.financial_flow_page_info['data'][5][3]))
                self.update_financial_flow_page6.setWindowTitle(
                    '财务流水信息' + str(self.financial_flow_page_info['data'][5][5]))

                self.financial_flow_delete_page7 = DeleteFinancialFlowInfo()
                self.financial_flow_delete_PushButton7.clicked.connect(self.financial_flow_delete_page7.show)
                self.financial_flow_delete_page7.setWindowTitle('警告' + str(self.financial_flow_page_info['data'][6][5]))
                self.update_financial_flow_page7 = UpdateFinancialFlow()
                self.financial_flow_PushButton7.clicked.connect(self.update_financial_flow_page7.show)
                self.update_financial_flow_page7.updateeventLineEdit.setText(
                    self.financial_flow_page_info['data'][6][0])
                self.update_financial_flow_page7.updatedataLineEdit.setText(
                    self.financial_flow_page_info['data'][6][2])
                self.update_financial_flow_page7.updateclassificationComboBox.addItems([
                    self.financial_flow_page_info['data'][6][1]])
                self.update_financial_flow_page7.updatevalueLineEdit.setText(
                    str(self.financial_flow_page_info['data'][6][3]))
                self.update_financial_flow_page7.setWindowTitle(
                    '财务流水信息' + str(self.financial_flow_page_info['data'][6][5]))

                self.financial_flow_delete_page8 = DeleteFinancialFlowInfo()
                self.financial_flow_delete_PushButton8.clicked.connect(self.financial_flow_delete_page8.show)
                self.financial_flow_delete_page8.setWindowTitle('警告' + str(self.financial_flow_page_info['data'][7][5]))
                self.update_financial_flow_page8 = UpdateFinancialFlow()
                self.financial_flow_PushButton8.clicked.connect(self.update_financial_flow_page8.show)
                self.update_financial_flow_page8.updateeventLineEdit.setText(
                    self.financial_flow_page_info['data'][7][0])
                self.update_financial_flow_page8.updatedataLineEdit.setText(
                    self.financial_flow_page_info['data'][7][2])
                self.update_financial_flow_page8.updateclassificationComboBox.addItems([
                    self.financial_flow_page_info['data'][7][1]])
                self.update_financial_flow_page8.updatevalueLineEdit.setText(
                    str(self.financial_flow_page_info['data'][7][3]))
                self.update_financial_flow_page8.setWindowTitle(
                    '财务流水信息' + str(self.financial_flow_page_info['data'][7][5]))

                self.financial_flow_delete_page9 = DeleteFinancialFlowInfo()
                self.financial_flow_delete_PushButton9.clicked.connect(self.financial_flow_delete_page9.show)
                self.financial_flow_delete_page9.setWindowTitle('警告' + str(self.financial_flow_page_info['data'][8][5]))
                self.update_financial_flow_page9 = UpdateFinancialFlow()
                self.financial_flow_PushButton9.clicked.connect(self.update_financial_flow_page9.show)
                self.update_financial_flow_page9.updateeventLineEdit.setText(
                    self.financial_flow_page_info['data'][8][0])
                self.update_financial_flow_page9.updatedataLineEdit.setText(
                    self.financial_flow_page_info['data'][8][2])
                self.update_financial_flow_page9.updateclassificationComboBox.addItems([
                    self.financial_flow_page_info['data'][8][1]])
                self.update_financial_flow_page9.updatevalueLineEdit.setText(
                    str(self.financial_flow_page_info['data'][8][3]))
                self.update_financial_flow_page9.setWindowTitle(
                    '财务流水信息' + str(self.financial_flow_page_info['data'][8][5]))

                self.financial_flow_delete_page10 = DeleteFinancialFlowInfo()
                self.financial_flow_delete_PushButton10.clicked.connect(self.financial_flow_delete_page10.show)
                self.financial_flow_delete_page10.setWindowTitle(
                    '警告' + str(self.financial_flow_page_info['data'][9][5]))
                self.update_financial_flow_page10 = UpdateFinancialFlow()
                self.financial_flow_PushButton10.clicked.connect(self.update_financial_flow_page10.show)
                self.update_financial_flow_page10.updateeventLineEdit.setText(
                    self.financial_flow_page_info['data'][9][0])
                self.update_financial_flow_page10.updatedataLineEdit.setText(
                    self.financial_flow_page_info['data'][9][2])
                self.update_financial_flow_page10.updateclassificationComboBox.addItems([
                    self.financial_flow_page_info['data'][9][1]])
                self.update_financial_flow_page10.updatevalueLineEdit.setText(
                    str(self.financial_flow_page_info['data'][9][3]))
                self.update_financial_flow_page10.setWindowTitle(
                    '财务流水信息' + str(self.financial_flow_page_info['data'][9][5]))

                self.financial_flow_delete_page11 = DeleteFinancialFlowInfo()
                self.financial_flow_delete_PushButton11.clicked.connect(self.financial_flow_delete_page11.show)
                self.financial_flow_delete_page11.setWindowTitle(
                    '警告' + str(self.financial_flow_page_info['data'][10][5]))
                self.update_financial_flow_page11 = UpdateFinancialFlow()
                self.financial_flow_PushButton11.clicked.connect(self.update_financial_flow_page11.show)
                self.update_financial_flow_page11.updateeventLineEdit.setText(
                    self.financial_flow_page_info['data'][10][0])
                self.update_financial_flow_page11.updatedataLineEdit.setText(
                    self.financial_flow_page_info['data'][10][2])
                self.update_financial_flow_page11.updateclassificationComboBox.addItems([
                    self.financial_flow_page_info['data'][10][1]])
                self.update_financial_flow_page11.updatevalueLineEdit.setText(
                    str(self.financial_flow_page_info['data'][10][3]))
                self.update_financial_flow_page11.setWindowTitle(
                    '财务流水信息' + str(self.financial_flow_page_info['data'][10][5]))

                self.financial_flow_delete_page12 = DeleteFinancialFlowInfo()
                self.financial_flow_delete_PushButton12.clicked.connect(self.financial_flow_delete_page12.show)
                self.financial_flow_delete_page12.setWindowTitle(
                    '警告' + str(self.financial_flow_page_info['data'][11][5]))
                self.update_financial_flow_page12 = UpdateFinancialFlow()
                self.financial_flow_PushButton12.clicked.connect(self.update_financial_flow_page12.show)
                self.update_financial_flow_page12.updateeventLineEdit.setText(
                    self.financial_flow_page_info['data'][11][0])
                self.update_financial_flow_page12.updatedataLineEdit.setText(
                    self.financial_flow_page_info['data'][11][2])
                self.update_financial_flow_page12.updateclassificationComboBox.addItems([
                    self.financial_flow_page_info['data'][11][1]])
                self.update_financial_flow_page12.updatevalueLineEdit.setText(
                    str(self.financial_flow_page_info['data'][11][3]))
                self.update_financial_flow_page12.setWindowTitle(
                    '财务流水信息' + str(self.financial_flow_page_info['data'][11][5]))

                self.financial_flow_delete_page13 = DeleteFinancialFlowInfo()
                self.financial_flow_delete_PushButton13.clicked.connect(self.financial_flow_delete_page13.show)
                self.financial_flow_delete_page13.setWindowTitle(
                    '警告' + str(self.financial_flow_page_info['data'][12][5]))
                self.update_financial_flow_page13 = UpdateFinancialFlow()
                self.financial_flow_PushButton13.clicked.connect(self.update_financial_flow_page13.show)
                self.update_financial_flow_page13.updateeventLineEdit.setText(
                    self.financial_flow_page_info['data'][12][0])
                self.update_financial_flow_page13.updatedataLineEdit.setText(
                    self.financial_flow_page_info['data'][12][2])
                self.update_financial_flow_page13.updateclassificationComboBox.addItems([
                    self.financial_flow_page_info['data'][12][1]])
                self.update_financial_flow_page13.updatevalueLineEdit.setText(
                    str(self.financial_flow_page_info['data'][12][3]))
                self.update_financial_flow_page13.setWindowTitle(
                    '财务流水信息' + str(self.financial_flow_page_info['data'][12][5]))

                self.financial_flow_delete_page14 = DeleteFinancialFlowInfo()
                self.financial_flow_delete_PushButton14.clicked.connect(self.financial_flow_delete_page14.show)
                self.financial_flow_delete_page14.setWindowTitle(
                    '警告' + str(self.financial_flow_page_info['data'][13][5]))
                self.update_financial_flow_page14 = UpdateFinancialFlow()
                self.financial_flow_PushButton14.clicked.connect(self.update_financial_flow_page14.show)
                self.update_financial_flow_page14.updateeventLineEdit.setText(
                    self.financial_flow_page_info['data'][13][0])
                self.update_financial_flow_page14.updatedataLineEdit.setText(
                    self.financial_flow_page_info['data'][13][2])
                self.update_financial_flow_page14.updateclassificationComboBox.addItems([
                    self.financial_flow_page_info['data'][13][1]])
                self.update_financial_flow_page14.updatevalueLineEdit.setText(
                    str(self.financial_flow_page_info['data'][13][3]))
                self.update_financial_flow_page14.setWindowTitle(
                    '财务流水信息' + str(self.financial_flow_page_info['data'][13][5]))

                self.financial_flow_delete_page15 = DeleteFinancialFlowInfo()
                self.financial_flow_delete_PushButton15.clicked.connect(self.financial_flow_delete_page15.show)
                self.financial_flow_delete_page15.setWindowTitle(
                    '警告' + str(self.financial_flow_page_info['data'][14][5]))
                self.update_financial_flow_page15 = UpdateFinancialFlow()
                self.financial_flow_PushButton15.clicked.connect(self.update_financial_flow_page15.show)
                self.update_financial_flow_page15.updateeventLineEdit.setText(
                    self.financial_flow_page_info['data'][14][0])
                self.update_financial_flow_page15.updatedataLineEdit.setText(
                    self.financial_flow_page_info['data'][14][2])
                self.update_financial_flow_page15.updateclassificationComboBox.addItems([
                    self.financial_flow_page_info['data'][14][1]])
                self.update_financial_flow_page15.updatevalueLineEdit.setText(
                    str(self.financial_flow_page_info['data'][14][3]))
                self.update_financial_flow_page15.setWindowTitle(
                    '财务流水信息' + str(self.financial_flow_page_info['data'][14][5]))

                self.financial_flow_delete_page16 = DeleteFinancialFlowInfo()
                self.financial_flow_delete_PushButton16.clicked.connect(self.financial_flow_delete_page16.show)
                self.financial_flow_delete_page16.setWindowTitle(
                    '警告' + str(self.financial_flow_page_info['data'][15][5]))
                self.update_financial_flow_page16 = UpdateFinancialFlow()
                self.financial_flow_PushButton16.clicked.connect(self.update_financial_flow_page16.show)
                self.update_financial_flow_page16.updateeventLineEdit.setText(
                    self.financial_flow_page_info['data'][15][0])
                self.update_financial_flow_page16.updatedataLineEdit.setText(
                    self.financial_flow_page_info['data'][15][2])
                self.update_financial_flow_page16.updateclassificationComboBox.addItems([
                    self.financial_flow_page_info['data'][15][1]])
                self.update_financial_flow_page16.updatevalueLineEdit.setText(
                    str(self.financial_flow_page_info['data'][15][3]))
                self.update_financial_flow_page16.setWindowTitle(
                    '财务流水信息' + str(self.financial_flow_page_info['data'][15][5]))

                self.financial_flow_delete_page17 = DeleteFinancialFlowInfo()
                self.financial_flow_delete_PushButton17.clicked.connect(self.financial_flow_delete_page17.show)
                self.financial_flow_delete_page17.setWindowTitle(
                    '警告' + str(self.financial_flow_page_info['data'][16][5]))
                self.update_financial_flow_page17 = UpdateFinancialFlow()
                self.financial_flow_PushButton17.clicked.connect(self.update_financial_flow_page17.show)
                self.update_financial_flow_page17.updateeventLineEdit.setText(
                    self.financial_flow_page_info['data'][16][0])
                self.update_financial_flow_page17.updatedataLineEdit.setText(
                    self.financial_flow_page_info['data'][16][2])
                self.update_financial_flow_page17.updateclassificationComboBox.addItems([
                    self.financial_flow_page_info['data'][16][1]])
                self.update_financial_flow_page17.updatevalueLineEdit.setText(
                    str(self.financial_flow_page_info['data'][16][3]))
                self.update_financial_flow_page17.setWindowTitle(
                    '财务流水信息' + str(self.financial_flow_page_info['data'][16][5]))

                self.financial_flow_delete_page18 = DeleteFinancialFlowInfo()
                self.financial_flow_delete_PushButton18.clicked.connect(self.financial_flow_delete_page18.show)
                self.financial_flow_delete_page18.setWindowTitle(
                    '警告' + str(self.financial_flow_page_info['data'][17][5]))
                self.update_financial_flow_page18 = UpdateFinancialFlow()
                self.financial_flow_PushButton18.clicked.connect(self.update_financial_flow_page18.show)
                self.update_financial_flow_page18.updateeventLineEdit.setText(
                    self.financial_flow_page_info['data'][17][0])
                self.update_financial_flow_page18.updatedataLineEdit.setText(
                    self.financial_flow_page_info['data'][17][2])
                self.update_financial_flow_page18.updateclassificationComboBox.addItems([
                    self.financial_flow_page_info['data'][17][1]])
                self.update_financial_flow_page18.updatevalueLineEdit.setText(
                    str(self.financial_flow_page_info['data'][17][3]))
                self.update_financial_flow_page18.setWindowTitle(
                    '财务流水信息' + str(self.financial_flow_page_info['data'][17][5]))

                self.financial_flow_delete_page19 = DeleteFinancialFlowInfo()
                self.financial_flow_delete_PushButton19.clicked.connect(self.financial_flow_delete_page19.show)
                self.financial_flow_delete_page19.setWindowTitle(
                    '警告' + str(self.financial_flow_page_info['data'][18][5]))
                self.update_financial_flow_page19 = UpdateFinancialFlow()
                self.financial_flow_PushButton19.clicked.connect(self.update_financial_flow_page19.show)
                self.update_financial_flow_page19.updateeventLineEdit.setText(
                    self.financial_flow_page_info['data'][18][0])
                self.update_financial_flow_page19.updatedataLineEdit.setText(
                    self.financial_flow_page_info['data'][18][2])
                self.update_financial_flow_page19.updateclassificationComboBox.addItems([
                    self.financial_flow_page_info['data'][18][1]])
                self.update_financial_flow_page19.updatevalueLineEdit.setText(
                    str(self.financial_flow_page_info['data'][18][3]))
                self.update_financial_flow_page19.setWindowTitle(
                    '财务流水信息' + str(self.financial_flow_page_info['data'][18][5]))

                self.financial_flow_delete_page20 = DeleteFinancialFlowInfo()
                self.financial_flow_delete_PushButton20.clicked.connect(self.financial_flow_delete_page20.show)
                self.financial_flow_delete_page20.setWindowTitle(
                    '警告' + str(self.financial_flow_page_info['data'][19][5]))
                self.update_financial_flow_page20 = UpdateFinancialFlow()
                self.financial_flow_PushButton20.clicked.connect(self.update_financial_flow_page20.show)
                self.update_financial_flow_page20.updateeventLineEdit.setText(
                    self.financial_flow_page_info['data'][19][0])
                self.update_financial_flow_page20.updatedataLineEdit.setText(
                    self.financial_flow_page_info['data'][19][2])
                self.update_financial_flow_page20.updateclassificationComboBox.addItems([
                    self.financial_flow_page_info['data'][19][1]])
                self.update_financial_flow_page20.updatevalueLineEdit.setText(
                    str(self.financial_flow_page_info['data'][19][3]))
                self.update_financial_flow_page20.setWindowTitle(
                    '财务流水信息' + str(self.financial_flow_page_info['data'][19][5]))

                self.financial_flow_delete_page21 = DeleteFinancialFlowInfo()
                self.financial_flow_delete_PushButton21.clicked.connect(self.financial_flow_delete_page21.show)
                self.financial_flow_delete_page21.setWindowTitle(
                    '警告' + str(self.financial_flow_page_info['data'][20][5]))
                self.update_financial_flow_page21 = UpdateFinancialFlow()
                self.financial_flow_PushButton21.clicked.connect(self.update_financial_flow_page21.show)
                self.update_financial_flow_page21.updateeventLineEdit.setText(
                    self.financial_flow_page_info['data'][20][0])
                self.update_financial_flow_page21.updatedataLineEdit.setText(
                    self.financial_flow_page_info['data'][20][2])
                self.update_financial_flow_page21.updateclassificationComboBox.addItems([
                    self.financial_flow_page_info['data'][20][1]])
                self.update_financial_flow_page21.updatevalueLineEdit.setText(
                    str(self.financial_flow_page_info['data'][20][3]))
                self.update_financial_flow_page21.setWindowTitle(
                    '财务流水信息' + str(self.financial_flow_page_info['data'][20][5]))

                self.financial_flow_delete_page22 = DeleteFinancialFlowInfo()
                self.financial_flow_delete_PushButton22.clicked.connect(self.financial_flow_delete_page22.show)
                self.financial_flow_delete_page22.setWindowTitle(
                    '警告' + str(self.financial_flow_page_info['data'][21][5]))
                self.update_financial_flow_page22 = UpdateFinancialFlow()
                self.financial_flow_PushButton22.clicked.connect(self.update_financial_flow_page22.show)
                self.update_financial_flow_page22.updateeventLineEdit.setText(
                    self.financial_flow_page_info['data'][21][0])
                self.update_financial_flow_page22.updatedataLineEdit.setText(
                    self.financial_flow_page_info['data'][21][2])
                self.update_financial_flow_page22.updateclassificationComboBox.addItems([
                    self.financial_flow_page_info['data'][21][1]])
                self.update_financial_flow_page22.updatevalueLineEdit.setText(
                    str(self.financial_flow_page_info['data'][21][3]))
                self.update_financial_flow_page22.setWindowTitle(
                    '财务流水信息' + str(self.financial_flow_page_info['data'][21][5]))

                self.financial_flow_delete_page23 = DeleteFinancialFlowInfo()
                self.financial_flow_delete_PushButton23.clicked.connect(self.financial_flow_delete_page23.show)
                self.financial_flow_delete_page23.setWindowTitle(
                    '警告' + str(self.financial_flow_page_info['data'][22][5]))
                self.update_financial_flow_page23 = UpdateFinancialFlow()
                self.financial_flow_PushButton23.clicked.connect(self.update_financial_flow_page23.show)
                self.update_financial_flow_page23.updateeventLineEdit.setText(
                    self.financial_flow_page_info['data'][22][0])
                self.update_financial_flow_page23.updatedataLineEdit.setText(
                    self.financial_flow_page_info['data'][22][2])
                self.update_financial_flow_page23.updateclassificationComboBox.addItems([
                    self.financial_flow_page_info['data'][22][1]])
                self.update_financial_flow_page23.updatevalueLineEdit.setText(
                    str(self.financial_flow_page_info['data'][22][3]))
                self.update_financial_flow_page23.setWindowTitle(
                    '财务流水信息' + str(self.financial_flow_page_info['data'][22][5]))

                self.financial_flow_delete_page24 = DeleteFinancialFlowInfo()
                self.financial_flow_delete_PushButton24.clicked.connect(self.financial_flow_delete_page24.show)
                self.financial_flow_delete_page24.setWindowTitle(
                    '警告' + str(self.financial_flow_page_info['data'][23][5]))
                self.update_financial_flow_page24 = UpdateFinancialFlow()
                self.financial_flow_PushButton24.clicked.connect(self.update_financial_flow_page24.show)
                self.update_financial_flow_page24.updateeventLineEdit.setText(
                    self.financial_flow_page_info['data'][23][0])
                self.update_financial_flow_page24.updatedataLineEdit.setText(
                    self.financial_flow_page_info['data'][23][2])
                self.update_financial_flow_page24.updateclassificationComboBox.addItems([
                    self.financial_flow_page_info['data'][23][1]])
                self.update_financial_flow_page24.updatevalueLineEdit.setText(
                    str(self.financial_flow_page_info['data'][23][3]))
                self.update_financial_flow_page24.setWindowTitle(
                    '财务流水信息' + str(self.financial_flow_page_info['data'][23][5]))

                self.financial_flow_delete_page25 = DeleteFinancialFlowInfo()
                self.financial_flow_delete_PushButton25.clicked.connect(self.financial_flow_delete_page25.show)
                self.financial_flow_delete_page25.setWindowTitle(
                    '警告' + str(self.financial_flow_page_info['data'][24][5]))
                self.update_financial_flow_page25 = UpdateFinancialFlow()
                self.financial_flow_PushButton25.clicked.connect(self.update_financial_flow_page25.show)
                self.update_financial_flow_page25.updateeventLineEdit.setText(
                    self.financial_flow_page_info['data'][24][0])
                self.update_financial_flow_page25.updatedataLineEdit.setText(
                    self.financial_flow_page_info['data'][24][2])
                self.update_financial_flow_page25.updateclassificationComboBox.addItems([
                    self.financial_flow_page_info['data'][24][1]])
                self.update_financial_flow_page25.updatevalueLineEdit.setText(
                    str(self.financial_flow_page_info['data'][24][3]))
                self.update_financial_flow_page25.setWindowTitle(
                    '财务流水信息' + str(self.financial_flow_page_info['data'][24][5]))

        except BaseException as e:
            base.consoleLog(str(e), 'e')

        return

    def select_financial_flow_list(self):
        """
        加载财务账单流水页面
        :return:
        """
        base.consoleLog('加载财务账单流水页面')
        # 给当前页面注入空白字符
        for i in range(25):
            for k in range(5):
                self.financial_flow_tableWidget.setItem(i, k, QTableWidgetItem(''))
        for key in self.financial_flow_PushButtonAll:
            key.show()
        for key in self.financial_flow_delete_PushButtonAll:
            key.show()

        dict_select = self.get_financial_flow_select_data()
        result = FinancialFlowData().return_list_data(dict_select)
        if result['count'] == 0:
            self.financial_flow_current_page_label.setText(result['page_number'])
            self.financial_flow_total_amount_of_flow_lineEdit.setText(str(result['repayment_amount']))
            self.financial_flow_amount_lineEdit.setText(str(result['count']))
            return
        elif result['count'] < 25:
            leng = result['count']
            for key in self.financial_flow_PushButtonAll:
                if self.financial_flow_PushButtonAll[key] > leng:
                    key.hide()
            for key in self.financial_flow_delete_PushButtonAll:
                if self.financial_flow_delete_PushButtonAll[key] > leng:
                    key.hide()
        else:
            leng = 25
        for i in range(leng):
            datas = result['data'][i]
            for k in range(5):
                self.financial_flow_tableWidget.setItem(i, k, QTableWidgetItem(str(datas[k])))
        self.financial_flow_current_page_label.setText(result['page_number'])
        self.financial_flow_total_amount_of_flow_lineEdit.setText(str(result['repayment_amount']))
        self.financial_flow_amount_lineEdit.setText(str(result['count']))
        self.get_financial_flow_info(result)
        return

    def select_financial_flow_data_previous_page(self):
        """
        账单流水上一页按钮
        :return:
        """
        base.consoleLog('点击账单流水上一页按钮')
        # 如果就在当前第一个页面，点击上一页之后就不搜索了
        label_page_number = self.financial_flow_current_page_label.text().split('/')
        if label_page_number[0] == '1':
            return
        else:
            label_page_number = label_page_number[0]
        for key in self.financial_flow_PushButtonAll:
            key.show()
        for key in self.financial_flow_delete_PushButtonAll:
            key.show()
        dict_select = self.get_financial_flow_select_data()
        dict_select['one'] = str((int(label_page_number) - 2) * 25)
        dict_select['two'] = str((int(label_page_number) - 1) * 25)
        result = FinancialFlowData().return_list_data(dict_select)
        if len(result['data']) < 25:
            leng = len(result['data'])
            for key in self.financial_flow_PushButtonAll:
                if self.financial_flow_PushButtonAll[key] > leng:
                    key.hide()
            for key in self.financial_flow_delete_PushButtonAll:
                if self.financial_flow_delete_PushButtonAll[key] > leng:
                    key.hide()
        else:
            leng = 25
        for i in range(leng):
            datas = result['data'][i]
            for k in range(5):
                self.financial_flow_tableWidget.setItem(i, k, QTableWidgetItem(str(datas[k])))
        self.financial_flow_current_page_label.setText(
            str(int(label_page_number) - 1) + '/' + result['page_number'].split('/')[1])
        self.financial_flow_total_amount_of_flow_lineEdit.setText(result['repayment_amount'])
        self.financial_flow_amount_lineEdit.setText(str(result['count']))
        self.get_financial_flow_info(result)
        return

    def select_financial_flow_data_next_page(self):
        """
        账单流水下一页按钮
        :return:
        """
        base.consoleLog('点击账单流水下一页按钮')
        # 如果就在当前最后页面
        label_page_number = self.financial_flow_current_page_label.text().split('/')
        if label_page_number[0] == label_page_number[1]:
            return
        else:
            label_page_number = label_page_number[0]
            for i in range(25):
                for k in range(5):
                    self.financial_flow_tableWidget.setItem(i, k, QTableWidgetItem(''))
        for key in self.financial_flow_PushButtonAll:
            key.show()
        for key in self.financial_flow_delete_PushButtonAll:
            key.show()
        dict_select = self.get_financial_flow_select_data()
        dict_select['two'] = str((int(label_page_number) + 1) * 25)
        dict_select['one'] = str((int(label_page_number)) * 25)
        result = FinancialFlowData().return_list_data(dict_select)
        if len(result['data']) < 25:
            leng = len(result['data'])
            for key in self.financial_flow_PushButtonAll:
                if self.financial_flow_PushButtonAll[key] > leng:
                    key.hide()
            for key in self.financial_flow_delete_PushButtonAll:
                if self.financial_flow_delete_PushButtonAll[key] > leng:
                    key.hide()
        else:
            leng = 25
        for i in range(leng):
            datas = result['data'][i]
            for k in range(5):
                self.financial_flow_tableWidget.setItem(i, k, QTableWidgetItem(str(datas[k])))
        self.financial_flow_current_page_label.setText(
            str(int(label_page_number) + 1) + '/' + result['page_number'].split('/')[1])
        self.financial_flow_total_amount_of_flow_lineEdit.setText(result['repayment_amount'])
        self.financial_flow_amount_lineEdit.setText(str(result['count']))
        self.get_financial_flow_info(result)
        return

    def get_credit_card_info(self, result):
        base.consoleLog('信用卡详情加载窗口及数据')
        self.credit_card_page_info = result
        try:
            # 详情按钮点击事件获取当前行的信息
            if self.credit_card_page_info:
                self.credit_card_delete_page1 = DeleteCreditCardInfo()
                self.credit_card_deletePushButton1.clicked.connect(self.credit_card_delete_page1.show)
                self.credit_card_delete_page1.setWindowTitle('警告' + str(self.credit_card_page_info['data'][0][0]))
                self.update_credit_card_page1 = UpdateCreditCard()
                self.credit_card_PushButton1.clicked.connect(self.update_credit_card_page1.show)
                self.update_credit_card_page1.credit_card_name_lineEdit.setText(
                    self.credit_card_page_info['data'][0][1])
                self.update_credit_card_page1.credit_card_number_lineEdit.setText(
                    self.credit_card_page_info['data'][0][2])
                self.update_credit_card_page1.credit_card_quota_lineEdit.setText(
                    self.credit_card_page_info['data'][0][3])
                self.update_credit_card_page1.credit_card_account_date_lineEdit.setText(
                    self.credit_card_page_info['data'][0][4])
                self.update_credit_card_page1.credit_card_repayment_date_lineEdit.setText(
                    self.credit_card_page_info['data'][0][5])
                self.update_credit_card_page1.credit_card_binding_payment_name_lineEdit.setText(
                    self.credit_card_page_info['data'][0][6])
                self.update_credit_card_page1.credit_card_welfare_lineEdit.setText(
                    self.credit_card_page_info['data'][0][7])
                self.update_credit_card_page1.credit_card_welfare_data_lineEdit.setText(
                    self.credit_card_page_info['data'][0][8])
                self.update_credit_card_page1.setWindowTitle('信用卡详情' + str(self.credit_card_page_info['data'][0][0]))

                self.credit_card_delete_page2 = DeleteCreditCardInfo()
                self.credit_card_deletePushButton2.clicked.connect(self.credit_card_delete_page2.show)
                self.credit_card_delete_page2.setWindowTitle('警告' + str(self.credit_card_page_info['data'][1][0]))
                self.update_credit_card_page2 = UpdateCreditCard()
                self.credit_card_PushButton2.clicked.connect(self.update_credit_card_page2.show)
                self.update_credit_card_page2.credit_card_name_lineEdit.setText(
                    self.credit_card_page_info['data'][1][1])
                self.update_credit_card_page2.credit_card_number_lineEdit.setText(
                    self.credit_card_page_info['data'][1][2])
                self.update_credit_card_page2.credit_card_quota_lineEdit.setText(
                    self.credit_card_page_info['data'][1][3])
                self.update_credit_card_page2.credit_card_account_date_lineEdit.setText(
                    self.credit_card_page_info['data'][1][4])
                self.update_credit_card_page2.credit_card_repayment_date_lineEdit.setText(
                    self.credit_card_page_info['data'][1][5])
                self.update_credit_card_page2.credit_card_binding_payment_name_lineEdit.setText(
                    self.credit_card_page_info['data'][1][6])
                self.update_credit_card_page2.credit_card_welfare_lineEdit.setText(
                    self.credit_card_page_info['data'][1][7])
                self.update_credit_card_page2.credit_card_welfare_data_lineEdit.setText(
                    self.credit_card_page_info['data'][1][8])
                self.update_credit_card_page2.setWindowTitle('信用卡详情' + str(self.credit_card_page_info['data'][1][0]))

                self.credit_card_delete_page3 = DeleteCreditCardInfo()
                self.credit_card_deletePushButton3.clicked.connect(self.credit_card_delete_page3.show)
                self.credit_card_delete_page3.setWindowTitle('警告' + str(self.credit_card_page_info['data'][2][0]))
                self.update_credit_card_page3 = UpdateCreditCard()
                self.credit_card_PushButton3.clicked.connect(self.update_credit_card_page3.show)
                self.update_credit_card_page3.credit_card_name_lineEdit.setText(
                    self.credit_card_page_info['data'][2][1])
                self.update_credit_card_page3.credit_card_number_lineEdit.setText(
                    self.credit_card_page_info['data'][2][2])
                self.update_credit_card_page3.credit_card_quota_lineEdit.setText(
                    self.credit_card_page_info['data'][2][3])
                self.update_credit_card_page3.credit_card_account_date_lineEdit.setText(
                    self.credit_card_page_info['data'][2][4])
                self.update_credit_card_page3.credit_card_repayment_date_lineEdit.setText(
                    self.credit_card_page_info['data'][2][5])
                self.update_credit_card_page3.credit_card_binding_payment_name_lineEdit.setText(
                    self.credit_card_page_info['data'][2][6])
                self.update_credit_card_page3.credit_card_welfare_lineEdit.setText(
                    self.credit_card_page_info['data'][2][7])
                self.update_credit_card_page3.credit_card_welfare_data_lineEdit.setText(
                    self.credit_card_page_info['data'][2][8])
                self.update_credit_card_page3.setWindowTitle('信用卡详情' + str(self.credit_card_page_info['data'][2][0]))

                self.credit_card_delete_page4 = DeleteCreditCardInfo()
                self.credit_card_deletePushButton4.clicked.connect(self.credit_card_delete_page4.show)
                self.credit_card_delete_page4.setWindowTitle('警告' + str(self.credit_card_page_info['data'][3][0]))
                self.update_credit_card_page4 = UpdateCreditCard()
                self.credit_card_PushButton4.clicked.connect(self.update_credit_card_page4.show)
                self.update_credit_card_page4.credit_card_name_lineEdit.setText(
                    self.credit_card_page_info['data'][3][1])
                self.update_credit_card_page4.credit_card_number_lineEdit.setText(
                    self.credit_card_page_info['data'][3][2])
                self.update_credit_card_page4.credit_card_quota_lineEdit.setText(
                    self.credit_card_page_info['data'][3][3])
                self.update_credit_card_page4.credit_card_account_date_lineEdit.setText(
                    self.credit_card_page_info['data'][3][4])
                self.update_credit_card_page4.credit_card_repayment_date_lineEdit.setText(
                    self.credit_card_page_info['data'][3][5])
                self.update_credit_card_page4.credit_card_binding_payment_name_lineEdit.setText(
                    self.credit_card_page_info['data'][3][6])
                self.update_credit_card_page4.credit_card_welfare_lineEdit.setText(
                    self.credit_card_page_info['data'][3][7])
                self.update_credit_card_page4.credit_card_welfare_data_lineEdit.setText(
                    self.credit_card_page_info['data'][3][8])
                self.update_credit_card_page4.setWindowTitle('信用卡详情' + str(self.credit_card_page_info['data'][3][0]))

                self.credit_card_delete_page5 = DeleteCreditCardInfo()
                self.credit_card_deletePushButton5.clicked.connect(self.credit_card_delete_page5.show)
                self.credit_card_delete_page5.setWindowTitle('警告' + str(self.credit_card_page_info['data'][4][0]))
                self.update_credit_card_page5 = UpdateCreditCard()
                self.credit_card_PushButton5.clicked.connect(self.update_credit_card_page5.show)
                self.update_credit_card_page5.credit_card_name_lineEdit.setText(
                    self.credit_card_page_info['data'][4][1])
                self.update_credit_card_page5.credit_card_number_lineEdit.setText(
                    self.credit_card_page_info['data'][4][2])
                self.update_credit_card_page5.credit_card_quota_lineEdit.setText(
                    self.credit_card_page_info['data'][4][3])
                self.update_credit_card_page5.credit_card_account_date_lineEdit.setText(
                    self.credit_card_page_info['data'][4][4])
                self.update_credit_card_page5.credit_card_repayment_date_lineEdit.setText(
                    self.credit_card_page_info['data'][4][5])
                self.update_credit_card_page5.credit_card_binding_payment_name_lineEdit.setText(
                    self.credit_card_page_info['data'][4][6])
                self.update_credit_card_page5.credit_card_welfare_lineEdit.setText(
                    self.credit_card_page_info['data'][4][7])
                self.update_credit_card_page5.credit_card_welfare_data_lineEdit.setText(
                    self.credit_card_page_info['data'][4][8])
                self.update_credit_card_page5.setWindowTitle('信用卡详情' + str(self.credit_card_page_info['data'][4][0]))

                self.credit_card_delete_page6 = DeleteCreditCardInfo()
                self.credit_card_deletePushButton6.clicked.connect(self.credit_card_delete_page6.show)
                self.credit_card_delete_page6.setWindowTitle('警告' + str(self.credit_card_page_info['data'][5][0]))
                self.update_credit_card_page6 = UpdateCreditCard()
                self.credit_card_PushButton6.clicked.connect(self.update_credit_card_page6.show)
                self.update_credit_card_page6.credit_card_name_lineEdit.setText(
                    self.credit_card_page_info['data'][5][1])
                self.update_credit_card_page6.credit_card_number_lineEdit.setText(
                    self.credit_card_page_info['data'][5][2])
                self.update_credit_card_page6.credit_card_quota_lineEdit.setText(
                    self.credit_card_page_info['data'][5][3])
                self.update_credit_card_page6.credit_card_account_date_lineEdit.setText(
                    self.credit_card_page_info['data'][5][4])
                self.update_credit_card_page6.credit_card_repayment_date_lineEdit.setText(
                    self.credit_card_page_info['data'][5][5])
                self.update_credit_card_page6.credit_card_binding_payment_name_lineEdit.setText(
                    self.credit_card_page_info['data'][5][6])
                self.update_credit_card_page6.credit_card_welfare_lineEdit.setText(
                    self.credit_card_page_info['data'][5][7])
                self.update_credit_card_page6.credit_card_welfare_data_lineEdit.setText(
                    self.credit_card_page_info['data'][5][8])
                self.update_credit_card_page6.setWindowTitle('信用卡详情' + str(self.credit_card_page_info['data'][5][0]))

                self.credit_card_delete_page7 = DeleteCreditCardInfo()
                self.credit_card_deletePushButton7.clicked.connect(self.credit_card_delete_page7.show)
                self.credit_card_delete_page7.setWindowTitle('警告' + str(self.credit_card_page_info['data'][6][0]))
                self.update_credit_card_page7 = UpdateCreditCard()
                self.credit_card_PushButton7.clicked.connect(self.update_credit_card_page7.show)
                self.update_credit_card_page7.credit_card_name_lineEdit.setText(
                    self.credit_card_page_info['data'][6][1])
                self.update_credit_card_page7.credit_card_number_lineEdit.setText(
                    self.credit_card_page_info['data'][6][2])
                self.update_credit_card_page7.credit_card_quota_lineEdit.setText(
                    self.credit_card_page_info['data'][6][3])
                self.update_credit_card_page7.credit_card_account_date_lineEdit.setText(
                    self.credit_card_page_info['data'][6][4])
                self.update_credit_card_page7.credit_card_repayment_date_lineEdit.setText(
                    self.credit_card_page_info['data'][6][5])
                self.update_credit_card_page7.credit_card_binding_payment_name_lineEdit.setText(
                    self.credit_card_page_info['data'][6][6])
                self.update_credit_card_page7.credit_card_welfare_lineEdit.setText(
                    self.credit_card_page_info['data'][6][7])
                self.update_credit_card_page7.credit_card_welfare_data_lineEdit.setText(
                    self.credit_card_page_info['data'][6][8])
                self.update_credit_card_page7.setWindowTitle('信用卡详情' + str(self.credit_card_page_info['data'][6][0]))

                self.credit_card_delete_page8 = DeleteCreditCardInfo()
                self.credit_card_deletePushButton8.clicked.connect(self.credit_card_delete_page8.show)
                self.credit_card_delete_page8.setWindowTitle('警告' + str(self.credit_card_page_info['data'][7][0]))
                self.update_credit_card_page8 = UpdateCreditCard()
                self.credit_card_PushButton8.clicked.connect(self.update_credit_card_page8.show)
                self.update_credit_card_page8.credit_card_name_lineEdit.setText(
                    self.credit_card_page_info['data'][7][1])
                self.update_credit_card_page8.credit_card_number_lineEdit.setText(
                    self.credit_card_page_info['data'][7][2])
                self.update_credit_card_page8.credit_card_quota_lineEdit.setText(
                    self.credit_card_page_info['data'][7][3])
                self.update_credit_card_page8.credit_card_account_date_lineEdit.setText(
                    self.credit_card_page_info['data'][7][4])
                self.update_credit_card_page8.credit_card_repayment_date_lineEdit.setText(
                    self.credit_card_page_info['data'][7][5])
                self.update_credit_card_page8.credit_card_binding_payment_name_lineEdit.setText(
                    self.credit_card_page_info['data'][7][6])
                self.update_credit_card_page8.credit_card_welfare_lineEdit.setText(
                    self.credit_card_page_info['data'][7][7])
                self.update_credit_card_page8.credit_card_welfare_data_lineEdit.setText(
                    self.credit_card_page_info['data'][7][8])
                self.update_credit_card_page8.setWindowTitle('信用卡详情' + str(self.credit_card_page_info['data'][7][0]))

                self.credit_card_delete_page9 = DeleteCreditCardInfo()
                self.credit_card_deletePushButton9.clicked.connect(self.credit_card_delete_page9.show)
                self.credit_card_delete_page9.setWindowTitle('警告' + str(self.credit_card_page_info['data'][8][0]))
                self.update_credit_card_page9 = UpdateCreditCard()
                self.credit_card_PushButton9.clicked.connect(self.update_credit_card_page9.show)
                self.update_credit_card_page9.credit_card_name_lineEdit.setText(
                    self.credit_card_page_info['data'][8][1])
                self.update_credit_card_page9.credit_card_number_lineEdit.setText(
                    self.credit_card_page_info['data'][8][2])
                self.update_credit_card_page9.credit_card_quota_lineEdit.setText(
                    self.credit_card_page_info['data'][8][3])
                self.update_credit_card_page9.credit_card_account_date_lineEdit.setText(
                    self.credit_card_page_info['data'][8][4])
                self.update_credit_card_page9.credit_card_repayment_date_lineEdit.setText(
                    self.credit_card_page_info['data'][8][5])
                self.update_credit_card_page9.credit_card_binding_payment_name_lineEdit.setText(
                    self.credit_card_page_info['data'][8][6])
                self.update_credit_card_page9.credit_card_welfare_lineEdit.setText(
                    self.credit_card_page_info['data'][8][7])
                self.update_credit_card_page9.credit_card_welfare_data_lineEdit.setText(
                    self.credit_card_page_info['data'][8][8])
                self.update_credit_card_page9.setWindowTitle('信用卡详情' + str(self.credit_card_page_info['data'][8][0]))

                self.credit_card_delete_page10 = DeleteCreditCardInfo()
                self.credit_card_deletePushButton10.clicked.connect(self.credit_card_delete_page10.show)
                self.credit_card_delete_page10.setWindowTitle('警告' + str(self.credit_card_page_info['data'][9][0]))
                self.update_credit_card_page10 = UpdateCreditCard()
                self.credit_card_PushButton10.clicked.connect(self.update_credit_card_page10.show)
                self.update_credit_card_page10.credit_card_name_lineEdit.setText(
                    self.credit_card_page_info['data'][9][1])
                self.update_credit_card_page10.credit_card_number_lineEdit.setText(
                    self.credit_card_page_info['data'][9][2])
                self.update_credit_card_page10.credit_card_quota_lineEdit.setText(
                    self.credit_card_page_info['data'][9][3])
                self.update_credit_card_page10.credit_card_account_date_lineEdit.setText(
                    self.credit_card_page_info['data'][9][4])
                self.update_credit_card_page10.credit_card_repayment_date_lineEdit.setText(
                    self.credit_card_page_info['data'][9][5])
                self.update_credit_card_page10.credit_card_binding_payment_name_lineEdit.setText(
                    self.credit_card_page_info['data'][9][6])
                self.update_credit_card_page10.credit_card_welfare_lineEdit.setText(
                    self.credit_card_page_info['data'][9][7])
                self.update_credit_card_page10.credit_card_welfare_data_lineEdit.setText(
                    self.credit_card_page_info['data'][9][8])
                self.update_credit_card_page10.setWindowTitle('信用卡详情' + str(self.credit_card_page_info['data'][9][0]))

                self.credit_card_delete_page11 = DeleteCreditCardInfo()
                self.credit_card_deletePushButton11.clicked.connect(self.credit_card_delete_page11.show)
                self.credit_card_delete_page11.setWindowTitle('警告' + str(self.credit_card_page_info['data'][10][0]))
                self.update_credit_card_page11 = UpdateCreditCard()
                self.credit_card_PushButton11.clicked.connect(self.update_credit_card_page11.show)
                self.update_credit_card_page11.credit_card_name_lineEdit.setText(
                    self.credit_card_page_info['data'][10][1])
                self.update_credit_card_page11.credit_card_number_lineEdit.setText(
                    self.credit_card_page_info['data'][10][2])
                self.update_credit_card_page11.credit_card_quota_lineEdit.setText(
                    self.credit_card_page_info['data'][10][3])
                self.update_credit_card_page11.credit_card_account_date_lineEdit.setText(
                    self.credit_card_page_info['data'][10][4])
                self.update_credit_card_page11.credit_card_repayment_date_lineEdit.setText(
                    self.credit_card_page_info['data'][10][5])
                self.update_credit_card_page11.credit_card_binding_payment_name_lineEdit.setText(
                    self.credit_card_page_info['data'][10][6])
                self.update_credit_card_page11.credit_card_welfare_lineEdit.setText(
                    self.credit_card_page_info['data'][10][7])
                self.update_credit_card_page11.credit_card_welfare_data_lineEdit.setText(
                    self.credit_card_page_info['data'][10][8])
                self.update_credit_card_page11.setWindowTitle('信用卡详情' + str(self.credit_card_page_info['data'][10][0]))

                self.credit_card_delete_page12 = DeleteCreditCardInfo()
                self.credit_card_deletePushButton12.clicked.connect(self.credit_card_delete_page12.show)
                self.credit_card_delete_page12.setWindowTitle('警告' + str(self.credit_card_page_info['data'][11][0]))
                self.update_credit_card_page12 = UpdateCreditCard()
                self.credit_card_PushButton12.clicked.connect(self.update_credit_card_page12.show)
                self.update_credit_card_page12.credit_card_name_lineEdit.setText(
                    self.credit_card_page_info['data'][11][1])
                self.update_credit_card_page12.credit_card_number_lineEdit.setText(
                    self.credit_card_page_info['data'][11][2])
                self.update_credit_card_page12.credit_card_quota_lineEdit.setText(
                    self.credit_card_page_info['data'][11][3])
                self.update_credit_card_page12.credit_card_account_date_lineEdit.setText(
                    self.credit_card_page_info['data'][11][4])
                self.update_credit_card_page12.credit_card_repayment_date_lineEdit.setText(
                    self.credit_card_page_info['data'][11][5])
                self.update_credit_card_page12.credit_card_binding_payment_name_lineEdit.setText(
                    self.credit_card_page_info['data'][11][6])
                self.update_credit_card_page12.credit_card_welfare_lineEdit.setText(
                    self.credit_card_page_info['data'][11][7])
                self.update_credit_card_page12.credit_card_welfare_data_lineEdit.setText(
                    self.credit_card_page_info['data'][11][8])
                self.update_credit_card_page12.setWindowTitle('信用卡详情' + str(self.credit_card_page_info['data'][11][0]))

                self.credit_card_delete_page13 = DeleteCreditCardInfo()
                self.credit_card_deletePushButton13.clicked.connect(self.credit_card_delete_page13.show)
                self.credit_card_delete_page13.setWindowTitle('警告' + str(self.credit_card_page_info['data'][12][0]))
                self.update_credit_card_page13 = UpdateCreditCard()
                self.credit_card_PushButton13.clicked.connect(self.update_credit_card_page13.show)
                self.update_credit_card_page13.credit_card_name_lineEdit.setText(
                    self.credit_card_page_info['data'][12][1])
                self.update_credit_card_page13.credit_card_number_lineEdit.setText(
                    self.credit_card_page_info['data'][12][2])
                self.update_credit_card_page13.credit_card_quota_lineEdit.setText(
                    self.credit_card_page_info['data'][12][3])
                self.update_credit_card_page13.credit_card_account_date_lineEdit.setText(
                    self.credit_card_page_info['data'][12][4])
                self.update_credit_card_page13.credit_card_repayment_date_lineEdit.setText(
                    self.credit_card_page_info['data'][12][5])
                self.update_credit_card_page13.credit_card_binding_payment_name_lineEdit.setText(
                    self.credit_card_page_info['data'][12][6])
                self.update_credit_card_page13.credit_card_welfare_lineEdit.setText(
                    self.credit_card_page_info['data'][12][7])
                self.update_credit_card_page13.credit_card_welfare_data_lineEdit.setText(
                    self.credit_card_page_info['data'][12][8])
                self.update_credit_card_page13.setWindowTitle('信用卡详情' + str(self.credit_card_page_info['data'][12][0]))

                self.credit_card_delete_page14 = DeleteCreditCardInfo()
                self.credit_card_deletePushButton14.clicked.connect(self.credit_card_delete_page14.show)
                self.credit_card_delete_page14.setWindowTitle('警告' + str(self.credit_card_page_info['data'][13][0]))
                self.update_credit_card_page14 = UpdateCreditCard()
                self.credit_card_PushButton14.clicked.connect(self.update_credit_card_page14.show)
                self.update_credit_card_page14.credit_card_name_lineEdit.setText(
                    self.credit_card_page_info['data'][13][1])
                self.update_credit_card_page14.credit_card_number_lineEdit.setText(
                    self.credit_card_page_info['data'][13][2])
                self.update_credit_card_page14.credit_card_quota_lineEdit.setText(
                    self.credit_card_page_info['data'][13][3])
                self.update_credit_card_page14.credit_card_account_date_lineEdit.setText(
                    self.credit_card_page_info['data'][13][4])
                self.update_credit_card_page14.credit_card_repayment_date_lineEdit.setText(
                    self.credit_card_page_info['data'][13][5])
                self.update_credit_card_page14.credit_card_binding_payment_name_lineEdit.setText(
                    self.credit_card_page_info['data'][13][6])
                self.update_credit_card_page14.credit_card_welfare_lineEdit.setText(
                    self.credit_card_page_info['data'][13][7])
                self.update_credit_card_page14.credit_card_welfare_data_lineEdit.setText(
                    self.credit_card_page_info['data'][13][8])
                self.update_credit_card_page14.setWindowTitle('信用卡详情' + str(self.credit_card_page_info['data'][13][0]))

                self.credit_card_delete_page15 = DeleteCreditCardInfo()
                self.credit_card_deletePushButton15.clicked.connect(self.credit_card_delete_page15.show)
                self.credit_card_delete_page15.setWindowTitle('警告' + str(self.credit_card_page_info['data'][14][0]))
                self.update_credit_card_page15 = UpdateCreditCard()
                self.credit_card_PushButton15.clicked.connect(self.update_credit_card_page15.show)
                self.update_credit_card_page15.credit_card_name_lineEdit.setText(
                    self.credit_card_page_info['data'][14][1])
                self.update_credit_card_page15.credit_card_number_lineEdit.setText(
                    self.credit_card_page_info['data'][14][2])
                self.update_credit_card_page15.credit_card_quota_lineEdit.setText(
                    self.credit_card_page_info['data'][14][3])
                self.update_credit_card_page15.credit_card_account_date_lineEdit.setText(
                    self.credit_card_page_info['data'][14][4])
                self.update_credit_card_page15.credit_card_repayment_date_lineEdit.setText(
                    self.credit_card_page_info['data'][14][5])
                self.update_credit_card_page15.credit_card_binding_payment_name_lineEdit.setText(
                    self.credit_card_page_info['data'][14][6])
                self.update_credit_card_page15.credit_card_welfare_lineEdit.setText(
                    self.credit_card_page_info['data'][14][7])
                self.update_credit_card_page15.credit_card_welfare_data_lineEdit.setText(
                    self.credit_card_page_info['data'][14][8])
                self.update_credit_card_page15.setWindowTitle('信用卡详情' + str(self.credit_card_page_info['data'][14][0]))

                self.credit_card_delete_page16 = DeleteCreditCardInfo()
                self.credit_card_deletePushButton16.clicked.connect(self.credit_card_delete_page16.show)
                self.credit_card_delete_page16.setWindowTitle('警告' + str(self.credit_card_page_info['data'][15][0]))
                self.update_credit_card_page16 = UpdateCreditCard()
                self.credit_card_PushButton16.clicked.connect(self.update_credit_card_page16.show)
                self.update_credit_card_page16.credit_card_name_lineEdit.setText(
                    self.credit_card_page_info['data'][15][1])
                self.update_credit_card_page16.credit_card_number_lineEdit.setText(
                    self.credit_card_page_info['data'][15][2])
                self.update_credit_card_page16.credit_card_quota_lineEdit.setText(
                    self.credit_card_page_info['data'][15][3])
                self.update_credit_card_page16.credit_card_account_date_lineEdit.setText(
                    self.credit_card_page_info['data'][15][4])
                self.update_credit_card_page16.credit_card_repayment_date_lineEdit.setText(
                    self.credit_card_page_info['data'][15][5])
                self.update_credit_card_page16.credit_card_binding_payment_name_lineEdit.setText(
                    self.credit_card_page_info['data'][15][6])
                self.update_credit_card_page16.credit_card_welfare_lineEdit.setText(
                    self.credit_card_page_info['data'][15][7])
                self.update_credit_card_page16.credit_card_welfare_data_lineEdit.setText(
                    self.credit_card_page_info['data'][15][8])
                self.update_credit_card_page16.setWindowTitle('信用卡详情' + str(self.credit_card_page_info['data'][15][0]))

                self.credit_card_delete_page17 = DeleteCreditCardInfo()
                self.credit_card_deletePushButton17.clicked.connect(self.credit_card_delete_page17.show)
                self.credit_card_delete_page17.setWindowTitle('警告' + str(self.credit_card_page_info['data'][16][0]))
                self.update_credit_card_page17 = UpdateCreditCard()
                self.credit_card_PushButton17.clicked.connect(self.update_credit_card_page17.show)
                self.update_credit_card_page17.credit_card_name_lineEdit.setText(
                    self.credit_card_page_info['data'][16][1])
                self.update_credit_card_page17.credit_card_number_lineEdit.setText(
                    self.credit_card_page_info['data'][16][2])
                self.update_credit_card_page17.credit_card_quota_lineEdit.setText(
                    self.credit_card_page_info['data'][16][3])
                self.update_credit_card_page17.credit_card_account_date_lineEdit.setText(
                    self.credit_card_page_info['data'][16][4])
                self.update_credit_card_page17.credit_card_repayment_date_lineEdit.setText(
                    self.credit_card_page_info['data'][16][5])
                self.update_credit_card_page17.credit_card_binding_payment_name_lineEdit.setText(
                    self.credit_card_page_info['data'][16][6])
                self.update_credit_card_page17.credit_card_welfare_lineEdit.setText(
                    self.credit_card_page_info['data'][16][7])
                self.update_credit_card_page17.credit_card_welfare_data_lineEdit.setText(
                    self.credit_card_page_info['data'][16][8])
                self.update_credit_card_page17.setWindowTitle('信用卡详情' + str(self.credit_card_page_info['data'][16][0]))

                self.credit_card_delete_page18 = DeleteCreditCardInfo()
                self.credit_card_deletePushButton18.clicked.connect(self.credit_card_delete_page18.show)
                self.credit_card_delete_page18.setWindowTitle('警告' + str(self.credit_card_page_info['data'][17][0]))
                self.update_credit_card_page18 = UpdateCreditCard()
                self.credit_card_PushButton18.clicked.connect(self.update_credit_card_page18.show)
                self.update_credit_card_page18.credit_card_name_lineEdit.setText(
                    self.credit_card_page_info['data'][17][1])
                self.update_credit_card_page18.credit_card_number_lineEdit.setText(
                    self.credit_card_page_info['data'][17][2])
                self.update_credit_card_page18.credit_card_quota_lineEdit.setText(
                    self.credit_card_page_info['data'][17][3])
                self.update_credit_card_page18.credit_card_account_date_lineEdit.setText(
                    self.credit_card_page_info['data'][17][4])
                self.update_credit_card_page18.credit_card_repayment_date_lineEdit.setText(
                    self.credit_card_page_info['data'][17][5])
                self.update_credit_card_page18.credit_card_binding_payment_name_lineEdit.setText(
                    self.credit_card_page_info['data'][17][6])
                self.update_credit_card_page18.credit_card_welfare_lineEdit.setText(
                    self.credit_card_page_info['data'][17][7])
                self.update_credit_card_page18.credit_card_welfare_data_lineEdit.setText(
                    self.credit_card_page_info['data'][17][8])
                self.update_credit_card_page18.setWindowTitle('信用卡详情' + str(self.credit_card_page_info['data'][17][0]))

                self.credit_card_delete_page19 = DeleteCreditCardInfo()
                self.credit_card_deletePushButton19.clicked.connect(self.credit_card_delete_page19.show)
                self.credit_card_delete_page19.setWindowTitle('警告' + str(self.credit_card_page_info['data'][18][0]))
                self.update_credit_card_page19 = UpdateCreditCard()
                self.credit_card_PushButton19.clicked.connect(self.update_credit_card_page19.show)
                self.update_credit_card_page19.credit_card_name_lineEdit.setText(
                    self.credit_card_page_info['data'][18][1])
                self.update_credit_card_page19.credit_card_number_lineEdit.setText(
                    self.credit_card_page_info['data'][18][2])
                self.update_credit_card_page19.credit_card_quota_lineEdit.setText(
                    self.credit_card_page_info['data'][18][3])
                self.update_credit_card_page19.credit_card_account_date_lineEdit.setText(
                    self.credit_card_page_info['data'][18][4])
                self.update_credit_card_page19.credit_card_repayment_date_lineEdit.setText(
                    self.credit_card_page_info['data'][18][5])
                self.update_credit_card_page19.credit_card_binding_payment_name_lineEdit.setText(
                    self.credit_card_page_info['data'][18][6])
                self.update_credit_card_page19.credit_card_welfare_lineEdit.setText(
                    self.credit_card_page_info['data'][18][7])
                self.update_credit_card_page19.credit_card_welfare_data_lineEdit.setText(
                    self.credit_card_page_info['data'][18][8])
                self.update_credit_card_page19.setWindowTitle('信用卡详情' + str(self.credit_card_page_info['data'][18][0]))

                self.credit_card_delete_page20 = DeleteCreditCardInfo()
                self.credit_card_deletePushButton20.clicked.connect(self.credit_card_delete_page20.show)
                self.credit_card_delete_page20.setWindowTitle('警告' + str(self.credit_card_page_info['data'][19][0]))
                self.update_credit_card_page20 = UpdateCreditCard()
                self.credit_card_PushButton20.clicked.connect(self.update_credit_card_page20.show)
                self.update_credit_card_page20.credit_card_name_lineEdit.setText(
                    self.credit_card_page_info['data'][19][1])
                self.update_credit_card_page20.credit_card_number_lineEdit.setText(
                    self.credit_card_page_info['data'][19][2])
                self.update_credit_card_page20.credit_card_quota_lineEdit.setText(
                    self.credit_card_page_info['data'][19][3])
                self.update_credit_card_page20.credit_card_account_date_lineEdit.setText(
                    self.credit_card_page_info['data'][19][4])
                self.update_credit_card_page20.credit_card_repayment_date_lineEdit.setText(
                    self.credit_card_page_info['data'][19][5])
                self.update_credit_card_page20.credit_card_binding_payment_name_lineEdit.setText(
                    self.credit_card_page_info['data'][19][6])
                self.update_credit_card_page20.credit_card_welfare_lineEdit.setText(
                    self.credit_card_page_info['data'][19][7])
                self.update_credit_card_page20.credit_card_welfare_data_lineEdit.setText(
                    self.credit_card_page_info['data'][19][8])
                self.update_credit_card_page20.setWindowTitle('信用卡详情' + str(self.credit_card_page_info['data'][19][0]))

                self.credit_card_delete_page21 = DeleteCreditCardInfo()
                self.credit_card_deletePushButton21.clicked.connect(self.credit_card_delete_page21.show)
                self.credit_card_delete_page21.setWindowTitle('警告' + str(self.credit_card_page_info['data'][20][0]))
                self.update_credit_card_page21 = UpdateCreditCard()
                self.credit_card_PushButton21.clicked.connect(self.update_credit_card_page21.show)
                self.update_credit_card_page21.credit_card_name_lineEdit.setText(
                    self.credit_card_page_info['data'][20][1])
                self.update_credit_card_page21.credit_card_number_lineEdit.setText(
                    self.credit_card_page_info['data'][20][2])
                self.update_credit_card_page21.credit_card_quota_lineEdit.setText(
                    self.credit_card_page_info['data'][20][3])
                self.update_credit_card_page21.credit_card_account_date_lineEdit.setText(
                    self.credit_card_page_info['data'][20][4])
                self.update_credit_card_page21.credit_card_repayment_date_lineEdit.setText(
                    self.credit_card_page_info['data'][20][5])
                self.update_credit_card_page21.credit_card_binding_payment_name_lineEdit.setText(
                    self.credit_card_page_info['data'][20][6])
                self.update_credit_card_page21.credit_card_welfare_lineEdit.setText(
                    self.credit_card_page_info['data'][20][7])
                self.update_credit_card_page21.credit_card_welfare_data_lineEdit.setText(
                    self.credit_card_page_info['data'][20][8])
                self.update_credit_card_page21.setWindowTitle('信用卡详情' + str(self.credit_card_page_info['data'][20][0]))

                self.credit_card_delete_page22 = DeleteCreditCardInfo()
                self.credit_card_deletePushButton22.clicked.connect(self.credit_card_delete_page22.show)
                self.credit_card_delete_page22.setWindowTitle('警告' + str(self.credit_card_page_info['data'][21][0]))
                self.update_credit_card_page22 = UpdateCreditCard()
                self.credit_card_PushButton22.clicked.connect(self.update_credit_card_page22.show)
                self.update_credit_card_page22.credit_card_name_lineEdit.setText(
                    self.credit_card_page_info['data'][21][1])
                self.update_credit_card_page22.credit_card_number_lineEdit.setText(
                    self.credit_card_page_info['data'][21][2])
                self.update_credit_card_page22.credit_card_quota_lineEdit.setText(
                    self.credit_card_page_info['data'][21][3])
                self.update_credit_card_page22.credit_card_account_date_lineEdit.setText(
                    self.credit_card_page_info['data'][21][4])
                self.update_credit_card_page22.credit_card_repayment_date_lineEdit.setText(
                    self.credit_card_page_info['data'][21][5])
                self.update_credit_card_page22.credit_card_binding_payment_name_lineEdit.setText(
                    self.credit_card_page_info['data'][21][6])
                self.update_credit_card_page22.credit_card_welfare_lineEdit.setText(
                    self.credit_card_page_info['data'][21][7])
                self.update_credit_card_page22.credit_card_welfare_data_lineEdit.setText(
                    self.credit_card_page_info['data'][21][8])
                self.update_credit_card_page22.setWindowTitle('信用卡详情' + str(self.credit_card_page_info['data'][21][0]))

                self.credit_card_delete_page23 = DeleteCreditCardInfo()
                self.credit_card_deletePushButton23.clicked.connect(self.credit_card_delete_page23.show)
                self.credit_card_delete_page23.setWindowTitle('警告' + str(self.credit_card_page_info['data'][22][0]))
                self.update_credit_card_page23 = UpdateCreditCard()
                self.credit_card_PushButton23.clicked.connect(self.update_credit_card_page23.show)
                self.update_credit_card_page23.credit_card_name_lineEdit.setText(
                    self.credit_card_page_info['data'][22][1])
                self.update_credit_card_page23.credit_card_number_lineEdit.setText(
                    self.credit_card_page_info['data'][22][2])
                self.update_credit_card_page23.credit_card_quota_lineEdit.setText(
                    self.credit_card_page_info['data'][22][3])
                self.update_credit_card_page23.credit_card_account_date_lineEdit.setText(
                    self.credit_card_page_info['data'][22][4])
                self.update_credit_card_page23.credit_card_repayment_date_lineEdit.setText(
                    self.credit_card_page_info['data'][22][5])
                self.update_credit_card_page23.credit_card_binding_payment_name_lineEdit.setText(
                    self.credit_card_page_info['data'][22][6])
                self.update_credit_card_page23.credit_card_welfare_lineEdit.setText(
                    self.credit_card_page_info['data'][22][7])
                self.update_credit_card_page23.credit_card_welfare_data_lineEdit.setText(
                    self.credit_card_page_info['data'][22][8])
                self.update_credit_card_page23.setWindowTitle('信用卡详情' + str(self.credit_card_page_info['data'][22][0]))

                self.credit_card_delete_page24 = DeleteCreditCardInfo()
                self.credit_card_deletePushButton24.clicked.connect(self.credit_card_delete_page24.show)
                self.credit_card_delete_page24.setWindowTitle('警告' + str(self.credit_card_page_info['data'][23][0]))
                self.update_credit_card_page24 = UpdateCreditCard()
                self.credit_card_PushButton24.clicked.connect(self.update_credit_card_page24.show)
                self.update_credit_card_page24.credit_card_name_lineEdit.setText(
                    self.credit_card_page_info['data'][23][1])
                self.update_credit_card_page24.credit_card_number_lineEdit.setText(
                    self.credit_card_page_info['data'][23][2])
                self.update_credit_card_page24.credit_card_quota_lineEdit.setText(
                    self.credit_card_page_info['data'][23][3])
                self.update_credit_card_page24.credit_card_account_date_lineEdit.setText(
                    self.credit_card_page_info['data'][23][4])
                self.update_credit_card_page24.credit_card_repayment_date_lineEdit.setText(
                    self.credit_card_page_info['data'][23][5])
                self.update_credit_card_page24.credit_card_binding_payment_name_lineEdit.setText(
                    self.credit_card_page_info['data'][23][6])
                self.update_credit_card_page24.credit_card_welfare_lineEdit.setText(
                    self.credit_card_page_info['data'][23][7])
                self.update_credit_card_page24.credit_card_welfare_data_lineEdit.setText(
                    self.credit_card_page_info['data'][23][8])
                self.update_credit_card_page24.setWindowTitle('信用卡详情' + str(self.credit_card_page_info['data'][23][0]))

                self.credit_card_delete_page25 = DeleteCreditCardInfo()
                self.credit_card_deletePushButton25.clicked.connect(self.credit_card_delete_page25.show)
                self.credit_card_delete_page25.setWindowTitle('警告' + str(self.credit_card_page_info['data'][24][0]))
                self.update_credit_card_page25 = UpdateCreditCard()
                self.credit_card_PushButton25.clicked.connect(self.update_credit_card_page25.show)
                self.update_credit_card_page25.credit_card_name_lineEdit.setText(
                    self.credit_card_page_info['data'][24][1])
                self.update_credit_card_page25.credit_card_number_lineEdit.setText(
                    self.credit_card_page_info['data'][24][2])
                self.update_credit_card_page25.credit_card_quota_lineEdit.setText(
                    self.credit_card_page_info['data'][24][3])
                self.update_credit_card_page25.credit_card_account_date_lineEdit.setText(
                    self.credit_card_page_info['data'][24][4])
                self.update_credit_card_page25.credit_card_repayment_date_lineEdit.setText(
                    self.credit_card_page_info['data'][24][5])
                self.update_credit_card_page25.credit_card_binding_payment_name_lineEdit.setText(
                    self.credit_card_page_info['data'][24][6])
                self.update_credit_card_page25.credit_card_welfare_lineEdit.setText(
                    self.credit_card_page_info['data'][24][7])
                self.update_credit_card_page25.credit_card_welfare_data_lineEdit.setText(
                    self.credit_card_page_info['data'][24][8])
                self.update_credit_card_page25.setWindowTitle('信用卡详情' + str(self.credit_card_page_info['data'][24][0]))


        except BaseException as e:
            base.consoleLog(str(e), 'e')
            pass
        return

    def select_credit_card_list(self):
        base.consoleLog('查询信用卡页面数据')
        # 给当前页面注入空白字符
        for i in range(25):
            for k in range(8):
                self.credit_card_tableWidget.setItem(i, k, QTableWidgetItem(''))
        for key in self.credit_card_PushButtonAll:
            key.show()
        for key in self.credit_card_deletePushButtonAll:
            key.show()

        result = CreditCardData().return_list_data()
        leng = result['count']
        for key in self.credit_card_PushButtonAll:
            if self.credit_card_PushButtonAll[key] > leng:
                key.hide()
        for key in self.credit_card_deletePushButtonAll:
            if self.credit_card_deletePushButtonAll[key] > leng:
                key.hide()

        for i in range(leng):
            datas = result['data'][i]
            for k in range(8):
                self.credit_card_tableWidget.setItem(i, k, QTableWidgetItem(str(datas[k + 1])))
        self.get_credit_card_info(result)
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())
