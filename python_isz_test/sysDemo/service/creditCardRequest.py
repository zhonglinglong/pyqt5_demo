# -*- coding: utf-8 -*-

"""
查询数据,返回给前端展示
"""
from sysDemo.sqlite.mySqlite import MySqlite
from common import base


class CreditCardData():

    def return_list_data(self):
        """
        根据搜索条件返回搜索结果
        :return:
        """
        base.consoleLog('加载信用卡页面数据')

        sql = """SELECT
	card_id,
	card_name,
	card_number,
	card_quota,
	account_date,
	repayment_date,
	binding_payment_name,
	welfare,
	welfare_data
FROM
	credit_card
WHERE
	deleted = 0
ORDER BY
	create_time ;"""
        data = MySqlite(sql).select_sql()

        sql = "SELECT count(*) from credit_card where deleted=0;"
        count = MySqlite(sql).select_sql()[0][0]
        result = {}
        result['data'] = data
        result['count'] = count
        return result
