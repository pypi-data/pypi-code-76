# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src/plugins'}

packages = \
['hk_reporter', 'hk_reporter.platform', 'platform']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'feedparser>=6.0.2,<7.0.0',
 'httpx>=0.16.1,<0.17.0',
 'nonebot2>=2.0.0-alpha.8,<3.0.0',
 'nonebot_plugin_apscheduler>=0.1.2,<0.2.0',
 'pillow>=8.1.0,<9.0.0',
 'pyppeteer>=0.2.5,<0.3.0',
 'tinydb>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'nonebot-hk-reporter',
    'version': '0.2.3',
    'description': 'Subscribe message from social medias',
    'long_description': '# hk-reporter  通用订阅推送插件\n\n## 简介\n一款自动爬取各种站点，社交平台更新动态，并将信息推送到QQ的机器人。基于 [`NoneBot2`](https://github.com/nonebot/nonebot2 ) 开发（诞生于明日方舟的蹲饼活动）\n\n支持的平台：\n* 微博\n    * 图片\n    * 文字\n    * 不支持视频\n    * 不支持转发的内容\n* bilibili\n    * 图片\n    * 专栏\n    * 文字\n    * 视频链接\n    * 不支持转发的内容\n* rss\n    * 从description中提取图片\n    * 文字\n\n## 使用方法\n\n### 使用以及部署\n本项目可作为单独插件使用，仅包含订阅相关功能（绝对simple和stupid），也可直接克隆项目进行使用（包含自动同意superuser，自动接受入群邀请等功能）  \n作为插件使用请安装`nonebot-hk-reporter`包，并在`bot.py`中加载`nonebot_hk_reporter`插件；或直接克隆本项目进行使用  \n配置与安装请参考[nonebot2文档](https://v2.nonebot.dev/)\n\n### 配置变量\n* `HK_REPORTER_CONFIG_PATH` (str) 配置文件保存目录，如果不设置，则为当前目录下的`data`文件夹\n* `HK_REPORTER_USE_PIC` (bool) 以图片形式发送文字（推荐在帐号被风控时使用）\n* `HK_REPORTER_USE_LOCAL` (bool) 使用本地chromium（文字转图片时需要），否则第一次启动会下载chromium\n\n### 命令\n所有命令都需要@bot触发\n* 添加订阅（仅管理员和群主）：`添加订阅`\n* 查询订阅：`查询订阅`\n* 删除订阅（仅管理员和群主）：`删除订阅`\n\n平台代码包含：weibo，bilibili，rss\n<details>\n<summary>各平台uid</summary>\n\n下面均以pc站点为例\n* weibo\n    * 对于一般用户主页`https://weibo.com/u/6441489862?xxxxxxxxxxxxxxx`，`/u/`后面的数字即为uid\n    * 对于有个性域名的用户如：`https://weibo.com/arknights`，需要点击左侧信息标签下“更多”，链接为`https://weibo.com/6279793937/about`，其中中间数字即为uid\n* bilibili\n    * 主页链接一般为`https://space.bilibili.com/161775300?xxxxxxxxxx`，数字即为uid\n* rss\n    * rss链接即为uid\n</details>\n\n### 文字转图片\n因为可能要发送长文本，所以bot很可能被风控，如有需要请开启以图片形式发送文字，本项目使用的图片转文字方法是chromium（经典杀鸡用牛刀）。\n\n如果确定要开启推荐自行安装chromium，设置使用本地chromium，并且保证服务器有比较大的内存。\n## 功能\n* 定时爬取制定网站\n* 通过图片发送文本，防止风控\n* 使用队列限制发送频率\n\n## 鸣谢\n* [`go-cqhttp`](https://github.com/Mrs4s/go-cqhttp)：简单又完善的 cqhttp 实现\n* [`NoneBot2`](https://github.com/nonebot/nonebot2)：超好用的开发框架\n* [`HarukaBot`](https://github.com/SK-415/HarukaBot/): 借鉴了大体的实现思路\n\n## License\nMIT\n\n',
    'author': 'felinae98',
    'author_email': 'felinae225@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/felinae98/nonebot-hk-reporter',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
