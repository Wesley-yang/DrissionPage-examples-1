#!/usr/bin/env python
# -*- coding:utf-8 -*-
from pathlib import Path
from typing import Union

from DrissionPage import *
import re


def main() -> list:
    base_url = 'https://maoyan.com/board/4?offset='
    总列表 = []
    for i in range(10):
        总列表.extend(get_一页(f'{base_url}{i * 10}'))
    return 总列表


def get_一页(url: str) -> list:
    page.get(url)
    数据列表 = []
    电影列表 = page.eles('tag:dd')
    for 电影 in 电影列表:
        数据 = {
            '序号': 电影.ele('tag:i').text,
            '标题': 电影.ele('@class:name').text,
            '主演': 电影.ele('@class:star').text[3:],
            '时间': get_上映时间(电影.ele('@class:releasetime').text),
            '地区': get_地区(电影.ele('@class:releasetime').text),
            '评分': 电影.ele('@class:score').text,
            '封面': 下载图片(电影.ele('tag:img').next.attr('data-src')),
            '链接': 电影.ele('tag:a').attr('href')
        }
        数据列表.append(数据)
        print(数据)
    return 数据列表


def 下载图片(src: str) -> str:
    src = src.split('@')[0]
    下载路径 = r'result\imgs'
    Path(下载路径).mkdir(parents=True, exist_ok=True)
    return page.download(src, r'result\imgs')[1]


def get_上映时间(text: str) -> str:
    r = re.search(r'(.*?)(\(|$)', text)
    return r.group(1)


def get_地区(text: str) -> Union[str, None]:
    r = re.search(r'.*\((.*)\)', text)
    try:
        return r.group(1)
    except AttributeError:
        return None


def main() -> list:
    base_url = 'https://maoyan.com/board/4?offset='
    总列表 = []
    for i in range(10):
        总列表.extend(get_一页(f'{base_url}{i * 10}'))
    return 总列表


if __name__ == '__main__':
    drission = Drission()
    page = MixPage(drission, 's')
    main()
