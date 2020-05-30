#!/usr/bin/env python
# -*- coding:utf-8 -*-

from 爬一本书 import *
from base_page.list_page import ListPageS
import re


class 书列表页(ListPageS):
    def __init__(self, drission: Drission, 首页url: str):
        xpaths = {'行': '//div[contains(@class,"bookbox")]', }
        super().__init__(drission, 首页url, **xpaths)

    def to_下一页(self, wait: float = None):
        t_url = self.url
        r = re.search(r'.*/p(\d+)/.*', t_url)
        下一页页码 = str(int(r.group(1)) + 1)
        t_url = t_url.replace(f'p{r.group(1)}', f'p{下一页页码}')
        self.get(t_url)


if __name__ == '__main__':
    drission = Drission()
    列表首页url = 'http://book.zongheng.com/store/c0/c0/b0/u0/p1/v0/s1/t0/u0/i1/ALL.html'
    保存路径 = 'result'
    待爬内容 = [['//a[1]', 'href']]

    page = 书列表页(drission, 列表首页url)
    url_list = page.get_列表(待爬内容, 3, 1)
    for url in url_list:
        page.get(url[0])
        目录_url = page.ele('@class:all-catalog').attr('href')
        book = BookDownloader(page)
        book.爬全书(目录_url, 保存路径)
