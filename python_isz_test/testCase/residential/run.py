#-*- coding:utf-8 -*-
import os
import unittest,time

from classDemo.myEmail import NewEmail
from common.HTMLTestReportCN import HTMLTestRunner
test_dir = "./"
discover = unittest.defaultTestLoader.discover(test_dir,pattern="*TestCase*")
path = "os.path.dirname(os.path.realpath(__file__))=%s" % os.path.dirname(os.path.realpath(__file__))  # 当前目录的路径



if __name__ == "__main__":
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = test_dir + '/' + now + "resourceTransfer.html"

    fp = open(filename,"wb")
    runner = HTMLTestRunner(stream=fp,title="测试报告",description="用例执行情况：")
    print(discover)
    runner.run(discover)
    fp.close()
    # NewEmail(html_path=path.split('=')[1]+"\\"+ filename.split(".//")[1])
