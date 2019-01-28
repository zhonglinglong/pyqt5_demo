# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年4月26日16:12:13
爱上租系统管理模块接口
"""


from common import interface
from common import  base


class User:
    def __init__(self, user_phone,rolename,role_name='线上测试权限0'):
        self.role_name = role_name #角色名称
        self.user_phone = user_phone
        self.rolename = rolename #岗位名称
    def add_role_authority(self):
        """
        给角色赋所有权限
        :param role_name: 角色名称
        :return: 执行接口之后的返回值
        """

        base.consoleLog('角色赋所有权限。角色名称：' + self.role_name)

        try:
            sql = "select role_id from sys_role where role_name = '%s' limit 1" % self.role_name
            role_id = base.searchSQL(sql)[0][0]

            sql = "select res_id from sys_res"
            res_list = base.searchSQL(sql)
        except BaseException as e:
            base.consoleLog('查询SQL报错。sql:' + sql + '  报错信息：' + str(e), 'e')
            return


        def reslist():
            list = []
            for i in range(len(res_list)):
                res = {}
                res["res_id"] = res_list[i][0]
                res["attributes"] = "DEPARTMENTS"
                list.append(res)
            return list


        url = "http://isz.ishangzu.com/isz_base/RoleController/saveResByRole.action"
        data = {
        "role_id": role_id,
        "flow_list": [{
            "activityId": "30",
            "attributes": "DEPARTMENTS"
        }, {
            "activityId": "31",
            "attributes": "DEPARTMENTS"
        }, {
            "activityId": "32",
            "attributes": "DEPARTMENTS"
        }, {
            "activityId": "22",
            "attributes": "DEPARTMENTS"
        }, {
            "activityId": "23",
            "attributes": "DEPARTMENTS"
        }, {
            "activityId": "24",
            "attributes": "DEPARTMENTS"
        }, {
            "activityId": "25",
            "attributes": "DEPARTMENTS"
        }, {
            "activityId": "14",
            "attributes": "DEPARTMENTS"
        }, {
            "activityId": "15",
            "attributes": "DEPARTMENTS"
        }, {
            "activityId": "16",
            "attributes": "DEPARTMENTS"
        }, {
            "activityId": "17",
            "attributes": "DEPARTMENTS"
        }, {
            "activityId": "6",
            "attributes": "DEPARTMENTS"
        }, {
            "activityId": "7",
            "attributes": "DEPARTMENTS"
        }, {
            "activityId": "8",
            "attributes": "DEPARTMENTS"
        }, {
            "activityId": "9",
            "attributes": "DEPARTMENTS"
        }, {
            "activityId": "2",
            "attributes": "DEPARTMENTS"
        }, {
            "activityId": "3",
            "attributes": "DEPARTMENTS"
        }, {
            "activityId": "4",
            "attributes": "DEPARTMENTS"
        }, {
            "activityId": "5",
            "attributes": "DEPARTMENTS"
        }, {
            "activityId": "10",
            "attributes": "DEPARTMENTS"
        }, {
            "activityId": "11",
            "attributes": "DEPARTMENTS"
        }, {
            "activityId": "12",
            "attributes": "DEPARTMENTS"
        }, {
            "activityId": "13",
            "attributes": "DEPARTMENTS"
        }, {
            "activityId": "18",
            "attributes": "DEPARTMENTS"
        }, {
            "activityId": "19",
            "attributes": "DEPARTMENTS"
        }, {
            "activityId": "20",
            "attributes": "DEPARTMENTS"
        }, {
            "activityId": "21",
            "attributes": "DEPARTMENTS"
        }],
        "data_list": [{
            "data_type": "HOUSECONTRACT",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "APARTMENTCONTRACT",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "CONTRACTRECEIVABLE",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "CONTRACTPAYABLE",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "GENERALCONTRACT",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "CUSTOMER",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "CUSTOMERPERSON",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "CUSTOMERFOLLOW",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "CUSTOMERVIEW",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "APARTMENTVIEW",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "CONTRACTRECEIVABLEFI",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "CONTRACTPAYABLEFI",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "APARTMENTCONTRACTEND",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "HOUSECONTRACTEND",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "REIMBURSEMENTEXPENSE",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "REIMBURSEMENTEXPENSEITEM",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "CONTRACTACHIEVEMENT",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "PUSHRENTRECORD",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "APARTMENTACHIEVEMENT",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "EARNEST",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "EARNESTBREACH",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "APARTMENTCONTRACTENDLIST",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "MANAGESHARE",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "HOUSECONTRACTENDLIST",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "GENERALCONTRACTRECEIVABLE",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "HOUSEPRICEMEASURE",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "REPAIRORDER",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "VACANCYACHIEVEMENTLIST",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "BREACHACHIEVEMENTLIST",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "BACKACHIEVEMENTLIST",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "INSTALLMENTREPAYPLANS",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "REPAYLIST",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "OVDLIST",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "LENDLIST",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "INSTREPAYLIST",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "CLEANINGORDER",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "DEDUCTIONEXPENSELIST",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "DEVELOPHOUSE",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "HOUSERESOURCE",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "VALIDHOUSE",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "TRUSTEESHIPHOUSE",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "DCOVERDUERECEIVABLELIST",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "LOANSTATUSLIST",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "LOCKLIST",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "DCFINANCIALSTAGINGLIST",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "HOUSESUBJECTACTIVITYLIST",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "COMPLAINORDER",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "ONLINEHOUSELIST",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "HOUSEDEVELOPLIST",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "HOUSESTATUSCHANGELIST",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "EXPLORATIONHOUSELIST",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "APARTMENTFOLLOWLIST",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "HOUSEFOLLOWLIST",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "LOCKHOUSEINSTALLED",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "SYSTEMUSERLIST",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "PROPERTYDELIVERYLIST",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "CONTRACTAPPLICATIONORDER",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "WORKORDERLIST",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "CALLLOGINDEX",
            "perm_type": "DEPARTMENTS"
        }, {
            "data_type": "WORKORDERINDEX",
            "perm_type": "DEPARTMENTS"
        }]
        }
        data["res_list"] = reslist()
        interface.myRequest(url, data)

        base.consoleLog('角色添加所有权限接口执行完成。')
        return

    def user_quit(self,valus=True):
        """
        提交用户离职
        :return:
        """
        base.consoleLog('用户离职。离职账号',self.user_phone)

        try:
            sql = "select user_id,update_time from sys_user where user_phone = '%s'" % self.user_phone
            user_id_update_time = base.searchSQL(sql)
        except BaseException as e:
            base.consoleLog('查询SQL报错。sql:' + sql + '  报错信息：' + str(e), 'e')
            return

        if valus:
            user_status = "LEAVING"
            url = "http://isz.ishangzu.com/isz_base/UserController/saveUser.action"
            data = {
                "remark": "测试专用",
                "Operation_type": "DEPARTURE",
                "user_status": user_status,
                "user_id": user_id_update_time[0][0],
                "update_time": str(user_id_update_time[0][1])}
            result = interface.myRequest(url, data)

            if result["code"] == 0 and valus:
                base.consoleLog("账号：" + self.user_phone + "提交离职成功！")
        else:
            try:
                sql = 'UPDATE sys_user set user_status = "INCUMBENCY" where user_phone = "%s"; ' % self.user_phone
                base.updateSQL(sql)
                base.consoleLog("账号：" + self.user_phone + "数据库更改在职成功！")
            except Exception as e:
                base.consoleLog("账号：" + self.user_phone + "数据库更改在职异常！" + str(e) + sql)

        base.consoleLog('用户离职离职接口执行完成。')
        return

    def modify_user_post(self):
        """
        修改用户岗位
        :return:
        """
        base.consoleLog('修改用户岗位。账号：' + self.user_phone)

        sql = 'SELECT user_id from sys_user where user_phone = "%s"' % self.user_phone
        user_id = base.searchSQL(sql)[0][0]
        url = "http://isz.ishangzu.com/isz_base/UserController/searchNewUser.action"
        data = {"user_id":user_id}
        result = interface.myRequest(url,data)["obj"]

        sql = 'select position_id from sys_position where position_name = "%s" ' % self.rolename
        position_id = base.searchSQL(sql)[0][0]
        sql = 'SELECT update_time from sys_user where user_phone = "%s"' % self.user_phone
        update_time =str(base.searchSQL(sql)[0][0])
        url = "http://isz.ishangzu.com/isz_base/UserController/saveUser.action"
        data = {
        "position_id": position_id,
        "update_time": update_time,
        "user_id": result["sysFollows"][0]["user_id"],
        "role_id": result["role_id"],
        "Operation_type": "POSTMOVE"}

        interface.myRequest(url, data)

        base.consoleLog('修改用户岗位接口执行完成。')
        return

    def update_did(self):
        """
        更新部门到技术开发中心
        :return:
        """

        self.modify_user_post()
        sql = 'SELECT user_id from sys_user where user_phone = "%s"' % self.user_phone
        user_id = base.searchSQL(sql)[0][0]
        sql = 'SELECT update_time from sys_user where user_phone = "%s"' % self.user_phone
        update_time = str(base.searchSQL(sql)[0][0])
        url = "http://isz.ishangzu.com/isz_base/UserController/saveUser.action"
        data = {
            "dep_id": "10013",
            "update_time": update_time,
            "user_id": user_id,
            "Operation_type": "DEPMOVE"}

        interface.myRequest(url, data)

        sql = 'SELECT update_time from sys_user where user_phone = "%s"' % self.user_phone
        update_time = str(base.searchSQL(sql)[0][0])
        url = "http://isz.ishangzu.com/isz_base/UserController/saveUser.action"
        data = {
            "role_id": "8AB398CA5D0D2944015D2B7FF10C6E49",
            "update_time": update_time,
            "user_id": user_id,
            "Operation_type": "ROLEMOVE"}
        interface.myRequest(url, data)


        return




print(User("18279881085","测试工程师（后台）").add_role_authority())