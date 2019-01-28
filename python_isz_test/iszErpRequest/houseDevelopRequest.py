# -*- coding:utf8 -*-
"""
2018年5月26日17:12:19
开发房源接口
"""


__auto__ = 'zhonglinglong'

from classDemo.myRequest import NewRequest
from common import base
from iszErpRequest import residentialRequest
from iszErpRequest import loginRequest

class HouseDelelop:
    """开发房源类"""

    def __init__(self,residential_name,source='转介绍',room_number=1):
        """
        初始化开发房源对象值
        :param residential_name: 楼盘名称
        :param room_number: 新增房间数量
        :param source: 房屋来源
        """
        self.residential_name = residential_name
        self.room_number = room_number
        self.source = base.get_conf('house',source)


    def add_house_delelop(self,value=True):
        """
        新增并审核开发自营房源
        :return:
        """
        base.consoleLog('新增并审核开发自营房源。')
        null = None


        # 查询楼盘所有房间id
        try:
            sql = """SELECT
                        house_no_id
                    FROM
                        residential_building_house_no
                    WHERE
                        floor_id IN (
                            SELECT
                                floor_id
                            FROM
                                residential_building_floor
                            WHERE
                                unit_id IN (
                                    SELECT
                                        unit_id
                                    FROM
                                        residential_building_unit
                                    WHERE
                                        building_id IN (
                                            SELECT
                                                building_id
                                            FROM
                                                residential_building
                                            WHERE
                                                residential_id IN (
                                                    SELECT
                                                        residential_id
                                                    FROM
                                                        residential
                                                    WHERE
                                                        residential_name = "%s"
                                                )
                                        )
                                )
                        ) and used = 'N';""" % self.residential_name
            new_house_no_id_list = base.searchSQL(sql)
        except BaseException as e:
            base.consoleLog('查询SQL报错。sql:' + sql + '  报错信息：' + str(e), 'e')
            return str(e)

        try:
            sql = "select residential_id from residential where residential_name = '%s' and deleted = 0" % self.residential_name
            residential_id = base.searchSQL(sql)[0][0]
        except BaseException as e:
            base.consoleLog('查询SQL报错。sql:' + sql + '  报错信息：' + str(e), 'e')
            return str(e)

        house_no_id_list = []
        for i in range(len(new_house_no_id_list)):
            house_no_id_list.append(new_house_no_id_list[i][0])


        # 查询楼盘信息
        residential = residentialRequest.ResidentialInfo(residential_id).select_residential_detail_request()
        area_code = residential["area_code"]
        area_name = residential["area_name"]
        city_code = residential["city_code"]
        city_name = residential["city_name"]
        residential_id = residential["residential_id"]
        byname = residential["byname"]
        business_circle_name = residential["taBusinessCircleList"][0]["business_circle_name"]
        business_circle_id = residential["taBusinessCircleList"][0]["business_circle_id"]
        address = residential["address"]

        #新增审核房源
        for i in range(int(self.room_number)):
            #新增房源
            url = "http://isz.ishangzu.com/isz_house/HouseController/saveHouseDevelop.action"

            try:
                sql = """SELECT
                building_id,
                unit_id,
                floor_id,
                house_no,
                rooms,
                livings,
                kitchens,
                bathrooms,
                balconys
                FROM
                residential_building_house_no
                WHERE
                house_no_id = '%s' """ % house_no_id_list[i]
                data_list = base.searchSQL(sql)[0]
                sql = "select building_name from residential_building where building_id = '%s'" % data_list[0]
                building_name = base.searchSQL(sql)[0][0]
                sql = "select unit_name from residential_building_unit where unit_id = '%s'" % data_list[1]
                unit_name = base.searchSQL(sql)[0][0]
                sql = "select floor_name from residential_building_floor where floor_id = '%s'" % data_list[2]
                floor_name = base.searchSQL(sql)[0][0]
            except BaseException as e:
                base.consoleLog('查询SQL报错。sql:' + sql + '  报错信息：' + str(e), 'e')
                return str(e)

            data = {
                "residential_name_search": residential_id,
                "building_name_search": data_list[0],
                "unit_search": data_list[1],
                "house_no_search": house_no_id_list[i],
                "residential_name": self.residential_name + "（" + byname + "）",
                "building_name": building_name,
                "unit": unit_name,
                "floor": floor_name,
                "house_no": data_list[3],
                "residential_address": city_name + " " + area_name + " " + business_circle_name + " " + address,
                "city_code": city_code,
                "area_code": area_code,
                "business_circle_id": business_circle_id,
                "contact": "联系人",
                "did": base.get_conf("loginUser", "dep_id"),
                "uid": base.get_conf("loginUser", "user_id"),
                "house_status": "WAITING_RENT",
                "category": "NOLIMIT",
                "source": self.source,
                "rental_price": "5000.00",
                "rooms": data_list[4],
                "livings": data_list[5],
                "kitchens": data_list[6],
                "bathrooms": data_list[7],
                "balconys": data_list[8],
                "build_area": "100",
                "orientation": "NORTH",
                "property_type": "HIGH_LIFE",
                "property_use": "HOUSE",
                "fitment_type": "FITMENT_ROUGH",
                "remark": "备注",
                "look_type": "DIRECTION",
                "residential_id": residential_id,
                "building_id": data_list[0],
                "unit_id": data_list[1],
                "floor_id": data_list[2],
                "house_no_id": house_no_id_list[i],
                "business_circle_name": business_circle_name,
                "contact_tel": base.get_conf('loginUser','user')}
            base.consoleLog('新增房源。物业地址：' + self.residential_name + building_name + unit_name + floor_name + data_list[3] )
            result = NewRequest(url, data).post()
            if result['code'] != 0:
                base.consoleLog('新增房源接口提交失败！房源信息：' + self.residential_name + building_name + unit_name + floor_name + data_list[3])

            #审核房源
            url = "http://erp.ishangzu.com/isz_house/HouseController/selectHouseDevelopDetail.action"

            try:
                sql = "select house_develop_id from house_develop where residential_name like '%s' ORDER BY create_time desc limit 1" % (self.residential_name + "%")
                house_develop_id = base.searchSQL(sql)
            except BaseException as e:
                base.consoleLog('查询SQL报错。sql:' + sql + '  报错信息：' + str(e), 'e')
                return str(e)

            #获取房源信息
            data = {"house_develop_id": house_develop_id[0][0]}
            house_develop = NewRequest(url, data).post()

            if house_develop['code'] != 0:
                base.consoleLog('获取房源信息失败。信息：' + self.residential_name + building_name + unit_name + floor_name + data_list[3])
            house_develop = house_develop["obj"]

            balconys = house_develop["balconys"]
            bathrooms = house_develop["bathrooms"]
            build_area = house_develop["build_area"]
            building_id = house_develop["building_id"]
            building_name = house_develop["building_name"]
            floor_id = house_develop["floor_id"]
            floor = house_develop["floor"]
            house_no = house_develop["house_no"]
            house_no_id = house_develop["house_no_id"]
            kitchens = house_develop["kitchens"]
            livings = house_develop["livings"]
            residential_dep_id = house_develop["residential_dep_id"]
            residential_id = house_develop["residential_id"]
            residential_names = house_develop["residential_name"]
            unit = house_develop["unit"]
            unit_id = house_develop["unit_id"]
            update_time = house_develop["update_time"]

            url = "http://erp.ishangzu.com/isz_house/HouseController/auditHouseDevelop.action"
            data = {
                "area_code": area_code,
                "audit_content": "Agree",
                "audit_status": "PASS",
                "balconys": balconys,
                "bathrooms": bathrooms,
                "build_area": build_area,
                "building_id": building_id,
                "building_name": building_name,
                "building_name_search": building_id,
                "category": "NOLIMIT",
                "city_code": city_code,
                "fitment_type": "FITMENT_ROUGH",
                "floor": floor,
                "floor_id": floor_id,
                "houseRent": {
                    "category": "NOLIMIT",
                    "house_status": "WAITING_RENT",
                    "look_date": null,
                    "look_type": "DIRECTION",
                    "rental_price": 5000,
                    "source": self.source
                },
                "house_develop_id": house_develop_id[0][0],
                "house_no": house_no,
                "house_no_id": house_no_id,
                "house_no_search": house_no_id,
                "house_no_suffix": null,
                "house_status": "WAITING_RENT",
                "kitchens": kitchens,
                "livings": livings,
                "look_date": null,
                "look_type": "DIRECTION",
                "orientation": "NORTH",
                "property_use": "HOUSE",
                "property_type": "HIGH_LIFE",
                "rental_price": 5000,
                "residential_address": city_name + " " + area_name + " " + business_circle_name + " " + address,
                "residential_department_did": residential_dep_id,
                "residential_id": residential_id,
                "residential_name": residential_names,
                "residential_name_search": residential_id,
                "remark": "test",
                "rooms": 1,
                "source": "MIDDLEMEN",
                "unit": unit,
                "unit_id": unit_id,
                "unit_search": unit_id,
                "update_time": update_time}
            base.consoleLog('审核房源。物业地址：' + self.residential_name + building_name + unit_name + floor_name + house_no )
            if value:
                result = NewRequest(url, data).post()
                if result['code'] != 0:
                    base.consoleLog('审核房源接口执行失败！信息：' + self.residential_name + building_name + unit_name + floor_name + data_list[3])

        return





