# -*- coding:utf8 -*-
"""
2018年5月30日09:48:59
__auto__ == zhonglinglong
爱上租ERP财务管理模块接口
"""


from common import interface
from common import base
from iszErpRequest import customerRequest
import json

class Finance:
    """财务管理"""
    def __init__(self,apartment_code=None,contract_num=None):
        """
        :param apartment_code: 房源编号
        :param contract_num:出租合同号
        """
        self.apartment_code = apartment_code
        self.contract_num = contract_num

    def pay_down_payment(self,earnest_money="4000"):
        """
        下定
        :param earnest_money: 下定金额
        :return:
        """
        base.consoleLog('下定。下定房源编号：' + self.apartment_code + '  下定金额：' + earnest_money)

        # 新增租客
        phone = '18279881085'
        try:
            sql = "select customer_id,customer_num,customer_from,customer_name from customer where phone = '%s'" % phone
            customer = base.searchSQL(sql)[0]
        except BaseException as e:
            base.consoleLog('sql执行报错。sql' + sql + '  报错信息：' + str(e),'e')
            return str(e)

        # 预定房源信息
        url = "http://isz.ishangzu.com/isz_customer/CustomerController/initBookAvailability.action"
        data = {"customer_id": customer[0]}
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            return result['msg']

        result = result["obj"]

        # 查询房源信息
        if "-" in self.apartment_code:
            url = "http://isz.ishangzu.com/isz_customer/CustomerController/searchBookAvailabilityShareList.action"
            rent_type_search = "SHARE"
        else:
            url = "http://isz.ishangzu.com/isz_customer/CustomerController/searchBookAvailabilityEntireList.action"
            rent_type_search = "ENTIRE"
        data = {"residential_name_house_code_search": self.apartment_code, "pageNumber": 1, "pageSize": 50,
                "sort": "update_time", "order": "DESC", "rent_type_search": rent_type_search}
        results = interface.myRequest(url, data)
        if results['code'] != 0:
            return results['msg']

        try:
            house_list = results["obj"]["rows"][0]
        except BaseException as e:
            return '查询下定房源数据为空。报错信息：' + str(e)

        # plan_sign_data,预计签约时间
        url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/getLastApartmentContractRealDueDate.action"
        datas = {
            "house_id": house_list["house_id"],
            "room_id": house_list["room_id"],
            "object_id": house_list["apartment_id"],
            "object_type": house_list["object_type"],
            "property_address": house_list["property_address"],
            "rent_type": house_list["rent_type"],
            "object_status": house_list["rent_status"],
            "rent_price": house_list["rent_price"]}
        results = interface.myRequest(url, datas)
        if results['code'] != 0:
            return results['msg']
        plan_sign_data = results["obj"]['sign_date_last']


        # 下定
        url = "http://isz.ishangzu.com/isz_contract/EarnestController/saveEarnest.action"
        data = {
            "earnest_money": earnest_money,
            "plan_sign_date": plan_sign_data,
            "remark": "下定备注",
            "customer_id": customer[0],
            "earnestImgList": [{
                "img_id": 'FF80808163814B6E01638197EA730030'
            }]}
        data.update(result)
        data.update(datas)

        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('下定接口执行失败！')
            return result['msg']
        base.consoleLog('下定接口执行成功。')
        return

    def confirmation_down_payment(self, breach_money="2000"):
        """
        违约
        :param breach_money: 违约金额
        :return:
        """
        base.consoleLog('下定违约。房源编号：' + self.apartment_code + ' 违约金额：' + breach_money)

        # 查询定金编号id
        url = "http://isz.ishangzu.com/isz_contract/EarnestController/searchEarnestList.action"
        data = {"residential_name_object_code_search": self.apartment_code, "pageNumber": 1, "pageSize": 50,
                "sort": "create_time", "order": "DESC", "current_dep_id": "00000000000000000000000000000000"}
        result = interface.myRequest(url, data)["obj"]["rows"][0]
        earnest_id = result["earnest_id"]

        # 确认定金
        url = "http://isz.ishangzu.com/isz_contract/EarnestController/confirmEarnest.action"
        data = {
            "receipt_date": base.now_time(),
            "earnest_id": earnest_id,
            "earnest_money": result["earnest_money"],
            "payment_way": "BANKTRANSFER",
            "receipt_name": "收据姓名",
            "company": "ISZTECH"}
        results = interface.myRequest(url, data)
        if results['code'] != 0:
            return results['msg']

        # 违约
        url = "http://isz.ishangzu.com/isz_contract/EarnestController/saveEarnestBreach.action"
        data = {
            "breach_reason": "auto违约原因",
            "breach_money": breach_money,
            "earnest_id": earnest_id,
            "earnest_money": result["earnest_money"]}

        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('下定违约接口执行失败！')
            return result['msg']
        base.consoleLog('下定违约接口执行成功！')
        return

    def apartment_contract_collecting_money(self,value=True):
        """
        出租合同首期款全部收钱
        :param contract_num:
        :param value:如果为真，收齐，否则收一种
        :return:
        """
        base.consoleLog('出租合同收首期款。出租合同号：' + self.contract_num)

        try:
            sql = "select contract_id from apartment_contract where contract_num = '%s'" % self.contract_num
            contract_id = base.searchSQL(sql)[0][0]
        except Exception as e:
            base.consoleLog("查询出租合同sql报错，sql:" + sql + "错误返回" + str(e),'e')
            return str(e)

        try:
            sql = """SELECT
            receivable_id,receivable_money
            FROM
            apartment_contract_receivable
            WHERE
            money_type IN (
                "FRIST_RENT",
                "FIRST_MANAGE_SERVER_FEE",
                "DEPOSIT"
            )
            AND contract_id = '%s' and end_status = 'NOTGET'""" % contract_id
            receivable_id_tuple = base.searchSQL(sql)
        except Exception as e:
            base.consoleLog("查询出租合同sql报错，sql:" + sql + "错误返回" + str(e),'e')
            return str(e)

        if receivable_id_tuple == ():
            base.consoleLog("该出租合同首期款都是已收状态")
            return u"该出租合同首期款都是已收状态"

        #收首期款
        url = "http://isz.ishangzu.com/isz_finance/ApartmentContractReceiptsController/saveOrUpdateNewReceipts.action"
        for i in range(len(receivable_id_tuple)):
            if value:
                data = {
                "receipts_date": base.now_time(),
                "company": "ISZTECH",
                "bank_name": "ABC",
                "bank_card_last_four": "3714",
                "operation_total": float(receivable_id_tuple[i][1]),
                "remark": "出租合同实收",
                "receipts_money": float(receivable_id_tuple[i][1]),
                "receivable_id": receivable_id_tuple[i][0],
                "contract_id": contract_id,
                "receipts_type": "BANKTRANSFER"}
                result = interface.myRequest(url,data)
                if result['code'] != 0:
                    base.consoleLog('出租合同所有首期款支付接口执行失败！')
                    return result['msg']
            else:
                if i == 0:
                    pass
                else:
                    data = {
                        "receipts_date": base.now_time(),
                        "company": "ISZTECH",
                        "bank_name": "ABC",
                        "bank_card_last_four": "3714",
                        "operation_total": int(receivable_id_tuple[i][1]),
                        "remark": "出租合同实收",
                        "receipts_money": int(receivable_id_tuple[i][1]),
                        "receivable_id": receivable_id_tuple[i][0],
                        "contract_id": contract_id,
                        "receipts_type": "BANKTRANSFER"}
                    result = interface.myRequest(url, data)
                    if result['code'] != 0:
                        base.consoleLog('出租合同所有首期款支付接口执行失败！')
                        return result['msg']

        base.consoleLog('出租合同收齐首期款接口执行成功!')
        return

    def reviewed_apartment_contract_receivable(self):
        """
        审核出租合同所有应收
        :return:
        """
        base.consoleLog('审核出租合同所有应收。出租合同号：' + self.contract_num)

        try:
            sql = "select contract_id from apartment_contract where contract_num = '%s'" % self.contract_num
            contract_id = base.searchSQL(sql)[0][0]
        except Exception as e:
            base.consoleLog("查询出租合同sql报错，sql:" + sql + "错误返回" + str(e),'e')
            return str(e)

        sql = 'SELECT receivable_id from apartment_contract_receivable where contract_id = "%s" and deleted =0' % contract_id
        receivable_id_tuple = base.searchSQL(sql)

        #循环审核应收
        url = 'http://isz.ishangzu.com/isz_finance/ApartmentContractReceiptsController/endReceivable.action'
        for i in range(len(receivable_id_tuple)):
            data = {"receivable_id": receivable_id_tuple[i][0]}
            result = interface.myRequest(url,data)
            if result['code'] == 0:
                base.consoleLog('审核应收接口执行成功。应收ID：' + receivable_id_tuple[i][0])
            else:
                base.consoleLog('审核应收接口执行失败。应收ID：' + receivable_id_tuple[i][0],level='e')
        return

    def delete_apartment_contract_collecting_money(self):
        """
        删除首期款实收
        :return:
        """
        base.consoleLog('删除首期款实收。出租合同号：' +self.contract_num )

        url = 'http://isz.ishangzu.com/isz_finance/ApartmentContractReceiptsController/deleteReceipts.action'

        try:
            sql = "select contract_id from apartment_contract where contract_num = '%s'" % self.contract_num
            contract_id = base.searchSQL(sql)[0][0]
        except Exception as e:
            base.consoleLog("查询出租合同sql报错，sql:" + sql + "错误返回" + str(e),'e')
            return str(e)

        sql = 'SELECT receivable_id from apartment_contract_receivable where contract_id = "%s" and deleted =0' % contract_id
        receivable_id_tuple = base.searchSQL(sql)

        for i in range(3):
            data = {"receipts_id":"FF80808164D5FFB20164E662B2111708","receivable_id":"FF80808164E4302C0164E662A80815D4","send_status":"UNSEND"}




