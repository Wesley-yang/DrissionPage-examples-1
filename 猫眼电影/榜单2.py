#!/usr/bin/env python
# -*- coding:utf-8 -*-
from DrissionPage import Drission

from base_page.list_page import ListPageS


class 榜单页(ListPageS):
    def __init__(self, drission: Drission, 首页url: str):
        xpaths = {
            '行': '//dl[@class="board-wrapper"]/dd',
            '下一页': '//a[text()="下一页"]',
            '页数': '//a[text()="下一页"]/../preceding-sibling::li[1]/a'
        }
        super().__init__(drission, 首页url, **xpaths)

    def check_page(self):
        return True


if __name__ == '__main__':
    drission = Drission()
    列表首页url = 'https://maoyan.com/board/4'
    保存路径 = 'result'
    待爬内容 = [
        ['//a[1]', 'href'],
        ['//p[@class="name"]/a', 'title'],
        # ['//p[@class="name"]/a', 'title'],
        # ['//p[@class="name"]/a', 'title'],
        # ['//p[@class="name"]/a', 'title'],
        # ['//p[@class="name"]/a', 'title'],
        # ['//p[@class="name"]/a', 'title'],
        # ['//p[@class="name"]/a', 'title'],
    ]

    page = 榜单页(drission, 列表首页url)
    url_list = page.get_列表(待爬内容)
    for url in url_list:
        print(url)
