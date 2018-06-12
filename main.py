#!/usr/bin/env python

import datetime
import numpy

import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

from mpl_finance import candlestick_ohlc

from jq import *


all_logs = []
date_tickers = []

def parse_splitted_log(splitted_log):
    trade_time = datetime.datetime.strptime(splitted_log[0].strip(),'%Y-%m-%d %H:%M:%S')
    oper_detail = splitted_log[2].split(' ')
    if oper_detail[0].strip() == 'Buying':
        buying = True
    else:
        buying = False
    security = oper_detail[1].strip()
    item = {'security' : security, 'buying' : buying, 'trade_time' : trade_time}
    all_logs.append(item)
    return item


def format_date(x,pos=None):
    global date_tickers
    if x<0 or x>len(date_tickers)-1:
        return ''
    return date_tickers[int(x)]


def show_plot(data_list, xy):
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    plt.axis(xy)
    plt.xticks(rotation=45)
    plt.yticks()
    plt.title(all_logs[0]['security'] + " Daily Candlestick Chart") # FIXME
    plt.xlabel("Time")
    plt.ylabel("Price")
    candlestick_ohlc(ax,data_list,width=0.6,colorup='r',colordown=(0.0, 1.0, 1.0))
    plt.grid()
    plt.show()


def find_time_index(list, item):
    n = len(list)
    for i in range(n):
        if (datetime.datetime.strptime(list[i], '%Y-%m-%d') >= item):
            return i
    return n - 1


def show_all_logs(latest_item = {}):
    global date_tickers
    if (all_logs):
        df = get_price_data(all_logs[0]['security']) # FIXME
        date_tickers = [str(i).split(' ')[0] for i in df.index]
        n = len(date_tickers)
        if latest_item:
            idx = find_time_index(date_tickers, latest_item['trade_time'])
            x1 = idx - 25
            x2 = idx + 15
            if x1<0:
                x1=0
            if x2 >= n:
                x2 = n - 1
        else:
            time_line = []
            for item in all_logs:
                time_line.append(item['trade_time'])
            tmp = numpy.array(time_line)
            x1 = find_time_index(date_tickers, tmp.min())
            x2 = find_time_index(date_tickers, tmp.max())

        open = df['open']
        high = df['high']
        low = df['low']
        close = df['close']

        high_list = []
        low_list = []
        for i in range(x1, x2):
            high_list.append(high[i])
            low_list.append(low[i])

        y1 = numpy.array(low_list).min()
        y2 = numpy.array(high_list).max()
        y1 = y1 - (y2 - y1) * 0.12
        y2 = y2 + (y2 - y1) * 0.12
        show_plot(zip(range(n), open, high, low, close), (x1, x2, y1, y2))
    else:
        print('还没输入数据')


init_jqdata()

input_mode = False # 连续输入模式
prompt = "\n请输入一行交易日志, 或输入 'i' 进入连续输入模式, 或输入 'p' 画总图, 或输入 'q' 退出:\n"

while True:
    if (input_mode):
        log_line = input()
    else:
        log_line = input(prompt)

    if log_line == 'q':
        break
    if log_line == 'i':
        input_mode = True
        continue
    if log_line == 'p':
        input_mode = False
        show_all_logs()
        continue

    splitted_log = log_line.split(' - ')
    if len(splitted_log) < 3:
        print("非法输入!")
        continue

    try:
        latest_item = parse_splitted_log(splitted_log)
    except (ValueError, IndexError):
        print("非法输入!")
    else:
        if not input_mode:
            show_all_logs(latest_item)
