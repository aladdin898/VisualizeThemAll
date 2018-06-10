#!/usr/bin/env python

import datetime

import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

from mpl_finance import candlestick_ohlc

from jq import *


date_tickers = []

def format_date(x,pos=None):
    if x<0 or x>len(date_tickers)-1:
        return ''
    return date_tickers[int(x)]


def show_plot(data_list, x1, x2):
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    plt.axis(xmin=x1, xmax=x2)
    plt.xticks(rotation=45)
    plt.yticks()
    plt.title(security + " Daily Candlestick Chart")
    plt.xlabel("Time")
    plt.ylabel("Price")
    candlestick_ohlc(ax,data_list,width=0.6,colorup='r',colordown='green')
    plt.grid()
    plt.show()


init_jqdata()

prompt = "\nPlease input a line of log (Or enter 'q' to quit):\n"

while True:
    log_line = input(prompt)
    if log_line == 'q':
        break

    splitted_log = log_line.split(' - ')
    if len(splitted_log) < 3:
        print("非法输入!")
        continue

    try:
        trade_time = datetime.datetime.strptime(splitted_log[0].strip(),'%Y-%m-%d %H:%M:%S')
        security = splitted_log[2].split(' ')[1].strip()
    except (ValueError, IndexError):
        print("非法输入!")
    else:
        df = get_price_data(security, trade_time)
        date_tickers = [str(i).split(' ')[0] for i in df.index]
        n = len(date_tickers)
        for i in range(n):
            if (datetime.datetime.strptime(date_tickers[i],'%Y-%m-%d') >= trade_time):
                x1 = i - 20
                x2 = i + 10
                if x1<0:
                    x1=0
                if x2 >= n:
                    x2 = n - 1
                break
        show_plot(zip(range(n),df['open'], df['high'],df['low'], df['close']), x1, x2)
