# -*- coding: utf-8 -*-
# @Time   : 2019/1/14 14:24
# @Author : linglong
# @File   : testDemoRequest.py


"""
查询数据,返回给前端展示
"""
import math

from sysDemo.sqlite.mySqlite import MySqlite
from common import base


class TestDemoData():

    def return_list_data(self, dict_data):
        """
        根据搜索条件返回搜索结果
        :param: dict_data
        :return:
        """
        base.consoleLog('查询 项目运行 的数据并返回')

        sql = """SELECT
	project,
	project_text,
	update_time,
	result,
	executor,
	script,
	ID
FROM
	test_demo
WHERE
	deleted = 0
AND project like '%s'
and project_text like '%s'
and executor like'%s'
ORDER BY
	update_time DESC limit '%s','25';""" % ('%'+dict_data['project']+'%', '%'+dict_data['project_text']+'%', '%'+dict_data['executor']+'%',dict_data['one'])
        data = MySqlite(sql).select_sql()

        sql_count = """SELECT
	count(*)
FROM
	test_demo
WHERE
	deleted = 0
AND project like '%s'
and project_text like '%s'
and executor like '%s'
ORDER BY
	update_time DESC;""" % ('%'+dict_data['project']+'%', '%'+dict_data['project_text']+'%', '%'+dict_data['executor']+'%')
        count = MySqlite(sql_count).select_sql()[0][0]

        if count == 0:
            page_number = '0/0'
        else:
            page_number = '1/' + str(math.ceil(float(count) / 25))

        result = {}
        result['data'] = data
        result['count'] = count
        result['page_number'] = page_number
        base.consoleLog('返回项目运行页面数据：' + str(result))
        return result



