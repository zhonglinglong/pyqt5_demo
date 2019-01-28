# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年4月10日17:41:05
爱上租ERP自营房源接口
"""

from common import interface
from common import base


class Apartment:
    """自营房源类"""

    def __init__(self, contract_num):
        """
        :param contract_num: 委托合同号
        """
        self.contract_num = contract_num

    def apartment_price_entire(self, rent_price='5030'):
        """
        自营房源整租定价
        :param rent_price: 价格
        :return:
        """

        base.consoleLog("自营房源整租定价。价格：" + rent_price)

        try:
            sql = 'SELECT apartment_id from apartment where house_id = (SELECT house_id from house_contract where contract_num ="%s") ORDER BY create_time desc limit 1 ' % self.contract_num
            apartment_id = base.searchSQL(sql)[0][0]
        except Exception as e:
            base.consoleLog("查询sql报错,sql:" + sql + "错误返回：" + str(e),'e')
            return str(e)

        #整租定价
        url = "http://erp.ishangzu.com/isz_house/ApartmentController/confirmApatmentRentPricing.action"
        data = {"apartment_id": apartment_id, "rent_price": rent_price}
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('自营房源整租定价接口执行失败！')
            return result['msg']
        base.consoleLog('自营房源整租定价接口执行成功！')
        return


    def apartment_price_share(self, rent_price=['2030','2360','2890']):
        """
        自营房源合租定价
        :param rent_price:列表
        :return:
        """
        base.consoleLog('自营房源合租定价。价格' + str(rent_price))

        try:
            sql = 'SELECT apartment_id from apartment where house_id = (SELECT house_id from house_contract where contract_num ="%s") ORDER BY create_time desc limit 1 ' % self.contract_num
            apartment_id = base.searchSQL(sql)[0][0]
        except Exception as e:
            base.consoleLog("查询自营公寓返回为空,sql:" + sql + "错误返回：" + str(e),'e')
            return str(e)

        # 查询合租房间信息
        url = "http://erp.ishangzu.com/isz_house/ApartmentController/searchShareApartment.action"
        data = {"apartment_id": apartment_id}
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            return result['msg']

        # 出租合同定价
        data = result["obj"]
        for i in range(len(data)):
            data[i]['canEdit'] = True
            data[i]['rent_price'] = rent_price[i]

        # 自营公寓合租定价
        url = "http://erp.ishangzu.com/isz_house/ApartmentController/confirmPricing.action"
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('自营房源合租定价接口执行失败！')
            return result['msg']
        base.consoleLog('自营房源合租定价接口执行成功！')
        return


class ApartmentInfo:
    """自营房源详情"""

    def __init__(self, apartment_code):
        """
        :param apartment_code: 房源编号
        """
        self.apartment_code = apartment_code

        try:
            sql = 'select apartment_id from apartment where apartment_code="%s" ' % self.apartment_code
            self.apartment_id = base.searchSQL(sql)[0][0]
        except BaseException as e:
            base.consoleLog("查询自营公寓返回为空,sql:" + sql + "错误返回：" + str(e),'e')

    def serach_apartment_cose_detail(self):
        """
        查询自营房源成本
        :return:
        """
        base.consoleLog('查询自营房源成本。房源编号，ID：' + self.apartment_code + ' , ' + self.apartment_id)

        url = 'http://erp.ishangzu.com/isz_house/ApartmentController/selectApartmentDetail.action'
        data = {"apartment_id": self.apartment_id}
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('查询自营房源成本接口执行失败！')
            return result['msg']
        result = result['obj']
        info = {}
        info['装修成本'] = float(result['fitment_cost'])
        info['资金成本'] = float(result['capital_cost'])
        info['租金成本'] = float(result['entrust_cost'])
        info['渠道成本'] = float(result['channel_cost'])
        info['物业能耗'] = float(result['propertyAndEnergyFee'])
        info['总成本'] = float(result['apartment_cost'])

        base.consoleLog('查询自营房源成本接口执行成功！')
        return info

