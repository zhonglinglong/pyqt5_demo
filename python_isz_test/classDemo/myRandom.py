# -*- coding: utf-8 -*-
# @Time   : 2019/1/11 16:33
# @Author : linglong
# @File   : myRandom.py

import random


class NewRandom(object):
    def __init__(self):
        """初始化有效的生成手机号码"""
        self.phone = random.choice(["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
                      "153", "155", "156", "157", "158", "159", "182", "186", "187", "188"]) + "".join(
            random.choice("0123456789") for i in range(8))
    def randome_string(self,**kwargs):
        req = {}
        for k,v in kwargs.items():
            re = []
            if k =='int':
                x = "".join(random.choice("0123456789") for i in range(v))
                re.append(x)
            elif k =='str':
                y = "".join(random.choice("qwertyuiopasdfghjklzxcvbnm") for i in range(v))
                re.append(y)
            elif k =='value':
                z = "".join(random.choice("QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm0123456789") for i in range(v))
                re.append(z)
            else:
                re.append('没有这个键')
            req[k] = re
        return req

# t = NewRandom()
# print(t.phone)
# print(t.randome_string(int=4,str=8,value=13,t=2))

