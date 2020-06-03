#!/usr/bin/env python
# -*- coding:utf-8 -*-
from base_page.list_page import *


class 猫眼榜单页(ListPageS):
    def __init__(self, drission: Drission, 首页url: str):
        xpaths = {
            '行': '//dl[@class="board-wrapper"]/dd',
            '下一页': '//a[text()="下一页"]',
            '页数': '//a[text()="下一页"]/../preceding-sibling::li[1]/a'
        }
        super().__init__(drission, 首页url, **xpaths)


if __name__ == '__main__':
    drission = Drission()
    列表首页url = 'https://maoyan.com/board/4'
    待爬内容 = [
        ['//i', 'text'],  # 序号
        ['//p[@class="name"]/a', 'title'],  # 标题
        ['//p[@class="star"]', 'text', '主演：(.*)'],  # 主演
        ['//p[@class="releasetime"]', 'text', r'(.*?)(\(|$)'],  # 时间
        ['//p[@class="releasetime"]', 'text', r'.*\((.*)\)'],  # 地区
        ['//p[@class="score"]', 'text'],  # 评分
        ['//img', 'src'],  # 封面url
        ['//a[1]', 'href']  # 链接
    ]

    page = 猫眼榜单页(drission, 列表首页url)
    if page.title.startswith(('验证中心', '页面不存在')):
        print('被反爬了')  # TODO: 再研究
    else:
        结果列表 = page.get_列表(待爬内容)
        for 数据 in 结果列表:
            print(数据)
