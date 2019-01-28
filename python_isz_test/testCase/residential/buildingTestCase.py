#-*- coding: utf-8 -*-
# @Time   : 2019/1/16 10:26
# @Author : linglong
# @File   : buildingTestCase.py
import unittest

from common import base
from iszErpRequest.residentialRequest import Residential


class TestBuilding(unittest.TestCase):

    def setUp(self):
        base.consoleLog('')
        base.consoleLog('*********************新增幢测试开始*************************************')

    def tearDown(self):
        base.consoleLog("""*******************新增幢测试结束****************************************""")
        base.consoleLog("")

    def test_1(self):
        """测试1"""
        result = Residential('楼盘','幢',1,1,1,1).add_building()
        self.assertEqual(result,None,msg=result)
    def test_2(self):
        """测试2"""
        result = Residential('楼盘','幢',1,1,1,1).add_building()
        self.assertEqual(result,None,msg=result)

    def test_3(self):
        """测试3"""
        result = Residential('楼盘','幢',1,1,1,1).add_building()
        self.assertEqual(result,None,msg=result)


if __name__ == "__main__":
    unittest.main()