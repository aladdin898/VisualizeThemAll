#!/usr/bin/env python

import datetime

import matplotlib.dates as mdates

from jqdatasdk import *

def init_jqdata():
    """登陆认证"""
    phone_number = ''
    while len(phone_number) < 1:
        phone_number = input('请输入您的聚宽帐号(即注册的手机号): ')

    password = ''
    while len(password) < 1:
        password = input('请输入您的登陆密码: ')

    auth(phone_number, password)


def get_price_data(security, middle_date):
    """获取middle_date前后1年的日线行情数据,不包括停牌时期"""
    start_date = middle_date - datetime.timedelta(weeks=52)
    end_date = middle_date + datetime.timedelta(weeks=52)
    df = get_price(security, start_date, end_date, skip_paused=True)
    return df
