# -*- coding:utf8 -*-

"""
ERP登录类
2018年5月25日18:16:00
"""

__auto__ = 'zhonglinglong'

from classDemo import getCookie
from common import base


class Login:
    """登录类"""
    def __init__(self,user,pwd):
        self.user = user
        self.pwd = pwd
    def isz_login(self):
        """
        ISZ ERP登录
        :return:登录用户的信息
        """
        base.consoleLog('ISZ测试登录。账号：'+ self.user)
        result = getCookie.get_cookie(self.user,self.pwd)
        if result == '登录成功':
            try:
                sql = "SELECT user_id from sys_user where user_phone= %s " % self.user
                user_id = base.searchSQL(sql)[0][0]

                sql = "SELECT dep_id from sys_user where user_phone= %s " % self.user
                dep_id = base.searchSQL(sql)[0][0]

                sql = "SELECT user_name from sys_user where user_phone= %s " % self.user
                user_name = base.searchSQL(sql)[0][0]
            except BaseException as e:
                base.consoleLog('查询SQL报错。sql:' + sql + '  报错信息：' + str(e), 'e')
                return

            base.set_conf('loginUser','user',self.user)
            base.set_conf('loginUser','pwd',self.pwd)
            base.set_conf('loginUser','user_id',user_id)
            base.set_conf('loginUser','user_name',user_name)
            base.set_conf('loginUser','dep_id',dep_id)
            return result

        else:
            return result

#
# Login('18279881085','1').isz_login()