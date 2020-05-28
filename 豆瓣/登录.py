#!/usr/bin/env python
# -*- coding:utf-8 -*-

from DrissionPage import *

drission = Drission()
page = MixPage(drission)

page.get('https://www.douban.com/')
page.to_iframe('css:.login>iframe')
page.ele('@class:account-tab-account').click()
page.ele('@id:username').input('xxxxxxx')
page.ele('@id:password').input('xxxxxxx')
page.ele('登录豆瓣').click()
