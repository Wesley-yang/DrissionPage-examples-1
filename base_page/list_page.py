#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
常见页面结构的基类，继承自MixPage
- ListPageS : 可使用session模式爬取的列表页基类
- ListPageD : 使用driver模式爬取的页表页基类
列表基类提取了列表页面共有的特征，即栏目名、下一页按钮、总页数、数据行，
封装了对页面的基本操作和读取方法。
只要传入这4个元素的xpth，即可实现页面的逐页爬取。
其中行xpath是必须的，其余3个可没有或为None
参数格式：
xpaths = {
    '栏目名': ['xpth字符串','正则字符串'],  # 若直接获取内容，正则字符串为None或(.*)
    '下一页': 'xpth字符串',
    '行': 'xpth字符串',
    '页数': ['xpth字符串','正则字符串'],
}
待爬内容：[[xpath1,参数1属性，正则字符串1],[xpath2,参数2属性，正则字符串2]...]  # 正则字符串项可省略
返回列表格式：[[参数1,参数2...],[参数1,参数2...]...]
使用时，根据实际情况派生之类，重写to_下一页()方法
若页面有跳转功能，建议重写to_第几页()方法

@date: 2020-05-31
@email: g1879@qq.com
"""
import re
from time import sleep
from typing import Union

from DrissionPage import MixPage, Drission


class ListPageBase(MixPage):
    def __init__(self, drission: Drission, 首页url: str = None, mode: str = 's', **xpaths):
        super().__init__(drission, mode)
        self.首页url = 首页url
        self.xpath_栏目名 = xpaths['栏目名'] if '栏目名' in xpaths else None
        self.xpath_下一页 = xpaths['下一页'] if '下一页' in xpaths else None
        self.xpath_行s = xpaths['行']
        self.xpath_页数 = xpaths['页数'] if '页数' in xpaths else None
        self.总页数 = self.get_总页数() if '页数' in xpaths else None
        if 首页url:
            self.get(首页url)

    def get_栏目名称(self) -> Union[str, None]:
        if not self.xpath_栏目名:
            return None
        xpath = self.xpath_栏目名 if isinstance(self.xpath_栏目名, str) else self.xpath_栏目名[0]
        值 = self.ele(f'xpath:{xpath}').text
        re_str = self.xpath_栏目名[1] if isinstance(self.xpath_栏目名, list) and len(self.xpath_栏目名) == 2 \
                                      and self.xpath_栏目名[1] else '(.*)'
        r = re.search(re_str, 值)
        return r.group(1)

    def get_总页数(self) -> Union[int, None]:
        if not self.xpath_页数:
            return None
        xpath = self.xpath_页数 if isinstance(self.xpath_页数, str) else self.xpath_页数[0]
        值 = self.ele(f'xpath:{xpath}').text
        re_str = self.xpath_页数[1] if isinstance(self.xpath_页数, list) and len(self.xpath_页数) == 2 \
                                     and self.xpath_页数[1] else '(.*)'
        r = re.search(re_str, 值)
        return int(r.group(1))

    def to_下一页(self, wait: float = None):
        pass

    def to_第几页(self, num: int):
        if num < 1 or not isinstance(num, int):
            raise KeyError('请传入正整数')
        if self.总页数 and num > self.总页数:
            raise KeyError('始页不能大于总页数')
        self.get(self.首页url)
        for _ in range(num - 1):
            self.to_下一页()

    def get_当前页(self, 待爬内容: list) -> list:
        """
        待爬内容格式：[[xpath1,参数1,正则1],[xpath2,参数2,正则2]...]
        返回列表格式：[[参数1,参数2...],[参数1,参数2...]...]
        """
        结果列表 = []
        行s = self.eles(f'xpath:{self.xpath_行s}')
        for 行 in 行s:
            行结果 = []
            for 项 in 待爬内容:
                参数值 = 行.ele(f'xpath:{项[0]}').attr(项[1])
                re_str = 项[2] if len(项) == 3 and 项[2] else '(.*)'
                r = re.search(re_str, 参数值)
                行结果.append(r.group(1))
            结果列表.append(行结果)
        return 结果列表

    def get_列表(self, 待爬内容: list, 始页: int = 1, 爬页数: int = None, wait: float = None) -> list:
        self.to_第几页(始页)
        if not 爬页数 and not self.get_总页数():
            raise KeyError('须传入爬取页数')
        if 爬页数 and (not isinstance(爬页数, int) or 爬页数 < 1):
            raise KeyError('须传入正整数')
        if self.总页数 and (not 爬页数 or 爬页数 > self.总页数 - 始页 + 1):
            爬页数 = self.总页数 - 始页 + 1
        列表 = self.get_当前页(待爬内容)
        for _ in range(爬页数 - 1):
            self.to_下一页(wait)
            列表.extend(self.get_当前页(待爬内容))
        return 列表


class ListPageS(ListPageBase):
    def __init__(self, drission: Drission, 首页url: str = None, **xpaths):
        super().__init__(drission, 首页url, 's', **xpaths)

    def to_下一页(self, wait: float = None):
        url = self.ele(f'xpath:{self.xpath_下一页}').attr('href')
        self.get(url)


class ListPageD(ListPageBase):
    def __init__(self, drission: Drission, 首页url: str = None, **xpaths):
        super().__init__(drission, 首页url, 'd', **xpaths)

    def to_下一页(self, wait: float = None):
        # TODO: 增加判断js是否加载完成功能
        self.ele(f'xpath:{self.xpath_下一页}').click()
        if wait:
            sleep(wait)
