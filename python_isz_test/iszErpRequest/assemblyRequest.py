# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年5月31日21:20:22
爱上租ERP组件接口,如 solr，ES,
"""

from common import interface
from common import base
import requests


class SolrEs:
    def __init__(self,core='apartment',number=-1):
        """

        :param core: 刷新页面
        :param number: 天数
        """
        self.core = core
        self.number = number
    def solr(self):
        """
            房源的solr增量或者全量
            :param core: 目前为house或者apartment
            :return: 执行结果
            """
        base.consoleLog('solr。数据源：' + self.core)

        url = {
            'house':'http://192.168.0.216:8080/solr/apartment_core/dataimport',
            'apartment':'http://192.168.0.203:8080/solr/apartment_core/dataimport'
        }
        data = 'command=delta-import&commit=true&wt=json&indent=true&verbose=false&clean=false&optimize=false&debug=false'
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
        }

        try:
            re = requests.post(url[self.core], data, headers=headers)
        except Exception as e:
            base.consoleLog("solr接口查询异常。错误返回：" + str(e),'e')
            return "solr接口查询异常。错误返回：" + str(e)

        if re.status_code is 200:
            base.consoleLog("执行" + self.core + "solr增量成功！")
            return
        else:
            base.consoleLog("执行" + self.core + "solr增量失败！ 错误返回：" + str(re.text))
            return "执行" + self.core + "solr增量失败！ 错误返回：" + str(re.text)

    def ES_house_contract(self):
        """
        ES委托合同列表数据更新
        :param number:
        :return:
        """
        base.consoleLog('ES委托合同列表数据更新。刷新起始日：' + base.now_time(self.number) + " 00:00:01")

        url = "http://isz.ishangzu.com/isz_base/EsController/update.action"
        data = {"time": base.now_time(self.number) + " 00:00:01", "index": "house_contract_type"}
        result = interface.myRequest(url, str(data))
        if result['code'] == 0:
            base.consoleLog("委托合同列表ES数据查询成功！")
            return
        else:
            base.consoleLog("委托合同列表ES数据查询不成功，结果返回：" + str(result))
            return "委托合同列表ES数据查询不成功，结果返回：" + str(result)


    def ES_apartment_contract(self):
        """
        ES出租合同列表数据更新
        :param number:
        :return:
        """
        base.consoleLog('ES出租合同列表数据更新。刷新起始日：' + base.now_time(self.number) + " 00:00:01")
        url = "http://isz.ishangzu.com/isz_base/EsController/update.action"
        data = {"time": base.now_time(self.number) + " 00:00:01", "index": "apartment_contract_type"}
        result = interface.myRequest(url, str(data))
        if result['code'] == 0:
            base.consoleLog("出租合同列表ES数据查询成功！")
            return
        else:
            base.consoleLog("出租合同列表ES数据查询不成功，结果返回：" + str(result))
            return "出租合同列表ES数据查询不成功，结果返回：" + str(result)








