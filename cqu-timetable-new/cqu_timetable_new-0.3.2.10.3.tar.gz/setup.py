# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cqu_timetable_new']

package_data = \
{'': ['*']}

install_requires = \
['icalendar>=4.0.7,<5.0.0', 'openpyxl>=3.0.6,<4.0.0']

extras_require = \
{'pyqt': ['pyside2>=5.15.2,<6.0.0'], 'tk': ['easygui>=0.98.2,<0.99.0']}

entry_points = \
{'console_scripts': ['cqu_timetable_new = cqu_timetable_new:main',
                     'cqu_timetable_new-qt = cqu_timetable_new.QTGUI:main',
                     'cqu_timetable_new-tk = cqu_timetable_new.tkgui:main']}

setup_kwargs = {
    'name': 'cqu-timetable-new',
    'version': '0.3.2.10.3',
    'description': 'Generate CQU timetable iCalendar (ics) file',
    'long_description': '# ICS 课程表文件生成脚本\n适用于最新选课站点生成的 `xlsx` 格式的课表转换为日历软件能认到的 `ICS` 格式文件.\n## 使用说明\n使用 pip 安装依赖：\n```bash\npip install .\n```\n\n### 直接运行 (demo)\n准备从新选课网站下载的 `课表.xlsx` 或者 json 文件，放置于任意目录。</br>\n配置文件格式如下:\n```editorconfig\n[config]\ndebug = False\nbase_dir = /home/ddqi/kb.xlsx\nstart_date = 20210301\nfile_name = timetable.ics\n```\n\n|配置项|类型|示例|注释|\n|:-|:--|:--|:--|\n|debug|boolean|True|控制是否为调试模式，可选值：True False|\n|base_dir|str|/home/ddqi/kb.xlsx|指向课表文件的路径|\n|start_date|str|20210301|行课日期|\n|file_name|str|timetable.ics|生成的 ics 文件名（为避免编码问题不要用中文），扩展名请勿更改，文件名不可包含中文|\n\n将配置文件 `config.txt` 放置在工作目录下，终端执行：\n```bash\ncqu_timetable_new\n```\n将生成指定文件名的 iCalendar 格式文件\n\n### tkinter 前端\n\n使用 pip 安装依赖：\n```bash\npip install .[tk]\n```\n之后可运行\n```bash\ncqu_timetable_new-tk\n```\n启动 tkinter 前端。\n\n###  Qt5 前端\n\n使用 pip 安装依赖：\n```bash\npip install .[pyqt]\n```\n之后可运行\n```bash\ncqu_timetable_new-qt\n```\n启动 Qt5 前端。\n\n### 作为库来使用\n\n使用时需要先生成课表数据，再从课表数据中生成日历\n\n1. 生成课表数据\n    - 可通过 `loadIO_from_json` 或 `loadIO_from_xlsx` 函数从文件或数据流中读取 json 或 xlsx，返回解析出的课表数据\n    - 也可通过 `load_from_json` 或 `load_from_xlsx` 函数读取 `str` 或 `bytes` 格式的 json 或 xlsx 数据，返回解析出的课表数据\n2. 生成日历数据\n\n    使用 `mkical` 函数，第一个参数是上一步得到的课表数据，第二个参数是 `datetime.date` 类型的开学日期，返回 `icalendar.Calendar` 类型的日历数据，可通过其 `to_ical` 得到 ics 文件的内容。\n\ndemo 可见于 [main.py](main.py) 中的 `main` 函数\n\n## FAQ\nQ: 为什么不带有登录功能？</br>\nA： 因为我懒。如果你能做出带有登录功能的脚本请随意 pr 。我只信得过可以下载的自动生成的课表。\n（主要还是依赖项少一些）\n## 姊妹项目\n[cm-http-api](https://github.com/weearc/cm-http-api) （开发中）\n## LICENSES\nAGPLv3\n',
    'author': 'weearc',
    'author_email': 'qby19981121@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/weearc/cqu_timetable_new',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
