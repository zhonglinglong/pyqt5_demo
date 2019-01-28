#-*- coding: utf-8 -*-
# @Time   : 2019/1/11 10:00
# @Author : linglong
# @File   : myMongoDB.py
import time

import pymongo
from classDemo.myConfigparser import NewConfigparser

class NewMongDB(object):
    """没有具体的应用场景,先设置基本的连接和单表排序的查询"""
    def __init__(self):
        self.mgConn = pymongo.MongoClient('mongodb://root:Ishangzu_mongodb@192.168.0.200:27020/')
    def db_find(self):
        self.mgDB = self.mgConn.sms.smsMtHis #指定库名,表名。
        for i in range(60):
            result = self.mgDB.find({"destPhone": '18279881085', "template_key": "login_safety_system", }).sort(
                [("create_time", -1)]).limit(1)
            for results in result:
                try:
                    print(results['content'])
                    return results['content'][24:28]
                except:
                    time.sleep(1)
                    pass
        return

t = NewMongDB()
b = t.db_find()
print(b)