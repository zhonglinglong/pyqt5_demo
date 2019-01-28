#-*- coding: utf-8 -*-
# @Time   : 2019/1/16 10:31
# @Author : linglong
# @File   : unitTestCase.py

import unittest

from common import base
from iszErpRequest.residentialRequest import Residential


class TestUnit(unittest.TestCase):

    def setUp(self):
        base.consoleLog('')
        base.consoleLog('*********************新增单元测试开始*************************************')

    def tearDown(self):
        base.consoleLog("""*******************新增单元测试结束****************************************""")
        base.consoleLog("")

    def test_1(self):
        """测试1"""
        result = Residential('楼盘','幢','单元',1,1,1).add_unit()
        self.assertEqual(result,None,msg=result)
    def test_2(self):
        """测试2"""
        result = Residential('楼盘','幢','单元',1,1,1).add_unit()
        self.assertEqual(result,None,msg=result)

    def test_3(self):
        """测试3"""
        result = Residential('楼盘','幢','单元',1,1,1).add_unit()
        self.assertEqual(result,None,msg=result)


if __name__ == "__main__":
    unittest.main()