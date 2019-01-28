# -*- coding: utf-8 -*-
"""
查询financial_repayment_data的数据,返回给前端展示
"""
import math
from sysDemo.sqlite.mySqlite import MySqlite
from common import base

class FinancialRepayment():

    def return_list_data(self, select_dict):
        """
        根据搜索条件返回搜索结果
        :return:
        """
        base.consoleLog('根据搜索条件返回还款计划数据')
        base.consoleLog('根据搜索条件' + str(select_dict))
        sql_count = """SELECT COUNT(*)
        FROM financial_repayment_data
        WHERE deleted = 0
            AND asset_type like "%s"
            AND statement_date >= "%s"
            AND statement_date <= "%s"
            AND repayment_date >= "%s"
            AND repayment_date <= "%s"  """ % (
            "%" + select_dict['assetTypeData'] + "%", select_dict['statementStartData'],
            select_dict['statementEndData'], select_dict['repaymentStartData'], select_dict['repaymentEndData'])
        count = MySqlite(sql_count).select_sql()[0][0]

        sql = """SELECT asset_type, statement_date, repayment_date, repayment_period, repayment_amount,ID,repayment_state
        FROM financial_repayment_data
        WHERE deleted = 0
            AND asset_type like "%s"
            AND statement_date >= "%s"
            AND statement_date <= "%s"
            AND repayment_date >= "%s"
            AND repayment_date <= "%s" ORDER BY repayment_date limit "%s",25 """ %  (
            "%" + select_dict['assetTypeData'] + "%", select_dict['statementStartData'],
            select_dict['statementEndData'], select_dict['repaymentStartData'], select_dict['repaymentEndData'],select_dict['one'])
        data = MySqlite(sql).select_sql()

        sql_repayment_amount = """SELECT sum(repayment_amount)
                   FROM financial_repayment_data
                   WHERE deleted = 0
                    AND asset_type like "%s"
                    AND statement_date >= "%s"
                    AND statement_date <= "%s"
                    AND repayment_date >= "%s"
                    AND repayment_date <= "%s" """ % (
            "%" + select_dict['assetTypeData'] + "%", select_dict['statementStartData'],
            select_dict['statementEndData'], select_dict['repaymentStartData'], select_dict['repaymentEndData'])
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
        base.consoleLog('返回财务流水数据：' + str(result))
        return result

