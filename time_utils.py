#!/usr/bin/python3
# _*_ coding:UTF-8 _*_

from datetime import datetime, timedelta, date, tzinfo


# 获取10天前的日期
def get_date_from_today(n=0):
    '''
    距今的日期
    :param n:几天
    :return:datime格式日期
    '''
    if n < 0:
        n = abs(n)
        return date.today() - timedelta(days=n)
    else:
        return date.today() + timedelta(days=n)
        
def get_days_from_today(timestr,format='%d%b,%Y') 
    '''
    :return 距离今天有多少天
    '''
    timestr = ''.join(timestr.split())
    return (datetime.today() - datetime.strptime(timestr, format)).days

def convert_ad_timestamp(timestamp):
    '''
    # 将Windows AD时间戳转换为datetime时间格式,有3种方法
    :param timestamp: AD时间戳
    :return: datetime格式时间
    '''
    # 第二种方法：从1601-01-01 8:00:00到1970-01-01 8:00:00共经过了11644473600秒，所以需要先将其减掉，然后再进行转换
    utc8_datetime = datetime.fromtimestamp(float(timestamp) / 10000000 - 11644473600)
    return utc8_datetime
