# -*- coding: utf-8 -*-

"""
查询数据,返回给前端展示
"""
import math
from sysDemo.sqlite.mySqlite import MySqlite
from common import base

class FinancialFlowData():

    def return_list_data(self, select_dict):
        """
        根据搜索条件返回搜索结果
        :return:
        """
        base.consoleLog('根据搜索条件返回财务流水数据')
        base.consoleLog('根据搜索条件' + str(select_dict))
        sql_count = """SELECT COUNT(*)
        FROM financial_flow
        WHERE deleted = 0
            AND classification like "%s"
            AND create_name like "%s"
            AND datas >= "%s"
            AND datas <= "%s"
            AND money >= "%s"
            AND money <= "%s"  """ % (
            "%" + select_dict['classificationtData'] + "%", "%" + select_dict['createNameData'] + "%",
            select_dict['dataStartData'], select_dict['dataEndData'], select_dict['moneyMinData'], select_dict['moneyMaxData'])
        count = MySqlite(sql_count).select_sql()[0][0]

        sql = """SELECT event, classification, datas, money, create_name,ID
        FROM financial_flow
        WHERE deleted = 0
            AND classification like "%s"
            AND create_name like "%s"
            AND datas >= "%s"
            AND datas <= "%s"
            AND money >= "%s"
            AND money <= "%s" ORDER BY datas desc limit "%s",25 """ %  (
            "%" + select_dict['classificationtData'] + "%", "%" + select_dict['createNameData'] + "%",
            select_dict['dataStartData'], select_dict['dataEndData'], select_dict['moneyMinData'], select_dict['moneyMaxData'],select_dict['one'])
        data = MySqlite(sql).select_sql()

        sql_repayment_amount = """SELECT sum(money)
                   FROM financial_flow
                    WHERE deleted = 0
            AND classification like "%s"
            AND create_name like "%s"
            AND datas >= "%s"
            AND datas <= "%s"
            AND money >= "%s"
            AND money <= "%s"  """ % (
            "%" + select_dict['classificationtData'] + "%", "%" + select_dict['createNameData'] + "%",
            select_dict['dataStartData'], select_dict['dataEndData'], select_dict['moneyMinData'], select_dict['moneyMaxData'])
        if count == 0:
            repayment_amount = 0.00
            page_number = '0/' + str(math.ceil(float(count) / 25))
        else:
            repayment_amount = '%.2f' % MySqlite(sql_repayment_amount).select_sql()[0][0]
            page_number = '1/' + str(math.ceil(float(count) / 25))

        result = {}
        result['data'] = data
        result['count'] = count
        result['page_number'] = page_number
        result['repayment_amount'] = repayment_amount
        base.consoleLog('返回还款计划数据：' + str(result))
        return result


