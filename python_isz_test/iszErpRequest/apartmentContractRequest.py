# -*- coding:utf8 -*-
"""
2018年5月28日22:25:43
出租合同类接口
"""
import json

__auto__ = 'zhonglinglong'

from common import interface
from common import base
from iszErpRequest import financeRequest
import datetime,time


class ApartmentContract:
    """出租合同类"""

    def __init__(self, apartment_code=None, contract_num=None, rent_start_date=None, rent_end_date=None,
                 sign_body=u"杭州爱上租科技有限公司"):
        self.apartment_code = apartment_code  # 房源编号
        self.contract_num = contract_num  # 出租合同号
        self.rent_start_date = rent_start_date  # 承租起算日
        if rent_end_date == None:
            self.rent_end_date = str(
                datetime.datetime.strptime(rent_start_date, '%Y-%m-%d') + datetime.timedelta(days=364))[0:10]  # 承租到期日
        else:
            self.rent_end_date = rent_end_date
        self.sign_body = base.get_conf('house_contract', sign_body)  # 签约城市

    def add_apartment_contract_entire(self,value=True):
        """
        新增整租出租合同
        :return:money_cycle
        """
        base.consoleLog('新增整租出租合同,合同名称：'+ self.contract_num + '  房源编号：' + self.apartment_code)

        #查询租客信息
        phone = '18279881085'
        try:
            sql = "select customer_id,customer_num,customer_from,customer_name from customer where phone = '%s'" % phone
            customer = base.searchSQL(sql)[0]
        except BaseException as e:
            base.consoleLog('sql查询报错。sql:' + sql + str(e),'e')
            return str(e)

        # 获取自营房源数据
        try:
            sql = "SELECT apartment_id,service_uid,service_did,rent_type from apartment where apartment_code = '%s' ORDER BY create_time desc limit 1" % self.apartment_code
            apartment_id = base.searchSQL(sql)[0]
            if apartment_id == ():
                return 'SQL查询为空。sql' + sql
        except Exception as e:
            base.consoleLog('sql报错。sql:' + sql + '   报错信息：' + str(e),'e')
            return str(e)


        # 根据规则设置的签约日期大于当前时间时,需自动把签约日期设置成当前时间。
        sign_date = self.rent_start_date
        if time.strptime(sign_date+ ' 00:00:00', "%Y-%m-%d %H:%M:%S") > time.strptime(base.now_time() + ' 00:00:00',
                                                                         "%Y-%m-%d %H:%M:%S"):
            sign_date = base.now_time()

        #查询整租自营房源详情信息
        url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/searchApartmentContractDetail.action"
        data = {"apartment_id": apartment_id[0], "contract_type": apartment_id[3]}
        dic = interface.myRequest(url, data)
        if dic['code'] != 0:
            return dic['msg']
        dic = dic["obj"]["apartmentContract"]

        # #把字典空值去掉
        # dic = empty_dict_null(dics)
        cash_rent = int(dic['rent_price']) * 0.1
        apartment_contract = {"house_id": dic["house_id"],
                              "residential_id": dic['residential_id'],
                              "building_id": dic['building_id'],
                              "city_code": dic['city_code'],
                              "area_code": dic['area_code'],
                              "entrust_type": dic['entrust_type'],
                              "apartment_id": dic['apartment_id'],
                              "server_flag": dic['server_flag'],
                              "apartment_rent_price": dic['rent_price'],
                              "contract_type": "NEWSIGN",
                              "apartment_code": dic['apartment_code'],
                              "property_address": dic['property_address'],
                              "production_address": dic['production_address'],
                              "apartment_type": dic['apartment_type'],
                              # "service_dep_name": dic['service_dep_name'],
                              # "service_user_name": dic['service_user_name'],
                              "input_dep_name": dic['input_dep_name'],
                              "input_user_name": dic['input_user_name'],
                              "sign_did": dic['sign_did'],
                              "sign_uid": dic['sign_uid'],
                              "contract_num": self.contract_num,
                              "sign_body": self.sign_body,
                              "sign_date": sign_date,
                              "apartment_check_in_date": dic['apartment_check_in_date'],
                              "rent_start_date": self.rent_start_date,
                              "rent_end_date": self.rent_end_date,
                              "payment_date": self.rent_start_date,
                              "deposit_type": "ONE",
                              "payment_type": "NORMAL",
                              "payment_cycle": "SEASON",
                              "cash_rent": cash_rent,
                              "deposit": dic['rent_price'],
                              "agency_fee": "0.00",
                              "month_server_fee": cash_rent,
                              "month_server_fee_discount": "100%",
                              "load_interest": dic['load_interest'],
                              "remark": "测试",
                              "undefined": self.rent_end_date,
                              "dispostIn": 1,
                              "sign_name": customer[3],
                              "sign_id_type": "IDNO",
                              "sign_id_no": "360729199112243714",
                              "sign_phone": phone,
                              "sign_is_customer": "Y",
                              "address": dic['address'],
                              "model": "4"}
        # 获取"person"列表字段值
        apartment_contract["person"] = {
            "urgent_customer_name": "租客紧急联系人",
            "urgent_phone": "15750935006",
            "customer_id": customer[0],
            "customer_num": customer[1],
            "customer_from": customer[2],
            "customer_type": "PERSONALITY",
            "customer_name": customer[3],
            "card_type": "IDNO",
            "id_card": '360729199112243714',
            "phone": phone,
            "gender": "MALE",
            "socialQualification": "on",
            "person_type": 2,
            "social_qualification": "N",
            "tent_contact_address": "签约人代理人通讯地址",
            "birth_date": "1991-12-24",
            "constellation": "CAPRICORN"}

        # 出租合同内的委托合同时间
        url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/getHouseContractByHouseId.action"
        data = {
            "rent_start_date": self.rent_start_date,
            "rent_end_date": self.rent_end_date,
            "houseId": dic["house_id"],
            "apartment_id": dic['apartment_id']}
            #"room_id": dic['room_id']}
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            return result['msg']

        # 获取houseContractList
        apartment_contract["houseContractList"] = result['obj']
        for i in range(len(apartment_contract["houseContractList"])):
            none = []
            for v,k in apartment_contract["houseContractList"][i].items():
                if k == None:
                    none.append(v)
            for j in range(len(none)):
                    del apartment_contract["houseContractList"][i][none[j]]


        # 获取应收数据
        month_server_fee = int(int(apartment_contract["apartment_rent_price"]) * 0.07)
        url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/createApartmentContractReceivable.action"
        if value:
            data = [{
                "firstRow": "true",
                "money": apartment_contract["apartment_rent_price"],
                "start_date": self.rent_start_date,
                "rowIndex": 0,
                "end_date": self.rent_end_date,
                "money_cycle": "SEASON",
                "payment_date": self.rent_start_date,
                "deposit": apartment_contract["apartment_rent_price"],
                "agencyFeeMoney": "0.00",
                "money_type": "RENT",
                "rent_start_date": self.rent_start_date,
                "rent_end_date": self.rent_end_date,
                "sign_date": sign_date,#base.now_time(-1),
                "month_server_fee": month_server_fee}]
        else:
            data = [{
                "firstRow": "true",
                "money": apartment_contract["apartment_rent_price"],
                "start_date": self.rent_start_date,
                "rowIndex": 0,
                "end_date": base.now_time(60),
                "money_cycle": "SEASON",
                "payment_date": self.rent_start_date,
                "deposit": apartment_contract["apartment_rent_price"],
                "agencyFeeMoney": "0.00",
                "money_type": "RENT",
                "rent_start_date": self.rent_start_date,
                "rent_end_date": self.rent_end_date,
                "sign_date": sign_date,  # base.now_time(-1),
                "month_server_fee": month_server_fee},
                {
                "firstRow": "true",
                "money": '5230',
                "start_date": base.now_time(61),
                "rowIndex": 1,
                "end_date": base.now_time(150),
                "money_cycle": "SEASON",
                "payment_date": self.rent_start_date,
                "deposit": '5030',
                "agencyFeeMoney": "0.00",
                "money_type": "RENT",
                "rent_start_date": self.rent_start_date,
                "rent_end_date": self.rent_end_date,
                "sign_date": sign_date,  # base.now_time(-1),
                "month_server_fee": month_server_fee},
                {
                "firstRow": "true",
                "money": '5330',
                "start_date": base.now_time(151),
                "rowIndex": 2,
                "end_date": self.rent_end_date,
                "money_cycle": "SEASON",
                "payment_date": self.rent_start_date,
                "deposit": '5230',
                "agencyFeeMoney": "0.00",
                "money_type": "RENT",
                "rent_start_date": self.rent_start_date,
                "rent_end_date": self.rent_end_date,
                "sign_date": sign_date,  # base.now_time(-1),
                "month_server_fee": month_server_fee}]

        receivables = interface.myRequest(url, data)
        print(data)
        print(url)
        if receivables['code'] != 0:
            return receivables['msg']
        apartment_contract["receivables"] = receivables['obj']

        # 获取 apartmentContractRentInfoList
        apartment_contract["apartmentContractRentInfoList"] = data

        # 保存出租合同
        url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/saveOrUpdateApartmentContract.action"
        result = interface.myRequest(url, apartment_contract)


        if result['code'] != 0:
            base.consoleLog('新增整租出租合同接口执行失败！')
            return result['msg']

        base.consoleLog('新增整租出租合同接口执行成功！')
        return

    def add_apartment_contract_share(self,value =True):
        """
        新增合租出租合同
        :return:
        """
        base.consoleLog("新增合租出租合同,出租合同号：" + self.contract_num)

        #查询租客信息
        phone = '18279881085'
        try:
            sql = "select customer_id,customer_num,customer_from,customer_name from customer where phone = '%s'" % phone
            customer = base.searchSQL(sql)[0]
        except Exception as e:
            base.consoleLog('sql报错。sql:' + sql + '   报错信息：' + str(e),'e')
            return str(e)

        # 根据规则设置的签约日期大于当前时间时,需自动把签约日期设置成当前时间。
        sign_date = self.rent_start_date
        if time.strptime(sign_date+ ' 00:00:00', "%Y-%m-%d %H:%M:%S") > time.strptime(base.now_time() + ' 00:00:00',
                                                                         "%Y-%m-%d %H:%M:%S"):
            sign_date = base.now_time()

        # 获取自营房源数据
        try:
            sql = "SELECT apartment_id,service_uid,service_did,rent_type from apartment where apartment_code = '%s' " % self.apartment_code
            apartment_id = base.searchSQL(sql)[0]
        except Exception as e:
            base.consoleLog('sql报错。sql:' + sql + '   报错信息：' + str(e),'e')
            return str(e)

        url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/searchApartmentContractDetail.action"
        data = {"apartment_id": apartment_id[0], "contract_type": apartment_id[3]}
        dic = interface.myRequest(url, data)
        if dic['code'] != 0:
            return dic['msg']
        dic = dic["obj"]["apartmentContract"]

        #把字典空值去掉
        # dic = empty_dict_null(dics)
        cash_rent = int(dic['rent_price']) * 0.1
        apartment_contract = {"house_id": dic["house_id"],
                              "production_address": dic["production_address"],
                              "room_id": dic["room_id"],
                              "residential_id": dic['residential_id'],
                              "building_id": dic['building_id'],
                              "city_code": dic['city_code'],
                              "area_code": dic['area_code'],
                              "entrust_type": dic['entrust_type'],
                              "apartment_id": dic['apartment_id'],
                              "server_flag": dic['server_flag'],
                              "apartment_rent_price": dic['rent_price'],
                              "contract_type": "NEWSIGN",
                              "apartment_code": dic['apartment_code'],
                              "property_address": dic['property_address'],
                              "production_address": dic['production_address'],
                              "apartment_type": dic['apartment_type'],
                              # "service_dep_name": dic['service_dep_name'],
                              # "service_user_name": dic['service_user_name'],
                              "input_dep_name": dic['input_dep_name'],
                              "input_user_name": dic['input_user_name'],
                              "sign_did": dic['sign_did'],
                              "sign_uid": dic['sign_uid'],
                              "contract_num": self.contract_num,
                              "sign_body": self.sign_body,
                              "sign_date": sign_date,
                              "apartment_check_in_date": dic['apartment_check_in_date'],
                              "rent_start_date": self.rent_start_date,
                              "rent_end_date": self.rent_end_date,
                              "payment_date": self.rent_start_date,
                              "deposit_type": "ONE",
                              "payment_type": "NORMAL",
                              "payment_cycle": "SEASON",
                              "cash_rent": cash_rent,
                              "deposit": dic['rent_price'],
                              "agency_fee": "0.00",
                              "month_server_fee": cash_rent,
                              "month_server_fee_discount": "100%",
                              "load_interest": dic['load_interest'],
                              "remark": "测试",
                              "undefined": self.rent_end_date,
                              "dispostIn": 1,
                              "sign_name": customer[3],
                              "sign_id_type": "IDNO",
                              "sign_id_no": "360729199112243714",
                              "sign_phone": phone,
                              "sign_is_customer": "Y",
                              "address": dic['property_address'],
                              "model": "4"}
        # 获取"person"列表字段值
        apartment_contract["person"] = {
            "urgent_customer_name": "租客紧急联系人",
            "urgent_phone": "15750935006",
            "customer_id": customer[0],
            "customer_num": customer[1],
            "customer_from": customer[2],
            "customer_type": "PERSONALITY",
            "customer_name": customer[3],
            "card_type": "IDNO",
            "id_card": '360729199112243714',
            "phone": phone,
            "gender": "MALE",
            "socialQualification": "on",
            "person_type": 2,
            "social_qualification": "N",
            "tent_contact_address": "签约人代理人通讯地址",
            "birth_date": "1991-12-24",
            "constellation": "CAPRICORN"}
        # 获取houseContractList
        # 出租合同内的委托合同时间
        url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/getHouseContractByHouseId.action"
        data = {
            "rent_start_date": self.rent_start_date,
            "rent_end_date": self.rent_end_date,
            "houseId": dic["house_id"],
            "apartment_id": dic['apartment_id']}
            #"room_id": dic['room_id']}
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            return result['msg']

        apartment_contract["houseContractList"] = result['obj']


        # 获取应收数据
        month_server_fee = int(int(apartment_contract["apartment_rent_price"]) * 0.07)
        url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/createApartmentContractReceivable.action"
        if value:
            data = [{
                "firstRow": "true",
                "money": apartment_contract["apartment_rent_price"],
                "start_date": self.rent_start_date,
                "rowIndex": 0,
                "end_date": self.rent_end_date,
                "money_cycle": "SEASON",
                "payment_date": self.rent_start_date,
                "deposit": apartment_contract["apartment_rent_price"],
                "agencyFeeMoney": "0.00",
                "money_type": "RENT",
                "rent_start_date": self.rent_start_date,
                "rent_end_date": self.rent_end_date,
                "sign_date": sign_date,  # base.now_time(-1),
                "month_server_fee": month_server_fee}]
        else:
            data = [{
                "firstRow": "true",
                "money": apartment_contract["apartment_rent_price"],
                "start_date": self.rent_start_date,
                "rowIndex": 0,
                "end_date": base.now_time(60),
                "money_cycle": "SEASON",
                "payment_date": self.rent_start_date,
                "deposit": apartment_contract["apartment_rent_price"],
                "agencyFeeMoney": "0.00",
                "money_type": "RENT",
                "rent_start_date": self.rent_start_date,
                "rent_end_date": self.rent_end_date,
                "sign_date": sign_date,  # base.now_time(-1),
                "month_server_fee": month_server_fee},
                {
                    "firstRow": "true",
                    "money": '5230',
                    "start_date": base.now_time(61),
                    "rowIndex": 1,
                    "end_date": base.now_time(150),
                    "money_cycle": "SEASON",
                    "payment_date": self.rent_start_date,
                    "deposit": '5030',
                    "agencyFeeMoney": "0.00",
                    "money_type": "RENT",
                    "rent_start_date": self.rent_start_date,
                    "rent_end_date": self.rent_end_date,
                    "sign_date": sign_date,  # base.now_time(-1),
                    "month_server_fee": month_server_fee},
                {
                    "firstRow": "true",
                    "money": '5330',
                    "start_date": base.now_time(151),
                    "rowIndex": 2,
                    "end_date": self.rent_end_date,
                    "money_cycle": "SEASON",
                    "payment_date": self.rent_start_date,
                    "deposit": '5230',
                    "agencyFeeMoney": "0.00",
                    "money_type": "RENT",
                    "rent_start_date": self.rent_start_date,
                    "rent_end_date": self.rent_end_date,
                    "sign_date": sign_date,  # base.now_time(-1),
                    "month_server_fee": month_server_fee}]
        receivables = interface.myRequest(url, data)
        if receivables['code'] != 0:
            return receivables['msg']
        apartment_contract["receivables"] = receivables['obj']

        # 获取 apartmentContractRentInfoList
        apartment_contract["apartmentContractRentInfoList"] = data

        # 保存出租合同
        print(apartment_contract)
        url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/saveOrUpdateApartmentContract.action"
        result = interface.myRequest(url, apartment_contract)
        if result['code'] != 0:
            base.consoleLog('新增合租出租合同接口执行失败！')
            return result['msg']

        base.consoleLog('新增合租出租合同接口执行成功！')
        return

    def add_renew_apartment_contract(self,contract_num):
        """
        续签出租合同
        :param: contract_num 续签的合同名称
        :return:
        """
        base.consoleLog('续签出租合同。合同名称：' + contract_num)

        try:
            sql = "select contract_id from apartment_contract where contract_num = '%s'" % self.contract_num
            contract_id = base.searchSQL(sql)[0][0]
        except Exception as e:
            base.consoleLog("查询出租合同sql报错。sql:" + sql + ";错误返回：" + str(e), 'e')
            return str(e)


        #判断出租合同是否可以续签
        url = 'http://isz.ishangzu.com/isz_contract/ApartmentContractController/validRenewApartmentContract.action'
        data =  {"contract_type":"RENEWSIGN","parent_id":contract_id}
        result = interface.myRequest(url,data)
        if result['code'] == 0:
            pass
        elif result['msg'] == '前合同还有实收款项未被财务审核，请确认！':
            base.consoleLog('前合同还有实收款项未被财务审核，请确认！'+'为了保证能续签。此时开始调用财务接口,把前一份出租合同应收全部收取',level='e')
            financeRequest.Finance(contract_num=self.contract_num).reviewed_apartment_contract_receivable()
            url = 'http://isz.ishangzu.com/isz_contract/ApartmentContractController/validRenewApartmentContract.action'
            data = {"contract_type": "RENEWSIGN", "parent_id": contract_id}
            result = interface.myRequest(url, data)
            if result['code'] == 0:
                pass
            else:
                base.consoleLog('调完财务的接口都还不能续签！' + result['msg'],level='e')
                return

        # 根据规则设置的签约日期大于当前时间时,需自动把签约日期设置成当前时间。
        sign_date = self.rent_start_date
        if time.strptime(sign_date+ ' 00:00:00', "%Y-%m-%d %H:%M:%S") > time.strptime(base.now_time() + ' 00:00:00',
                                                                         "%Y-%m-%d %H:%M:%S"):
            sign_date = base.now_time()

        #查询前出租合同详情
        url = 'http://isz.ishangzu.com/isz_contract/ApartmentContractController/searchApartmentContractDetail.action'
        data = {"parent_id":contract_id,"contract_type":"RENEWSIGN"}
        qian_apartment_contract_info = interface.myRequest(url,data)['obj']
        apartmentContract = qian_apartment_contract_info['apartmentContract']

        # 判断输入的出租起算日要大于等于可入住日期
        if time.strptime(qian_apartment_contract_info['apartmentContract']['apartment_check_in_date']+ ' 00:00:00',
                         "%Y-%m-%d %H:%M:%S") > time.strptime(self.rent_start_date + ' 00:00:00',
                                                              "%Y-%m-%d %H:%M:%S"):
            base.consoleLog('出租起算日小于了可入住日期,不能签约！',level='e')
            return

        # 出租合同内的委托合同时间
        # 获取houseContractList
        url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/getHouseContractByHouseId.action"
        data = {
            "rent_start_date": self.rent_start_date,
            "rent_end_date": self.rent_end_date,
            "houseId": apartmentContract["house_id"],
            "apartment_id": apartmentContract['apartment_id'],
            "room_id": apartmentContract['room_id']}
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            return result['msg']
        houseContractList = result['obj']

        # 获取月服务费
        url = 'http://isz.ishangzu.com/isz_contract/ApartmentContractController/getServiceAgencyProperty.action'
        data = {
            "houseContractId": houseContractList[0]['contract_id'],
            "firstMoney": qian_apartment_contract_info['apartmentContract']['parent_deposit_payable'],
            "rent_start_date": self.rent_start_date,
            "rent_end_date": self.rent_end_date,
            "contract_type": "RENEWSIGN",
            "sign_date": sign_date,
            "house_id": qian_apartment_contract_info['apartmentContract']['house_id'],
            "old_contract_id": contract_id,
            "room_id": qian_apartment_contract_info['apartmentContract']['room_id']
        }
        month_server_fee = interface.myRequest(url, data)['obj']['month_server_fee']

        # 获取应收数据
        url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/createApartmentContractReceivable.action"
        data = [{
            "firstRow": True,
            "money": "530.00",
            "start_date": self.rent_start_date,
            "rowIndex": 0,
            "end_date": self.rent_end_date,
            "money_cycle": "SEASON",
            "payment_date": self.rent_start_date,
            "deposit": qian_apartment_contract_info['apartmentContract']['parent_deposit_payable'],
            "agencyFeeMoney": "0.00",
            "money_type": "RENT",
            "rent_start_date": self.rent_start_date,
            "rent_end_date": self.rent_end_date,
            "sign_date": sign_date,
            "month_server_fee":month_server_fee
        }]
        receivables = interface.myRequest(url, data)
        if receivables['code'] != 0:
            return receivables['msg']


        #生成出租合同
        url = 'http://isz.ishangzu.com/isz_contract/ApartmentContractController/saveOrUpdateApartmentContract.action'
        data = {
            "house_id": qian_apartment_contract_info['apartmentContract']['house_id'],
            "residential_id": qian_apartment_contract_info['apartmentContract']["residential_id"],
            "building_id":  qian_apartment_contract_info['apartmentContract']["building_id"],
            "city_code":  qian_apartment_contract_info['apartmentContract']["city_code"],
            "area_code":  qian_apartment_contract_info['apartmentContract']["area_code"],
            "entrust_type":  qian_apartment_contract_info['apartmentContract']["entrust_type"],
            "apartment_id":  qian_apartment_contract_info['apartmentContract']["apartment_id"],
            "contract_status":  qian_apartment_contract_info['apartmentContract']["contract_status"],
            "room_id": qian_apartment_contract_info['apartmentContract']["room_id"],
            "parent_id":  qian_apartment_contract_info['apartmentContract']["parent_id"],
            "server_flag":  qian_apartment_contract_info['apartmentContract']["server_flag"],
            "apartment_rent_price":  qian_apartment_contract_info['apartmentContract']["parent_rent_price"],
            "contract_type":  qian_apartment_contract_info['apartmentContract'][ "contract_type"],
            "apartment_code":  qian_apartment_contract_info['apartmentContract'][ "apartment_code"],
            "property_address":  qian_apartment_contract_info['apartmentContract']["property_address"],
            "houseRoom":qian_apartment_contract_info['apartmentContract']["houseRoom"],
            "production_address":  qian_apartment_contract_info['apartmentContract']["production_address"],
            "apartment_type":  qian_apartment_contract_info['apartmentContract']["apartment_type"],
            "input_dep_name":  qian_apartment_contract_info['apartmentContract']["input_dep_name"],
            "input_user_name":  qian_apartment_contract_info['apartmentContract']["input_user_name"],
            "sign_did":  qian_apartment_contract_info['apartmentContract']["sign_did"],
            "sign_uid": qian_apartment_contract_info['apartmentContract']["sign_uid"],
            "parent_contract_num":  qian_apartment_contract_info['apartmentContract']["parent_contract_num"],
            "parent_rent_price":  qian_apartment_contract_info['apartmentContract']["parent_rent_price"],
            "parent_sign_username":  qian_apartment_contract_info['apartmentContract'][ "parent_sign_username"],
            "parent_rent_start_date": qian_apartment_contract_info['apartmentContract']["parent_rent_start_date"],
            "parent_rent_end_date":  qian_apartment_contract_info['apartmentContract']["parent_rent_end_date"],
            "parent_deposit_payable":  qian_apartment_contract_info['apartmentContract']["parent_deposit_payable"],
            "parent_deposit":  qian_apartment_contract_info['apartmentContract']["parent_deposit"],
            "contract_num": contract_num,
            "sign_body":  qian_apartment_contract_info['apartmentContract']['sign_body'],
            "sign_date": sign_date,
            "apartment_check_in_date":  qian_apartment_contract_info['apartmentContract']["apartment_check_in_date"],       # 可入住日期
        "rent_start_date": self.rent_start_date,
        "rent_end_date": self.rent_end_date,
        "payment_date": self.rent_start_date,
        "deposit_type": "ONE",
        "payment_type": "NORMAL",
        "payment_cycle": "SEASON",
        "financing_type": "NONE",
        "cash_rent":str(qian_apartment_contract_info['apartmentContract']["rent_price"]*0.1),
        "deposit": str(qian_apartment_contract_info['apartmentContract']["rent_price"]),
        "agency_fee": "0.00",
        "month_server_fee": month_server_fee,
        "month_server_fee_discount": "100%",
        "load_interest": 8, #贷款利息
        "undefined": self.rent_end_date,
        "sign_type": 'Y',
        "dispostIn": 1,
        "sign_name": qian_apartment_contract_info['apartmentContract']["sign_name"],
        "sign_id_type":qian_apartment_contract_info['apartmentContract'][ "sign_id_type"],
        "sign_id_no": qian_apartment_contract_info['apartmentContract']["sign_id_no"],
        "sign_phone": qian_apartment_contract_info['apartmentContract']["sign_phone"],
        "sign_is_customer": qian_apartment_contract_info['apartmentContract']["sign_is_customer"],
        "address":qian_apartment_contract_info['apartmentContract']["property_address"],
        "apartmentContractRentInfoList": [{
            "firstRow":True,
            "money": str(qian_apartment_contract_info['apartmentContract']["rent_price"]),
            "start_date": self.rent_start_date,
            "rowIndex": 0,
            "end_date":self.rent_end_date,
            "money_cycle": "SEASON",
            "payment_date": self.rent_start_date,
            "deposit": str(qian_apartment_contract_info['apartmentContract']["rent_price"]),
            "agencyFeeMoney": "0.00",
            "money_type": "RENT",
            "rent_start_date": self.rent_start_date,
            "rent_end_date": self.rent_end_date,
            "sign_date": sign_date,
            "month_server_fee": month_server_fee
        }],
        "createReceivable": "N",
        "model": "4"
        }
        data['person'] = qian_apartment_contract_info['customerPerson']  # 继承前出租合同签约人承租人信息
        data["persons"] = qian_apartment_contract_info['customerPersonList']   # 继承前出租合同入住人信息
        data["receivables"] = receivables['obj']  # 出租合同应收
        data['houseContractList'] = houseContractList  # 出租合同关联的委托合同

        result = interface.myRequest(url,data)
        if result['code'] == 0:
            base.consoleLog('续签出租合同接口执行成功！')
            return
        else:
            base.consoleLog('续签失败！' + result['msg'],level='e')
            return result['msg']

    def apartment_contract_end(self, end_type, end_date=base.now_time(),receivable_total=None,payable_totle=None):
        """
        出租合同终止结算
        :param end_type:终止类型
        :param end_date:终止日期
        :param receivable_total:应收总金额
        :param payable_totle: 应付总金额
        :return:
        """
        base.consoleLog('出租合同终止结算。出租合同号：' + self.contract_num + ' 终止类型：' + end_type)

        url = 'http://erp.ishangzu.com/isz_house/UploadController/uploadImageFile.action'
        idCardPhotos = interface.upLoadPhoto(url, base.get_conf('Img', 'picture_name'),
                                             base.get_conf('Img', 'file_path'), name='multipartFile')

        if end_type == "正退":
            # 类型明细，终止原因
            end_type_detail = None
            end_reason = None
        elif end_type == "退租":
            end_type_detail = "CUSTOMER_BREAK_CONTRACT"
            end_reason = "CANT_DO_PROMISE"
        elif end_type == "转租" or end_type == u"换租":
            end_type_detail = None
            end_reason = "CANT_DO_PROMISE"
        elif end_type == "收房":
            end_type_detail = None
            end_reason = "ARREARAGE"
        elif end_type == '退单':
            end_type_detail = None
            end_reason = "OTHER"

        end_type = base.get_conf("contract_end", end_type)

        try:
            sql = "select contract_id from apartment_contract where contract_num = '%s'" % self.contract_num
            contract_id = base.searchSQL(sql)[0][0]
        except Exception as e:
            base.consoleLog("查询出租合同sql报错。sql:" + sql + "错误返回：" + str(e), 'e')
            return str(e)

        # 查询出租终止合同款项结算
        url = "http://erp.ishangzu.com/isz_contract/ContractEndController/settlementOfContract"
        data = {"contract_id": contract_id, "end_date": end_date, "end_type": end_type}
        apartmentContractEndReceivableList = interface.myRequest(url, data)
        if apartmentContractEndReceivableList['code'] != 0:
            return apartmentContractEndReceivableList['msg']
        apartmentContractEndReceivableList = apartmentContractEndReceivableList["obj"]

        # if end_type == "COLLECTHOUSE":
        #     apartmentContractEndReceivableList[3]["balance_amount"] = -3000

        # 查询出租终止合同基本信息
        url = "http://erp.ishangzu.com/isz_contract/ContractEndController/searchContractEndInfo"
        data = {"contract_id": contract_id, "is_old_data": "N"}
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            return result['msg']
        result = result["obj"]
        detailList = result["detailList"]
        endBasicInfo = result["endBasicInfo"]

        # 获取liquidateOrTurnFee        data = {"contract_id": contract_id, "end_type": end_type, "end_type_detail": end_type_detail}
        url = "http://erp.ishangzu.com/isz_contract/ContractEndController/calculateLiquidatedOrTurnFee"
        data = {"contract_id": contract_id, "end_type": end_type, "end_type_detail": end_type_detail}
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            return result['msg']
        result = result["obj"]

        liquidatedOrTurnFee = {}
        if end_type == '退单':
            liquidatedOrTurnFee["liquidatedOrTurnFee"] = {
                "liquidated_receivable": 0,
                "discount_liquidated_receivable": 0,
                "liquidated_discount_scale": 0,
                "turn_receivable": 0,
                "discount_turn_receivable": 0,
                "turn_discount_scale": 0,
                "liquidated_return": 0,
                "fileList": [],
                "discount_img_id": '',
                "discountImgList": [],
                "discount_img_src": ''
            }
        else:
            liquidatedOrTurnFee["liquidatedOrTurnFee"] = {
                "liquidated_receivable": result["liquidated_receivable"],
                "discount_liquidated_receivable": result["discount_liquidated_receivable"],
                "liquidated_discount_scale": "100.00%",
                "turn_receivable": result["turn_receivable"],
                "discount_turn_receivable": result["discount_turn_receivable"],
                "turn_discount_scale": 0,
                "liquidated_return": result["liquidated_return"],
                "fileList": [{
                    "create_time": base.now_time() + " 14:15:04",
                    "create_uid": base.get_conf("loginUser", "user_id"),
                    "deleted": 0,
                    "img_id": idCardPhotos["img_id"],
                    "src": idCardPhotos["src"],
                    "update_time": base.now_time() + " 14:15:04",
                    "update_uid": base.get_conf("loginUser", "user_id"),
                    "url": idCardPhotos["src"]
                }],
                "discount_img_id": None,
                "discountImgList": [{
                    "img_id": idCardPhotos["img_id"],
                    "src": idCardPhotos["src"]
                }],
                "discount_img_src": None
            }

        # 提交终止结算
        # 终止结算的参数列表：imgList,receiverInfo,loanFee,apartmentContractEndReceivableList,detailList,endBasicInfo,liquidatedOrTurnFee
        url = "http://erp.ishangzu.com/isz_contract/ContractEndController/saveOrUpdateApartmentContractEnd"
        data = {"imgList": [{
            "attachment_type": None,
            "img_id": idCardPhotos["img_id"],
            "src": idCardPhotos["src"]
        }],
            "loanFee": {
                "is_show": None
            },
            "receiverInfo": {
                "contractEndPayerAgintType": "PAYER",
                "receipt_name": "testauto",
                "pay_object": "PERSONAL",
                "receipt_bank_no": "622848156",
                "bank": "未知发卡银行",
                "receipt_bank_location": "测试"}
        }

        data["apartmentContractEndReceivableList"] = apartmentContractEndReceivableList
        data["detailList"] = detailList
        data["endBasicInfo"] = endBasicInfo
        data["liquidatedOrTurnFee"] = liquidatedOrTurnFee["liquidatedOrTurnFee"]
        data["endBasicInfo"]["end_reason"] = end_reason
        data["endBasicInfo"]["receivable_date"] = base.now_time() + " 16:00:00"
        data["endBasicInfo"]['end_reason_remark'] = u"终止原因"
        data["endBasicInfo"]['contract_id'] = contract_id
        data["endBasicInfo"]['end_contract_num'] = u"终止协议" + base.random_name()[14:17]
        data["endBasicInfo"]['end_date'] = end_date + " 00:00:00"
        data["endBasicInfo"]['remark'] = u"备注"
        data["endBasicInfo"]['is_old_data'] = "N"
        data["endBasicInfo"]['end_type'] = end_type
        data["endBasicInfo"]["end_type_detail"] = end_type_detail

        # 留个后门,可以控制终止结算应收和应退的金额。
        if receivable_total != None:
            data["endBasicInfo"]['receivable_total'] = receivable_total
        if payable_totle != None:
            data["endBasicInfo"]['payable_totle'] = payable_totle

        try:
            sql = 'SELECT contract_num from house_contract where house_id = (SELECT house_id from apartment_contract where contract_num= "%s")' % self.contract_num
            data["endBasicInfo"]['house_contract_num'] = base.searchSQL(sql)[0][0]
        except Exception as e:
            base.consoleLog("查询委托合同sql报错，sql:" + sql + "。返回错误：" + str(e), 'e')
            return str(e)

        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('提交出租合同终止结算接口执行失败！')
            return result['msg']

        base.consoleLog('提交出租合同终止结算接口执行成功！')
        return

    def reviewed_apartment_contract(self, value=True):
        """
        审核出租合同
        :param contract_num: 出租合同号
        :param Value:
        :return:
        """
        base.consoleLog('审核出租合同。出租合同号：' + self.contract_num)

        # 出租合同详情
        try:
            sql = "select contract_id from apartment_contract where contract_num = '%s'" % self.contract_num
            contract_id = base.searchSQL(sql)[0][0]
        except Exception as e:
            base.consoleLog("查询出租合同sql报错。sql:" + sql + ";错误返回：" + str(e), 'e')
            return str(e)

        # 查询出租合同详情
        url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/searchApartmentContractDetail.action"
        data = {"contract_id": contract_id}
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            return result['msg']
        result = result["obj"]
        receivables = []
        for i in range(len(result["apartmentContractReceivableList"])):
            dicts = result["apartmentContractReceivableList"][i]
            dicts["rowIndex"] = i
            del dicts['houseRoom']
            del dicts['address']
            dicts["edit"] = False
            receivables.append(dicts)

        person = result['customerPerson']
        del person['customer_from_name']
        del person['person_type_name']
        del person['card_type_name']
        del person['customer_type_name']
        del person['gender_name']
        person["yesNo"] = "N"
        person["socialQualification"] = "on"

        apartmentContractRentInfoList = result["apartmentContractRentInfoList"][0]
        apartmentContractRentInfoList["agencyFeeMoney"] = "0.00"
        apartmentContractRentInfoList["deposit"] = result["apartmentContract"]["deposit"]
        apartmentContractRentInfoList["money_cycle"] = result["apartmentContract"]["payment_cycle"]
        apartmentContractRentInfoList["money_type"] = "RENT"
        apartmentContractRentInfoList["month_server_fee"] = result["apartmentContract"]["month_server_fee"]
        apartmentContractRentInfoList["payment_date"] = result["apartmentContract"]["payment_date"]
        apartmentContractRentInfoList["rent_end_date"] = result["apartmentContract"]["rent_end_date"]
        apartmentContractRentInfoList["rent_start_date"] = result["apartmentContract"]["rent_start_date"]
        apartmentContractRentInfoList["firstRow"] = True
        apartmentContractRentInfoList["rowIndex"] = 0
        apartmentContractRentInfoList["sign_date"] = result["apartmentContract"]["sign_date"]

        url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/saveOrUpdateApartmentContract.action"
        data = {
            "contract_id": result['apartmentContract']["contract_id"],
            "house_id": result['apartmentContract']["house_id"],
            "residential_id": result['apartmentContract']["residential_id"],
            "building_id": result['apartmentContract']["building_id"],
            "city_code": result['apartmentContract']["city_code"],
            "area_code": result['apartmentContract']["area_code"],
            "entrust_type": result['apartmentContract']["entrust_type"],
            "apartment_id": result['apartmentContract']["apartment_id"],
            "contract_status": result['apartmentContract']["contract_status"],
            "audit_uid": result['apartmentContract']["audit_uid"],
            "server_flag": result['apartmentContract']["server_flag"],
            "apartment_rent_price": result['apartmentContract']["apartment_rent_price"],
            "contract_type": result['apartmentContract']["contract_type"],
            "apartment_code": result['apartmentContract']["apartment_code"],
            "property_address": result['apartmentContract']["property_address"],
            "production_address": result['apartmentContract']["production_address"],
            "apartment_type": result['apartmentContract']["apartment_type"],
            "input_dep_name": result['apartmentContract']['sign_dep_name'],
            "input_user_name": result['apartmentContract']['sign_user_name'],
            "sign_did": result['apartmentContract']['sign_did'],
            "sign_uid": result['apartmentContract']["sign_uid"],
            "results_belong_did": result['apartmentContract']["results_belong_did"],
            "results_belong_uid": result['apartmentContract']["results_belong_uid"],
            "contract_num": result['apartmentContract']["contract_num"],
            "sign_body": result['apartmentContract']["sign_body"],
            "sign_date": result['apartmentContract']["sign_date"],
            "apartment_check_in_date": result['apartmentContract']["apartment_check_in_date"],
            "rent_start_date": result['apartmentContract']["rent_start_date"],
            "rent_end_date": result['apartmentContract']["rent_end_date"],
            "payment_date": result['apartmentContract']["payment_date"],
            "deposit_type": result['apartmentContract']["deposit_type"],
            "payment_type": result['apartmentContract']["payment_type"],
            "payment_cycle": result['apartmentContract']["payment_cycle"],
            "financing_type": result['apartmentContract']["financing_type"],
            "cash_rent": result['apartmentContract']["cash_rent"],
            "deposit": result['apartmentContract']["deposit"],
            "agency_fee": result['apartmentContract']["agency_fee"],
            "month_server_fee": result['apartmentContract']["month_server_fee"],
            "month_server_fee_discount": result['apartmentContract']["month_server_fee_discount"],
            "load_interest": result['apartmentContract']["load_interest"],
            "remark": result['apartmentContract']["remark"],
            "dispostIn": result['apartmentContract']["dispostIn"],
            "sign_name": result['apartmentContract']["sign_name"],
            "sign_id_type": result['apartmentContract']["sign_id_type"],
            "sign_id_no": result['apartmentContract']["sign_id_no"],
            "sign_phone": result['apartmentContract']["sign_phone"],
            "sign_is_customer": result['apartmentContract']["sign_is_customer"],
            "address": result['apartmentContract']["property_address"],
            "model": "4",
            "achieveid": result['apartmentContract']["contract_id"],
            "activityId": "25",
            "content": "同意"}
        houseContractList_list = []
        houseContractList_list.append(result['houseContractList'][0])
        data['houseContractList'] = houseContractList_list
        data["receivables"] = receivables
        data["person"] = person
        apartmentContractRentInfo = []
        apartmentContractRentInfo.append(apartmentContractRentInfoList)
        data["apartmentContractRentInfoList"] = apartmentContractRentInfo
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            return result['msg']
        if not value:
            base.consoleLog('出租合同初审接口执行成功！')
            return

        ### 出租合同复审
        try:
            sql = "select contract_id from apartment_contract where contract_num = '%s'" % self.contract_num
            contract_id = base.searchSQL(sql)[0][0]
        except Exception as e:
            base.consoleLog("查询出租合同sql报错。sql:" + sql + ";错误返回：" + str(e))
            return "查询出租合同sql报错。sql:" + sql + ";错误返回：" + str(e)

        # 出租合同详情
        url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/searchApartmentContractDetail.action"
        data = {"contract_id": contract_id}
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            return result['msg']
        result = result["obj"]
        receivables = []
        for i in range(len(result["apartmentContractReceivableList"])):
            dicts = result["apartmentContractReceivableList"][i]
            dicts["rowIndex"] = i
            del dicts['houseRoom']
            del dicts['address']
            dicts["edit"] = False
            receivables.append(dicts)

        person = result['customerPerson']
        del person['customer_from_name']
        del person['person_type_name']
        del person['card_type_name']
        del person['customer_type_name']
        del person['gender_name']
        person["yesNo"] = "N"
        person["socialQualification"] = "on"

        apartmentContractRentInfoList = result["apartmentContractRentInfoList"][0]
        apartmentContractRentInfoList["agencyFeeMoney"] = "0.00"
        apartmentContractRentInfoList["deposit"] = result["apartmentContract"]["deposit"]
        apartmentContractRentInfoList["money_cycle"] = result["apartmentContract"]["payment_cycle"]
        apartmentContractRentInfoList["money_type"] = "RENT"
        apartmentContractRentInfoList["month_server_fee"] = result["apartmentContract"]["month_server_fee"]
        apartmentContractRentInfoList["payment_date"] = result["apartmentContract"]["payment_date"]
        apartmentContractRentInfoList["rent_end_date"] = result["apartmentContract"]["rent_end_date"]
        apartmentContractRentInfoList["rent_start_date"] = result["apartmentContract"]["rent_start_date"]
        apartmentContractRentInfoList["firstRow"] = True
        apartmentContractRentInfoList["rowIndex"] = 0
        apartmentContractRentInfoList["sign_date"] = result["apartmentContract"]["sign_date"]

        url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/saveOrUpdateApartmentContract.action"
        data = {
            "contract_id": result['apartmentContract']["contract_id"],
            "house_id": result['apartmentContract']["house_id"],
            "residential_id": result['apartmentContract']["residential_id"],
            "building_id": result['apartmentContract']["building_id"],
            "city_code": result['apartmentContract']["city_code"],
            "area_code": result['apartmentContract']["area_code"],
            "entrust_type": result['apartmentContract']["entrust_type"],
            "apartment_id": result['apartmentContract']["apartment_id"],
            "contract_status": result['apartmentContract']["contract_status"],
            "audit_uid": result['apartmentContract']["audit_uid"],
            "server_flag": result['apartmentContract']["server_flag"],
            "apartment_rent_price": result['apartmentContract']["apartment_rent_price"],
            "contract_type": result['apartmentContract']["contract_type"],
            "apartment_code": result['apartmentContract']["apartment_code"],
            "property_address": result['apartmentContract']["property_address"],
            "production_address": result['apartmentContract']["production_address"],
            "apartment_type": result['apartmentContract']["apartment_type"],
            "input_dep_name": result['apartmentContract']['sign_dep_name'],
            "input_user_name": result['apartmentContract']['sign_user_name'],
            "sign_did": result['apartmentContract']['sign_did'],
            "sign_uid": result['apartmentContract']["sign_uid"],
            "results_belong_did": result['apartmentContract']["results_belong_did"],
            "results_belong_uid": result['apartmentContract']["results_belong_uid"],
            "contract_num": result['apartmentContract']["contract_num"],
            "sign_body": result['apartmentContract']["sign_body"],
            "sign_date": result['apartmentContract']["sign_date"],
            "apartment_check_in_date": result['apartmentContract']["apartment_check_in_date"],
            "rent_start_date": result['apartmentContract']["rent_start_date"],
            "rent_end_date": result['apartmentContract']["rent_end_date"],
            "payment_date": result['apartmentContract']["payment_date"],
            "deposit_type": result['apartmentContract']["deposit_type"],
            "payment_type": result['apartmentContract']["payment_type"],
            "payment_cycle": result['apartmentContract']["payment_cycle"],
            "financing_type": result['apartmentContract']["financing_type"],
            "cash_rent": result['apartmentContract']["cash_rent"],
            "deposit": result['apartmentContract']["deposit"],
            "agency_fee": result['apartmentContract']["agency_fee"],
            "month_server_fee": result['apartmentContract']["month_server_fee"],
            "month_server_fee_discount": result['apartmentContract']["month_server_fee_discount"],
            "load_interest": result['apartmentContract']["load_interest"],
            "remark": result['apartmentContract']["remark"],
            "dispostIn": result['apartmentContract']["dispostIn"],
            "sign_name": result['apartmentContract']["sign_name"],
            "sign_id_type": result['apartmentContract']["sign_id_type"],
            "sign_id_no": result['apartmentContract']["sign_id_no"],
            "sign_phone": result['apartmentContract']["sign_phone"],
            "sign_is_customer": result['apartmentContract']["sign_is_customer"],
            "address": result['apartmentContract']["property_address"],
            "model": "4",
            "achieveid": result['apartmentContract']["contract_id"],
            "activityId": "22",
            "content": "同意"}
        houseContractList_list = []
        houseContractList_list.append(result['houseContractList'][0])
        data['houseContractList'] = houseContractList_list
        data["receivables"] = receivables
        data["person"] = person
        apartmentContractRentInfo = []
        apartmentContractRentInfo.append(apartmentContractRentInfoList)
        data["apartmentContractRentInfoList"] = apartmentContractRentInfo

        # 复审
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('出租合同审核接口执行失败！')
            return result['msg']
        base.consoleLog('出租合同审核接口执行成功！')
        return

    def reviewed_apartment_contract_end(self):
        """
        初审,复审终止结算
        :return:
        """
        base.consoleLog('审核出租终止结算。出租合同：' + self.contract_num)

        try:
            sql = "select contract_id from apartment_contract where contract_num = '%s'" % self.contract_num
            contract_id = base.searchSQL(sql)[0][0]
            sql = "select end_id from apartment_contract_end where contract_id = '%s' and deleted = 0" % contract_id
            end_id = base.searchSQL(sql)[0][0]
        except Exception as e:
            base.consoleLog("查询出租合同sql报错。sql:" + sql + ";错误返回：" + str(e), 'e')
            return str(e)

        # 查询终止结算信息
        url = 'http://erp.ishangzu.com/isz_contract/ContractEndController/searchContractEndInfo'
        data = {"contract_id": contract_id, "end_id": end_id, "is_old_data": "N"}

        end_info = interface.myRequest(url, data)['obj']

        url = 'http://erp.ishangzu.com/isz_contract/ContractEndController/auditApartmrntContractEnd'
        data = {
            "endBasicInfo": {
                "audit_status": "PASS",
                "content": "同意！",
                "contract_id": contract_id,
                "end_contract_num": end_info['endBasicInfo']['end_contract_num'],
                "end_date": end_info['endBasicInfo']['end_date'],
                "update_time": end_info['endBasicInfo']['update_time'],
                "end_id": end_id,
                "end_type": end_info['endBasicInfo']['end_type'],
                "ins_result": "",
                "payment_type": end_info['endBasicInfo']['payment_type']
            },
            "liquidatedOrTurnFee": {
                "discount_liquidated_receivable": end_info['liquidatedOrTurnFee']['discount_liquidated_receivable'],
                "liquidated_receivable": end_info['liquidatedOrTurnFee']['liquidated_receivable'],
                "discountImgList": [{
                    "img_id": "FF808081648867400164889459280029",
                    "src": "erp/2018/7/11/17/7d300073-325c-4417-a0ea-e8521494f311.png"
                }],
                "discount_img_id": None
            },
            "receiverInfo": {
                "bank": "未知发卡银行",
                "contractEndPayerAgintType": "PAYER",
                "pay_object": "PERSONAL",
                "receipt_bank_location": "测试",
                "receipt_bank_no": "622848888888",
                "receipt_name": "钟玲龙"
            }
        }

        result = interface.myRequest(url, data)
        if result['code'] == 0:
            base.consoleLog('初审出租合同终止结算接口执行成功！')
        elif result['code'] != 0:
            base.consoleLog('初审出租合同终止结算接口执行失败！')
            return

        # 查询终止结算信息 复审
        url = 'http://erp.ishangzu.com/isz_contract/ContractEndController/searchContractEndInfo'
        data = {"contract_id": contract_id, "end_id": end_id, "is_old_data": "N"}

        end_info = interface.myRequest(url, data)['obj']

        url = 'http://erp.ishangzu.com/isz_contract/ContractEndController/auditApartmrntContractEnd'
        data = {
            "endBasicInfo": {
                "audit_status": "REVIEW",
                "content": "同意！",
                "contract_id": contract_id,
                "end_contract_num": end_info['endBasicInfo']['end_contract_num'],
                "end_date": end_info['endBasicInfo']['end_date'],
                "update_time": end_info['endBasicInfo']['update_time'],
                "end_id": end_id,
                "end_type": end_info['endBasicInfo']['end_type'],
                "ins_result": "",
                "payment_type": end_info['endBasicInfo']['payment_type']
            },
            "liquidatedOrTurnFee": {
                "discount_liquidated_receivable": end_info['liquidatedOrTurnFee']['discount_liquidated_receivable'],
                "liquidated_receivable": end_info['liquidatedOrTurnFee']['liquidated_receivable'],
                "discountImgList": [{
                    "img_id": "FF808081648867400164889459280029",
                    "src": "erp/2018/7/11/17/7d300073-325c-4417-a0ea-e8521494f311.png"
                }],
                "discount_img_id": None
            },
            "receiverInfo": {
                "bank": "未知发卡银行",
                "contractEndPayerAgintType": "PAYER",
                "pay_object": "PERSONAL",
                "receipt_bank_location": "测试",
                "receipt_bank_no": "622848888888",
                "receipt_name": "钟玲龙"
            }
        }

        result = interface.myRequest(url, data)
        if result['code'] == 0:
            base.consoleLog('复审出租合同终止结算接口执行成功！')
        elif result['code'] != 0:
            base.consoleLog('复审出租合同终止结算接口执行失败！')
            return

    def fanshen_apartment_contract(self):
        """
        反审出租合同
        :return:
        """

        base.consoleLog('反审出租合同。合同号;' + self.contract_num)

        # 出租合同详情
        try:
            sql = "select contract_id from apartment_contract where contract_num = '%s'" % self.contract_num
            contract_id = base.searchSQL(sql)[0][0]
        except Exception as e:
            base.consoleLog("查询出租合同sql报错。sql:" + sql + ";错误返回：" + str(e), 'e')
            return str(e)
        # 反审接口
        url = 'http://isz.ishangzu.com/isz_contract/ApartmentContractController/apartmentContractAudit.action'
        data = {"achieveid": contract_id, "activityId": "24", "content": "测试"}

        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('出租合同反审接口执行失败！')
            return result['msg']
        base.consoleLog('出租合同反审接口执行成功！')
        return

    def fanshen_apartment_contract_end(self):
        """
        反审出租合同终止结算
        :return:
        """
        base.consoleLog('反审出租合同终止结算。出租合同号：' + self.contract_num)

        try:
            sql = "select contract_id from apartment_contract where contract_num = '%s'" % self.contract_num
            contract_id = base.searchSQL(sql)[0][0]
            sql = "select end_id from apartment_contract_end where contract_id = '%s' and deleted = 0" % contract_id
            end_id = base.searchSQL(sql)[0][0]
        except Exception as e:
            base.consoleLog("查询出租合同sql报错。sql:" + sql + ";错误返回：" + str(e), 'e')
            return str(e)

        # 查询终止结算信息
        url = 'http://erp.ishangzu.com/isz_contract/ContractEndController/searchContractEndInfo'
        data = {"contract_id": contract_id, "end_id": end_id, "is_old_data": "N"}

        end_info = interface.myRequest(url, data)['obj']

        url = 'http://erp.ishangzu.com/isz_contract/ContractEndController/auditApartmrntContractEnd'
        data = {
            "endBasicInfo": {
                "audit_status": "REAUDIT",
                "content": "反审！",
                "contract_id": contract_id,
                "end_contract_num": end_info['endBasicInfo']['end_contract_num'],
                "end_date": end_info['endBasicInfo']['end_date'],
                "update_time": end_info['endBasicInfo']['update_time'],
                "end_id": end_id,
                "end_type": end_info['endBasicInfo']['end_type'],
                "ins_result": "",
                "payment_type": end_info['endBasicInfo']['payment_type']
            },
            "liquidatedOrTurnFee": {
                "discount_liquidated_receivable": end_info['liquidatedOrTurnFee']['discount_liquidated_receivable'],
                "liquidated_receivable": end_info['liquidatedOrTurnFee']['liquidated_receivable'],
                "discountImgList": [{
                    "img_id": "FF808081648867400164889459280029",
                    "src": "erp/2018/7/11/17/7d300073-325c-4417-a0ea-e8521494f311.png"
                }],
                "discount_img_id": None
            },
            "receiverInfo": {
                "bank": "未知发卡银行",
                "contractEndPayerAgintType": "PAYER",
                "pay_object": "PERSONAL",
                "receipt_bank_location": "测试",
                "receipt_bank_no": "622848156",
                "receipt_name": "钟玲龙"
            }
        }

        result = interface.myRequest(url, data)
        if result['code'] == 0:
            base.consoleLog('反审出租合同终止结算接口执行成功！')
        elif result['code'] != 0:
            base.consoleLog('反审出租合同终止结算接口执行失败！')
            return

    def delete_apartment_contract(self):
        """
        删除出租合同
        :return:
        """
        base.consoleLog("删除出租合同。出租合同号：" + self.contract_num)

        try:
            sql = "select contract_id from apartment_contract where contract_num = '%s'" % self.contract_num
            contract_id = base.searchSQL(sql)[0][0]
        except Exception as e:
            base.consoleLog("查询出租合同sql报错。sql:" + sql + ";错误返回：" + str(e), 'e')
            return str(e)

        url = 'http://isz.ishangzu.com/isz_contract/ApartmentContractController/deleteApartmentContract.action'
        data = {"contract_id": contract_id}

        result = interface.myRequest(url, data)

        if result['code'] == 0:
            base.consoleLog("删除出租合同接口执行成功！")
            return
        else:
            base.consoleLog("删除出租合同接口执行失败！  " + result)
            return result

    def delete_apartment_contract_end(self):
        """
        删除出租合同终止结算
        :return:
        """
        base.consoleLog("删除出租合同终止结算。出租合同号：" + self.contract_num)

        try:
            sql = "select contract_id from apartment_contract where contract_num = '%s'" % self.contract_num
            contract_id = base.searchSQL(sql)[0][0]
        except Exception as e:
            base.consoleLog("查询出租合同sql报错。sql:" + sql + ";错误返回：" + str(e), 'e')
            return str(e)

        url = 'http://erp.ishangzu.com/isz_contract/endAgreementControl/apartmentContractEnd/' + contract_id

        result = interface.myRequest(url, method='deleted')

        if result['code'] == 0:
            base.consoleLog("删除出租合同终止结算接口执行成功！")
            return
        else:
            base.consoleLog("删除出租合同终止结算接口执行失败！  " + result)
            return result

    def apartment_contract_info(self):
        """
        出租合同详情
        :return:
        """
        base.consoleLog('查询出租合同详情。出租合同号：'+ self.contract_num)

        try:
            sql = "select contract_id from apartment_contract where contract_num = '%s'" % self.contract_num
            contract_id = base.searchSQL(sql)[0][0]
        except Exception as e:
            base.consoleLog("查询出租合同sql报错。sql:" + sql + ";错误返回：" + str(e), 'e')
            return str(e)

        url = 'http://isz.ishangzu.com/isz_contract/ApartmentContractController/searchApartmentContractDetail.action'
        data = {"contract_id":contract_id}

        result = interface.myRequest(url,data)['obj']

        self.apartment_contract_info = {}
        self.apartment_contract_info['apartmentContract'] = result['apartmentContract']
        self.apartment_contract_info['apartmentContractReceivableList'] = result['apartmentContractReceivableList']
        self.apartment_contract_info['apartmentContractAttachmentList'] = result['apartmentContractAttachmentList']
        self.apartment_contract_info['apartmentContractRentInfoList'] = result['apartmentContractRentInfoList']
        self.apartment_contract_info['customerPerson'] = result['customerPerson']
        self.apartment_contract_info['houseContractList'] = result['houseContractList']

        return self.apartment_contract_info

    def update_sign_uid(self, phone='18824321245'):
        """
        资源划转修改出租合同签约人
        :param:phone  账号
        :return:
        """
        base.consoleLog('出租合同资源划转。划转到账号：' + phone)


        try:
            sql = "select contract_id from apartment_contract where contract_num = '%s'" % self.contract_num
            contract_id = base.searchSQL(sql)[0][0]
        except Exception as e:
            base.consoleLog("查询出租合同sql报错。sql:" + sql + ";错误返回：" + str(e), 'e')
            return str(e)

        sql = "SELECT user_id,user_name,dep_id from sys_user where user_phone='%s';" % phone
        user_data = base.search_sql(sql)

        sql = "SELECT dep_name from sys_department where dep_id ='%s';" % user_data[0][2]
        dep_name = base.search_sql(sql)[0][0]

        url = 'http://isz.ishangzu.com/isz_contract/ApartmentContractController/updateSign.action'
        data = {
            "contract_ids": contract_id,
            "sign_did":user_data[0][2],
            "new_sign_user":dep_name,
            "sign_uid": user_data[0][0]}

        result = interface.myRequest(url,data)
        if result['code'] == 0:
            base.consoleLog('委托合同签约人修改接口执行成功！')
        else:
            base.consoleLog('委托合同签约人修改接口执行失败！'+result['msg'],level='e')
            return result['msg']
        return

    def updata_apartment_contract(self):
        """
        更新出租合同第一页
        :return:
        """
        base.consoleLog('更新出租合同第一页。出租合同号：' + self.contract_num)
        url = 'http://isz.ishangzu.com/isz_contract/ApartmentContractController/saveOrUpdateApartmentContract.action'
        data = {}

# t = ApartmentContract(contract_num='zll2018-07-31mgi867',rent_start_date=base.now_time())
# print(t.apartment_contract_info()['apartmentContract'])




