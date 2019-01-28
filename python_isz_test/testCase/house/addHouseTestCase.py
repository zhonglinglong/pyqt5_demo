#-*- coding: utf-8 -*-
# @Time   : 2019/1/16 10:33
# @Author : linglong
# @File   : addHouseTestCase.py

import unittest
from time import sleep

from common import base
from iszErpRequest.houseDevelopRequest import HouseDelelop


class TestAddHouse(unittest.TestCase):
    """新增房源"""
    def setUp(self):
        base.consoleLog('')
        base.consoleLog('*********************新增单元测试开始*************************************')

    def tearDown(self):
        base.consoleLog("""*******************新增单元测试结束****************************************""")
        base.consoleLog("")

    def test_1(self):
        """测试1"""
        result = HouseDelelop('zll测试专用').add_house_delelop()
        sleep(60)
        self.assertEqual(result,None,msg=result)
    def test_2(self):
        """测试2"""
        result = HouseDelelop('zll测试专用').add_house_delelop()
        self.assertEqual(result,None,msg=result)

    def test_3(self):
        """测试3"""
        result = HouseDelelop('zll测试专用').add_house_delelop()
        self.assertEqual(result,None,msg=result)


if __name__ == "__main__":
    unittest.main()