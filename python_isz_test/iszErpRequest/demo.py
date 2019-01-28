# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年5月30日13:14:16
接口demo
"""


from iszErpRequest import apartmentContractRequest
from common import base




# contract_num = base.random_name()
# obj = houseContractRequest.HouseContract('陈飞鸿测试专用楼盘',contract_num,base.now_time(-100),'品质公寓','合租','修配',channel_fee='1000')
# obj.add_house_contract()
# sleep(2)
# decorationRequest.Decoration(contract_num,value=False).run_class()
#obj.reviewed_house_contract()


# sleep(1)
# apartmentRequest.Apartment(contract_num).apartment_price_entire()
# sleep(1)
#
# sql = "SELECT apartment_code from apartment where house_id = (SELECT house_id from house_contract where contract_num='%s')" % contract_num
# apartment_code = base.searchSQL(sql)[0][0]
#
# sleep(1)
# aobj = apartmentContractRequest.ApartmentContract(apartment_code ,base.random_name(),base.now_time())
# aobj.add_apartment_contract_entire()
# aobj.reviewed_apartment_contract()
# aobj.apartment_contract_end('退租')



contract_num = base.random_name()
apartment_contract =apartmentContractRequest.ApartmentContract('HZBJ1806230138',contract_num, '2018-06-22','2019-09-15')
apartment_contract.add_apartment_contract_entire()
