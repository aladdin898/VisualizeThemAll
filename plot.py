#!/usr/bin/env python

import numpy

import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

from mpl_finance import candlestick_ohlc


def plot_main(ax, n, o, h, l, c, operations, arrow_len):
    candlestick_ohlc(ax,zip(range(n), o, h, l, c),width=0.6,colorup='r',colordown=(0.0, 1.0, 1.0))

    for operation in operations:
        x = operation[0]
        if operation[1]:
            ax.arrow(x, l[x] - arrow_len * 2.2, 0, arrow_len, color='white', width=0.4, head_length=arrow_len)
        else:
            ax.arrow(x, h[x] + arrow_len * 2.2, 0, - arrow_len, color='yellow', width=0.4, head_length=arrow_len)


def show_plots(title, date_tickers, o, h, l, c, operations, x1, x2, extra=[]):
    n = len(date_tickers)
    # x1,x2为横轴显示范围, x1d,x2d为横轴数据索引范围(0~n-1)
    x1d=x1
    x2d=x2
    if x1d<0:
        x1d=0
    if x2d >= n:
        x2d = n - 1

    high_list = []
    low_list = []
    for i in range(x1d, x2d):
        high_list.append(h[i])
        low_list.append(l[i])

    ymin = numpy.array(low_list).min()
    ymax = numpy.array(high_list).max()
    height = ymax - ymin
    y1main = ymin - height * 0.12
    y2main = ymax + height * 0.12
    arrow_len = height * 0.04 # arrow_len = head_length

    if len(extra) > 0:
        fig, ax = plt.subplots(2, 1, True)
        main_ax = ax[0]

        ax[1].plot(range(n), extra)
        extra_high_list = []
        extra_low_list = []
        for j in range(x1d, x2d):
            extra_high_list.append(extra[j])
            extra_low_list.append(extra[j])
        y1extra = numpy.array(extra_low_list).min()
        y2extra = numpy.array(extra_high_list).max()
        ax[1].axis(ymin=y1extra,ymax=y2extra)
    else:
        fig, ax = plt.subplots(1, 1, True)
        main_ax = ax
    fig.subplots_adjust(bottom=0.2)

    plot_main(main_ax, n, o, h, l, c, operations, arrow_len)

    def format_date(x,pos=None):
        if x<0 or x>len(date_tickers)-1:
            return ''
        return date_tickers[int(x)][2:]
    main_ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    main_ax.set_facecolor("black")
    main_ax.axis((x1,x2,y1main,y2main))

    plt.xticks(rotation=45)
    plt.yticks()
    plt.title(title)
    plt.xlabel("Time")
    main_ax.set_ylabel("Price")

    plt.grid()
    plt.show()
