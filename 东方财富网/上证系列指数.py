#!/usr/bin/env python
# -*- coding:utf-8 -*-
from time import sleep

from DrissionPage import *

drission = Drission()
page = MixPage(drission)
page.get('http://quote.eastmoney.com/center/gridlist.html#hs_a_board')


def main():
    总数据 = []
    while True:
        总数据.extend(get_一页())
        if not is_末页():
            click_下一页()
        else:
            break
    return 总数据


def get_一页():
    行s = page.ele('@id:table_wrapper-table').ele('tag:tbody').eles('tag:tr')
    页数据 = []
    for 行 in 行s:
        列s = 行.eles('tag:td')
        行数据 = {
            '序号': 列s[0].text,
            '代码': 列s[1].text,
            '名称': 列s[2].text,
            '最新价': 列s[4].text,
            '涨跌幅': 列s[5].text,
            '成交量': 列s[6].text,
            '成交额': 列s[7].text,
            '振幅': 列s[8].text,
            # 以下省略
        }
        print(行数据)
        页数据.append(行数据)
    return 页数据


def click_下一页():
    if not is_末页():
        page.ele('下一页').click()
        sleep(0.5)


def is_末页():
    下一页 = page.ele('下一页')
    return True if 'disabled' in 下一页.attr('class') else False


if __name__ == '__main__':
    main()
