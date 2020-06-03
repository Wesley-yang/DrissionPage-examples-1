# 迁移通知
## 本库已迁移到gitee，github暂停维护。
**项目地址：** [https://gitee.com/g1879/DrissionPage-demos](https://gitee.com/g1879/DrissionPage-demos)
  
# 简介
使用DrissionPage爬取各网站的示例。
DrissionPage项目地址：
- [gitee](https://gitee.com/g1879/DrissionPage)
- [github](https://github.com/g1879/DrissionPage)

## base_page

以MixPage为基类派生的页面类，针对常见页面形态做抽象，结构相同的页面只须继承这些类，并作少量重写，即可进行爬取。避免了大量的重复性开发。

### list_page

- ListPageS : 可使用session模式爬取的列表页基类
- ListPageD : 使用driver模式爬取的页表页基类

列表基类提取了列表页面共有的特征，即栏目名、下一页按钮、总页数、数据行，封装了对页面的基本操作和读取方法。只要传入这4个元素的xpth，即可实现页面的逐页爬取。其中只有行xpath是必须的。

可爬取每数据行里任意个数的数据，只需传入数据元素相对于行的xpath和要取的属性。还可传入正则表达式对数据进行初步提取（可选）。

示例：爬取猫眼TOP100电影链接

```python
xpaths = {
            '行': '//dl[@class="board-wrapper"]/dd',
            '下一页': '//a[text()="下一页"]',
            '页数': '//a[text()="下一页"]/../preceding-sibling::li[1]/a'
        }
列表首页url = 'https://maoyan.com/board/4'
待爬内容 = [['//a[1]', 'href']]
page = ListPageD(drission, 列表首页url, **xpath)
全部列表 = page.get_列表(待爬内容)
print(全部列表)
#  [['https://maoyan.com/films/1375'], ['https://maoyan.com/films/4883'], ['https://maoyan.com/films/3294'], ...]
```

**参数格式：** 
xpaths = {
    '栏目名': ['xpth字符串','正则字符串'],  # 若直接获取内容，正则字符串为None或(.*)
    '下一页': 'xpth字符串',
    '行': 'xpth字符串',
    '页数': ['xpth字符串','正则字符串'],
}

**待爬内容格式：** 
[[xpath1,参数1属性，正则字符串1],[xpath2,参数2属性，正则字符串2]...]  # 正则字符串项可省略

**返回内容格式：** 
[[参数1值,参数2值...],[参数1值,参数2值...]...]
