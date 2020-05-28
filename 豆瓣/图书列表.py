#!/usr/bin/env python
# -*- coding:utf-8 -*-


from pathlib import Path
# from typing import Union
from urllib.parse import quote

from DrissionPage import *


# import re


def main() -> list:
    tags = ['推理', '随笔']
    base_url = 'https://book.douban.com/tag'
    总列表 = []
    for tag in tags:
        print(tag)
        总列表.extend(get_列表(f'{base_url}/{quote(tag)}', 1, 1))
    return 总列表


def get_列表(url: str, 始页: int = 1, 末页: int = None) -> list:
    page.get(url)
    总页数 = get_总页数()
    begin = 始页 if 1 < 始页 <= 总页数 else 1
    stop = 末页 if 末页 and 末页 <= 总页数 else 总页数
    begin, stop = (begin, stop) if begin <= stop else (1, 总页数)
    列表 = []
    for 页码 in range(begin - 1, stop):
        url = f'{url}?start={页码 * 20}&type=T'
        # page.cookies_to_session(copy_user_agent=True)
        page.get(url)
        列表.extend(get_一页(url))
    return 列表


def get_总页数() -> int:
    return int(page.ele('@class:next').prev.text)


def get_一页(url: str) -> list:
    page.get(url)
    数据列表 = []
    图书列表 = page.eles('@class:subject-item')
    for 图书 in 图书列表:
        信息 = 图书.ele('@class:pub').text.split('/')
        数据 = {
            '书名': 图书.ele('tag:h2').text,
            '作者': 信息[0].strip(),
            '出版社': 信息[1].strip(),
            '时间': 信息[2].strip(),
            '价格': 信息[3].strip(),
            '评分': 图书.ele('@class:rating_nums').text,
            '封面': 下载图片(图书.ele('tag:img').attr('src')),
            '链接': 图书.ele('tag:h2').ele('tag:a').attr('href')
        }
        数据列表.append(数据)
        print(数据)
    return 数据列表


def 下载图片(src: str) -> str:
    下载路径 = r'result\imgs'
    Path(下载路径).mkdir(parents=True, exist_ok=True)
    return page.download(src, r'result\imgs', show_msg=True)[1]


if __name__ == '__main__':
    drission = Drission()
    page = MixPage(drission, 's')
    main()
