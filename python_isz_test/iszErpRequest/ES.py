#-*- coding: utf-8 -*-
# @Time   : 2019/1/15 17:27
# @Author : linglong
# @File   : ES.py
from time import sleep

from classDemo.myTime import NewTime
from classDemo.getCookie import get_cookie
from classDemo.myRequest import NewRequest


get_cookie("18279881085","a123456789")
url = "http://isz.ishangzu.com/isz_base/EsController/update.action"


for i in range(15):
    print('                    ')
    time = NewTime().now_month(i-14) + " 00:00:00"
    end_time = NewTime().now_month(i-13) + " 00:00:00"
    data = {"time": time, "end_time": end_time, "index":"apartment_contract_type"}
    result = NewRequest(url,data).post()
    print(result)
    try:
        if result['code'] == -1:
            sleep(300)
            result = NewRequest(url,data).post()
        else:
            pass
    except BaseException as e:
        print(str(e))
        pass