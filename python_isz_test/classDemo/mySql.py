# -*- coding: utf-8 -*-
# @Time   : 2019/1/10 16:15
# @Author : linglong
# @File   : mySql.py
import pymysql
from classDemo.myConfigparser import NewConfigparser


class MySql(object):
    def __init__(self):
        self.db = 'isz_erp'
        self.host, self.port, self.user, self.password, self.charset = map(
            NewConfigparser('.//conf.ini', self.db).get_conf, ['host', 'port', 'user', 'password',
                                                               'charset'])
        self.sqlConn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, charset=self.charset, port=int(self.port))
        self.sqlCursor = self.sqlConn.cursor()

    def select(self,sql):
        """
        查询sql
        :param sql:
        :return: [{},{},{}],如果没有数据返回Fales
        """
        self.sqlCursor.execute(sql)
        cur = self.sqlCursor.description # 查询返回值的字段名称
        result = self.sqlCursor.fetchall() # 查询返回的值
        data = []
        try:
            for i in range(len(result)):
                lie = {}
                for j in range(len(cur)):
                    lie[cur[j][0]] = result[i][j]
                data.append(lie)
            self.sqlConn.close()
        except BaseException as e:
            return str(e)
        if data == []:
            return False
        return data

    def update_insert(self,sql):
        """
        更新或者插入sql
        :param sql:
        :return: 无
        """
        try:
            # 执行SQL语句
            self.sqlCursor.execute(sql)
            # 提交到数据库执行
            self.sqlConn.commit()
        except BaseException as e:
            # 发生错误时回滚
            self.sqlConn.rollback()
            return ('sql更新出错'+str(e))
        # 关闭数据库连接
        self.sqlConn.close()
        return




sql = "select contract_id,residential_id,house_id from house_contract  limit 3;"
t = MySql().select(sql)
if t:
    print(1)
else:
    print(2)