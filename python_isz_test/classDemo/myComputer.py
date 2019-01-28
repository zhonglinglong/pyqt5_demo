#-*- coding: utf-8 -*-
# @Time   : 2019/1/10 15:27
# @Author : linglong
# @File   : myComputer.py
import subprocess


class NewCmd(object):
    def __init__(self,cmd=None):
        """
        初始化
        :param cmd: cmd命令行
        """
        self.cmd = cmd

    def getCpuID(self):
        """
        获取当前电脑ProcessorID
        :return: ProcessorID
        """
        p = subprocess.check_output('wmic CPU get ProcessorID')
        ProcessorID = str(p).split('\\r\\r\\n')[1].strip()
        return ProcessorID

    def getMAC(self):
        """
        获取当前电脑的物理地址
        :return:物理地址
        """
        p = subprocess.check_output('getmac')
        return p.decode('gbk')[154:171]

    def get_value(self):
        """
        输入cmd命令获取返回结果
        :return:
        """
        p = subprocess.check_output(self.cmd)
        return p.decode('gbk')

# t = NewCmd()
# print(t.getCpuID())
# print(t.getMAC())
# t.cmd='ipconfig'
# print(t.get_value())