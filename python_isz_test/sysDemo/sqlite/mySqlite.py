# -*- coding: utf-8 -*-
from common import base
import sqlite3

class MySqlite(object):
    def __init__(self, sql):
        self.sql = sql

    def select_sql(self):
        """
        查询sql
        :return:
        """
        base.consoleLog('查询sql:'+self.sql)
        try:
            conn = sqlite3.connect('../sysDemo/sqlite/database.db')
            c = conn.cursor()
            cursor = c.execute(self.sql)
            b = cursor.fetchall()
            conn.close()
        except Exception as e:
            base.consoleLog(str(e),'e')
            return str(e)
        base.consoleLog(b)
        return b

    def insert_sql(self):
        """
        插入数据
        :return:
        """
        base.consoleLog('插入sql:'+self.sql)
        try:
            self.conn = sqlite3.connect('../sysDemo/sqlite/database.db')
            self.c = self.conn.cursor()
            self.cursor = self.c.execute(self.sql)
            b = self.cursor.fetchall()
            self.conn.commit()
            self.conn.close()
        except Exception as e:
            base.consoleLog(str(e), 'e')
            pass
        return b

    def update_sql(self):
        """
        更新数据
        :return:
        """
        base.consoleLog('更新sql:'+self.sql)
        try:
            conn = sqlite3.connect('../sysDemo/sqlite/database.db')
            c = conn.cursor()
            c.execute(self.sql)
            conn.commit()
            conn.close()
        except Exception as e:
            base.consoleLog(str(e), 'e')
            return str(e)
        return c

# sql = """SELECT event, classification, datas, money, create_name
#         FROM financial_flow
#         WHERE deleted = 0
#             AND classification like "%%"
#             AND create_name like "%%"
#             AND datas >= "1971-01-01"
#             AND datas <= "2099-12-31"
#             AND money >= "0"
#             AND money <= "999999" ORDER BY datas limit "0","30" """
# print(MySqlite(sql).select_sql())