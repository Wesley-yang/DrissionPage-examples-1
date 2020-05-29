#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
爬取多多看书网一本书
@time: 2020-05-29
"""
from pathlib import Path

from DrissionPage import *


def 爬一本书(url: str) -> None:
    page.get(url)
    书名 = page.ele('xpath://div[@class="sitepath"]/a[3]').text
    存放路径 = f'result\\{书名}'
    for 章节url in 读取列表(url):
        爬取一章(章节url, 存放路径)


def 读取列表(url: str) -> list:
    page.get(url)
    章节列表 = page.eles('css:.chapter.clear>li>a')
    return [x.attr('href') for x in 章节列表]


def 爬取一章(url: str, 存放路径: str) -> None:
    page.get(url)
    标题 = page.ele('tag:h1').text
    段落s = page.eles('css:#contentWp>p')
    Path(存放路径).mkdir(parents=True, exist_ok=True)
    with open(f'{存放路径}\\{标题}.txt', 'w', encoding='utf-8') as f:
        for 段 in 段落s:
            f.write(f'{段.text}\n')


if __name__ == '__main__':
    drission = Drission()
    page = MixPage(drission)
    书url = 'https://xs.sogou.com/list/5728502428'
    爬一本书(书url)
