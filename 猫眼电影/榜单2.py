#!/usr/bin/env python
# -*- coding:utf-8 -*-
from DrissionPage import Drission

from base_page.list_page import ListPageD


class 榜单页(ListPageD):
    def __init__(self, drission: Drission, 首页url: str):
        xpaths = {
            '行': '//dl[@class="board-wrapper"]/dd',
            '页数': '//a[text()="下一页"]/../preceding-sibling::li[1]/a'
        }
        super().__init__(drission, 首页url, **xpaths)

    def check_page(self):
        return True

    # def to_下一页(self, wait: float = None):
    #     t_url = self.url
    #     r = re.search(r'.*/p(\d+)/.*', t_url)
    #     下一页页码 = str(int(r.group(1)) + 1)
    #     t_url = t_url.replace(f'p{r.group(1)}', f'p{下一页页码}')
    #     self.get(t_url)


if __name__ == '__main__':
    drission = Drission()
    列表首页url = 'https://maoyan.com/board/7'
    保存路径 = 'result'
    待爬内容 = [['//a[1]', 'href']]

    page = 榜单页(drission, 列表首页url)
    # print(page.html)
    # url_list = page.get_列表(待爬内容, 3, 1)
    print(page.get_总页数())