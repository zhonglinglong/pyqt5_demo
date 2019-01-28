# -*- coding:utf8 -*-
"""
2018年4月10日17:42:22
__auto__ == zhonglinglong
爱上租ERP客户管理类接口
"""

from common import interface
import time
from common import base



class Customer:
    def __init__(self,phone):
        self.phone = phone

    def add_customer(self):
        """
        新增租客
        :return:
        """
        base.consoleLog('新增租客,手机号码：' + self.phone)

        rent_date = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
        url = "http://isz.ishangzu.com/isz_customer/CustomerController/saveCustomer.action"
        data = {
            "customer_name": "crazytest",
            "phone": self.phone,
            "customer_status": "EFFECTIVE",
            "email": "zhonglinglong@ishangzu.com",
            "belong_did": base.get_conf("loginUser", "dep_id"),
            "belong_uid": base.get_conf("loginUser", "user_id"),
            "customer_from": "GANJICOM",
            "rent_class": "NOCLASS",
            "rent_type": "GATHERHOUSE",
            "rent_use": "RESIDENCE",
            "rent_fitment": "FITMENT_SIMPLE",
            "city_code": "330100",
            "rent_area_code": "330102",
            "rent_business_circle_ids": "35",
            "rent_rooms": "1",
            "rent_livings": "1",
            "rent_bathrooms": "1",
            "rent_from_price": "0.00",
            "rent_to_price": "6000.00",
            "rent_date": rent_date,
            "rent_people": "1",
            "area": "40",
            "gender": "MALE",
            "marriage": "UNMARRIED",
            "submit_channels": "ERP"}

        #新增租客
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('新增租客接口执行失败！')
            return result['msg']
        base.consoleLog('新增租客接口执行成功！')
        return


Customer('18279881085').add_customer()