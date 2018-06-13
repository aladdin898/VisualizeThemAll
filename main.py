#!/usr/bin/env python

import datetime
import numpy

import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

from mpl_finance import candlestick_ohlc

from jq import *


all_logs = []

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


def show_plot(date_tickers, index, open, high, low, close, xy):
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)

    def format_date(x,pos=None):
        if x<0 or x>len(date_tickers)-1:
            return ''
        return date_tickers[int(x)][2:]
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    ax.set_facecolor("black")
    plt.axis(xy)
    plt.xticks(rotation=45)
    plt.yticks()
    plt.title(all_logs[0]['security'] + " Daily Candlestick Chart") # FIXME
    plt.xlabel("Time")
    plt.ylabel("Price")
    candlestick_ohlc(ax,zip(index, open, high, low, close),width=0.6,colorup='r',colordown=(0.0, 1.0, 1.0))

    height = xy[3] - xy[2]
    arrow_len = height * 0.04 # arrow_len = head_length
    for item in all_logs:
        idx = find_time_index(date_tickers, item['trade_time'])
        if item['buying']:
            plt.arrow(idx, low[idx] - arrow_len * 2.2, 0, arrow_len, color='blue', width=0.4, head_length=arrow_len)
        else:
            plt.arrow(idx, high[idx] + arrow_len * 2.2, 0, - arrow_len, color='yellow', width=0.4, head_length=arrow_len)
    plt.grid()
    plt.show()


def find_time_index(list, item):
    n = len(list)
    for i in range(n):
        if (datetime.datetime.strptime(list[i], '%Y-%m-%d') >= item):
            return i
    return n - 1


def show_all_logs(latest_item = {}):
    if (all_logs):
        df = get_price_data(all_logs[0]['security']) # FIXME
        date_tickers = [str(i).split(' ')[0] for i in df.index]
        n = len(date_tickers)
        if latest_item:
            idx = find_time_index(date_tickers, latest_item['trade_time'])
            x1 = idx - 25
            x2 = idx + 15
        else:
            time_line = []
            for item in all_logs:
                time_line.append(item['trade_time'])
            tmp = numpy.array(time_line)
            x1 = find_time_index(date_tickers, tmp.min())
            x2 = find_time_index(date_tickers, tmp.max())
            x1 = x1 - 1
            x2 = x2 + 1

        if x1<0:
            x1=0
        if x2 >= n:
            x2 = n - 1

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
        show_plot(date_tickers, range(n), open, high, low, close, (x1, x2, y1, y2))
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

    if not log_line:
        continue
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
