# -*- coding:utf8 -*-

"""
楼盘模块接口
2018年5月26日14:33:54
"""

__auto__ = 'zhonglinglong'

from classDemo.myRequest import NewRequest
from common import base
from  iszErpRequest import loginRequest



class Residential():
    def __init__(self,residential_name,building_name,unit_name,floor_name,house_no,house_no_number):
        """
        初始化Residential对象的值
        :param residential_name:楼盘名称
        :param building_name: 栋座名称
        :param unit_name: 单元名称
        :param floor_name:楼层名称
        :param house_no:房间名称
        :param house_no_number:
        """
        self.residential_name = residential_name
        self.building_name = building_name
        self.unit_name = unit_name
        self.floor_name = floor_name
        self.house_no = house_no
        self.house_no_number = house_no_number

        # try:
        #     sql = """SELECT
        #                 residential_id
        #             FROM
        #                 residential
        #             WHERE
        #                 residential_name = '%s'
        #             AND deleted = 0
        #             ORDER BY
        #                 create_time DESC LIMIT 1 """ % self.residential_name
        #     self.residential_id = base.searchSQL(sql)[0][0]
        # except:
        #     base.consoleLog('不存在名称是' + self.residential_name + '的楼盘，请先创建！','e')
        #
        #
        # try:
        #     sql = """SELECT
        #                 building_id
        #             FROM
        #                 residential_building
        #             WHERE
        #                 residential_id = '%s'
        #             AND deleted = 0
        #             ORDER BY
        #                 create_time DESC
        #             LIMIT 1""" % self.residential_id
        #     self.building_id = base.searchSQL(sql)[0][0]
        # except:
        #     base.consoleLog('不存在名称是' + self.building_name + '的栋座，请先创建！','e')
        #
        # try:
        #     sql = """SELECT
        #                 unit_id
        #             FROM
        #                 residential_building_unit
        #             WHERE
        #                 building_id = '%s'
        #             ORDER BY
        #                 create_time DESC
        #             LIMIT 1""" % self.building_id
        #     self.unit_id = base.searchSQL(sql)[0][0]
        # except:
        #     base.consoleLog('不存在名称是' + self.building_name + '的栋座，请先创建！','e')


    def add_residential(self):
        """
        新增楼盘
        :param residential_name:楼盘名称
        :return:
        """
        base.consoleLog('新增楼盘。楼盘名称：' + self.residential_name)

        try:
            sql = "SELECT sd.parent_id from sys_department sd INNER JOIN sys_user sur on sur.dep_id = sd.dep_id INNER JOIN sys_position spt on spt.position_id = sur.position_id " \
                  "where sd.dep_district = '330100' and sd.dep_id <> '00000000000000000000000000000000' and (spt.position_name like '资产管家%' or spt.position_name like '综合管家%') " \
                  "ORDER BY RAND() LIMIT 1"
            parent_id = base.searchSQL(sql)[0][0]
        except BaseException as e:
            base.consoleLog('查询SQL报错。sql:' + sql + '  报错信息：' + str(e), 'e')
            return str(e)

            #新增楼盘
        url = "http://isz.ishangzu.com/isz_house/ResidentialController/saveResidential.action"
        data = {
            "residential_name": self.residential_name,
            "residential_jianpin": "xqzxcslp",
            "city_code": "330100",
            "area_code": "330108",
            "taBusinessCircleString": "4",
            "address": "海创基地南楼",
            "gd_lng": "120.138631",
            "gd_lat": "30.186537",
            "property_type": "ordinary",
            "taDepartString": parent_id,
            "build_date": "1975",
            "totle_buildings": "50",
            "total_unit_count": "200",
            "total_house_count": "4000",
            "build_area": "5000.00",
            "property_company": "我是物业公司",
            "property_fee": "2",
            "plot_ratio": "20.00",
            "green_rate": "30.00",
            "parking_amount": "2500",
            "other_info": "我是楼盘亮点",
            "bus_stations": "我是公交站",
            "metro_stations": "我是地铁站",
            "byname": "cs"}
        result = NewRequest(url, data).post()
        if result['code'] != 0:
            base.consoleLog('新增楼盘接口执行失败！')
            return result['msg']
        base.consoleLog('新增楼盘接口执行成功！')
        return

    def add_building(self):
        """
        新增栋座
        :return:
        """
        base.consoleLog('新增栋座。栋座名称：'+self.building_name)
        try:
            sql =  """SELECT
                residential_id
            FROM
                residential
            WHERE
                residential_name = '%s'
            AND deleted = 0
            ORDER BY
                create_time DESC LIMIT 1 """  % self.residential_name
            self.residential_id = base.searchSQL(sql)[0][0]
        except BaseException as e:
            base.consoleLog('查询SQL报错。sql:' + sql + '  报错信息：' + str(e), 'e')
            return str(e)

        url = 'http://isz.ishangzu.com/isz_house/ResidentialBuildingController/saveResidentialBuildingNew.action'
        data = {"property_name": self.residential_name,
                "building_name": self.building_name,
                "no_building": "无",
                "gd_lng": "120.152476",
                "gd_lat": "30.287232",
                "housing_type": "ordinary",
                "ground_floors": "20",
                "underground_floors": "2",
                "ladder_count": "10",
                "house_count": "200",
                "residential_id": self.residential_id,
                "have_elevator": "Y"}
        result = NewRequest(url, data).post()
        if result['code'] != 0:
            base.consoleLog('新增栋座接口执行失败！')
            return result['msg']
        base.consoleLog('新增栋座接口执行成功！')
        return

    def add_unit(self):
        """
        新增单元
        :return:
        """
        base.consoleLog('新增单元。单元名称：' + self.unit_name)

        try:
            sql = """SELECT
                building_id
            FROM
                residential_building
            WHERE
                residential_id = '%s'
            AND deleted = 0
            ORDER BY
                create_time DESC
            LIMIT 1""" % self.residential_id
            self.building_id = base.searchSQL(sql)[0][0]
        except BaseException as e:
            base.consoleLog('查询SQL报错。sql:' + sql + '  报错信息：' + str(e), 'e')
            return str(e)

        url = 'http://isz.ishangzu.com/isz_house/ResidentialBuildingController/saveResidentialBuildingUnit.action'
        data = {"property_name": self.residential_name + self.building_name,
                "unit_name": self.unit_name,
                "no_unit": "无",
                "building_id": self.building_id
                }
        result = NewRequest(url, data).post()

        if result['code'] != 0:
            base.consoleLog('新增单元接口执行失败！')
            return result['msg']
        base.consoleLog('新增单元接口执行成功！')
        return

    def add_floor(self):
        """
        新增楼层
        :return:
        """
        base.consoleLog('新增楼层：' + str(self.floor_name))

        try:
            sql = """SELECT
                unit_id
            FROM
                residential_building_unit
            WHERE
                building_id = '%s'
            ORDER BY
                create_time DESC
            LIMIT 1""" % self.building_id
            self.unit_id = base.searchSQL(sql)[0][0]
        except BaseException as e:
            base.consoleLog('查询SQL报错。sql:' + sql + '  报错信息：' + str(e), 'e')
            return str(e)

        url = 'http://isz.ishangzu.com/isz_house/ResidentialBuildingController/saveResidentialBuildingFloor.action'
        data = {
            "property_name": self.residential_name + self.building_name +self.unit_name,
            "floor_name": self.floor_name,
            "building_id": self.building_id,
            "unit_id": self.unit_id
            }
        result = NewRequest(url, data).post()
        if result['code'] != 0:
            base.consoleLog('新增楼层接口执行失败！')
            return result['msg']
        base.consoleLog('新增楼层接口执行成功！')
        return

    def add_house_no(self):
        """
        新增房间
        """
        base.consoleLog('新增房间数量：' + str(self.house_no_number))

        try:
            sql = "SELECT floor_id from residential_building_floor where unit_id='%s' ORDER BY create_time desc LIMIT 1" % self.unit_id
            self.floor_id = base.searchSQL(sql)[0][0]
        except BaseException as e:
            base.consoleLog('查询SQL报错。sql:' + sql + '  报错信息：' + str(e), 'e')
            return str(e)

        url = 'http://isz.ishangzu.com/isz_house/ResidentialBuildingController/saveResidentialBuildingHouseNo.action'
        for i in range(int(self.house_no_number)):
            house_no = int(self.house_no) + i
            data = {
                "property_name": self.residential_name + self.building_name + self.unit_name + self.floor_name,
                "house_no": house_no,
                "rooms": "1",
                "livings": "1",
                "bathrooms": "1",
                "kitchens": "1",
                "balconys": "1",
                "build_area": "100.00",
                "orientation": "NORTH",
                "building_id": self.building_id,
                "unit_id": self.unit_id,
                "floor_id": self.floor_id}
            base.consoleLog('新增房间号：' + str(house_no))
            result = NewRequest(url, data).post()
            if result['code'] != 0:
                base.consoleLog('新增房间号接口执行失败！')

        base.consoleLog('新增房间接口执行完成。')

        return

            # try:
            #     sql = """SELECT
            #         house_no_id
            #         FROM
            #         residential_building_house_no
            #         WHERE
            #         floor_id = '%s'
            #         ORDER BY
            #         create_time DESC
            #         LIMIT 1 """ % self.floor_id
            #     self.house_no_id_list = []
            #     house_no_id = base.searchSQL(sql)
            # except BaseException as e:
            #     base.consoleLog('查询SQL报错。sql:' + sql + '  报错信息：' + str(e), 'e')
            #     return
            #
            # for i in range(len(house_no_id)):
            #     self.house_no_id_list.append(house_no_id[i])

    def residential_info(self):
        """
        返回需要返回的信息
        :return:
        """
        residential_info = ResidentialInfo()
        residential_info.residential_id = self.residential_id
        residential_info.building_id = self.building_id
        residential_info.unit_id = self.unit_id
        residential_info.floor = self.floor_id
        residential_info.house_no_id = self.house_no_id_list
        return residential_info

    def run_class(self):
        """
        楼盘到房间流程
        :return:
        """
        base.consoleLog('创建楼盘流程')
        self.add_residential()
        self.add_building()
        self.add_unit()
        self.add_floor()
        self.add_house_no()
        return

    def select_residential_detail_request(self):
        """
        ERP查询楼盘信息接口
        :return:
        """
        base.consoleLog('楼盘详情接口。楼盘名称：' + self.residential_name)
        url = 'http://isz.ishangzu.com/isz_house/ResidentialController/selectResidentialDetail.action'
        data = {"residential_id":self.residential_id}
        result = NewRequest(url, data).post()['obj']
        return result


class ResidentialInfo:
    def __init__(self,residential_id):
        self.info_name = '楼盘信息'
        self.residential_id = residential_id
    def select_residential_detail_request(self):
        """
        查询楼盘信息
        :return:
        """
        url = 'http://isz.ishangzu.com/isz_house/ResidentialController/selectResidentialDetail.action'
        data = {"residential_id":self.residential_id}
        result = NewRequest(url, data).post()['obj']
        return result






