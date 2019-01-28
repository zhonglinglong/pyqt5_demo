# -*- coding: utf-8 -*-
# @Time   : 2019/1/10 14:25
# @Author : linglong
# @File   : myTime.py
import calendar
import datetime
import time


class NewTime(object):
    def __init__(self):
        self.current_date = str(datetime.date.today())
        self.current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def _get_days_of_date(self, year, mon):
        """
        内置函数：获取某年某月的天数
        :param year: 年
        :param mon: 月
        :return: 当月天数
        """
        return int(calendar.monthrange(int(year), mon)[1])

    def _getyearandmonth(self, n=0, date=None):
        """
        内置函数：获取当前月份
        :param n: 已当前为标准,正整数往后加N月,负整数往前减N月
        :param date:当前日 默认为空
        :return:
        """

        def addzero(n):
            """
            把传入的字符串变成标准的月份 比如03 12
            :param n: 传入的月份字符串
            :return: 标准的月份显示字符串
            """
            nabs = abs(int(n))
            if (nabs < 10):
                return "0" + str(nabs)
            else:
                return nabs

        date = date if date else self.current_date
        time = date.split('-')
        thisyear, thismon = int(time[0]), int(time[1])
        totalmon = thismon + n
        if (n >= 0):
            if (totalmon <= 12):
                totalmon = addzero(totalmon)
                return (time[0], totalmon, time[2])
            else:
                i = totalmon / 12
                j = totalmon % 12
                if (j == 0):
                    i -= 1
                    j = 12
                thisyear += i
                days = str(self._get_days_of_date(int(thisyear), j))
                j = addzero(j)
                return (str(thisyear), str(j), days if not date else time[2])
        else:
            if ((totalmon > 0) and (totalmon < 12)):
                days = str(self._get_days_of_date(thisyear, totalmon))
                totalmon = addzero(totalmon)
                return (time[0], totalmon, time[2])
            else:
                i = totalmon / 12
                j = totalmon % 12
                if (j == 0):
                    i -= 1
                    j = 12
                thisyear += i
                days = str(self._get_days_of_date(thisyear, j))
                j = addzero(j)
                return (str(thisyear), str(j), days if not date else time[2])

    def now_day(self, days=0, value=True):
        if value:
            date = str(datetime.date.today() + datetime.timedelta(days=days))
            return date
        else:
            date = str(datetime.date.today() + datetime.timedelta(days=days))
            dates = date + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))[10:20]
            return dates

    def now_month(self, months=0, date=None, value=True):
        (y, m, d) = self._getyearandmonth(months) if not date else self._getyearandmonth(months, date)
        arr = (y, m, d)
        if (int(d) > self._get_days_of_date(int(y[0:4]), int(m))):
            arr = (y[0:4], m, self._get_days_of_date(int(y), int(m)))
        if value:
            return (arr[0][0:4] + '-' + arr[1] + "-" + arr[2])
        else:
            return (arr[0][0:4] + '-' + arr[1] + "-" + arr[2]) + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))[10:20]


# t = NewTime()
# print(t.current_date)
# print(t.current_time)
# print(t.now_month(20, value=False))
