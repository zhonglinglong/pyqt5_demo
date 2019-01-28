#-*- coding:utf-8 -*-

import configparser
import os

import datetime
import zipfile
import os.path
import time
import logging
import random

log_name = time.strftime("%Y-%m")
logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)
path = os.path.dirname(
    os.path.join(
        os.path.split(
            os.path.realpath(__file__))[0])) + '\\%sautotest.log' % log_name
fileHandler = logging.FileHandler(path)
consoleHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(process)s - %(levelname)s : %(message)s')
fileHandler.setFormatter(formatter)
consoleHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)


def log(func):
    def wrapper(*args, **kwargs):
        info = func.__name__
        logger.info('调用函数名称 : %s' % info)
        return
        # try:
        #     return func(*args, **kwargs)
        # except BaseException:
        #     consoleLog(func.__name__, level='e', fromAssert=False)
        #     pass
    return wrapper()

def consoleLog(msg, level='i', fromAssert=True):
    """
    对错误的记录，写进log文件中，对于error级别的适用于断言，如存在这种用例：删除合同后，判断合同表中的deleted的字段是否为1或者再查询，是否还能查到，此时，如果不为1或者还能查到
    则调用此方法，定义为error级别
    :param msg: 需要写入的描述，如’合同删除后deleted未变成0‘
    :param level: 定义日志级别，分为i:info  w:warning  e:error
    """
    if level is 'i':
        logger.info(msg)
    elif level is 'w':
        logger.warning(msg)
    elif level is 'e':
        if fromAssert:
            logger.error('one assert at : \n%s\n' % msg)
        else:
            logger.error('======================================== one error at "%s" ========================================' % msg)

def get_conf(section, option, valueType=str):
    """
    获取配置文件值
    :param section: 配置文件的片段
    :param option: 配置文件对应的key
    :param valueType: 默认值
    :return:
    """
    config = configparser.RawConfigParser()
    path = os.path.join(os.path.split(os.path.realpath(__file__))[0]) + '\conf.ini'
    config.read(path,encoding="gbk")
    if valueType is str:
        value = config.get(section, option)
        return value
    elif valueType is int:
        value = config.getint(section, option)
        return value
    elif valueType is bool:
        value = config.getboolean(section, option)
        return value
    elif valueType is float:
        value = config.getfloat(section, option)
        return value

    else:
        value = config.get(section, option)
        return value

def set_conf(section,k,v):
    """
    写入值到配置文件中
    :param section: 配置文件中的片段名称
    :param k: 写入文件中的key
    :param v: 写入配置中的值
    :return:
    """
    config = configparser.ConfigParser()
    path = os.path.join(os.path.split(os.path.realpath(__file__))[0]) + '\conf.ini'
    config.read(path,encoding="gbk")
    config.set(section, str(k), str(v))
    config.write(open(path, 'w'))


def host_set():
    """
    插入地址到本地hosts
    :param condition: 预发还是测试环境的标识
    :return:
    """
    filepath = r'C:\Windows\System32\drivers\etc\hosts'
    hosts = None
    f = open(filepath, 'w')
    hosts = get_conf('host','test')
    f.write(hosts)
    f.close()


def add_phone_number():
    """
    随机生成电话号码
    :return: 返回手机号码
    """
    prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
               "153", "155", "156", "157", "158", "159", "186", "187", "188"]
    id_card = random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))
    return id_card

def now_time(day=0):
    """
    返回年月日
    :param day: 与当前日期累加，可正负
    :return:
    """
    Time = str(datetime.date.today() + datetime.timedelta(days=day))
    return Time

def random_name():
    """
    随机名称
    :return:zll+当前年月日+3个字母+3个数字
    """
    name = "zll" + now_time()+"".join(random.choice("qwertyuiopasdfghjklzxcvbnm") for i in range(3))+"".join(random.choice("0123456789") for i in range(3))
    return name


def time_time(type="second"):
    """
    返回当前时间
    :param type:根据选择类型，返回不同的内容
    :return:
    """
    if type == "year":
        return time.strftime('%Y',time.localtime(time.time()))
    elif type == "month":
        return time.strftime('%Y-%m', time.localtime(time.time()))
    elif type == "day":
        return time.strftime('%Y-%m-%d', time.localtime(time.time()))
    elif type == "hour":
        return time.strftime('%Y-%m-%d %H', time.localtime(time.time()))
    elif type == "minute":
        return time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
    elif type == "second":
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    else:
        return type + "不属于任何一个指定的键"

