#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
爬取纵横中文网一本书
@time: 2020-05-29
"""
import re
from pathlib import Path

from DrissionPage import *


class BookDownloader(object):
    def __init__(self, page: MixPage):
        self.page = page

    def 爬全书(self, 目录_url, 存放路径: str) -> None:
        self.page.get(目录_url)
        书名 = self.page.ele('tag:h1').text
        路径 = f'{存放路径}\\{书名}'
        for 章节url in self.读取列表(目录_url):
            self.爬取一章(章节url, 路径)

    def 读取列表(self, 目录_url) -> list:
        self.page.get(目录_url)
        章节列表 = self.page.eles('css:.chapter-list.clearfix>li>a')
        return [x.attr('href') for x in 章节列表]

    def 爬取一章(self, url: str, 存放路径: str) -> None:
        self.page.get(url)
        标题 = self.page.ele('@class:title_txtbox').text
        段落s = self.page.eles('css:.content>p')
        Path(存放路径).mkdir(parents=True, exist_ok=True)
        标题 = re.sub(r'[/\\:*?\"<>|]', "_", 标题)
        file_path = f'{存放路径}\\{标题}.txt'
        with open(file_path, 'w', encoding='utf-8') as f:
            for 段 in 段落s:
                f.write(f'{段.text}\n')


if __name__ == '__main__':
    drission = Drission()
    p = MixPage(drission, 's')
    目录url = 'http://book.zongheng.com/showchapter/1005547.html'
    保存路径 = 'result'
    BookDownloader(p).爬全书(目录url, 保存路径)
