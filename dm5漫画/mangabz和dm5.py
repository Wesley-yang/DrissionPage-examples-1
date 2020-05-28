#!/usr/bin/env python
# -*- coding:utf-8 -*-
from pathlib import Path
from time import sleep

from DrissionPage import *

drission = Drission()
page = MixPage(drission)

漫画url = ['http://www.mangabz.com/280bz/']

for url in 漫画url:
    page.get(url, go_anyway=True)

    mtitle = page.ele('@class:detail-info-title').text
    展开全部 = page.ele('@class:detail-list-form-more', timeout=1)
    if 展开全部:
        展开全部.click()
        the_class = 'detail-list-form-item'
    else:
        the_class = 'detail-list-form-item  '

    mlist = page.eles(f'@class:{the_class}')
    漫画列表 = [[i.text, i.attr('href')] for i in mlist]

    for i in 漫画列表[::-1]:
        page.get(i[1])
        while True:
            img = page.ele('@id:cp_image')
            link = img.attr('src')

            下载位置 = f'漫画\\{mtitle}\\{i[0]}'
            Path(下载位置).mkdir(parents=True, exist_ok=True)
            page.download(link, 下载位置)

            page.ele('@href:javascript:ShowNext();').click(True)

            sleep(0.2)
            提示框 = page.ele('@class:toast-win')
            if 'none' not in 提示框.attr('style'):
                break
