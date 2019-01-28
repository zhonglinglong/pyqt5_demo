#-*- coding: utf-8 -*-
# @Time   : 2019/1/10 9:55
# @Author : linglong
# @File   : myConfigparser.py

import configparser
#os.path.join(os.path.split(os.path.realpath(__file__))[0]) 当前文件所在文件夹的绝对路径

class NewConfigparser(object):
    """
    读写.ini后缀文件的类
    """
    def __init__(self,section,path='D:\\Python3.7\\python_isz_test\\common\\conf.ini'):
        """
        初始化值
        :param path: 配置文件的相对路径或者绝对路径
        :param section: 配置文件中的节点
        """
        self.path = path
        self.section = section

    def get_conf(self,option,valueType='str'):
        """
        获取配置文件的值
        :param option:节点下对应的key
        :param valueType:获取值的类型,默认为字符串
        :return:key对应的value
        """
        config = configparser.RawConfigParser()
        config.read(self.path, encoding="gbk")
        try:
            if valueType is str:
                value = config.get(self.section, option)
                return value
            elif valueType is int:
                value = config.getint(self.section, option)
                return value
            elif valueType is bool:
                value = config.getboolean(self.section, option)
                return value
            elif valueType is float:
                value = config.getfloat(self.section, option)
                return value
            else:
                value = config.get(self.section, option)
                return value
        except Exception as e:
            return str(e)

    def set_conf(self,**kwargs):
        """
        把数据写入配置文件
        :param kwargs: 要写入的key和value
        :return:
        """
        config = configparser.ConfigParser()
        try:
            print(self.path,self.section)
            config.read(self.path, encoding="gbk")
            for k,v in kwargs.items():
                config.set(self.section, str(k), str(v))
                config.write(open(self.path, 'w'))
        except BaseException as e:
            return str(e)
        return


# test = NewConfigparser('.//conf.ini','new')
# print(test.get_conf('test'))
# test.section='news'
# print(test.set_conf(test='~12212~',zll='ll2222l'))