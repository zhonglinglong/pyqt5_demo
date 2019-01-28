# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年5月29日09:38:35
爱上租ERP工程管理接口类
"""


from common import interface
from common import base
from time import sleep


class Decoration:
    """工程管理类"""

    def __init__(self,contract_num,value=True):
        """
        :param contract_num: 委托合同号
        :param value: 是否需要交房
        """
        self.now_times = base.now_time(1)
        self.contract_num = contract_num
        self.url = 'http://decorate.ishangzu.com/isz_decoration/DecorationFileController/uploadPhoto' #工程管理上传图片地址

        for i in range(5):
            try:
                sql = 'SELECT project_id from new_decoration_project where info_id = (SELECT info_id from decoration_house_info where contract_num = "%s")' % self.contract_num
                print(sql)
                self.project_id = base.searchSQL(sql, db="isz_decoration")[0][0]
                print(self.project_id)
            except Exception as e:
                base.consoleLog("查询委托工程信息sql报错，sql:" + sql + "错误返回：" + str(e),'e')
                sleep(1)
                pass
        self.value = value

    def place_order(self):
        """
        下单
        :return:
        """
        base.consoleLog('下单')

        url = "http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/changeProgress/placeOrder"
        place_order_date = self.now_times + " 10:09:54"
        predict_survey_date = self.now_times + " 11:00"
        data = {
            "place_order_dep": "8A2152435E2E34E5015E30F811BB2653", # 下单部门id 测试专用店。
            "place_order_reason": "测试下单原因",
            "place_order_uid": "1444",
            "place_order_uname": "测试专用 勿改",
            "place_order_date": place_order_date,
            "predict_survey_date": predict_survey_date,
            "project_id": self.project_id}

        #下单
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('下单接口执行失败！')
            return result['msg']
        base.consoleLog('下单接口执行成功！')
        return

    def dispach(self):
        """
        派单
        :return:
        """
        base.consoleLog('派单')
        # 装配专员
        url = "http://decorate.ishangzu.com/isz_decoration/AssembleAreaController/searchAssemblyPerson"
        data = {"city_code": "330100"}
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            return result['msg']
        result = result["obj"][0]

        construct_uname = result["user_name"]
        construct_uid = result["user_id"]

        # 供应商
        # url = "http://decorate.ishangzu.com/isz_decoration/DecorationProjectController/suppliers?city_code=330100&supplier_type=STUFF"
        # result = interface.myRequest(url, method="get")
        # if result['code'] != 0:
        #     return result['msg']
        # result = result["obj"][0]
        # supplier_name = result["item_name"]
        # supplier_id = result["item_id"]

        supplier_name = "测试专用硬装供应商"
        supplier_id = "8A2152435FBAEFC3015FBAEFC3000000"

        # 工长
        url = "http://decorate.ishangzu.com/isz_decoration/DecorationProjectController/supplier/" + supplier_id + "/persons?supplier_person_type=MANAGER&supplier_id=" + supplier_id
        result = interface.myRequest(url, method="get")
        if result['code'] != 0:
            return result['msg']
        result = result["obj"][0]
        supplier_uname = result["item_name"]
        supplier_uid = result["item_id"]

        # 派单
        url = "http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/changeProgress/dispatchOrder"
        data = {
            "construct_uid": construct_uid,
            "construct_uname": construct_uname,
            "dispach_remark": "派单备注",
            "project_id": self.project_id,
            "supplier_id": supplier_id,
            "supplier_uid": supplier_uid,
            "predict_survey_date": "",
            "supplier_name": supplier_name,
            "supplier_uname": supplier_uname}
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('派单接口执行失败！')
            return result['msg']
        base.consoleLog('派单接口执行成功！')
        return

    def rceipt(self):
        """
        接单
        :return:
        """
        base.consoleLog('接单')
        url = "http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/changeProgress/acceptOrder"
        data = {"project_id": self.project_id}
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('接单接口执行失败！')
            return result['msg']
        base.consoleLog('接单接口执行成功！')
        return

    def volume_room(self):
        """
        量房评分
        :return:
        """
        base.consoleLog('量房评分')
        url = "http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/survey/score"
        idCardPhotos = interface.upLoadPhoto(self.url, base.get_conf('Img', 'picture_name'),
                                             base.get_conf('Img', 'file_path'),value='rsm')
        data = {
            "grade": "3",
            "project_id": self.project_id,
            "reform_way_fact": "REFORM",
            "score_remark": "",
            "attachments": [{
                "attach_type": "TOILET",
                "imgs": []
            }, {
                "attach_type": "KITCHEN",
                "imgs": []
            }, {
                "attach_type": "LIVING_ROOM",
                "imgs": []
            }, {
                "attach_type": "ROOM",
                "imgs": []
            }, {
                "attach_type": "OTHER",
                "imgs": [{
                    "url": idCardPhotos['src'],
                    "img_id": idCardPhotos["img_id"],
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 0,
                    "type": "OTHER"
                }]
            }]}
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('量房接口执行失败！')
            return result['msg']
        base.consoleLog('量房接口执行成功！')
        return

    def property_delivery(self):
        """
        物业交割
        :return:
        """
        base.consoleLog('物业交割')
        # 勘测
        url = "http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/survey/profee"
        idCardPhotos = interface.upLoadPhoto(self.url, base.get_conf('Img', 'picture_name'),
                                             base.get_conf('Img', 'file_path'),value='rsm')
        data = {
            "air_switch": "",
            "door_card": "",
            "door_key": "",
            "electricity_card": "",
            "electricity_meter_num": "",
            "electricity_meter_remain": "",
            "gas_card": "",
            "gas_meter_num": "",
            "gas_meter_remain": "",
            "project_id": self.project_id,
            "water_card": "",
            "water_card_remain": "",
            "water_meter_num": "",
            "attachments": [{
                "attach_type": "PROPERTY_DELIVERY_ORDER",
                "imgs": [{
                    "url": idCardPhotos["src"],
                    "img_id": idCardPhotos["img_id"],
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 0,
                    "type": ""
                }]
            }],
            "resource": "SURVEY"}
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('物业交割接口执行失败！')
            return result['msg']
        base.consoleLog('物业交割接口执行成功！')
        return

    def water_closed_test(self):
        """
        闭水试验
        :return:
        """
        base.consoleLog('闭水试验')
        url = "http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/survey/closed"
        idCardPhotos = interface.upLoadPhoto(self.url, base.get_conf('Img', 'picture_name'),
                                             base.get_conf('Img', 'file_path'),value='rsm')
        data = {
            "remark": "闭水试验备注",
            "attachments": [{
                "attach_type": "SCENE",
                "imgs": [{
                    "url": idCardPhotos["src"],
                    "img_id": idCardPhotos["img_id"],
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 0,
                    "type": ""
                }]
            }],
            "project_id": self.project_id,
            "closed_water_test_result": "Y",
            "is_need_waterproofing": "N"}
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('闭水试验接口执行失败！')
            return result['msg']
        base.consoleLog('闭水试验接口执行成功！')
        return

    def project_plan(self):
        """
        项目计划
        :return:
        """
        base.consoleLog('项目计划')
        sql = """SELECT
        b.info_id,
        a.project_no,
        b.entrust_type,
        b.build_area
        FROM
        new_decoration_project a
        INNER JOIN decoration_house_info b ON a.info_id = b.info_id
        AND a.project_id = '%s'
        WHERE
        b.deleted = 0 """ % self.project_id

        projectInfo = base.searchSQL(sql,db='isz_decoration')[0]

        idCardPhotos = interface.upLoadPhoto(self.url, base.get_conf('Img', 'picture_name'),
                                             base.get_conf('Img', 'file_path'), value='rsm')

        url = 'http://decorate.ishangzu.com/isz_decoration/decoHouseInfoController/saveOrUpdateApartment/saveApartment/projectOrder'
        data = {
            'build_area': str(projectInfo[3]),
            'reform_way_fact': 'OLDRESTYLE',
            'decoration_style': 'WUSHE_BREEZE',
            'house_orientation': 'SOURTH',
            'remould_rooms': 3,
            'remould_livings': '1',
            'remould_kitchens': '1',
            'remould_bathrooms': '2',
            'remould_balconys': '2',
            'info_id': projectInfo[0],
            'module_type': 'projectOrder',
            'handle_type': 'updateApartment',
            "layout_attachs": {
                "attach_type": "LAYOUT",
                "imgs": [{
                    "url": idCardPhotos['src'],
                    "img_id": idCardPhotos['img_id'],
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 0,
                    "type": ""
                }]
            },
            'zoneList': [
                {
                    "zone_type": "PUBLIC_TOILET",
                    "zone_type_name": "公共卫生间",
                    "room_no": "PUBLIC_TOILET_1",
                    "room_no_name": "公共卫生间1",
                    "zone_orientation": "NORTH",
                    "zone_orientation_name": "北",
                    "have_toilet": "WITHOUT",
                    "have_toilet_name": "-",
                    "toilet_area": "0",
                    "have_balcony": "WITHOUT",
                    "have_balcony_name": "-",
                    "balcony_area": "0",
                    "have_window_name": "有(1平米)",
                    "window_area": "1",
                    "zone_status_name": "已创建",
                    "zone_status": "FOUND",
                    "usearea": "4",
                    "window_type": "ORDINARYWINDOW",
                    "zone_id": "",
                    "is_fictitious_room": "N"
                },
                {
                    "zone_type": "KITCHEN",
                    "zone_type_name": "厨房",
                    "room_no": "KITCHEN_1",
                    "room_no_name": "厨房",
                    "zone_orientation": "EAST",
                    "zone_orientation_name": "东",
                    "have_toilet": "WITHOUT",
                    "have_toilet_name": "-",
                    "toilet_area": "0",
                    "have_balcony": "WITHOUT",
                    "have_balcony_name": "-",
                    "balcony_area": "0",
                    "have_window_name": "有(1平米)",
                    "window_area": "1",
                    "zone_status_name": "已创建",
                    "zone_status": "FOUND",
                    "usearea": "8",
                    "window_type": "ORDINARYWINDOW",
                    "zone_id": "",
                    "is_fictitious_room": "N"
                },
                {
                    "zone_type": "PARLOUR",
                    "zone_type_name": "客厅",
                    "room_no": "PARLOUR_1",
                    "room_no_name": "客厅1",
                    "zone_orientation": "EAST",
                    "zone_orientation_name": "东",
                    "have_toilet": "WITHOUT",
                    "have_toilet_name": "-",
                    "toilet_area": "0",
                    "have_balcony": "WITHOUT",
                    "have_balcony_name": "-",
                    "balcony_area": "0",
                    "have_window_name": "有(1平米)",
                    "window_area": "1",
                    "zone_status_name": "已创建",
                    "zone_status": "FOUND",
                    "usearea": "16",
                    "window_type": "ORDINARYWINDOW",
                    "zone_id": "",
                    "is_fictitious_room": "N"
                },
                {
                    "zone_type": "ROOM",
                    "zone_type_name": "房间",
                    "room_no": "METH",
                    "room_no_name": "甲",
                    "zone_orientation": "SOURTH",
                    "zone_orientation_name": "南",
                    "have_toilet": "HAVE",
                    "have_toilet_name": "有(4平米)",
                    "toilet_area": "4",
                    "have_balcony": "WITHOUT",
                    "have_balcony_name": "-",
                    "balcony_area": "0",
                    "have_window_name": "有(1平米)",
                    "window_area": "1",
                    "zone_status_name": "已创建",
                    "zone_status": "FOUND",
                    "usearea": "11",
                    "window_type": "ORDINARYWINDOW",
                    "zone_id": "",
                    "is_fictitious_room": "N"
                },
                {
                    "zone_type": "ROOM",
                    "zone_type_name": "房间",
                    "room_no": "ETH",
                    "room_no_name": "乙",
                    "zone_orientation": "SOURTH",
                    "zone_orientation_name": "南",
                    "have_toilet": "WITHOUT",
                    "have_toilet_name": "-",
                    "toilet_area": "0",
                    "have_balcony": "WITHOUT",
                    "have_balcony_name": "-",
                    "balcony_area": "0",
                    "have_window_name": "有(1平米)",
                    "window_area": "1",
                    "zone_status_name": "已创建",
                    "zone_status": "FOUND",
                    "usearea": "12",
                    "window_type": "ORDINARYWINDOW",
                    "zone_id": "",
                    "is_fictitious_room": "N"
                },
                {
                    "zone_type": "ROOM",
                    "zone_type_name": "房间",
                    "room_no": "PROP",
                    "room_no_name": "丙",
                    "zone_orientation": "SOURTH",
                    "zone_orientation_name": "南",
                    "have_toilet": "WITHOUT",
                    "have_toilet_name": "-",
                    "toilet_area": "0",
                    "have_balcony": "WITHOUT",
                    "have_balcony_name": "-",
                    "balcony_area": "0",
                    "have_window_name": "有(1平米)",
                    "window_area": "1",
                    "zone_status_name": "已创建",
                    "zone_status": "FOUND",
                    "usearea": "13",
                    "window_type": "ORDINARYWINDOW",
                    "zone_id": "",
                    "is_fictitious_room": "N"
                },
                {
                    "zone_type": "BALCONY",
                    "zone_type_name": "阳台",
                    "room_no": "BALCONY_1",
                    "room_no_name": "阳台1",
                    "zone_orientation": "SOURTH",
                    "zone_orientation_name": "南",
                    "have_toilet": "WITHOUT",
                    "have_toilet_name": "-",
                    "toilet_area": "0",
                    "have_balcony": "WITHOUT",
                    "have_balcony_name": "-",
                    "balcony_area": "0",
                    "have_window_name": "有(0平米)",
                    "window_area": "0",
                    "zone_status_name": "已创建",
                    "zone_status": "FOUND",
                    "usearea": "2",
                    "window_type": "ORDINARYWINDOW",
                    "zone_id": "",
                    "is_fictitious_room": "N"
                },
                {
                    "zone_type": "BALCONY",
                    "zone_type_name": "阳台",
                    "room_no": "BALCONY_2",
                    "room_no_name": "阳台2",
                    "zone_orientation": "SOURTH",
                    "zone_orientation_name": "南",
                    "have_toilet": "WITHOUT",
                    "have_toilet_name": "-",
                    "toilet_area": "0",
                    "have_balcony": "WITHOUT",
                    "have_balcony_name": "-",
                    "balcony_area": "0",
                    "have_window_name": "有(1平米)",
                    "window_area": "1",
                    "zone_status_name": "已创建",
                    "zone_status": "FOUND",
                    "usearea": "3",
                    "window_type": "ORDINARYWINDOW",
                    "zone_id": "",
                    "is_fictitious_room": "N"
                }
            ],
            'project_id': self.project_id,
            'project_no': projectInfo[1],
            'entrust_type': projectInfo[2]
        }
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('项目计划接口执行失败！')
            return result['msg']
        base.consoleLog('项目计划接口执行成功！')
        return

    def config_list(self):
        """
        物品清单提交及验证
        :return:
        """
        base.consoleLog('物品清单提交及验证')
        #查找房间
        url = 'http://decorate.ishangzu.com/isz_decoration/NewConfigurationController/queryZone/%s' % self.project_id
        result = interface.myRequest(url, method='get')
        if result['code'] != 0:
            return result['msg']
        result = result['obj']
        zoneId = None
        for i in result:
            if i['function_zone'] == u'甲':
                zoneId = i['zone_id']

        #添加物品
        url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationConfigController/confirm'
        data = [{
            "acceptance_num": None,
            "acceptance_num_this": None,
            "brand_id": None,
            "brand_name": "爱上租定制",
            "category_flag": None,
            "category_one_id": None,
            "category_one_len": None,
            "category_one_nm": "家具",
            "category_two_id": None,
            "category_two_nm": "书桌",
            "config_list_id": None,
            "config_list_status": None,
            "config_list_status_name": None,
            "create_name": None,
            "create_time": None,
            "create_uid": None,
            "deleted": None,
            "flag": None,
            "function_zone": "甲",
            "function_zone_len": None,
            "new_replenish_id": None,
            "order_type": None,
            "predict_delivery_date": None,
            "project_id": self.project_id,
            "purchase_num": "10",
            "purchase_order_no": None,
            "real_delivery_time": None,
            "remark": None,
            "remark_accept": None,
            "remark_return": None,
            "replacement_order": None,
            "return_num": None,
            "return_num_this": None,
            "standard_id": None,
            "standard_name": "0.86M（3.0）",
            "submit_time": None,
            "supplier_id": "8A2152435CF3FFF3015D0C64330F0011",
            "supplier_name": "浙江品至家具有限公司",
            "total_account": None,
            "total_paid": 3100,
            "unit_id": None,
            "unit_name": "张",
            "unit_price": 310,
            "update_time": None,
            "update_uid": None,
            "zone_id": zoneId,
            "index": 0,
            "disabled": "true"}]
        result = interface.myRequest(url,data)
        if result['code'] != 0:
            return result['msg']

        #提交订单
        url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationConfigController/submitOrder'
        data = [{
            "predict_delivery_date": '%s 13:00:00' % self.now_times,
            "project_id": self.project_id,
            "supplier_id": "8A2152435CF3FFF3015D0C64330F0011",
            "supplier_name": "家具供应商:浙江品至家具有限公司"
        }]
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            return result['msg']

        #验收物品清单
        url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationConfigController/supplierOrdersDetail'
        sql = "select supplier_id from new_config_list where project_id='%s' and deleted=0  and config_list_status<>'CHECKED'" % self.project_id
        supplier_id = base.searchSQL(sql,db='isz_decoration')[0][0]
        data = {"project_id": self.project_id, "supplier_id": supplier_id}
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            return result['msg']
        result = result['obj']

        url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationConfigController/acceptance/confirm'
        for i in result:
            i['real_delivery_time'] = base.time_time('second')
        results = interface.myRequest(url, result)
        if results['code'] != 0:
            base.consoleLog('配置清单接口执行失败！')
            return results['msg']
        base.consoleLog('配置清单接口执行成功！')
        return

    def decoration_list(self):
        """
        硬装清单提交及验证
        :return:
        """
        base.consoleLog('硬装清单提交及验证')
        #制定物品清单
        url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationStuffController/preview'
        commonData = [
            {
                "acceptance_num": None,
                "acceptance_num_this": 0,
                "acceptance_time": None,
                "create_time": base.time_time('second'),
                "create_uid": base.get_conf('loginUser','user_id'),
                "data_type": "成品安装",
                "data_type_len": 26,
                "decoration_detial": "家具安装",
                "deleted": 0,
                "function_zone": "甲",
                "function_zone_len": 100,
                "hard_deliver_audit_status": None,
                "order_type": None,
                "predict_delivery_date": None,
                "project_id": self.project_id,
                "purchase_num": "10",
                "purchase_order_no": None,
                "remark": None,
                "remark_accept": None,
                "remark_detail": "",
                "remark_return": None,
                "replacement_order": None,
                "return_name": None,
                "return_num": None,
                "return_num_this": 0,
                "stuff_fees_change_reason": None,
                "stuff_list_id": None,
                "stuff_list_status": "DRAFT",
                "submit_time": None,
                "supplier_id": None,
                "supplier_name": None,
                "total_account": None,
                "total_paid": "100.00",
                "unit_id": None,
                "unit_name": "件",
                "unit_price": 10,
                "update_time": base.time_time('second'),
                "update_uid": base.get_conf('loginUser','user_id'),
                "zone_type": None,
                "type_index": 0,
                "fun_index": 0
            }, {
                "acceptance_num": None,
                "acceptance_num_this": 0,
                "acceptance_time": None,
                "create_time": base.time_time('second'),
                "create_uid": base.get_conf('loginUser','user_id'),
                "data_type": "成品安装",
                "data_type_len": 26,
                "decoration_detial": "嵌入式天花灯-改造",
                "deleted": 0,
                "function_zone": "甲",
                "function_zone_len": 100,
                "hard_deliver_audit_status": None,
                "order_type": None,
                "predict_delivery_date": None,
                "project_id": self.project_id,
                "purchase_num": "11",
                "purchase_order_no": None,
                "remark": None,
                "remark_accept": None,
                "remark_detail": "",
                "remark_return": None,
                "replacement_order": None,
                "return_name": None,
                "return_num": None,
                "return_num_this": 0,
                "stuff_fees_change_reason": None,
                "stuff_list_id": None,
                "stuff_list_status": "DRAFT",
                "submit_time": None,
                "supplier_id": None,
                "supplier_name": None,
                "total_account": None,
                "total_paid": "264.00",
                "unit_id": None,
                "unit_name": "个",
                "unit_price": 24,
                "update_time": base.time_time('second'),
                "update_uid": base.get_conf('loginUser','user_id'),
                "zone_type": None,
                "fun_index": 1,
                "type_index": 1
            }, {
                "acceptance_num": None,
                "acceptance_num_this": 0,
                "acceptance_time": None,
                "create_time": base.time_time('second'),
                "create_uid": base.get_conf('loginUser','user_id'),
                "data_type": "成品安装",
                "data_type_len": 26,
                "decoration_detial": "明装筒灯-改造",
                "deleted": 0,
                "function_zone": "甲",
                "function_zone_len": 100,
                "hard_deliver_audit_status": None,
                "order_type": None,
                "predict_delivery_date": None,
                "project_id": self.project_id,
                "purchase_num": "12",
                "purchase_order_no": None,
                "remark": None,
                "remark_accept": None,
                "remark_detail": "",
                "remark_return": None,
                "replacement_order": None,
                "return_name": None,
                "return_num": None,
                "return_num_this": 0,
                "stuff_fees_change_reason": None,
                "stuff_list_id": None,
                "stuff_list_status": "DRAFT",
                "submit_time": None,
                "supplier_id": None,
                "supplier_name": None,
                "total_account": None,
                "total_paid": "403.20",
                "unit_id": None,
                "unit_name": "个",
                "unit_price": 33.6,
                "update_time": base.time_time('second'),
                "update_uid": base.get_conf('loginUser','user_id'),
                "zone_type": None,
                "fun_index": 1,
                "type_index": 1
            }
        ]
        result = interface.myRequest(url,commonData)
        if result['code'] != 0:
            return result['msg']

        #提交硬装清单
        url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationStuffController/saveStuffLists'
        sql = """SELECT
        b.address,
        a.config_order_no,
        b.contract_id,
        b.contract_num,
        b.create_time,
        b.entrust_end_date,
        b.entrust_start_date,
        b.house_code,
        b.housekeep_mange_uid,
        b.info_id,
        a.project_no,
        b.sign_date,
        b.city_code,
        b.city_name
        FROM
        decoration_house_info b
        INNER JOIN new_decoration_project a ON a.info_id = b.info_id
        AND a.project_id = '%s' """ % self.project_id
        projectInfo = base.searchSQL(sql,db='isz_decoration')[0]
        data = {
            "newStuffList": commonData,
            "project": {
                "address": projectInfo[0],
                "build_area": "120.00",
                "cable_laying_type": "INNERPIPEINNERLINE",
                "cable_laying_type_name": None,
                "city_code": "330100",
                "city_name": "杭州市",
                "closed_water_test_result": "Y",
                "complete_two_nodes": "[\"VOLUME_SCORE\",\"SURVEY_PROPERTY_DELIVERY\",\"WATER_CLOSED_TEST\",\"PROJECT_PLAN\",\"GOODS_CONFIG_LIST\"]",
                "complete_two_nodes_list": ["VOLUME_SCORE", "SURVEY_PROPERTY_DELIVERY", "WATER_CLOSED_TEST",
                                            "PROJECT_PLAN", "GOODS_CONFIG_LIST"],
                "config_list_status": "CHECKED",
                "config_list_status_name": "已验收",
                "config_order_no": projectInfo[1],
                "config_progress": "WAIT_DESIGN",
                "config_progress_name": "待设计",
                "config_submit_time": '%s 13:35:00' % self.now_times,
                "config_submit_uid": base.get_conf('loginUser','user_id'),
                "config_submit_uname": base.get_conf('loginUser','user_name'),
                "construct_uid": "1610",
                "construct_uname": "徐经纬",
                "construct_uname_phone": "徐经纬/13105715060",
                "contract_id": projectInfo[2],
                "contract_num": projectInfo[3],
                "contract_type": "NEWSIGN",
                "contract_type_name": "新签",
                "create_time": str(projectInfo[4]),
                "create_uid": "8AEF8688600F30F30160257579287F96",
                "current_one_node": "PROJECT_PLAN",
                "decoration_style": "WUSHE_BREEZE",
                "decoration_style_name": "随寓和风",
                "deleted": 0,
                "deliver_room_date": "1970-01-02 00:00:00.0",
                "dispach_remark": "测试",
                "entrust_end_date": str(projectInfo[5]),
                "entrust_start_date": str(projectInfo[6]),
                "entrust_type_fact": "SHARE",
                "entrust_type_fact_name": "合租",
                "grade": 20,
                "hidden_check_date": "1970-01-02 00:00:00.0",
                "house_code": projectInfo[7],
                "housekeep_mange_name": None,
                "housekeep_mange_uid": projectInfo[8],
                "info_id": projectInfo[9],
                "is_active": "Y",
                "is_active_name": "是",
                "one_level_nodes": "[\"PLACE_ORDER\",\"DISPATCH_ORDER\",\"SURVEY\",\"PROJECT_PLAN\",\"CONSTRUCTING\",\"PROJECT_CHECK\",\"PROJECT_COMPLETION\"]",
                "order_status_name": "进程中",
                "order_type_name": "新收配置订单",
                "overall_check_date": "1970-01-02 00:00:00.0",
                "phone": "18815286582",
                "place_order_date": "2018-03-20 20:47:38",
                "place_order_dep": "",
                "place_order_dep_name": None,
                "place_order_reason": "测试",
                "place_order_uid": base.get_conf('loginUser','user_id'),
                "place_order_uname": base.get_conf('loginUser','user_name'),
                "plumbing_type": "INNERPIPE",
                "plumbing_type_name": None,
                "predict_complete_date": "",
                "predict_days": 0,
                "predict_hidden_check_date": '%s 00:00:00' % base.now_time(2),
                "predict_overall_check_date": '%s 00:00:00' % base.now_time(2),
                "predict_stuff_check_date": '%s 00:00:00' % base.now_time(2),
                "predict_survey_date": '%s 09:00:00' % base.now_time(2),
                "project_id": self.project_id,
                "project_no": projectInfo[10],
                "project_order_status": "INPROCESS",
                "project_order_type": "NEW_COLLECT_ORDER",
                "reform_way": "OLDRESTYLE",
                "reform_way_fact": "OLDRESTYLE",
                "reform_way_fact_name": "老房全装",
                "reform_way_name": "老房全装",
                "remark": "",
                "room_toilet": "3/2",
                "sign_date": str(projectInfo[11]),
                "sign_name": None,
                "sign_uid": "8A2152435DC1AEAA015DDE96F9276279",
                "sign_user_phone": None,
                "start_time": '%s 00:00:00' % base.now_time(2),
                "stuff_check_date": "1970-01-02 00:00:00.0",
                "stuff_list_status": "DRAFT",
                "stuff_list_status_name": "待下单",
                "stuff_order_no": "",
                "stuff_submit_time": "1970-01-02 00:00:00.0",
                "stuff_submit_uid": "",
                "stuff_submit_uname": "",
                "supplier_id": "8A2152435FBAEFC3015FBAEFC3000000",
                "supplier_name": "测试专用硬装供应商",
                "supplier_uid": "8AB398CA5FBAF072015FBB26338A0002",
                "supplier_uname": "测试专用硬装员工",
                "supplier_uname_phone": "测试专用硬装员工/18815286582",
                "timeMap": None,
                "total_paid": 0,
                "two_level_nodes": "[\"VOLUME_SCORE\",\"SURVEY_PROPERTY_DELIVERY\",\"WATER_CLOSED_TEST\",\"DECORATION_CONFIG_LIST\",\"GOODS_CONFIG_LIST\",\"PROJECT_PLAN\",\"CONCEALMENT_ACCEPTANCE\",\"HARD_ACCEPTANCE\",\"ACCEPTANCE_PROPERTY_DELIVERY\",\"COST_SETTLEMENT\",\"OVERALL_ACCEPTANCE\",\"HOUSE_DELIVERY\",\"INDOOR_PICTURE\"]",
                "update_time": '%s 13:35:00' % self.now_times,
                "update_uid": "8AEF8688600F30F30160257579287F96",
                "wall_condition": "OLDHOUSE",
                "wall_condition_name": None
            }
        }
        result = interface.myRequest(url,data)
        if result['code'] != 0:
            return result['msg']


        #装修清单验收
        geturl = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationStuffController/getSuffList/%s' % self.project_id
        result = interface.myRequest(geturl, method='get')
        if result['code'] != 0:
            return result['msg']
        url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationStuffController/acceptanceAll'
        acceptance_time = base.time_time('second')
        data = result['obj']['newStuffList']
        for stufflist in data:
            stufflist['acceptance_time'] = acceptance_time
            stufflist['acceptance_num_this'] = stufflist['purchase_num']
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('硬装清单提交验收接口执行失败！')
            return result['msg']
        base.consoleLog('硬装清单提交验收接口执行成功！')
        return

    def concealment_acceptance(self):
        """
        隐蔽验收
        :return:
        """
        base.consoleLog('隐蔽验收')
        idCardPhotos = interface.upLoadPhoto(self.url, base.get_conf('Img', 'picture_name'),
                                             base.get_conf('Img', 'file_path'), value='rsm')
        url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/constructing/hideCheck'
        data = {
            "air_switch": None,
            "attachments": [{
                "attach_type": "TOILET",
                "imgs": [{
                    "url": idCardPhotos['src'],
                    "img_id": idCardPhotos['img_id'],
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 0,
                    "type": "TOILET"
                }]
            }, {
                "attach_type": "KITCHEN",
                "imgs": [{
                    "url": idCardPhotos['src'],
                    "img_id": idCardPhotos['img_id'],
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 1,
                    "type": "KITCHEN"
                }]
            }, {
                "attach_type": "LIVING_ROOM",
                "imgs": [{
                    "url": idCardPhotos['src'],
                    "img_id": idCardPhotos['img_id'],
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 2,
                    "type": "LIVING_ROOM"
                }]
            }, {
                "attach_type": "BALCONY",
                "imgs": [{
                    "url": idCardPhotos['src'],
                    "img_id": idCardPhotos['img_id'],
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 3,
                    "type": "BALCONY"
                }]
            }, {
                "attach_type": "OTHER",
                "imgs": []
            }],
            "check_remark": "",
            "closed_water_test_result": None,
            "curOneLevelNode": None,
            "curTwoLevelNode": None,
            "door_card": None,
            "door_key": None,
            "electricity_card": None,
            "electricity_meter_num": None,
            "electricity_meter_remain": None,
            "gas_card": None,
            "gas_meter_num": None,
            "gas_meter_remain": None,
            "grade": None,
            "hidden_check_date": '%s 09:00:00' % self.now_times,
            "landlordGoods": None,
            "project_id": self.project_id,
            "reform_way_fact": None,
            "reform_way_fact_name": "",
            "remark": None,
            "score_remark": None,
            "water_card": None,
            "water_card_remain": None,
            "water_meter_num": None
        }
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('隐蔽验收接口执行失败！')
            return result['msg']
        base.consoleLog('隐蔽验收接口执行成功！')
        return

    def overall_acceptance(self):
        """
        整体验收
        :return:
        """
        base.consoleLog('整体验收')
        idCardPhotos = interface.upLoadPhoto(self.url, base.get_conf('Img', 'picture_name'),
                                             base.get_conf('Img', 'file_path'), value='rsm')
        url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/proCheck/wholeCheck'
        data = {
            "air_switch": None,
            "attachments": None,
            "card_attachs": [{
                "attach_type": "CARDS",
                "imgs": [{
                    "url": idCardPhotos['src'],
                    "img_id": idCardPhotos['img_id'],
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 0,
                    "type": ""
                }]
            }],
            "closed_water_test_result": None,
            "curOneLevelNode": None,
            "curTwoLevelNode": None,
            "door_card": None,
            "door_key": None,
            "electricity_card": None,
            "electricity_meter_num": None,
            "electricity_meter_remain": None,
            "gas_card": None,
            "gas_meter_num": None,
            "gas_meter_remain": None,
            "grade": None,
            "landlordGoods": None,
            "newStuffList": None,
            "overall_check_date": '%s 14:00:00' % self.now_times,
            "project_id": self.project_id,
            "remark": "",
            "score_remark": None,
            "three_attachs": [{
                "attach_type": "THREE",
                "imgs": [{
                    "url": idCardPhotos['src'],
                    "img_id": idCardPhotos['img_id'],
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 0,
                    "type": ""
                }]
            }],
            "water_card": None,
            "water_card_remain": None,
            "water_meter_num": None
        }
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('整体验收接口执行失败！')
            return result['msg']
        base.consoleLog('整体验收接口执行成功！')
        return

    def property_acceptance(self):
        """
        物业交割验收
        :return:
        """
        base.consoleLog('物业交割验收')

        idCardPhotos = interface.upLoadPhoto(self.url, base.get_conf('Img', 'picture_name'),
                                             base.get_conf('Img', 'file_path'), value='rsm')

        url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/proCheck/profee'
        data = {
            "air_switch": "",
            "door_card": "",
            "door_key": "",
            "electricity_card": "",
            "electricity_meter_num": "",
            "electricity_meter_remain": "",
            "gas_card": "",
            "gas_meter_num": "",
            "gas_meter_remain": "",
            "project_id": self.project_id,
            "water_card": "",
            "water_card_remain": "",
            "water_meter_num": "",
            "attachments": [{
                "attach_type": "PROPERTY_DELIVERY_ORDER",
                "imgs": [{
                    "url": idCardPhotos['src'],
                    "img_id": idCardPhotos['img_id'],
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 0,
                    "type": ""
                }]
            }],
            "resource": "PROJECT_CHECK"
        }
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('物业交割确认接口执行失败！')
            return result['msg']
        base.consoleLog('物业交割确认接口执行成功！')
        return

    def cost_settlement(self):
        """
        费用结算
        :return:
        """
        base.consoleLog('费用结算')
        url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/proCheck/costsettle'
        data = {
            "project_id": self.project_id,
            "remark": ""
        }
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('费用结算提交接口执行失败！')
            return result['msg']
        base.consoleLog('费用结算提交接口执行成功！')
        return

    def indoor_img(self):
        """
        室内图提交
        :return:
        """
        base.consoleLog('室内图提交')

        idCardPhotos = interface.upLoadPhoto(self.url, base.get_conf('Img', 'picture_name'),
                                             base.get_conf('Img', 'file_path'), value='rsm')
        url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/proComp/indoor'
        data = {
            "curOneLevelNode": None,
            "curTwoLevelNode": None,
            "deliver_room_date": None,
            "house_attachs": [{
                "attach_type": "PUBLIC_TOILET_1",
                "imgs": [{
                    "url": idCardPhotos['src'],
                    "img_id": idCardPhotos['img_id'],
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 0,
                    "type": "PUBLIC_TOILET_1"
                }]
            }, {
                "attach_type": "KITCHEN_1",
                "imgs": [{
                    "url": idCardPhotos['src'],
                    "img_id": idCardPhotos['img_id'],
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 1,
                    "type": "KITCHEN_1"
                }]
            }, {
                "attach_type": "PARLOUR_1",
                "imgs": [{
                    "url": idCardPhotos['src'],
                    "img_id": idCardPhotos['img_id'],
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 2,
                    "type": "PARLOUR_1"
                }]
            }, {
                "attach_type": "METH",
                "imgs": [{
                    "url": idCardPhotos['src'],
                    "img_id": idCardPhotos['img_id'],
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 3,
                    "type": "METH"
                }]
            }, {
                "attach_type": "ETH",
                "imgs": [{
                    "url": idCardPhotos['src'],
                    "img_id": idCardPhotos['img_id'],
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 4,
                    "type": "ETH"
                }]
            }, {
                "attach_type": "PROP",
                "imgs": [{
                    "url": idCardPhotos['src'],
                    "img_id": idCardPhotos['img_id'],
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 5,
                    "type": "PROP"
                }]
            }, {
                "attach_type": "BALCONY_1",
                "imgs": [{
                    "url": idCardPhotos['src'],
                    "img_id": idCardPhotos['img_id'],
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 6,
                    "type": "BALCONY_1"
                }]
            }, {
                "attach_type": "BALCONY_2",
                "imgs": [{
                    "url": idCardPhotos['src'],
                    "img_id": idCardPhotos['img_id'],
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 7,
                    "type": "BALCONY_2"
                }]
            }],
            "layout_attachs": [{
                "attach_type": "LAYOUT",
                "imgs": [{
                    "url": idCardPhotos['src'],
                    "img_id": idCardPhotos['img_id'],
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 0,
                    "type": ""
                }]
            }],
            "project_id": self.project_id,
            "remark": None
        }
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('室内图提交接口执行失败！')
            return result['msg']
        base.consoleLog('室内图提交接口执行成功！')
        return

    def delivery(self):
        """
        竣工交付
        :return:
        """
        base.consoleLog('竣工交付')
        url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/proComp/delivery'
        data = {
            "deliver_room_date": '%s 18:00:00' % self.now_times,
            "project_id": self.project_id,
            "remark": ""
        }
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('竣工交付接口执行失败！')
            return result['msg']
        base.consoleLog('竣工交付接口执行成功！')
        return

    def run_class(self):
        """
        按业务流程执行所有方法
        :return:
        """
        base.consoleLog('工程管理交房流程。委托合同号：' + self.contract_num)
        self.place_order()  # 下单
        self.dispach()  # 派单
        self.rceipt()  # 接单
        self.volume_room()  # 量房
        self.property_delivery()  # 物业交割
        self.water_closed_test()  # 闭水试验
        self.project_plan()  # 项目计划
        self.config_list()  # 物品清单
        self.decoration_list()  # 硬装清单
        self.concealment_acceptance()  # 隐蔽验收
        self.overall_acceptance()  # 整体验收
        self.property_acceptance()  # 物业交割验收
        self.cost_settlement()  # 费用结算
        self.indoor_img()  # 室内图提交
        if self.value:
            self.delivery()  # 交房
            base.consoleLog('工程管理工程订单接口执行完成。')
        else:
            base.consoleLog('工程管理工程订单接口执行到已交房。')






