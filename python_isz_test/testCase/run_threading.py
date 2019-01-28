# -*- coding:utf-8 -*-
import os
import subprocess


def getCaseFile(filePath):
    list = os.listdir(filePath)
    print(list)
    caseFile = []
    for i in range(len(list)):
        path = os.path.abspath(os.path.join(filePath,list[i]))  # 路径下所有文件及文件夹
        if not os.path.isfile(path) and 'test' in path.split("\\")[-1]:  # 如果是测试用例文件夹就继续走下去
            # print(path)
            list2 = os.listdir(path)
            for i in range(len(list2)):
                path2 = os.path.abspath(os.path.join(path,list2[i]))
                # print(path2)
                if '.py' in path2.split("\\")[-1] and 'test' in path2.split("\\")[-1] and '.pyc' not in path2.split("\\")[-1]:
                    print(path2.split("\\")[-1])
                    caseFile.append(path2)
    print(caseFile)
    return caseFile

path = '..//testCase'
file_path_name = getCaseFile(path)



import threading
from time import ctime,sleep


def one(func):
    subprocess.Popen('python3 %s' % func)

def two(func):
    for i in range(1):
        print ("I was at the %s! %s" %(func,ctime()))
        sleep(5)

def three(func):
    for i in range(1):
        print ("I was at the %s! %s" %(func,ctime()))
        sleep(5)

threads = []
t1 = threading.Thread(target=one,args=(file_path_name[0],))
threads.append(t1)
t2 = threading.Thread(target=two,args=(u'国产',))
threads.append(t2)
t3 = threading.Thread(target=three,args=(u'阿凡达',))
threads.append(t3)

if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    print ("all over %s" %ctime())




