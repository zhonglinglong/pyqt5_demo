# -*- coding: utf-8 -*-
# @Time   : 2019/1/11 10:45
# @Author : linglong
# @File   : myRequest.py
import json

import requests
from classDemo.myConfigparser import NewConfigparser
from classDemo.loginRequest import Login
from classDemo.getCookie import get_cookie


class NewRequest(object):
    def __init__(self, url, data=None):
        self.headers = {
            'content-type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
        }
        self.cookie = eval(NewConfigparser('cookieInfo').get_conf('cookie'))
        self.url = url
        self.data = data

    def post(self):
        """
        post 请求,如果登录失效,重新登录一次,然后重新请求一次
        :return:
        """
        req = requests.post(
            url=self.url, headers=self.headers, cookies=self.cookie,
            data=json.dumps(self.data) if isinstance(self.data, dict) else self.data
        ).text
        try:
            if json.loads(req)['msg'] in ('登陆状态失效请重新登陆', '用户未登录，请先登录系统。'):
                user_info = NewConfigparser('loginUser')
                get_cookie(user_info.get_conf('user'), user_info.get_conf('pwd'))
            req = requests.post(
                url=self.url, headers=self.headers, cookies=eval(NewConfigparser('cookieInfo').get_conf('cookie')),
                data=json.dumps(self.data) if isinstance(self.data, dict) else self.data
            ).text
        except BaseException as e:
            return str(e)
        return json.loads(req)

    def get(self):
        """
        get 请求,如果登录失效,重新登录一次,然后重新请求一次
        :return:
        """
        req = requests.get(
            url=self.url, headers=self.headers, cookies=self.cookie).text
        try:
            if json.loads(req)['msg'] in ('登陆状态失效请重新登陆', '用户未登录，请先登录系统。'):
                user_info = NewConfigparser('loginUser')
                get_cookie(user_info.get_conf('user'), user_info.get_conf('pwd'))
            req = requests.get(
                url=self.url, headers=self.headers, cookies=eval(NewConfigparser('cookieInfo').get_conf('cookie'))).text
        except BaseException as e:
            return str(e)
        return json.loads(req)

#
# t = NewRequest('http://erp.ishangzu.com/isz_housecontract/houseContractController/searchHouseContractInfo/FF80808168290CB201682C8391A10199')
# a = t.get()
# print(a)
# t.url = 'http://erp.ishangzu.com/isz_housecontract/houseContractController/searchHouseContractListByEs'
# t.data = {"residential_name":"","building_name":"","unit":"","house_no":"","contract_num":"","sign_did":"","sign_did_name":"","sign_uid":"","sign_user_name":"","contract_type":"","entrust_type":"","apartment_type":"","contract_status_list":[],"audit_status_list":[],"sign_body_list":[],"server_manage_did":"","server_manage_did_name":"","server_manage_uid":"","server_manage_user_name":"","create_date_start":"","create_date_end":"","sign_date_start":"","sign_date_end":"","entrust_end_date_start":"","entrust_end_date_end":"","real_due_date_start":"","real_due_date_end":"","owner_sign_date_start":"","owner_sign_date_end":"","is_electron":"","order":"","sort":"","sign_user_num":"","pageNumber":1,"pageSize":30}
# b = t.post()
# print(b)