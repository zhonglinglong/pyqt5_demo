# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年4月12日13:15:44
爱上租业绩查询接口
"""

from common import interface
from common import base


class SerachIssueAchievement:
    """查询出单业绩"""

    def __init__(self, contract_num=None):
        """
        :param contract_num: 出租合同号
        """
        self.contract_num = contract_num
        try:
            sql = "select contract_id from apartment_contract where contract_num = '%s' and deleted=0" % self.contract_num
            self.contract_id = base.searchSQL(sql)[0][0]
        except Exception as e:
            base.consoleLog("查询出租合同返回为空,sql:" + sql + "错误返回：" + str(e))
            self.contract_id = ''

    def serach_condition_info(self):
        """
        出租合同右键查询业绩信息
        :return:出单条件所有字段
        """

        url = "http://erp.ishangzu.com/isz_achievement/issueAchieve/issueConditions/" + self.contract_id
        result = interface.myRequest(url, method='get')

        try:
            if result['code'] != 0:
                return result['msg']
        except BaseException as e:
            base.consoleLog(str(e))
            return

        result = result["obj"]
        issue_conditions = {}

        if result == None:
            base.consoleLog(str(result))
            return


        data = []
        # 处理业绩核算条件返回信息
        for i in range(len(result['resultsAccountingConditionsList'])):
            condition_type_cn = []
            condition_type_cn.append(result['resultsAccountingConditionsList'][i]['condition_type_cn'])
            condition_type_cn.append(result['resultsAccountingConditionsList'][i]['finish_time'])
            condition_type_cn.append(result['resultsAccountingConditionsList'][i]['is_finish'])
            data.append(condition_type_cn)
        dic = {}
        for i in range(len(data)):
            dic.setdefault(data[i][0], data[i])
        issue_conditions['出单条件'] = dic


        data = []
        #处理业绩分成角色
        for i in range(len(result['resultsDividedRoleList'])):
            resultsDividedRoleList = []
            resultsDividedRoleList.append(result['resultsDividedRoleList'][i]['divide_type_cn'])
            resultsDividedRoleList.append(result['resultsDividedRoleList'][i]['divide_dname'])
            resultsDividedRoleList.append(result['resultsDividedRoleList'][i]['divide_uname'])
            resultsDividedRoleList.append(result['resultsDividedRoleList'][i]['divide_proportion_view'])
            data.append(resultsDividedRoleList)
        dic = {}
        for i in range(len(data)):
            dic.setdefault(data[i][0], data[i])
        issue_conditions['分成角色'] = dic


        data = []
        # 处理业绩核算记录
        for i in range(len(result['accountingRecordList'])):
            accountingRecordList = []
            accountingRecordList.append(result['accountingRecordList'][i]['is_active_cn'])
            accountingRecordList.append(result['accountingRecordList'][i]['active_time'])
            accountingRecordList.append(result['accountingRecordList'][i]['divide_house_source_us_uname'])
            accountingRecordList.append(result['accountingRecordList'][i]['divide_house_source_us_dname'])
            accountingRecordList.append(result['accountingRecordList'][i]['apartment_contract_num'])
            accountingRecordList.append(result['accountingRecordList'][i]['house_rent_times_cn'])
            accountingRecordList.append(result['accountingRecordList'][i]['accounting_num_view'])
            accountingRecordList.append(result['accountingRecordList'][i]['apartment_contract_type_cn'])
            accountingRecordList.append(result['accountingRecordList'][i]['profit_diff'])
            accountingRecordList.append(result['accountingRecordList'][i]['adjust_achievement'])
            accountingRecordList.append(result['accountingRecordList'][i]['accounting_month'])
            data.append(accountingRecordList)
        dic = {}
        for i in range(len(data)):
            dic.setdefault(data[i][6], data[i])
        issue_conditions['核算记录'] = dic

        base.consoleLog('出单条件返回值：' + str(issue_conditions))
        return issue_conditions

    def serach_issue_info(self):
        """
        同一个出租合同下所有出单业绩列表的详情字段
        :return:
        """
        base.consoleLog('出单业绩详情。合同号：' + self.contract_num)

        sql = "SELECT achievement_issue_id from achievement_issue where apartment_contract_id = '%s' and deleted=0" % self.contract_id
        achievement_issue_id = base.searchSQL(sql)

        # 同一个出租合同所有出单业绩详情
        achievement_issue_info_list = []
        url_ = 'http://erp.ishangzu.com/isz_achievement/issueAchieve/details/'
        for i in range(len(achievement_issue_id)):
            achievement_issue_info_list.append(
                interface.myRequest(url_ + str(achievement_issue_id[i][0]), method='get')['obj'])
        base.consoleLog('出单业绩详情查询接口执行完成！')

        # 每一条出单业绩对应的出租合同信息
        apartment_contract_info = []
        for i in range(len(achievement_issue_info_list)):
            data = {}
            data["合同提交日"] = achievement_issue_info_list[i]["apartment_contract_commit_date"]
            data["合同号"] = achievement_issue_info_list[i]["apartment_contract_num"]
            data["出租周期"] = achievement_issue_info_list[i]["apartment_rental_cycles"]
            data["核算周期"] = achievement_issue_info_list[i]["apartment_accounting_cycles"]
            data["月租金"] = achievement_issue_info_list[i]["apartment_rent_month"]
            data["付款方式"] = achievement_issue_info_list[i]["apartment_payment_type_cn"]
            data["付款周期"] = achievement_issue_info_list[i]["apartment_payment_cycle_cn"]
            data["承租类别"] = achievement_issue_info_list[i]["apartment_contract_type_cn"]
            data["客源方"] = achievement_issue_info_list[i]["apartment_customer_source_uname"]
            data["客源方部门"] = achievement_issue_info_list[i]["apartment_customer_source_dname"]
            apartment_contract_info.append(data)

        # 每一条出单业绩对应的委托合同信息
        house_contract_info = []
        for i in range(len(achievement_issue_info_list)):
            data = {}
            house_contract_num = []
            house_rent_times_cn = []
            house_rent_month_total = []
            house_decoration_cycles = []
            house_source_cn = []
            house_apartment_type_cn = []
            house_entrust_type_cn = []
            house_contract_type_cn = []
            house_source_us_uname = []
            house_source_us_dname = []

            for j in range(len(achievement_issue_info_list[i]['houseContractRelations'])):
                house_contract_num.append(
                    achievement_issue_info_list[i]['houseContractRelations'][j]['house_contract_num'])
                house_rent_times_cn.append(
                    achievement_issue_info_list[i]['houseContractRelations'][j]['house_rent_times_cn'])
                house_rent_month_total.append(
                    achievement_issue_info_list[i]['houseContractRelations'][j]['house_rent_month_total'])
                house_decoration_cycles.append(
                    achievement_issue_info_list[i]['houseContractRelations'][j]['house_decoration_cycles'])
                house_source_cn.append(achievement_issue_info_list[i]['houseContractRelations'][j]['house_source_cn'])
                house_apartment_type_cn.append(
                    achievement_issue_info_list[i]['houseContractRelations'][j]['house_apartment_type_cn'])
                house_entrust_type_cn.append(
                    achievement_issue_info_list[i]['houseContractRelations'][j]['house_entrust_type_cn'])
                house_contract_type_cn.append(
                    achievement_issue_info_list[i]['houseContractRelations'][j]['house_contract_type_cn'])
                house_source_us_uname.append(
                    achievement_issue_info_list[i]['houseContractRelations'][j]['house_source_us_uname'])
                house_source_us_dname.append(
                    achievement_issue_info_list[i]['houseContractRelations'][j]['house_source_us_dname'])

            data["合同号"] = house_contract_num
            data["出租次数"] = house_rent_times_cn
            data["月总租金"] = house_rent_month_total
            data["核算装修期"] = house_decoration_cycles
            data["房屋来源"] = house_source_cn
            data["公寓类型"] = house_apartment_type_cn
            data["合同类型"] = house_entrust_type_cn
            data["委托类型"] = house_contract_type_cn
            data['房源方'] = house_source_us_uname
            data['房源方部门'] = house_source_us_dname
            house_contract_info.append(data)

        # 每一条出单的利润业绩
        profit_info = []
        for i in range(len(achievement_issue_info_list)):
            data = {}
            data["月租金成本"] = achievement_issue_info_list[i]["profit_rent_month"]
            data["月装修成本"] = achievement_issue_info_list[i]["profit_decoration_month"]
            data["月资金成本"] = achievement_issue_info_list[i]["profit_capital_month"]
            data["月渠道成本"] = achievement_issue_info_list[i]["profit_channel_month"]
            data["出租总价"] = achievement_issue_info_list[i]["profit_rent_total"]
            data["收房总价"] = achievement_issue_info_list[i]["profit_inhouse_total"]
            data["装修总价"] = achievement_issue_info_list[i]["profit_decoration_total"]
            data["成本总价"] = achievement_issue_info_list[i]["profit_cost_total"]
            data["差价业绩"] = achievement_issue_info_list[i]["profit_diff"]
            profit_info.append(data)

        # 每一条出单的核算业绩
        adjust_info = []
        for i in range(len(achievement_issue_info_list)):
            data = {}
            data["核算免租期"] = achievement_issue_info_list[i]["adjust_free_days"]
            data["委托年限"] = achievement_issue_info_list[i]["adjust_house_year"]
            data["委托年限加成"] = achievement_issue_info_list[i]["adjust_house_year_add"]
            data["委托付款周期"] = achievement_issue_info_list[i]["adjust_pay_cycle"]
            data["付款周期加成"] = achievement_issue_info_list[i]["adjust_pay_cycle_add"]
            data["业绩核算系数"] = achievement_issue_info_list[i]["adjust_ratio_percent"]
            data["核算业绩"] = achievement_issue_info_list[i]["adjust_achievement"]
            adjust_info.append(data)

        # 每一条出单业绩对应的业绩分成信息
        divides_info = []
        for i in range(len(achievement_issue_info_list)):
            data = {}
            create_time = []
            divide_type_cn = []
            divide_dname = []
            divide_uname = []
            divide_post = []
            up_level_store_manager_name = []
            up_level_dist_manager_name = []
            accounting_time = []
            divided_money = []

            for j in range(len(achievement_issue_info_list[i]['divides'])):
                create_time.append(achievement_issue_info_list[i]['divides'][j]['create_time'])
                divide_type_cn.append(achievement_issue_info_list[i]['divides'][j]['divide_type_cn'])
                divide_dname.append(achievement_issue_info_list[i]['divides'][j]['divide_dname'])
                divide_post.append(achievement_issue_info_list[i]['divides'][j]['divide_post'])
                divide_uname.append(achievement_issue_info_list[i]['divides'][j]['divide_uname'])
                up_level_store_manager_name.append(
                    achievement_issue_info_list[i]['divides'][j]['up_level_store_manager_name'])
                up_level_dist_manager_name.append(
                    achievement_issue_info_list[i]['divides'][j]['up_level_dist_manager_name'])
                accounting_time.append(achievement_issue_info_list[i]['divides'][j]['accounting_month'])
                divided_money.append(achievement_issue_info_list[i]['divides'][j]['divided_money'])

            data["创建日期"] = create_time
            data["分成方"] = divide_type_cn
            data["部门"] = divide_dname
            data["员工"] = divide_uname
            data["岗位"] = divide_post
            data["上级店经理"] = up_level_store_manager_name
            data["上级区经理"] = up_level_dist_manager_name
            data['业绩金额'] = divided_money
            data["核发月份"] = accounting_time

            divides_info.append(data)

        issue_info = {}
        issue_info['出租合同信息'] = apartment_contract_info
        issue_info['委托合同信息'] = house_contract_info
        issue_info['利润业绩'] = profit_info
        issue_info['核算业绩'] = adjust_info
        issue_info['业绩分成'] = divides_info

        base.consoleLog('出单业绩详情返回值：' + str(issue_info))

        return issue_info

    def serach_issue_list(self, serach_tiao_jian, perPageSize=10000,value=True):
        """
        出单业绩列表搜索
        :param serach_tiao_jian
        :param perPageSize:
        :param value True返回的数据包含第一行
        :return:搜索结果，按列表每个字段集合返回
        """
        base.consoleLog('查询出单业绩详情。')
        null = None

        url = 'http://erp.ishangzu.com/isz_achievement/issueAchieve/list'
        data = {
            "query_apartment": serach_tiao_jian['楼盘名称房源编号'],
            "building_name": serach_tiao_jian['栋座'],
            "unit": serach_tiao_jian['单元'],
            "house_no": serach_tiao_jian['房号'],
            "contract_num": serach_tiao_jian['出租合同号'],
            "is_active": serach_tiao_jian['状态'],
            "apartment_contract_type": serach_tiao_jian['承租类别'],
            "contract_audit_status": serach_tiao_jian['合同复审状态'],
            "frist_pay_status": serach_tiao_jian['首期款收款状态'],
            "apartment_type": serach_tiao_jian['公寓类型'],
            "apartment_entrust_type": serach_tiao_jian['合同类型'],
            "audit_status": serach_tiao_jian['审核状态'],
            "rent_times": serach_tiao_jian['出租次数'],
            "divide_house_source_us_did": serach_tiao_jian['房源方部门'],
            "divide_house_source_us_uname": serach_tiao_jian['房源方'],
            "apartment_customer_source_did": serach_tiao_jian['客源方部门'],
            "apartment_customer_source_uname": serach_tiao_jian['客源方'],
            "contract_commit_date_start": serach_tiao_jian['合同提交日期起始'],
            "contract_commit_date_end": serach_tiao_jian['合同提交日期结束'],
            "active_time_start": serach_tiao_jian['生效日期起始'],
            "active_time_end": serach_tiao_jian['生效日期结束'],
            "accounting_month_start": serach_tiao_jian['核发月份起始'],
            "accounting_month_end": serach_tiao_jian['核发月份结束'],
            "contract_audit_time_start": serach_tiao_jian['复审日期起始'],
            "contract_audit_time_end": serach_tiao_jian['复审日期结束'],
            "orderArr": null,
            "sortArr": null,
            "pageNum": 1,
            "perPageSize": perPageSize
        }
        base.consoleLog(data)
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog('出单业绩列表查询报错' + str(result))
            return

        issue_info_list = {}
        list = result['obj']['rows']
        base.consoleLog(list)

        # 处理返回的数据。按照返回的值分类。
        property_name = []
        apartment_code = []
        apartment_contract_num = []
        is_active_cn = []
        apartment_contract_type_cn = []
        contract_audit_status_cn = []
        frist_pay_status_cn = []
        apartment_type_cn = []
        apartment_entrust_type_cn = []
        audit_status_cn = []
        house_rent_times_cn = []
        house_source_us_dname = []
        house_source_us_uname = []
        apartment_customer_source_dname = []
        apartment_customer_source_uname = []
        apartment_contract_commit_date = []
        active_time = []
        accounting_month = []
        contract_audit_time = []
        profit_diff = []
        adjust_achievement = []
        if value:
            for i in range(len(list)):
                property_name.append(list[i]['property_name'])
                apartment_code.append(list[i]['apartment_code'])
                apartment_contract_num.append(list[i]['apartment_contract_num'])
                is_active_cn.append(list[i]['is_active_cn'])
                apartment_contract_type_cn.append(list[i]['apartment_contract_type_cn'])
                contract_audit_status_cn.append(list[i]['contract_audit_status_cn'])
                frist_pay_status_cn.append(list[i]['frist_pay_status_cn'])
                apartment_type_cn.append(list[i]['apartment_type_cn'])
                apartment_entrust_type_cn.append(list[i]['apartment_entrust_type_cn'])
                audit_status_cn.append(list[i]['audit_status_cn'])
                house_rent_times_cn.append(list[i]['house_rent_times_cn'])
                house_source_us_dname.append(list[i]['divide_house_source_us_dname'])
                house_source_us_uname.append(list[i]['divide_house_source_us_uname'])
                apartment_customer_source_dname.append(list[i]['apartment_customer_source_dname'])
                apartment_customer_source_uname.append(list[i]['apartment_customer_source_uname'])
                apartment_contract_commit_date.append(list[i]['apartment_contract_commit_date'])
                active_time.append(list[i]['active_time'])
                accounting_month.append(list[i]['accounting_month'])
                contract_audit_time.append(list[i]['contract_audit_time'])
                profit_diff.append(list[i]['profit_diff'])
                adjust_achievement.append(list[i]['adjust_achievement'])
        else:
            for i in range(1,len(list)):
                property_name.append(list[i]['property_name'])
                apartment_code.append(list[i]['apartment_code'])
                apartment_contract_num.append(list[i]['apartment_contract_num'])
                is_active_cn.append(list[i]['is_active_cn'])
                apartment_contract_type_cn.append(list[i]['apartment_contract_type_cn'])
                contract_audit_status_cn.append(list[i]['contract_audit_status_cn'])
                frist_pay_status_cn.append(list[i]['frist_pay_status_cn'])
                apartment_type_cn.append(list[i]['apartment_type_cn'])
                apartment_entrust_type_cn.append(list[i]['apartment_entrust_type_cn'])
                audit_status_cn.append(list[i]['audit_status_cn'])
                house_rent_times_cn.append(list[i]['house_rent_times_cn'])
                house_source_us_dname.append(list[i]['divide_house_source_us_dname'])
                house_source_us_uname.append(list[i]['divide_house_source_us_uname'])
                apartment_customer_source_dname.append(list[i]['apartment_customer_source_dname'])
                apartment_customer_source_uname.append(list[i]['apartment_customer_source_uname'])
                apartment_contract_commit_date.append(list[i]['apartment_contract_commit_date'])
                active_time.append(list[i]['active_time'])
                accounting_month.append(list[i]['accounting_month'])
                contract_audit_time.append(list[i]['contract_audit_time'])
                profit_diff.append(list[i]['profit_diff'])
                adjust_achievement.append(list[i]['adjust_achievement'])

        issue_info_list['楼盘地址'] = property_name
        issue_info_list['房源编号'] = apartment_code
        issue_info_list['出租合同号'] = apartment_contract_num
        issue_info_list['状态'] = is_active_cn
        issue_info_list['承租类别'] = apartment_contract_type_cn
        issue_info_list['合同复审状态'] = contract_audit_status_cn
        issue_info_list['首期款收款状态'] = frist_pay_status_cn
        issue_info_list['公寓类型'] = apartment_type_cn
        issue_info_list['合同类型'] = apartment_entrust_type_cn
        issue_info_list['审核状态'] = audit_status_cn
        issue_info_list['出租次数'] = house_rent_times_cn
        issue_info_list['房源方部门'] = house_source_us_dname
        issue_info_list['房源方'] = house_source_us_uname
        issue_info_list['客源方部门'] = apartment_customer_source_dname
        issue_info_list['客源方'] = apartment_customer_source_uname
        issue_info_list['合同提交日'] = apartment_contract_commit_date
        issue_info_list['生效日期'] = active_time
        issue_info_list['核发月份'] = accounting_month
        issue_info_list['复审日期'] = contract_audit_time
        issue_info_list['利润业绩'] = profit_diff
        issue_info_list['核算业绩'] = adjust_achievement

        base.consoleLog('出单业绩列表字段数据返回：' + str(issue_info_list))
        return issue_info_list

    def serach_divide_into_list(self, serach_tiao_jian, perPageSize=10000):
        """
        预估业绩排行榜---业绩分成搜索
        :param:serach_tiao_jian 查询条件
        :param perPageSize 查询的最大条数
        :return:
        """
        base.consoleLog('查询预估业绩排行榜---业绩分成')

        url = 'http://erp.ishangzu.com/isz_achievement/rankAchieve/divide/estimate'
        data = {
            "query_apartment": serach_tiao_jian['楼盘名称房源编号'],
            "building_name": serach_tiao_jian['栋座'],
            "unit": serach_tiao_jian['单元'],
            "house_no": serach_tiao_jian['房号'],
            "contract_num": serach_tiao_jian['委托合同号出租合同号'],
            "is_active": serach_tiao_jian['状态'],
            "achievement_type": serach_tiao_jian['业绩类型'],
            "type": serach_tiao_jian['分类'],
            "house_apartment_type": serach_tiao_jian['公寓类型'],
            "house_entrust_type": serach_tiao_jian['合同类型'],
            "divide_did": serach_tiao_jian['分成部门'],
            "divide_uname": serach_tiao_jian['分成人'],
            "audit_status": serach_tiao_jian['审核状态'],
            "contract_commit_date_start": serach_tiao_jian['提交日期起始'],
            "contract_commit_date_end": serach_tiao_jian['提交日期结束'],
            "active_time_start": serach_tiao_jian['生效日期起始'],
            "active_time_end": serach_tiao_jian['生效日期结束'],
            "accounting_month_start": serach_tiao_jian['核发月份起始'],
            "accounting_month_end": serach_tiao_jian['核发月份结束'],
            "orderArr": '',
            "sortArr": '',
            "pageNum": 1,
            "perPageSize": perPageSize,
            "tableFilter": ''
        }
        base.consoleLog(data)
        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog(str(result))
            return

        divide_into = {}
        list = result['obj']['rows']
        base.consoleLog(str(list))

        # 处理返回的数据。按照返回的值分类
        property_name = []
        apartment_code = []
        house_contract_num = []
        apartment_contract_num = []
        is_active = []
        achievement_type_cn = []
        type_cn = []
        house_apartment_type_cn = []
        house_entrust_type_cn = []
        divide_dname = []
        divide_uname = []
        audit_status_cn = []
        contract_commit_date = []
        active_time = []
        accounting_month = []
        xxCycles = []
        divide_type_cn = []
        divided_money = []
        for i in range(len(list)):
            property_name.append(list[i]['property_name'])
            apartment_code.append(list[i]['apartment_code'])
            house_contract_num.append(list[i]['house_contract_num'])
            apartment_contract_num.append(list[i]['apartment_contract_num'])
            is_active.append(list[i]['is_active_cn'])
            achievement_type_cn.append(list[i]['achievement_type_cn'])
            type_cn.append(list[i]['type_cn'])
            house_apartment_type_cn.append(list[i]['house_apartment_type_cn'])
            house_entrust_type_cn.append(list[i]['house_entrust_type_cn'])
            divide_dname.append(list[i]['divide_dname'])
            divide_uname.append(list[i]['divide_uname'])
            audit_status_cn.append(list[i]['audit_status_cn'])
            contract_commit_date.append(list[i]['contract_commit_date'])
            active_time.append(list[i]['active_time'])
            accounting_month.append(list[i]['accounting_month'])
            xxCycles.append(list[i]['xxCycles'])
            divide_type_cn.append(list[i]['divide_type_cn'])
            divided_money.append(list[i]['divided_money'])
        divide_into['物业地址'] = property_name
        divide_into['房源编号'] = apartment_code
        divide_into['委托合同号'] = house_contract_num
        divide_into['出租合同号'] = apartment_contract_num
        divide_into['状态'] = is_active
        divide_into['业绩类型'] = achievement_type_cn
        divide_into['分类'] = type_cn
        divide_into['公寓类型'] = house_apartment_type_cn
        divide_into['合同类型'] = house_entrust_type_cn
        divide_into['分成部门'] = divide_dname
        divide_into['分成人'] = divide_uname
        divide_into['审核状态'] = audit_status_cn
        divide_into['提交日期'] = contract_commit_date
        divide_into['生效日期'] = active_time
        divide_into['核发月份'] = accounting_month
        divide_into['核算周期'] = xxCycles
        divide_into['分成方'] = divide_type_cn
        divide_into['核算业绩'] = divided_money
        base.consoleLog('预估排行榜业绩分成数据返回: ' + str(divide_into))
        return divide_into

    def serach_department_summary_list(self, serach_tiao_jian, perPageSize=10000):
        """
        预估业绩-部门汇总查询
        :param serach_tiao_jian:
        :param perPageSize:
        :return:
        """
        base.consoleLog('预估业绩-部门汇总查询')

        url = 'http://erp.ishangzu.com/isz_achievement/rankAchieve/depart/estimate'
        data = {
            "divide_level": serach_tiao_jian['部门层级'],
            "house_apartment_type": serach_tiao_jian['公寓类型'],
            "house_entrust_type": serach_tiao_jian['合同类型'],
            "accounting_status": serach_tiao_jian['核发状态'],
            "contract_commit_date_start": serach_tiao_jian['提交日期起始'],
            "apartment_contract_commit_date": serach_tiao_jian['提交日期结束'],
            "accounting_month_start": serach_tiao_jian['核发月份起始'],
            "accounting_month_end": serach_tiao_jian['核发月份结束'],
            "orderArr": serach_tiao_jian[''],
            "sortArr": serach_tiao_jian[''],
            "pageNum": 1,
            "perPageSize": perPageSize
        }

        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog(str(result))
            return

        department_summary = {}
        list = result['obj']['rows']

        index = []
        depart_name = []
        manager_name = []
        depart_num = []
        issue_achieve = []
        issue_achieve_num = []
        breach_achieve = []
        loss_achieve = []
        total_achieve = []

        for i in range(len(list)):
            index.append(list[i]['index'])
            depart_name.append(list[i]['depart_name'])
            manager_name.append(list[i]['manager_name'])
            depart_num.append(list[i]['depart_num'])
            issue_achieve.append(list[i]['issue_achieve'])
            issue_achieve_num.append(list[i]['issue_achieve_num'])
            breach_achieve.append(list[i]['breach_achieve'])
            loss_achieve.append(list[i]['loss_achieve'])
            total_achieve.append(list[i]['total_achieve'])

        department_summary['名次'] = index
        department_summary['部门名称'] = depart_name
        department_summary['负责人'] = manager_name
        department_summary['人数'] = depart_num
        department_summary['出单业绩'] = issue_achieve
        department_summary['单数'] = issue_achieve_num
        department_summary['违约业绩'] = breach_achieve
        department_summary['亏损业绩'] = loss_achieve
        department_summary['总业绩'] = total_achieve

        return department_summary

    def serach_personal_summary_list(self, serach_tiao_jian, perPageSize=10000):
        """
        预估业绩-个人汇总查询
        :param serach_tiao_jian:
        :param perPageSize:
        :return:
        """
        base.consoleLog('预估业绩-个人汇总查询')

        url = 'http://erp.ishangzu.com/isz_achievement/rankAchieve/person/estimate'
        data = {
            "user_status": serach_tiao_jian['在职状态'],
            "house_apartment_type": serach_tiao_jian['公寓类型'],
            "house_entrust_type": serach_tiao_jian['合同类型'],
            "accounting_status": serach_tiao_jian['核发状态'],
            "current_depart_id": serach_tiao_jian['当前部门'],
            "divide_uname": serach_tiao_jian['姓名'],
            "contract_commit_date_start": serach_tiao_jian['提交日期起始'],
            "contract_commit_date_end": serach_tiao_jian['提交日期结束'],
            "accounting_month_start": serach_tiao_jian['核发月份起始'],
            "accounting_month_end": serach_tiao_jian['核发月份结束'],
            "orderArr": '',
            "sortArr": '',
            "pageNum": 1,
            "perPageSize": perPageSize
        }

        result = interface.myRequest(url, data)
        if result['code'] != 0:
            base.consoleLog( str(result))
            return

        personal_summary = {}
        list = result['obj']['rows']

        index = []
        name = []
        current_depart_name = []
        user_status_cn = []
        issue_achieve = []
        issue_achieve_num = []
        breach_achieve = []
        loss_achieve = []
        total_achieve = []

        for i in range(len(list)):
            index.append(list[i]['index'])
            name.append(list[i]['name'])
            current_depart_name.append(list[i]['current_depart_name'])
            user_status_cn.append(list[i]['user_status_cn'])
            issue_achieve.append(list[i]['issue_achieve'])
            issue_achieve_num.append(list[i]['issue_achieve_num'])
            breach_achieve.append(list[i]['breach_achieve'])
            loss_achieve.append(list[i]['loss_achieve'])
            total_achieve.append(list[i]['total_achieve'])

        personal_summary['名次'] = index
        personal_summary['姓名'] = name
        personal_summary['当前部门'] = current_depart_name
        personal_summary['在职状态'] = user_status_cn
        personal_summary['出单业绩'] = issue_achieve
        personal_summary['单数'] = issue_achieve_num
        personal_summary['违约业绩'] = breach_achieve
        personal_summary['亏损业绩'] = loss_achieve
        personal_summary['总业绩'] = total_achieve

        return personal_summary

    def update_issue_audit_status(self):
        """
        更新业绩审核状态
        :return:
        """
        base.consoleLog('更新业绩审核状态。出租合同。' + self.contract_num)

        url = 'http://erp.ishangzu.com/isz_achievement/issueAchieve/audite'

        sql = "SELECT achievement_issue_id from achievement_issue where apartment_contract_num='%s' and deleted=0" % self.contract_num
        achievement_issue_id = base.searchSQL(sql)

        for i in range(len(achievement_issue_id[0])):
            data = {"achievement_issue_id": achievement_issue_id[0][i], "content": "审核业绩"}
            result = interface.myRequest(url, data)
            if result['code'] == 0:
                base.consoleLog('业绩状态更新成已审核~~')
            else:
                base.consoleLog(str(result))
        return

    def issue_reaccounting(self):
        """
        业绩重新核算
        :return:
        """
        base.consoleLog('业绩重新核算')

        url = 'http://erp.ishangzu.com/isz_achievement/issueAchieve/adjustAchieve/'

        sql = "SELECT achievement_issue_id from achievement_issue where apartment_contract_num='%s' and deleted=0" % self.contract_num
        achievement_issue_id = base.searchSQL(sql)

        for i in range(len(achievement_issue_id[0])):
            result = interface.myRequest(url+str(achievement_issue_id[0][i]), method='get')
            if result['code'] == 0:
                base.consoleLog('业绩重新核算成功~~')
            else:
                base.consoleLog(str(result))
        return



