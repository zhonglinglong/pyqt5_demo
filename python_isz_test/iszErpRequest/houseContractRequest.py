# -*- coding:utf8 -*-
"""
2018年5月27日10:57:46
委托合同类接口
"""

__auto__ = 'zhonglinglong'

from classDemo.myRequest import NewRequest
from common import base
import datetime
import time
import json


class HouseContract:
    """委托合同类"""

    def __init__(self, residential_name=None, contract_num=None, entrust_start_date=None, apartment_type="品质公寓",
                 entrust_type="合租", reform_way="小改",
                 payment_cycle='年付', sign_body='杭州爱上租物业管理有限公司', rentMoney='3000', channel_fee='500', entrust_year='3',
                 house_code=None,rent_free_type='免租期外置',rent_strategy=True):
        self.residential_name = residential_name
        self.contract_num = contract_num
        self.entrust_start_date = entrust_start_date  # 委托起算日
        self.apartment_type = base.get_conf('house_contract', apartment_type)  # 公寓类型
        self.entrust_type = base.get_conf('house_contract', entrust_type)  # 合同类型
        self.reform_way = base.get_conf('house_contract', reform_way)  # 改造方式
        self.payment_cycle = base.get_conf('house_contract', payment_cycle)  # 付款方式
        self.sign_body = base.get_conf('house_contract', sign_body)  # 签约公司
        self.url = 'http://erp.ishangzu.com/isz_housecontract/houseContractController/uploadImageFile'  # 委托合同所有上传图片的地址
        self.rentMoney = rentMoney  # 月租金
        self.channel_fee = channel_fee  # 渠道服务费
        self.entrust_year = entrust_year  # 委托年限
        self.house_code = house_code  # 房源编号
        self.rent_free_type = base.get_conf('house_contract', rent_free_type) # 合同标志
        self.rent_strategy = rent_strategy # 租金策略。默认为True.生成一样的租金。Fasles,生成不一样的租金。

    def add_house_contract(self):
        """
        新签委托合同
        :return:
        """
        base.consoleLog('新增委托合同。委托合同号：' + self.contract_num)

        null = None

        if self.house_code == None:
            # 查询该楼盘下是否有满足签合同的房源
            sql = """SELECT
                            h.house_code
                        FROM
                            house h
                        LEFT JOIN house_rent hr ON hr.house_id = h.house_id
                        LEFT JOIN residential re ON re.residential_id = h.residential_id
                        AND hr.house_status = 'WAITING_RENT'
                        AND hr.deleted = 0
                        WHERE
                        re.residential_name = "%s"
                        AND h.deleted = 0
                        AND NOT EXISTS (
                            SELECT
                                1
                            FROM
                                house_contract hc
                            WHERE
                                hc.house_id = h.house_id
                            AND deleted = 0
                        ) LIMIT 1 """ % self.residential_name
            try:
                base.searchSQL(sql)
                self.house_code = base.searchSQL(sql)[0][0]
            except BaseException as e:
                base.consoleLog("该楼盘所有开发自营房源至少签过一次，为了避免被老数据影响，请新增开发房源或者换个楼盘~!  报错信息：" + str(e), 'e')
                return str(e)

        # 查询house信息
        sql = """SELECT
                property_name,
                house_code,
                building_id,
                house_id,
                city_code,
                area_code,
                residential_id,
                bathrooms,
                rooms,
                kitchens,
                livings
                FROM
                house
                WHERE
                house_code = '%s' """ % self.house_code
        house_contact_data = base.searchSQL(sql)

        # 委托合同第一页
        idCardPhotos = interface.upLoadPhoto(self.url, base.get_conf('Img', 'picture_name'),
                                             base.get_conf('Img', 'file_path'))  # 上传图片

        HouseContractFrist = {}
        HouseContractFrist["houseContractFrist"] = {
            "address": house_contact_data[0][0],
            "bathrooms":  house_contact_data[0][7],
            "rooms":  house_contact_data[0][8],
            "kitchens": house_contact_data[0][9],
            "livings": house_contact_data[0][10],
            "certificate_type": "",
            "certificate_type_id": "3",  # 产权证类型id
            "commonLandlords": [],
            "common_case": "PRIVATE",  # 产权证私有
            "common_case_cn": "",
            "contract_id": null,
            "contract_type": "NEWSIGN",
            "contract_type_cn": "新签",
            "houseContractLandlord": {
                "card_type": "PASSPORT",  # 护照
                "id_card": "55667788",  # 护照证件号
                "landlord_name": "产权人姓名",
                "property_owner_type": "PROPERTYOWNER", # 产权类型：个人
                "property_card_id": "123456789", # 产权证号
                "idCardPhotos": [{
                    "src": idCardPhotos['src'],
                    "url": idCardPhotos['src'],
                    "remark": "其他",
                    "img_id": idCardPhotos['img_id']
                }],
                "phone": "18279881085"
            },
            "house_code": house_contact_data[0][1],
            "inside_space": "138", #面积
            "is_new_data": null,
            "mortgageeStatementOriginal": [],
            "pledge": "0",
            "productionVos": [{
                "attachments": [{
                    "src": idCardPhotos['src'],
                    "url": idCardPhotos['src'],
                    "remark": "",
                    "img_id": idCardPhotos['img_id']
                }],
                "file_type": "附记页",
                "file_type_id": 3,
                "is_active": "Y",
                "is_approved_need": "Y",
                "is_audit_need": "Y",
                "is_save_need": "N"
            }, {
                "attachments": [{
                    "src": idCardPhotos['src'],
                    "url": idCardPhotos['src'],
                    "remark": "",
                    "img_id": idCardPhotos['img_id']
                }],
                "file_type": "带证号页(有产权证编号页)",
                "file_type_id": 1,
                "is_active": "Y",
                "is_approved_need": "Y",
                "is_audit_need": "Y",
                "is_save_need": "Y"
            }, {
                "attachments": [{
                     "src": idCardPhotos['src'],
                    "url": idCardPhotos['src'],
                    "remark": "",
                    "img_id": idCardPhotos['img_id']
                }],
                "file_type": "主页(有业主姓名/物业地址页)",
                "file_type_id": 2,
                "is_active": "Y",
                "is_approved_need": "Y",
                "is_audit_need": "Y",
                "is_save_need": "Y"
            }],
            "production_address": "产权地址",
            "property_card_id": null,
            "property_use": "HOUSE",
            "property_use_cn": ""
        }

        # 委托合同第二页
        idCardPhotos = interface.upLoadPhoto(self.url, base.get_conf('Img', 'picture_name'),
                                             base.get_conf('Img', 'file_path'))  #上传图片
        HouseContractSecond = {}
        HouseContractSecond["houseContractSecond"] = {
            "agreedRentOriginalStatements": [{
                "src": idCardPhotos['src'],
                "url": idCardPhotos['src'],
                "type": "",
                "img_id": idCardPhotos['img_id']
            }],
            "any_agent": "0",
            "assetsOfLessor": [{
                "landlord_name": "产权人姓名",
                "phone": "18279881085",
                "email": "zhonglinglong@ishangzu.com",
                "mailing_address": "通讯地址"
            }],
            "contract_id": null,
            "houseContractSign": {
                "address": "",
                "agent_type": "",
                "attachments": [],
                "card_type": "",
                "email": "",
                "id_card": "",
                "phone": "",
                "sign_name": ""
            },
            "is_new_data": null,
            "originalAgentDataRelations": [],
            "originalLessorHasDied": []
        }

        # 委托合同第三页
        idCardPhotos = interface.upLoadPhoto(self.url, base.get_conf('Img', 'picture_name'),
                                             base.get_conf('Img', 'file_path'))
        HouseContractThird = {}
        HouseContractThird["houseContractThird"] = {
            "account_bank": "支行",
            "account_name": "产权人姓名",
            "account_num": "622848888888",
            "bank": "未知发卡银行",
            "contract_id": null,
            "is_new_data": null,
            "notPropertyOwnerGrantReceipts": [],
            "pay_object": "PERSONAL",
            "payeeIdPhotos": [{
                "src": idCardPhotos['src'],
                "url": idCardPhotos['src'],
                "remark": "其他",
                "img_id": idCardPhotos['img_id']
            }],
            "payee_card_type": "PASSPORT",
            "payee_card_type_cn": "",
            "payee_emergency_name": "紧急联系人",
            "payee_emergency_phone": "15750935006",
            "payee_id_card": "55667788",
            "payee_type": "PROPERTYOWNER",
            "payee_type_cn": "",
            "receiptAccountProve": [{
                "src": "http://img.ishangzu.com/erp/2018/11/23/16/e41d2d92-26ae-4405-9efd-65361da44643.jpg",
                "url": "http://img.ishangzu.com/erp/2018/11/23/16/e41d2d92-26ae-4405-9efd-65361da44643.jpg",
                "type": "",
                "img_id": "FF808081673F9B5301673FA229780040"
            }]

        }

        # 委托合同第四页数据
        idCardPhotos = interface.upLoadPhoto(self.url, base.get_conf('Img', 'picture_name'),
                                             base.get_conf('Img', 'file_path'))   #图片上传

        # 免租天数和付款方式关联
        if self.payment_cycle == 'MONTH':  # 月付
            self.free_days = 25
        elif self.payment_cycle == 'TOW_MONTH' or self.payment_cycle == 'SEASON' or self.payment_cycle == 'ALL':  # 二月付,季付,一次性付款
            self.free_days = 30
        elif self.payment_cycle == 'HALF_YEAR':  # 半年付
            self.free_days = 40
        elif self.payment_cycle == 'ONE_YEAR':  # 半年付
            self.free_days = 50

        day_number = (365+self.free_days) * int(self.entrust_year)   # 委托起算日至委托到期日天数
        self.entrust_end_date = str(
            datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') + datetime.timedelta(
                days=(day_number)))  # 委托结束日

        # 根据改造类型,设置了委托起算日。
        # 装修起算日,装修结束日,业主交房日,签约日期。
        if self.reform_way == 'OLDRESTYLE' or self.reform_way == 'BLANKRESTYLE'  or self.reform_way == 'RESTYLE':  # 老房全装 or 毛坯全装 or 全装
            fitment_start_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=61))  # 装修起算日
            fitment_end_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=1))  # 装修结束日
            owner_sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=61))  # 业主交房日
            self.sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=61))  # 签约日期
        elif self.reform_way == 'RESTYLED':  # 大改
            fitment_start_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=31))
            fitment_end_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=1))
            owner_sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=31))
            self.sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=31))
        elif self.reform_way == 'RETROFITTING' or self.reform_way == 'REFORM':  # 小改 or 改造
            fitment_start_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=16))
            fitment_end_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=1))
            owner_sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=16))
            self.sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=16))
        elif self.reform_way == 'TINYCHANGE': # 修配
            fitment_start_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=8))
            fitment_end_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=1))
            owner_sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=8))
            self.sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=8))
        elif self.reform_way == 'UNRRESTYLE': # 不改造
            fitment_start_date = ""
            fitment_end_date = ""
            owner_sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=0))
            self.sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=0))

            day_number = 365 * int(self.entrust_year)
            self.entrust_end_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') + datetime.timedelta(
                    days=(day_number)))  # 委托结束日

        # 根据规则设置的签约日期大于当前时间时,需自动把签约日期设置成当前时间。
        if time.strptime(self.sign_date, "%Y-%m-%d %H:%M:%S") > time.strptime(base.now_time() + ' 00:00:00',
                                                                              "%Y-%m-%d %H:%M:%S"):
            self.sign_date = base.now_time()

        # 首次付款日
        first_pay_date = str(datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d'))[0:7] + "-15"



        residential_id = house_contact_data[0][6]
        sign_dep_name = base.get_conf("loginUser", "sign_dep_name")
        sign_did = base.get_conf("loginUser", "dep_id")
        sign_uid = base.get_conf("loginUser", "user_id")
        sign_user_name = base.get_conf("loginUser", "user_name")
        area_code = house_contact_data[0][5]
        building_id = house_contact_data[0][2]
        self.city_code = house_contact_data[0][4]
        house_id = house_contact_data[0][3]

        # 房屋渠道来源
        url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/searchHouseContractInfoBase?contract_type=NEWSIGN&house_id=" + house_id
        result = interface.myRequest(url, method="get")
        if result['code'] != 0:
            return result['msg']
        result = result["obj"]
        house_source = result["houseContractFour"]["house_source"]

        # 根据房源类型,区分是否需要渠道费用。为了方便测试,直接把外部提交和中介合作的房源设置成有服务费。
        # 系统规则应该是,取新增房源接口第4个页面,看返回channelFeeServiceFactors是否为空。
        if house_source == "MIDDLEMEN" or house_source == "AISHANGFANG":
            channelFeeServiceFactors =  [{
                "channel_pay_type": "PAY_PRIVATE",
                "max": 3000,
                "percent": 25
            }, {
                "channel_pay_type": "PAY_PUBLIC",
                "max": 2500,
                "percent": 25
            }]
            channel_pay_type = "PAY_PRIVATE"
            channel_fee = self.channel_fee
        else:
            channelFeeServiceFactors = []
            channel_pay_type = ''
            channel_fee = ''

        # 服务费系数
        url_self = 'http://erp.ishangzu.com/isz_housecontract/houseContractController/getHouseContractServiceFactor?'
        url_at = 'apartment_type=' + self.apartment_type
        url_cc = '&city_code=' + self.city_code
        url_ct = '&contract_type=NEWSIGN&sign_date='
        url = url_self + url_at + url_cc + url_ct + self.sign_date[0:10]
        freeFactor = interface.myRequest(url, method='get')
        if freeFactor['code'] != 0:
            return result['msg']
        freeFactor = freeFactor['obj']['freeFactor']

        HouseContractFour = {}
        HouseContractFour["houseContractFour"] = {
            "apartment_type": self.apartment_type,
            "apartment_type_cn": "",
            "area_code": area_code,
            "audit_status": null,
            "audit_time": null,
            "audit_uid": null,
            "building_id": building_id,
            "can_update_channel_fee": False,
            "channelFeeServiceFactors": channelFeeServiceFactors,
            "channel_fee": channel_fee,
            "channel_pay_type": channel_pay_type,
            "city_code": self.city_code,
            "contractAttachments": [{
                "src": idCardPhotos['src'],
                "url": idCardPhotos['src'],
                "img_id": idCardPhotos['img_id']
            }],
            "contract_id": null,
            "contract_num": self.contract_num,
            "contract_status": null,
            "contract_type": "NEWSIGN",
            "contract_type_cn": "新签",
            "electron_file_src": null,
            "energy_company": null,
            "energy_fee": null,
            "entrust_end_date": self.entrust_end_date,
            "entrust_start_date": self.entrust_start_date,
            "entrust_type": self.entrust_type,
            "entrust_type_cn": "",
            "entrust_year": self.entrust_year,
            "entrust_year_cn": "",
            "first_pay_date": first_pay_date,
            "fitment_end_date": fitment_end_date,
            "fitment_start_date": fitment_start_date,
            "freeType": null,
            "freeType_cn": "",
            "free_days": self.free_days,
            "free_end_date": null,
            "free_start_date": null,
            "have_parking": "N",
            "houseContractPDFs": null,
            "house_id": house_id,
            "house_source": house_source,
            "housekeep_mange_dep": null,
            "housekeep_mange_dep_user": "-",
            "housekeep_mange_did": null,
            "housekeep_mange_uid": null,
            "housekeep_mange_user_name": null,
            "is_electron": null,
            "is_new_data": null,
            "owner_sign_date": owner_sign_date,
            "parent_id": null,
            "parking": "",
            "payment_cycle": self.payment_cycle,
            "payment_cycle_cn": "",
            "property": null,
            "property_company": null,
            "rent_free_type": self.rent_free_type,
            "reform_way": self.reform_way,
            "reform_way_cn": "",
            "remark": null,
            "rentMoney": self.rentMoney,
            "rental_price": self.rentMoney,
            "reset_finance": False,
            "residential_id": residential_id,
            "server_manage_dep_user": "",
            "server_manage_did": null,
            "server_manage_did_name": null,
            "server_manage_uid": null,
            "server_manage_uid_name": null,
            "service_fee_factor": freeFactor,
            "sign_body": self.sign_body,
            "sign_date": self.sign_date,
            "sign_dep_name": sign_dep_name,
            "sign_did": sign_did,
            "sign_uid": sign_uid,
            "sign_user_name": sign_user_name,
            "year_service_fee": null}



        # 生成租金策略
        url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/getHouseRentStrategyVo"
        data = {
            "apartment_type": self.apartment_type,
            "contract_type": "NEWSIGN",
            "entrust_start_date": self.entrust_start_date,
            "entrust_end_date": self.entrust_end_date,
            "free_end_date": "",
            "free_start_date": "",
            "parking": "",
            "payment_cycle": self.payment_cycle,
            "rent_money": self.rentMoney,
            "sign_date": self.sign_date,
            "city_code": self.city_code,
            "entrust_year": self.entrust_year,
            "free_days": self.free_days,
            "version": "V_THREE"}
        HouseContractFour_02 = interface.myRequest(url, data)
        if HouseContractFour_02['code'] != 0:
            return HouseContractFour_02['msg']
        HouseContractFour_02["rentStrategys"] = HouseContractFour_02["obj"]
        #如果租金策略为false：self.rent_strategy  生成不一样的租金策略
        if not self.rent_strategy:
            add = 0.01
            rentStrategys =HouseContractFour_02["rentStrategys"]
            for i in range(len(rentStrategys)-1):
                add = add +0.01
                rentStrategys[i+1]['rentMoney'] = int(rentStrategys[0]['rentMoney']) * (add+1)

            HouseContractFour["houseContractFour"]["rentStrategys"] = rentStrategys
        else:
            HouseContractFour["houseContractFour"]["rentStrategys"] = HouseContractFour_02["rentStrategys"]


        # 委托合同第五页
        # 生成租金明细
        url = "http://erp.ishangzu.com/isz_finance/HouseContractPayableController/createContractPayable"
        data = {
            "contractId": "",
            'rentFreeType': self.rent_free_type,
            "firstPayDate": first_pay_date,
            "version": "V_THREE"}
        datas = {}
        datas["rentInfoList"] = HouseContractFour_02["rentStrategys"]
        data.update(datas)
        # print(data)
        HouseContractFive = interface.myRequest(url, data)
        print(HouseContractFive)
        if HouseContractFive['code'] != 0:
            return HouseContractFive['msg']

        #委托合同五个页面参数合一起
        HouseContractFive["houseContractFive"] = HouseContractFive["obj"]
        houseContract = {}
        houseContract.update(HouseContractFrist)
        houseContract.update(HouseContractSecond)
        houseContract.update(HouseContractThird)
        houseContract.update(HouseContractFour)
        houseContract.update(HouseContractFive)

        print(houseContract)

        # 新签委托合同
        url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/saveHouseContract"
        result = interface.myRequest(url, houseContract)
        if result['code'] != 0:
            base.consoleLog('新增委托合同接口执行失败！')
            return result['msg']
        base.consoleLog('新增委托合同接口执行成功！')
        return


    def add_dian_house_contract(self):
        """
        新增委托合同ERP电签
        :return:
        """

        base.consoleLog('新增erp电签委托合同。委托合同号：' + self.contract_num)

        null = None

        if self.house_code == None:
            # 查询该楼盘下是否有满足签合同的房源
            sql = """SELECT
                                   h.house_code
                               FROM
                                   house h
                               LEFT JOIN house_rent hr ON hr.house_id = h.house_id
                               LEFT JOIN residential re ON re.residential_id = h.residential_id
                               AND hr.house_status = 'WAITING_RENT'
                               AND hr.deleted = 0
                               WHERE
                               re.residential_name = "%s"
                               AND h.deleted = 0
                               AND NOT EXISTS (
                                   SELECT
                                       1
                                   FROM
                                       house_contract hc
                                   WHERE
                                       hc.house_id = h.house_id
                                   AND deleted = 0
                               ) LIMIT 1 """ % self.residential_name
            try:
                base.searchSQL(sql)
                self.house_code = base.searchSQL(sql)[0][0]
            except BaseException as e:
                base.consoleLog("该楼盘所有开发自营房源至少签过一次，为了避免被老数据影响，请新增开发房源或者换个楼盘~!  报错信息：" + str(e), 'e')
                return str(e)

        # 查询house信息
        sql = """SELECT
                       property_name,
                       house_code,
                       building_id,
                       house_id,
                       city_code,
                       area_code,
                       residential_id,
                       bathrooms,
                       rooms,
                       kitchens,
                       livings
                       FROM
                       house
                       WHERE
                       house_code = '%s' """ % self.house_code
        house_contact_data = base.searchSQL(sql)

        # 委托合同第一页
        idCardPhotos = interface.upLoadPhoto(self.url, base.get_conf('Img', 'picture_name'),
                                             base.get_conf('Img', 'file_path'))  # 上传图片

        HouseContractFrist = {}
        HouseContractFrist["houseContractFrist"] = {
            "address": house_contact_data[0][0],
            "bathrooms": house_contact_data[0][7],
            "rooms": house_contact_data[0][8],
            "kitchens": house_contact_data[0][9],
            "livings": house_contact_data[0][10],
            "certificate_type": "",
            "certificate_type_id": "3",  # 产权证类型id
            "commonLandlords": [],
            "common_case": "PRIVATE",  # 产权证私有
            "common_case_cn": "",
            "contract_id": null,
            "contract_type": "NEWSIGN",
            "contract_type_cn": "新签",
            "houseContractLandlord": {
                "card_type": "PASSPORT",  # 护照
                "id_card": "55667788",  # 护照证件号
                "landlord_name": "产权人姓名",
                "property_owner_type": "PROPERTYOWNER",  # 产权类型：个人
                "property_card_id": "123456789",  # 产权证号
                "idCardPhotos": [{
                    "src": idCardPhotos['src'],
                    "url": idCardPhotos['src'],
                    "remark": "其他",
                    "img_id": idCardPhotos['img_id']
                }],
                "phone": "18279881085"
            },
            "house_code": house_contact_data[0][1],
            "inside_space": "138",  # 面积
            "is_new_data": null,
            "mortgageeStatementOriginal": [],
            "pledge": "0",
            "productionVos": [{
                "attachments": [{
                    "src": idCardPhotos['src'],
                    "url": idCardPhotos['src'],
                    "remark": "",
                    "img_id": idCardPhotos['img_id']
                }],
                "file_type": "附记页",
                "file_type_id": 3,
                "is_active": "Y",
                "is_approved_need": "Y",
                "is_audit_need": "Y",
                "is_save_need": "N"
            }, {
                "attachments": [{
                    "src": idCardPhotos['src'],
                    "url": idCardPhotos['src'],
                    "remark": "",
                    "img_id": idCardPhotos['img_id']
                }],
                "file_type": "带证号页(有产权证编号页)",
                "file_type_id": 1,
                "is_active": "Y",
                "is_approved_need": "Y",
                "is_audit_need": "Y",
                "is_save_need": "Y"
            }, {
                "attachments": [{
                    "src": idCardPhotos['src'],
                    "url": idCardPhotos['src'],
                    "remark": "",
                    "img_id": idCardPhotos['img_id']
                }],
                "file_type": "主页(有业主姓名/物业地址页)",
                "file_type_id": 2,
                "is_active": "Y",
                "is_approved_need": "Y",
                "is_audit_need": "Y",
                "is_save_need": "Y"
            }],
            "production_address": "产权地址",
            "property_card_id": null,
            "property_use": "HOUSE",
            "property_use_cn": ""
        }

        # 委托合同第二页
        idCardPhotos = interface.upLoadPhoto(self.url, base.get_conf('Img', 'picture_name'),
                                             base.get_conf('Img', 'file_path'))  # 上传图片
        HouseContractSecond = {}
        HouseContractSecond["houseContractSecond"] = {
            "agreedRentOriginalStatements": [{
                "src": idCardPhotos['src'],
                "url": idCardPhotos['src'],
                "type": "",
                "img_id": idCardPhotos['img_id']
            }],
            "any_agent": "0",
            "assetsOfLessor": [{
                "landlord_name": "产权人姓名",
                "phone": "18279881085",
                "email": "zhonglinglong@ishangzu.com",
                "mailing_address": "通讯地址"
            }],
            "contract_id": null,
            "houseContractSign": {
                "address": "",
                "agent_type": "",
                "attachments": [],
                "card_type": "",
                "email": "",
                "id_card": "",
                "phone": "",
                "sign_name": ""
            },
            "is_new_data": null,
            "originalAgentDataRelations": [],
            "originalLessorHasDied": []
        }

        # 委托合同第三页
        # 委托合同第三页
        idCardPhotos = interface.upLoadPhoto(self.url, base.get_conf('Img', 'picture_name'),
                                             base.get_conf('Img', 'file_path'))
        HouseContractThird = {}
        HouseContractThird["houseContractThird"] = {
            "account_bank": "支行",
            "account_name": "产权人姓名",
            "account_num": "622848888888",
            "bank": "未知发卡银行",
            "contract_id": null,
            "is_new_data": null,
            "notPropertyOwnerGrantReceipts": [],
            "pay_object": "PERSONAL",
            "payeeIdPhotos": [{
                "src": idCardPhotos['src'],
                "url": idCardPhotos['src'],
                "remark": "其他",
                "img_id": idCardPhotos['img_id']
            }],
            "payee_card_type": "PASSPORT",
            "payee_card_type_cn": "",
            "payee_emergency_name": "紧急联系人",
            "payee_emergency_phone": "15750935006",
            "payee_id_card": "55667788",
            "payee_type": "PROPERTYOWNER",
            "payee_type_cn": "",
            "receiptAccountProve": [{
                "src": "http://img.ishangzu.com/erp/2018/11/23/16/e41d2d92-26ae-4405-9efd-65361da44643.jpg",
                "url": "http://img.ishangzu.com/erp/2018/11/23/16/e41d2d92-26ae-4405-9efd-65361da44643.jpg",
                "type": "",
                "img_id": "FF808081673F9B5301673FA229780040"
            }]

        }

        # 委托合同第四页数据
        idCardPhotos = interface.upLoadPhoto(self.url, base.get_conf('Img', 'picture_name'),
                                             base.get_conf('Img', 'file_path'))  # 图片上传

        # 免租天数和付款方式关联
        if self.payment_cycle == 'MONTH':  # 月付
            self.free_days = 25
        elif self.payment_cycle == 'TOW_MONTH' or self.payment_cycle == 'SEASON' or self.payment_cycle == 'ALL':  # 二月付,季付,一次性付款
            self.free_days = 30
        elif self.payment_cycle == 'HALF_YEAR':  # 半年付
            self.free_days = 40
        elif self.payment_cycle == 'ONE_YEAR':  # 半年付
            self.free_days = 50

        day_number = (365 + self.free_days) * int(self.entrust_year)  # 委托起算日至委托到期日天数
        self.entrust_end_date = str(
            datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') + datetime.timedelta(
                days=(day_number)))  # 委托结束日

        # 根据改造类型,设置了委托起算日。
        # 装修起算日,装修结束日,业主交房日,签约日期。
        if self.reform_way == 'OLDRESTYLE' or self.reform_way == 'BLANKRESTYLE' or self.reform_way == 'RESTYLE':  # 老房全装 or 毛坯全装 or 全装
            fitment_start_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=61))  # 装修起算日
            fitment_end_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=1))  # 装修结束日
            owner_sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=61))  # 业主交房日
            self.sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=61))  # 签约日期
        elif self.reform_way == 'RESTYLED':  # 大改
            fitment_start_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=31))
            fitment_end_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=1))
            owner_sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=31))
            self.sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=31))
        elif self.reform_way == 'RETROFITTING' or self.reform_way == 'REFORM':  # 小改 or 改造
            fitment_start_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=16))
            fitment_end_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=1))
            owner_sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=16))
            self.sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=16))
        elif self.reform_way == 'TINYCHANGE':  # 修配
            fitment_start_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=8))
            fitment_end_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=1))
            owner_sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=8))
            self.sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=8))
        elif self.reform_way == 'UNRRESTYLE':  # 不改造
            fitment_start_date = ""
            fitment_end_date = ""
            owner_sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=0))
            self.sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=0))

            day_number = 365 * int(self.entrust_year)
            self.entrust_end_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') + datetime.timedelta(
                    days=(day_number)))  # 委托结束日

        # 根据规则设置的签约日期大于当前时间时,需自动把签约日期设置成当前时间。
        if time.strptime(self.sign_date, "%Y-%m-%d %H:%M:%S") > time.strptime(base.now_time() + ' 00:00:00',
                                                                              "%Y-%m-%d %H:%M:%S"):
            self.sign_date = base.now_time()

        # 首次付款日
        first_pay_date = str(datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d'))[0:7] + "-15"

        residential_id = house_contact_data[0][6]
        sign_dep_name = base.get_conf("loginUser", "sign_dep_name")
        sign_did = base.get_conf("loginUser", "dep_id")
        sign_uid = base.get_conf("loginUser", "user_id")
        sign_user_name = base.get_conf("loginUser", "user_name")
        area_code = house_contact_data[0][5]
        building_id = house_contact_data[0][2]
        self.city_code = house_contact_data[0][4]
        house_id = house_contact_data[0][3]

        # 房屋渠道来源
        url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/searchHouseContractInfoBase?contract_type=NEWSIGN&house_id=" + house_id
        result = interface.myRequest(url, method="get")
        if result['code'] != 0:
            return result['msg']
        result = result["obj"]
        house_source = result["houseContractFour"]["house_source"]

        # 根据房源类型,区分是否需要渠道费用。为了方便测试,直接把外部提交和中介合作的房源设置成有服务费。
        # 系统规则应该是,取新增房源接口第4个页面,看返回channelFeeServiceFactors是否为空。
        if house_source == "MIDDLEMEN" or house_source == "AISHANGFANG":
            channelFeeServiceFactors = [{
                "channel_pay_type": "PAY_PRIVATE",
                "max": 3000,
                "percent": 25
            }, {
                "channel_pay_type": "PAY_PUBLIC",
                "max": 2500,
                "percent": 25
            }]
            channel_pay_type = "PAY_PRIVATE"
            channel_fee = self.channel_fee
        else:
            channelFeeServiceFactors = []
            channel_pay_type = ''
            channel_fee = ''

        # 服务费系数
        url_self = 'http://erp.ishangzu.com/isz_housecontract/houseContractController/getHouseContractServiceFactor?'
        url_at = 'apartment_type=' + self.apartment_type
        url_cc = '&city_code=' + self.city_code
        url_ct = '&contract_type=NEWSIGN&sign_date='
        url = url_self + url_at + url_cc + url_ct + self.sign_date[0:10]
        freeFactor = interface.myRequest(url, method='get')
        if freeFactor['code'] != 0:
            return result['msg']
        freeFactor = freeFactor['obj']['freeFactor']

        HouseContractFour = {}
        HouseContractFour["houseContractFour"] = {
            "apartment_type": self.apartment_type,
            "apartment_type_cn": "",
            "area_code": area_code,
            "audit_status": null,
            "audit_time": null,
            "audit_uid": null,
            "building_id": building_id,
            "can_switch_channel_type": True,
            "can_update_channel_fee": True,
            "channelFeeServiceFactors": channelFeeServiceFactors,
            "channel_fee": channel_fee,
            "channel_pay_type": channel_pay_type,
            "city_code": self.city_code,
            "contractAttachments": [{
                "src": idCardPhotos['src'],
                "url": idCardPhotos['src'],
                "img_id": idCardPhotos['img_id']
            }],
            "contract_id": null,
            "contract_num": self.contract_num,
            "contract_status": null,
            "contract_type": "",
            "contract_type_cn": "",
            "delay_date": "111111111111111111111111111111111111111111111111111111111111111111111111",
            "enable_rent_free": True,
            "electron_file_src": null,
            "energy_company": null,
            "energy_fee": null,
            "entrust_end_date": self.entrust_end_date,
            "entrust_start_date": self.entrust_start_date,
            "entrust_type": self.entrust_type,
            "entrust_type_cn": "",
            "entrust_year": self.entrust_year,
            "entrust_year_cn": "",
            "first_pay_date": first_pay_date,
            "fitment_end_date": fitment_end_date,
            "fitment_start_date": fitment_start_date,
            "freeType": null,
            "freeType_cn": "",
            "free_days": self.free_days,
            "free_end_date": null,
            "free_start_date": null,
            "have_parking": "N",
            "houseContractPDFs": null,
            "house_id": house_id,
            "house_source": house_source,
            "housekeep_mange_dep": null,
            "housekeep_mange_dep_user": "-",
            "housekeep_mange_did": null,
            "housekeep_mange_uid": null,
            "housekeep_mange_user_name": null,
            "is_electron": null,
            "is_new_data": null,
            "owner_sign_date": owner_sign_date,
            "parent_id": null,
            "parking": "",
            "payment_cycle": self.payment_cycle,
            "payment_cycle_cn": "",
            "property": null,
            "property_company": null,
            "rent_free_type": self.rent_free_type,
            "reform_way": self.reform_way,
            "reform_way_cn": "",
            "remark": null,
            "rentMoney": self.rentMoney,
            "rental_price": self.rentMoney,
            "reset_finance": False,
            "residential_id": residential_id,
            "server_manage_dep_user": "",
            "server_manage_did": null,
            "server_manage_did_name": null,
            "server_manage_uid": null,
            "server_manage_uid_name": null,
            "service_fee_factor": freeFactor,
            "sign_body": self.sign_body,
            "sign_date": self.sign_date,
            "sign_dep_name": sign_dep_name,
            "sign_did": sign_did,
            "sign_uid": sign_uid,
            "sign_user_name": sign_user_name,
            "year_service_fee": null}

        # 生成租金策略
        url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/getHouseRentStrategyVo"
        data = {
            "apartment_type": self.apartment_type,
            "contract_type": "NEWSIGN",
            "entrust_start_date": self.entrust_start_date,
            "entrust_end_date": self.entrust_end_date,
            "free_end_date": "",
            "free_start_date": "",
            "parking": "",
            "payment_cycle": self.payment_cycle,
            "rent_money": self.rentMoney,
            "sign_date": self.sign_date,
            "city_code": self.city_code,
            "entrust_year": self.entrust_year,
            "free_days": self.free_days,
            "version": "V_THREE"}
        HouseContractFour_02 = interface.myRequest(url, data)
        if HouseContractFour_02['code'] != 0:
            return HouseContractFour_02['msg']
        HouseContractFour_02["rentStrategys"] = HouseContractFour_02["obj"]
        # 如果租金策略为false：self.rent_strategy  生成不一样的租金策略
        if not self.rent_strategy:
            add = 0.01
            rentStrategys = HouseContractFour_02["rentStrategys"]
            for i in range(len(rentStrategys) - 1):
                add = add + 0.01
                rentStrategys[i + 1]['rentMoney'] = int(rentStrategys[0]['rentMoney']) * (add + 1)

            HouseContractFour["houseContractFour"]["rentStrategys"] = rentStrategys
        else:
            HouseContractFour["houseContractFour"]["rentStrategys"] = HouseContractFour_02["rentStrategys"]

        # 委托合同第五页
        # 生成租金明细
        url = "http://erp.ishangzu.com/isz_finance/HouseContractPayableController/createContractPayable"
        data = {
            "contractId": "",
            'rentFreeType': self.rent_free_type,
            "firstPayDate": first_pay_date,
            "version": "V_THREE"}
        datas = {}
        datas["rentInfoList"] = HouseContractFour_02["rentStrategys"]
        data.update(datas)
        print(data)
        HouseContractFiveINFO = interface.myRequest(url, data)
        if HouseContractFiveINFO['code'] != 0:
            return HouseContractFiveINFO['msg']
        HouseContractFive={}
        HouseContractFive["houseContractFive"] = HouseContractFiveINFO["obj"]

        # # 获取委托合同类型
        # url = 'http://erp.ishangzu.com/isz_housecontract/houseContractController/calculationHouseContractType'
        # data = {
        #     "entrust_start_date": self.entrust_start_date,
        #     "fitment_start_date": self.entrust_start_date,
        #     "house_id":house_id ,
        #     "cardInfoVos": [{
        #         "card_type": "PASSPORT",
        #         "id_card": "55667788"
        #     }]
        # }

        # 委托合同五个页面参数合一起
        houseContract = {"is_e_visa":True}
        houseContract.update(HouseContractFrist)
        houseContract.update(HouseContractSecond)
        houseContract.update(HouseContractThird)
        houseContract.update(HouseContractFour)
        houseContract.update(HouseContractFive)

        print(houseContract)

        #生成预览的pdf
        url='http://erp.ishangzu.com/isz_housecontract/houseContractController/downloadPrePdf'
        result = interface.myRequest(url, houseContract)
        if result['code'] != 0:
            return result['msg']

        #保存erp电签委托合同
        url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/saveHouseContract"
        result = interface.myRequest(url, houseContract)
        if result['code'] != 0:
            base.consoleLog('新增委托合同erp电签接口执行失败！')
            return result['msg']
        base.consoleLog('新增委托合同erp电签接口执行成功！')
        return


    def add_renew_house_contract(self, contract_num):
        """
        续签委托合同
        :param contract_num:
        :return:
        """
        base.consoleLog('续签委托合同号。委托合同名称：' + contract_num)

        # 点击续签返回老合同的初始化数据
        url_1 = "http://erp.ishangzu.com/isz_housecontract/houseContractController/searchHouseContractInfoBase?"
        sql = "SELECT contract_type,house_id,contract_id from house_contract where contract_num = '%s' and deleted=0" % self.contract_num
        try:
            InfoBase = base.searchSQL(sql)[0]
        except BaseException as e:
            base.consoleLog("旧合同不存在,请重新输入!" + str(e), 'e')
            return str(e)

        url_2 = "contract_type=" + InfoBase[0] + "&house_id=" + InfoBase[1] + "&parent_id=" + InfoBase[2]
        url = url_1 + url_2
        result = interface.myRequest(url, method="get")
        if result['code'] != 0:
            return result['msg']
        if result['msg'] == "查询委托合同对应的上一份合同失败,原因：已续的合同不能续签.":
            return result['msg']
        else:
            ContractInfoBase = result['obj']

        null = None

        # 委托合同第一页
        houseContractFrist = {}
        houseContractFrist['houseContractFrist'] = ContractInfoBase['houseContractFrist']
        houseContractFrist['houseContractFrist']['contract_type_cn'] = "续签"
        houseContractFrist['houseContractFrist']['contract_type'] = "RENEWSIGN"

        # 委托合同第二页
        houseContractSecond = {}
        houseContractSecond["houseContractSecond"] = {
            "agreedRentOriginalStatements": [],
            "any_agent": "0",
            "assetsOfLessor": [{
                "landlord_name": "产权人姓名",
                "phone": "18279881085",
                "email": "zhonglinglong@aishangzu.com",
                "mailing_address": "通讯地址"
            }],
            "contract_id": null,
            "houseContractSign": {
                "address": "",
                "agent_type": "",
                "attachments": [],
                "card_type": "",
                "email": "",
                "id_card": "",
                "phone": "",
                "sign_name": ""
            },
            "is_new_data": "Y",
            "originalAgentDataRelations": [],
            "originalLessorHasDied": []
        }

        # 委托合同第三页
        attachment_id = houseContractFrist['houseContractFrist']['houseContractLandlord']['idCardPhotos'][0][
            "attachment_id"]
        contract_id = houseContractFrist['houseContractFrist']['houseContractLandlord']['idCardPhotos'][0][
            "contract_id"]
        img_id = houseContractFrist['houseContractFrist']['houseContractLandlord']['idCardPhotos'][0]['img_id']
        src = houseContractFrist['houseContractFrist']['houseContractLandlord']['idCardPhotos'][0]['src']
        houseContractThird = {}
        houseContractThird["houseContractThird"] = {
            "account_bank": "支行",
            "account_name": "产权人姓名",
            "account_num": "622848888888",
            "bank": "未知发卡银行",
            "contract_id": null,
            "is_new_data": "Y",
            "notPropertyOwnerGrantReceipts": [],
            "pay_object": "PERSONAL",
            "payeeIdPhotos": [{
                "attachment_id": attachment_id,
                "attachment_type": null,
                "attachment_type_name": "",
                "contract_id": contract_id,
                "contract_landlord_id": "",
                "create_dep": null,
                "create_time": null,
                "create_uid": null,
                "create_user": null,
                "deleted": null,
                "file_type_id": null,
                "img_id": img_id,
                "landlord_crad_no": null,
                "remark": "",
                "sort": 0,
                "src": src,
                "update_time": null,
                "update_uid": null
            }],
            "payee_card_type": "PASSPORT",
            "payee_card_type_cn": "",
            "payee_emergency_name": "紧急联系人姓名",
            "payee_emergency_phone": "15750935006",
            "payee_id_card": "55667788",
            "payee_type": "PROPERTYOWNER",
            "payee_type_cn": ""
        }

        # 委托合同第四页数据
        idCardPhotos = interface.upLoadPhoto(self.url, base.get_conf('Img', 'picture_name'),
                                             base.get_conf('Img', 'file_path'))  # 图片上传

        day_number = 390 * int(self.entrust_year) - 1  # 委托起算日至委托到期日天数
        self.entrust_end_date = str(
            datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') + datetime.timedelta(
                days=(day_number)))  # 委托结束日

        # 根据改造类型,设置了委托起算日。
        # 装修起算日,装修结束日,业主交房日,签约日期。
        if self.reform_way == 'OLDRESTYLE' or self.reform_way == 'BLANKRESTYLE':  # 老房全装 or 毛坯全装
            self.fitment_start_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=61))  # 装修起算日
            self.fitment_end_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=1))  # 装修结束日
            self.owner_sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=61))  # 业主交房日
            self.sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=61))  # 签约日期
        elif self.reform_way == 'RESTYLED':  # 大改
            self.fitment_start_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=31))
            self.fitment_end_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=1))
            self.owner_sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=31))
            self.sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=31))
        elif self.reform_way == 'RETROFITTING' or self.reform_way == 'REFORM':  # 小改 or 改造
            self.fitment_start_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=16))
            self.fitment_end_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=1))
            self.owner_sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=16))
            self.sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=16))
        elif self.reform_way == 'TINYCHANGE':  # 修配
            self.fitment_start_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=8))
            self.fitment_end_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=1))
            self.owner_sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=8))
            self.sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=8))
        elif self.reform_way == 'UNRRESTYLE':  # 不改造
            self.fitment_start_date = ""
            self.fitment_end_date = ""
            self.owner_sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=0))
            self.sign_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') - datetime.timedelta(days=0))

            day_number = 365 * int(self.entrust_year)
            self.entrust_end_date = str(
                datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d') + datetime.timedelta(
                    days=(day_number)))  # 委托结束日

        # 根据规则设置的签约日期大于当前时间时,需自动把签约日期设置成当前时间。
        if time.strptime(self.sign_date, "%Y-%m-%d %H:%M:%S") > time.strptime(base.now_time() + ' 00:00:00',
                                                                         "%Y-%m-%d %H:%M:%S"):
            self.sign_date = base.now_time()

        # 首次付款日
        first_pay_date = str(datetime.datetime.strptime(self.entrust_start_date, '%Y-%m-%d'))[0:7] + "-15"

        # 免租天数和付款方式关联
        if self.payment_cycle == 'MONTH':  # 月付
            self.free_days = 25
        elif self.payment_cycle == 'TOW_MONTH' or self.payment_cycle == 'SEASON' or self.payment_cycle == 'ALL':  # 二月付,季付,一次性付款
            self.free_days = 30
        elif self.payment_cycle == 'HALF_YEAR':  # 半年付
            self.free_days = 40
        elif self.payment_cycle == 'ONE_YEAR':  # 半年付
            self.free_days = 50

        # 房屋渠道来源
        house_id = ContractInfoBase["houseContractFour"]["house_id"]
        url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/searchHouseContractInfoBase?contract_type=NEWSIGN&house_id=" + house_id
        result = interface.myRequest(url, method="get")["obj"]

        house_source = result["houseContractFour"]["house_source"]

        area_code = ContractInfoBase["houseContractFour"]["area_code"]
        building_id = ContractInfoBase["houseContractFour"]["building_id"]
        city_code = ContractInfoBase["houseContractFour"]["city_code"]
        residential_id = ContractInfoBase["houseContractFour"]["residential_id"]
        sign_dep_name = base.get_conf("loginUser", "sign_dep_name")
        sign_did = base.get_conf("loginUser", "dep_id")
        sign_uid = base.get_conf("loginUser", "user_id")
        sign_user_name = base.get_conf("loginUser", "user_name")
        parent_id = contract_id

        # 服务费系数
        url_self = 'http://erp.ishangzu.com/isz_housecontract/houseContractController/getHouseContractServiceFactor?'
        url_at = 'apartment_type=' + self.apartment_type
        url_cc = '&city_code=' + city_code
        url_ct = '&contract_type=NEWSIGN&sign_date='
        url = url_self + url_at + url_cc + url_ct + self.sign_date[0:10]
        freeFactor = interface.myRequest(url, method='get')['obj']['freeFactor']

        self.contract_num = contract_num  # 初始化对象的合同名称，方便审核调用
        if self.entrust_type == 'ENTIRE':
            entrust_type_cn = '整租'
        else:
            entrust_type_cn = '合租'

        houseContractFour = {}
        houseContractFour["houseContractFour"] = {
            "apartment_type": self.apartment_type,
            "apartment_type_cn": "",
            "area_code": area_code,
            "audit_status": null,
            "audit_time": null,
            "audit_uid": null,
            "building_id": building_id,
            "can_update_channel_fee": True,
            "channelFeeServiceFactors": [],
            "channel_fee": 0,
            "channel_pay_type": null,
            "city_code": city_code,
            "contractAttachments": [],
            "contract_id": null,
            "contract_num": self.contract_num,
            "contract_status": null,
            "contract_type": "RENEWSIGN",
            "contract_type_cn": "续签",
            # "delay_date": delay_date,
            "electron_file_src": null,
            "energy_company": null,
            "energy_fee": null,
            "entrust_end_date": self.entrust_end_date,
            "entrust_start_date": self.entrust_start_date,
            "entrust_type": self.entrust_type,
            "entrust_type_cn": entrust_type_cn,
            "entrust_year": self.entrust_year,
            "entrust_year_cn": "",
            "first_pay_date": first_pay_date,
            "fitment_end_date": self.fitment_end_date,
            "fitment_start_date": self.fitment_start_date,
            "freeType": null,
            "freeType_cn": "",
            "free_days": self.free_days,
            "free_end_date": null,
            "free_start_date": null,
            "have_parking": "N",
            "houseContractPDFs": null,
            "house_id": house_id,
            "house_source": house_source,
            "housekeep_mange_dep": null,
            "housekeep_mange_dep_user": "-",
            "housekeep_mange_did": null,
            "housekeep_mange_uid": null,
            "housekeep_mange_user_name": null,
            "is_electron": null,
            "is_new_data": "Y",
            "owner_sign_date": self.owner_sign_date,
            "parent_id": parent_id,
            "parking": "",
            "payment_cycle": self.payment_cycle,
            "payment_cycle_cn": "",
            "property": null,
            "property_company": null,
            "reform_way": self.reform_way,
            "reform_way_cn": "",
            "remark": null,
            "rentMoney": self.rentMoney,
            "rental_price": self.rentMoney,
            "reset_finance": False,
            "residential_id": residential_id,
            "server_manage_dep_user": "",
            "server_manage_did": null,
            "server_manage_did_name": null,
            "server_manage_uid": null,
            "server_manage_uid_name": null,
            "service_fee_factor": freeFactor,
            "sign_body": self.sign_body,
            "sign_date": self.sign_date,
            "sign_dep_name": sign_dep_name,
            "sign_did": sign_did,
            "sign_uid": sign_uid,
            "sign_user_name": sign_user_name,
            "year_service_fee": null
        }

        # 生成租金策略
        url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/getHouseRentStrategyVo"
        data = {
            "apartment_type": self.apartment_type,
            "contract_type": "RENEWSIGN",
            "entrust_start_date": self.entrust_start_date,
            "entrust_end_date": self.entrust_end_date,
            "free_end_date": "",
            "free_start_date": "",
            "parking": "",
            "payment_cycle": self.payment_cycle,
            "rent_money": self.rentMoney,
            "sign_date": self.sign_date,
            "city_code": city_code,
            "entrust_year": self.entrust_year,
            "free_days": self.free_days,
            "version": "V_THREE"}
        HouseContractFour_02 = interface.myRequest(url, data)
        if HouseContractFour_02['code'] != 0:
            return HouseContractFour_02['msg']
        HouseContractFour_02["rentStrategys"] = HouseContractFour_02["obj"]
        # 如果租金策略为false：self.rent_strategy  生成不一样的租金策略
        if not self.rent_strategy:
            add = 0.01
            rentStrategys = HouseContractFour_02["rentStrategys"]
            for i in range(len(rentStrategys) - 1):
                add = add + 0.01
                rentStrategys[i + 1]['rentMoney'] = int(rentStrategys[0]['rentMoney']) * add
            houseContractFour["houseContractFour"]["rentStrategys"] = rentStrategys
        else:
            houseContractFour["houseContractFour"]["rentStrategys"] = HouseContractFour_02["rentStrategys"]


        # 委托合同第五页
        # 生成租金明细
        url = "http://erp.ishangzu.com/isz_finance/HouseContractPayableController/createContractPayable"
        data = {
            "contractId": "",
            'rentFreeType': self.rent_free_type,
            "firstPayDate": first_pay_date,
            "version": "V_THREE"}
        datas = {}
        datas["rentInfoList"] = HouseContractFour_02["rentStrategys"]
        data.update(datas)
        houseContractFive = interface.myRequest(url, data)
        if houseContractFive['code'] != 0:
            return houseContractFive['msg']
        houseContractFive["houseContractFive"] = houseContractFive["obj"]

        #五个页面的数据
        houseContract = {}
        houseContract.update(houseContractFrist)
        houseContract.update(houseContractSecond)
        houseContract.update(houseContractThird)
        houseContract.update(houseContractFour)
        houseContract.update(houseContractFive)

        # 续签委托合同
        url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/saveHouseContract"
        result = interface.myRequest(url, houseContract)
        if result['code'] != 0:
            base.consoleLog('续签委托合同接口执行失败！')
            return result['msg']
        base.consoleLog('续签委任合同接口执行成功！')
        return

    def reviewed_house_contract(self, value=True):
        """
        初审，复审委托合同
        :return:
        """
        base.consoleLog('委托合同审核。委托合同号：' + self.contract_num)

        # 委托合同详情
        try:
            sql = "select contract_id from house_contract where contract_num = '%s'" % self.contract_num
            self.contract_id = base.searchSQL(sql)[0][0]
        except BaseException as e:
            base.consoleLog('sql执行报错。sql' + sql + ' 报错信息：' + str(e), 'e')
            return str(e)

        url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/searchHouseContractInfo/" + self.contract_id
        details = interface.myRequest(url, method="get")
        if details['code'] != 0:
            return details['msg']
        details = details["obj"]

        # 初审第一个页面
        try:
            sql = "SELECT house_id,entrust_type from house_contract where contract_id='%s'" % self.contract_id
            house_id_entrust_type = base.searchSQL(sql)
        except BaseException as e:
            base.consoleLog('sql执行报错。sql' + sql + ' 报错信息：' + str(e), 'e')
            return str(e)

        url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/saveOrUpdateHouseContractDetailByPart"
        houseContractFrist = {}
        houseContractFrist["houseContractFrist"] = details["houseContractFrist"]
        houseContractFrist["entrust_type"] = house_id_entrust_type[0][1]
        houseContractFrist["house_id"] = house_id_entrust_type[0][0]

        data = {
            "auditForm": {
                "audit_status": "PASS",
                "content": "同意!"
            },
            "action_type": "AUDIT",
            "save_part": "ONE",
            "contract_id": self.contract_id
        }
        data.update(houseContractFrist)
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            return result['msg']

        # ###复审第一页

        # url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/saveOrUpdateHouseContractDetailByPart"
        # data = {
        #     "auditForm": {
        #         "audit_status": "APPROVED",
        #         "content": "同意!"
        #     },
        #     "action_type": "AUDIT",
        #     "save_part": "ONE",
        #     "contract_id": self.contract_id
        # }
        # data.update(houseContractFrist)
        # result = interface.myRequest(url, data)
        # if result['code'] != 0:
        #     return result['msg']

        # 初审第二个页面
        data = {
            "auditForm": {
                "audit_status": "PASS",
                "content": "同意!"
            },
            "action_type": "AUDIT",
            "save_part": "TWO",
            "contract_id": self.contract_id
        }
        data["houseContractSecond"] = details["houseContractSecond"]
        result = interface.myRequest(url, data)
        if result['code']:
            return result['msg']

        # 复审审第二个页面
        # data = {
        #     "auditForm": {
        #         "audit_status": "APPROVED",
        #         "content": "同意!"
        #     },
        #     "action_type": "AUDIT",
        #     "save_part": "TWO",
        #     "contract_id": self.contract_id
        # }
        # data["houseContractSecond"] = details["houseContractSecond"]
        # result = interface.myRequest(url, data)
        # if result['code'] != 0:
        #     return result['msg']

        # 初审第三个页面
        data = {
            "auditForm": {
                "audit_status": "PASS",
                "content": "同意!"
            },
            "action_type": "AUDIT",
            "save_part": "THREE",
            "contract_id": self.contract_id}
        data["houseContractThird"] = details["houseContractThird"]
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            return result['msg']

        # 复审第三个页面
        # data = {
        #     "auditForm": {
        #         "audit_status": "APPROVED",
        #         "content": "同意!"
        #     },
        #     "action_type": "AUDIT",
        #     "save_part": "THREE",
        #     "contract_id": self.contract_id}
        # data["houseContractThird"] = details["houseContractThird"]
        # result = interface.myRequest(url, data)
        # if result['code'] != 0:
        #     return result['msg']

        # 初审第四个页面
        data = {
            "auditForm": {
                "audit_status": "PASS",
                "content": "同意!"
            },
            "action_type": "AUDIT",
            "save_part": "FOUR",
            "contract_id": self.contract_id}
        data["houseContractFour"] = details["houseContractFour"]
        result = interface.myRequest(url, data)
        if result['code']:
            return result['msg']

        # 复审第四个页面
        # data = {
        #     "auditForm": {
        #         "audit_status": "APPROVED",
        #         "content": "同意!"
        #     },
        #     "action_type": "AUDIT",
        #     "save_part": "FOUR",
        #     "contract_id": self.contract_id}
        # data["houseContractFour"] = details["houseContractFour"]
        # result = interface.myRequest(url, data)
        # if result['code'] != 0:
        #     return result['msg']

        # 租金审核
        # 委托合同应付列表获取应付id
        url = "http://erp.ishangzu.com/isz_finance/HouseContractPayableController/getPayablesByContract/" + self.contract_id
        payable = interface.myRequest(url, method="get")
        if payable['code'] != 0:
            return payable['msg']
        payable = payable["obj"]

        payableId = []
        for i in range(len(payable)):
            payableId.append(payable[i]['payable_id'])

        url = "http://erp.ishangzu.com/isz_finance/HouseContractPayableController/updatePayableAuditStatusById"
        data = {
            "audit_status": "AUDITED",
            "payableIds": payableId}
        result = interface.myRequest(url, data, method="put")
        if result['code'] != 0:
            return result['msg']

        # 复审完结
        url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/houseContractAudit"
        if value:
            data = {"audit_status":"PASS","content":"合同内容、资料、备件无误，正常审核通过。同意!","is_normal_approved":"0","contract_id":self.contract_id}
        else:
            data = {"audit_status": "APPROVED", "content": "合同无法正常履约，需终止，策略性复审。同意!", "contract_id": self.contract_id,
                    "is_normal_approved": "1"}

        result = interface.myRequest(url, data, method="put")
        if result['code'] != 0:
            base.consoleLog('委托合同审核接口执行失败！')
            return result['msg']
        base.consoleLog('委托合同审核接口执行成功！')
        return

    def fanshen_house_contract(self):
        """
        反审委托合同
        :return:
        """

        base.consoleLog('反审委托合同。合同号：' + self.contract_num)

        try:
            sql = "select contract_id from house_contract where contract_num = '%s'" % self.contract_num
            self.contract_id = base.searchSQL(sql)[0][0]
        except BaseException as e:
            base.consoleLog('sql执行报错。sql' + sql + ' 报错信息：' + str(e), 'e')
            return str(e)

        #反审委托合同,只需带第一个页面的内容。
        url = 'http://erp.ishangzu.com/isz_housecontract/houseContractController/saveOrUpdateHouseContractDetailByPart'
        data = {
            "auditForm": {
                "audit_status": "REAUDIT",
                "content": "测试"
            },
            "action_type": "AUDIT",
            "save_part": "ONE",
            "contract_id": self.contract_id
        }

        self.house_contract_info()
        data.update(self.dic['houseContractFrist'])

        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('委托合同反审接口执行失败！')
            return result['msg']
        base.consoleLog('委托合同反审接口执行成功！')
        return

    def house_contract_end(self, end_type, end_date=base.now_time()):
        """
        委托合同终止结算
        :param contract_num:委托合同号
        :param end_type:终止类似，正退，公司违约，业主违约
        :param end_date:终止日期
        :return:
        """
        base.consoleLog('委托合同终止结算。委托合同号：' + self.contract_num)

        null = None
        idCardPhotos = interface.upLoadPhoto(self.url, base.get_conf('Img', 'picture_name'),
                                             base.get_conf('Img', 'file_path'))

        try:
            sql = "select contract_id from house_contract where contract_num = '%s'" % self.contract_num
            self.contract_id = base.searchSQL(sql)[0][0]
        except BaseException as e:
            base.consoleLog('查询SQL报错。sql:' + sql + '  报错信息：' + str(e), 'e')
            return str(e)

        # 委托合同终止基础数值
        url = "http://erp.ishangzu.com/isz_housecontract/houseContractEndController/searchHouseContractEndMsg/" + self.contract_id
        house_contract_list = interface.myRequest(url, method="get")
        if house_contract_list['code'] != 0:
            return house_contract_list['msg']
        house_contract_list = house_contract_list["obj"]

        # 提交委托合同终止结算
        url = "http://erp.ishangzu.com/isz_housecontract/houseContractEndController/saveHouseContractEnd"
        data = {
            "achieve_audit_status": null,
            "address": house_contract_list["address"],
            "apartment_type": null,
            "audit_status": null,
            "audit_time": null,
            "audit_uid": null,
            "bank": null,
            "building_name": house_contract_list["building_name"],
            "company_no": "还款公司",
            "complement_status": null,
            "complete_money": null,
            "complete_remark": null,
            "complete_time": null,
            "contractImgList": [{
                "src": idCardPhotos["src"],
                "url": idCardPhotos["src"],
                "type": "",
                "img_id": idCardPhotos["img_id"]
            }],
            "contract_id": house_contract_list["contract_id"],
            "contract_num": house_contract_list["contract_num"],
            "create_time": null,
            "create_uid": null,
            "deleted": null,
            "delivery_code": null,
            "dids": null,
            "end_balance_type": null,
            "end_contract_num": "终止合同号" + base.random_name()[14:18],
            "end_dName": house_contract_list["end_dName"],
            "end_date":end_date + " 00:00:00",
            "end_dep_name": null,
            "end_did": house_contract_list["end_did"],
            "end_id": null,
            "end_reason": null,
            "end_type": base.get_conf("contract_end", end_type),
            "end_uName": house_contract_list["end_uName"],
            "end_uid": house_contract_list["end_uid"],
            "end_user_name": null,
            "entrust_end_date": house_contract_list["entrust_end_date"],
            "entrust_start_date": house_contract_list["entrust_start_date"],
            "entrust_type": null,
            "financial_provide_money": null,
            "fitment_charge": house_contract_list["fitment_charge"],
            "fitment_charge_remark": "装修扣款备注",
            "floor": house_contract_list["floor"],
            "houseContractEndReturnList": [],
            "house_code": house_contract_list["house_code"],
            "house_id": house_contract_list["house_id"],
            "house_no": house_contract_list["house_no"],
            "landlord_name": house_contract_list["landlord_name"],
            "no_charge": house_contract_list["no_charge"],
            "no_charge_remark": "未扣款项备注",
            "other": house_contract_list["other"],
            "other_remark": "其他备注",
            "pay_bank": "测试",
            "pay_bank_no": "6228448151615",
            "pay_emp_bank_location": null,
            "pay_emp_bank_no": null,
            "pay_emp_name": null,
            "pay_name": "测试",
            "pay_object": "PERSONAL",
            "pay_owner": null,
            "pay_owner_bank_location": null,
            "pay_owner_bank_no": null,
            "pay_type": "OWNER",
            "payable_date": end_date + " 00:00:00",
            "payable_totle": null,
            "payerType": null,
            "penalty": '10000',
            "penalty_remark": "违约金赔入备注",
            "real_due_date": null,
            "receipt_bank_location": null,
            "receipt_bank_no": null,
            "receipt_name": null,
            "receivable_date": end_date + " 00:00:00",
            "receivable_total": '10000',
            "remark": "终止结算备注",
            "repair_charge": house_contract_list["repair_charge"],
            "repair_charge_remark": null,
            "residential_name": house_contract_list["residential_name"],
            "return_company": null,
            "return_emp_name": null,
            "return_rent": house_contract_list["return_rent"],
            "return_rent_remark": "返还房租备注",
            "server_manage_did": null,
            "server_manage_uid": null,
            "sign_body": house_contract_list["sign_body"],
            "sign_body_en": house_contract_list["sign_body_en"],
            "sign_dep_name": house_contract_list["sign_dep_name"],
            "sign_did": null,
            "sign_name": house_contract_list["sign_name"],
            "sign_uid": null,
            "submit_audit_time": null,
            "submit_audit_uid": null,
            "suffix": null,
            "uids": null,
            "unit": house_contract_list["unit"],
            "update_time": null,
            "update_uid": null,
            "user_name": null}

        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('委托合同提交终止结算接口执行失败！')
            return result['msg']
        base.consoleLog('委托合同提交终止结算接口执行成功！')
        return

    def reviewed_house_contract_end(self, value=True):
        """
        复审委托合同终止结算
        :param value:
        :return:
        """
        base.consoleLog('复审委托合同终止结算。委托合同号：' + self.contract_num)

        try:
            sql = "select end_id from house_contract_end where contract_id = (select contract_id from house_contract where contract_num = '%s')" % self.contract_num
            end_id = base.searchSQL(sql)[0][0]
        except BaseException as e:
            base.consoleLog('查询SQL报错。sql:' + sql + '  报错信息：' + str(e), 'e')
            return str(e)

        # 初审
        url = "http://isz.ishangzu.com/isz_contract/endAgreementControl/houseContractEndAudit.action"
        data = {
            "achieveid": end_id,
            "activityId": "18",
            "content": "同意"}
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            return result['msg']

        if not value:
            base.consoleLog('委托合同终止结算初审接口执行完成。')
            return

        # 复审
        url = "http://isz.ishangzu.com/isz_contract/endAgreementControl/houseContractEndAudit.action"
        data = {
            "achieveid": end_id,
            "activityId": "19",
            "content": "同意"}
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('委托合同终止结算审核接口执行失败！')
            return result['msg']
        base.consoleLog('委托合同终止结算审核接口执行成功！')
        return

    def house_contract_info(self):
        """
        委托合同详情
        :return:
        """
        base.consoleLog('查询委托合同详情。委托合同号：' + self.contract_num)

        try:
            sql = "select contract_id from house_contract where contract_num = '%s'" % self.contract_num
            self.contract_id = base.searchSQL(sql)[0][0]
        except BaseException as e:
            base.consoleLog('查询SQL报错。sql:' + sql + '  报错信息：' + str(e), 'e')
            return str(e)

        url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/searchHouseContractInfo/" + self.contract_id
        details = interface.myRequest(url, method="get")
        if details['code'] != 0:
            base.consoleLog('查询委托合同详情接口执行失败！')
            return details['msg']
        details = details["obj"]
        base.consoleLog('查询委托合同详情接口执行成功！')

        self.dic = {}
        self.dic['houseContractFive'] = details['houseContractFive']
        self.dic['houseContractFour'] = details['houseContractFour']
        self.dic['houseContractThird'] = details['houseContractThird']
        self.dic['houseContractSecond'] = details['houseContractSecond']
        self.dic['houseContractFrist'] = details['houseContractFrist']
        self.dic['houseContractSixth'] = details['houseContractSixth']
        return json.dumps(self.dic)

    def update_house_contract_four(self, houseContractfour):
        """
        修改委托合同第4个页签
        :param houseContractFour: 保存的参数
        :return:
        """
        base.consoleLog('修改委托合同第4个页面。合同号：' + self.contract_num)
        urlz = 'http://erp.ishangzu.com/isz_housecontract/houseContractController/saveOrUpdateHouseContractDetailByPart'

        houseContractFour = {}
        houseContractFour['houseContractFour'] = houseContractfour
        houseContractFour["action_type"] = "UPDATE"
        houseContractFour["save_part"] = "FOUR"
        houseContractFour["contract_id"] = houseContractfour["contract_id"]

        # 生成租金策略
        url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/getHouseRentStrategyVo"
        data = {
            "apartment_type": self.apartment_type,
            "contract_type": "NEWSIGN",
            "entrust_start_date": self.entrust_start_date,
            "entrust_end_date": self.entrust_end_date,
            "free_end_date": "",
            "free_start_date": '',
            "parking": "",
            "payment_cycle": self.payment_cycle,
            "rent_money": self.rentMoney,
            "sign_date": self.sign_date,
            "city_code": self.city_code,
            "entrust_year": self.entrust_year,
            "free_days": self.free_days,
            "version": "V_THREE"}
        rentStrategys = interface.myRequest(url, data)['obj']
        houseContractFour["houseContractFour"]["fitment_start_date"] = self.entrust_start_date
        houseContractFour["houseContractFour"]["fitment_end_date"] = houseContractFour["houseContractFour"]["fitment_end_date"] + " 00:00:00"
        houseContractFour["houseContractFour"]["rentStrategys"] = rentStrategys

        result = interface.myRequest(urlz, houseContractFour)
        if result['code'] != 0:
            base.consoleLog('修改委托合同第4个页签接口执行失败！')
            return result['msg']
        base.consoleLog('修改委托合同第4个页签接口执行成功！')

        return

    def delete_house_contract(self):
        """
        删除委托合同
        :return:
        """
        base.consoleLog("删除委托合同。委托合同号：" + self.contract_num)

        try:
            sql = "select contract_id from house_contract where contract_num = '%s'" % self.contract_num
            self.contract_id = base.searchSQL(sql)[0][0]
        except BaseException as e:
            base.consoleLog('查询SQL报错。sql:' + sql + '  报错信息：' + str(e), 'e')
            return str(e)

        url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/deletedHouseContractById/" + self.contract_id

        result = interface.myRequest(url, method='delete')
        if result['code'] == 0:
            base.consoleLog("删除委托合同接口执行完成！")
            return
        else:
            return result

    def deleted_house_contract_end(self):
        """
        删除委托合同终止结算
        :return:
        """
        base.consoleLog('删除委托合同终止结算。委托合同号：' + self.contract_num)

        try:
            sql = "select contract_id from house_contract where contract_num = '%s'" % self.contract_num
            self.contract_id = base.searchSQL(sql)[0][0]
        except BaseException as e:
            base.consoleLog('查询SQL报错。sql:' + sql + '  报错信息：' + str(e), 'e')
            return str(e)

        sql = 'SELECT end_id from house_contract_end where contract_id = "%s"' %  self.contract_id
        end_id = base.searchSQL()[0][0]

        url = 'http://isz.ishangzu.com/isz_contract/endAgreementControl/deleteHouseContractEnd.action'
        data = {'end_id': end_id}

        result = interface.myRequest(url,data)
        if result['code'] == 0:
            base.consoleLog('委托合同终止结算删除接口执行成功！')
            return
        else:
            base.consoleLog(result['msg'],level='e')

    def update_sign_uid(self, phone='18824321245'):
        """
        资源划转修改委托合同签约人
        :param:phone  账号
        :return:
        """
        base.consoleLog('委托合同资源划转。划转到账号：' + phone)

        try:
            sql = "select contract_id from house_contract where contract_num = '%s'" % self.contract_num
            self.contract_id = base.searchSQL(sql)[0][0]
        except BaseException as e:
            base.consoleLog('sql执行报错。sql' + sql + ' 报错信息：' + str(e), 'e')
            return str(e)

        sql = "SELECT user_id,user_name,dep_id from sys_user where user_phone='%s';" % phone
        user_data = base.search_sql(sql)

        sql = "SELECT dep_name from sys_department where dep_id ='%s';" % user_data[0][2]
        dep_name = base.search_sql(sql)[0][0]

        url = 'http://erp.ishangzu.com/isz_housecontract/houseContractController/batchUpdateSign'
        data = {
            "contract_ids": [self.contract_id],
            "sign_did":user_data[0][2],
            "sign_did_name":dep_name,
            "sign_uid": user_data[0][0],
            "sign_uid_name": user_data[0][1]}

        result = interface.myRequest(url,data,method='put')
        if result['code'] == 0:
            base.consoleLog('委托合同签约人修改接口执行成功！')
        else:
            base.consoleLog('委托合同签约人修改接口执行失败！'+result['msg'],level='e')
            return result['msg']
        return


#print(HouseContract(contract_num='测试2332').house_contract_info())