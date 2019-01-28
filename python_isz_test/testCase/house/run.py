#-*- coding:utf-8 -*-
import os
import sys
import unittest,time

from classDemo.myEmail import NewEmail
from common.HTMLTestReportCN import HTMLTestRunner
# test_dir = "./"
# discover = unittest.defaultTestLoader.discover(test_dir,pattern="*testCase.py")
discover = unittest.defaultTestLoader.discover("D:\Python3.7\python_isz_test\\testCase\\house\\", pattern="*testCase.py")
path = "os.path.dirname(os.path.realpath(__file__))=%s" % os.path.dirname(os.path.realpath(__file__))  # 当前目录的路径



if __name__ == "__main__":
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = "D:\Python3.7\python_isz_test\\testCase\\house\\" + now + "resourceTransfer.html"

    fp = open(filename,"wb")
    runner = HTMLTestRunner(stream=fp,title="测试报告",description="用例执行情况：")
    print(discover)
    runner.run(discover)
    fp.close()
    # NewEmail(html_path=filename)
    print(sys.path)