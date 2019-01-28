#-*- coding: utf-8 -*-
# @Time   : 2019/1/28 10:04
# @Author : linglong
# @File   : keywordRequest.py
import math

from sysDemo.sqlite.mySqlite import MySqlite
from common import base

class KeywordData():

    def return_list_data(self, select_dict):
        """
        根据搜索条件返回搜索结果
        :return:
        """
        base.consoleLog('根据搜索条件返回关键字页面数据')
        base.consoleLog('根据搜索条件' + str(select_dict))
        sql_count = """SELECT COUNT(*)
        FROM keyword
        WHERE deleted = 0
            AND keyword_name like "%s"
            AND keyword_name like "%s"
              """ % (
            "%" + select_dict['keyword_name'] + "%", "%" + select_dict['keyword_name'] + "%")
        count = MySqlite(sql_count).select_sql()[0][0]

        sql = """SELECT keyword_name, keyword_text, keyword_data, keyword_data_text, demo,ID
       FROM keyword
        WHERE deleted = 0
            AND keyword_name like "%s"
            AND keyword_name like "%s"
              """ % (
            "%" + select_dict['keyword_name'] + "%", "%" + select_dict['keyword_name'] + "%")
        data = MySqlite(sql).select_sql()


        if count == 0:
            page_number = '0/' + str(math.ceil(float(count) / 25))
        else:
            page_number = '1/' + str(math.ceil(float(count) / 25))
        result = {}
        result['data'] = data
        result['count'] = count
        result['page_number'] = page_number
        base.consoleLog('返回关键字页面查询数据：' + str(result))
        return result