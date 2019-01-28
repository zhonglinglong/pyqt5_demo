#-*- coding: utf-8 -*-
# @Time   : 2019/1/16 10:40
# @Author : linglong
# @File   : myEmail.py

import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from email.header import Header
from email.utils import formatdate


class NewEmail(object):
    def __init__(self,text='正文',to_addr=['zhonglinglong@ishangzu.com'],html_path=None,txt_path=None,pic_path=None):
        #实例化一个类，处理正文及附件
        self.to_addr = to_addr
        self.message = MIMEMultipart()
        self.message['From'] = 'zhonglinglong@ishangzu.com'
        self.message['to'] = to_addr[0]
        self.message['Subject'] = '测试报告'
        self.message['Date'] = formatdate()
        self.message.attach(MIMEText(text, 'plain', 'utf-8'))
        try:
            self.send_html(html_path)
            self.send_pic(pic_path)
            self.send_text(txt_path)
        except BaseException as e:
            print(str(e))
        self.send()

    def send_html(self,path):
        """
        带html附件的邮件
        :param path:
        :return:
        """
        html = MIMEText(open(path, 'rb').read(), 'base64', 'utf-8')
        html["Content-Type"] = 'application/octet-stream'
        html["Content-Disposition"] = 'attachment; filename="autoTestReport.html"'
        self.message.attach(html)

    def send_text(self,path):
        """
        带text附件的邮件
        :param path:
        :return:
        """
        text = MIMEText(open(path, 'rb').read(), 'base64', 'utf-8')
        text["Content-Type"] = 'application/octet-stream'
        text["Content-Disposition"] = 'attachment; filename="textInfo.txt"'
        self.message.attach(text)

    def send_pic(self,path):
        """
        带图片附件的邮件
        :param path:
        :return:
        """
        pic = MIMEText(open(path, 'rb').read(), 'base64', 'utf-8')
        pic["Content-Type"] = 'application/octet-stream'
        pic["Content-Disposition"] = 'attachment; filename="test.jpg"'
        self.message.attach(pic)

    def send(self):
        """
        发送邮件
        :return:
        """
        try:
            user = 'zhonglinglong@ishangzu.com'
            pwd = 'Long268244'
            smtp_server = 'smtp.mxhichina.com'
            server = smtplib.SMTP(smtp_server, 25)
            server.login(user, pwd)
            server.sendmail(user, self.to_addr, self.message.as_string())
            server.quit()
        except BaseException as e:
            return str(e)
        return

#
# NewEmail(html_path="D:\Python3.7\python_isz_test\classDemo\\fer.html",txt_path='D:\Python3.7\python_isz_test\classDemo\\test.txt',pic_path="D:\Python3.7\python_isz_test\classDemo\\test.png")

