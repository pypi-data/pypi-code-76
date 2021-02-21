# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_bam',
 'nonebot_plugin_bam.bilibili',
 'nonebot_plugin_bam.database',
 'nonebot_plugin_bam.database.tables',
 'nonebot_plugin_bam.tasks']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.7.2,<4.0.0',
 'nonebot-plugin-apscheduler>=0.1.2,<0.2.0',
 'nonebot2>=2.0.0a10,<3.0.0',
 'peewee>=3.14.1,<4.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-bam',
    'version': '0.1.3',
    'description': 'Bilibili activity monitor plugin for nonebot',
    'long_description': '# Bilibili Activity Monitor\n\nB 站用户监视器，自动监控用户的动态和直播状态，在有新动态和直播状态改变时向关注群发送提示信息。\n\n可多群共用，每个群可以有不同的关注列表。自带数据落地存储机制，重启后可保留各群关注状态。\n\n## 功能示例\n\n### 直播提醒\n\n![screenshot-live]\n\n### 动态提醒\n\n![screenshot-act-normal]\n\n![screenshot-act-repost]\n\n*特定用户 at 特定群友功能暂时没来得及做命令，目前需要直接改数据库，目前可以假装这个功能不存在。*\n\n## 使用\n\n```bash\npip install nonebot-plugin-bam\n```\n\n```python\nimport nonebot\nfrom nonebot.adapters.cqhttp import Bot as CQHTTPBot\n\nnonebot.init(_env_file=".env")\n\ndriver = nonebot.get_driver()\ndriver.register_adapter("cqhttp", CQHTTPBot)\n\nnonebot.load_builtin_plugins()\n\n# load other plugins\n\n# bam need this to manage background tasks\nnonebot.load_plugin("nonebot_plugin_apscheduler")\nnonebot.load_plugin("nonebot_plugin_bam")\n\nnonebot.run()\n```\n\n其中 `.env` 文件除了 nonebot 的常规配置项外，还有可添加以下配置属性（下面展示的是默认值）：\n\n```env\n# 数据落地文件路径，建议设置一下。\n# 用默认值（储存在内存中）的话一重启数据就没了\nBAM_DB_FILE=":memory:"\n\n# 重启时将所有用户的直播状态设置为未开播，而不是使用上次记录的状态。\n# 正常使用不要打开此选项，是调试用的\nBAM_ON_STARTUP_CLEAN_LIVE_STATUS=false \n\n# 监控任务的间隔，这里设置的是每个用户间的间隔，而不是一轮的间隔。\n# 所以如果一共关注了 N 个人（多个群关注同一个人只算一个）\n# 那对于每个人来说，两次检测之间的间隔就是 N * interval\n# 一般来说不要设置在 5 以下，可能会被 B 站 API 反爬而拒绝响应\nBAM_TASK_INTERVAL=5\n\n# 使用那一个直播间状态查询 API，默认为 2，如果发现被封禁了可以临时调到 1 试试\nBAM_LIVE_API=2\n\n# 动态内容在发送到 QQ 时的最大长度，超过长度会截断，设置为 0 或负数表示不截断\nBAM_ACTIVITY_CONTENT_MAX_LENGTH=0\n```\n\n## 命令列表\n\n<details>\n<summary>点击展开</summary>\n\n### 群相关\n\n#### 群初始化\n\n命令：`@bot /bam/group/add [superuser_qq]`\n\nSUPERUSER ONLY，GROUP ONLY。\n\n在机器人加入群之后，首先使用此命令将群加入服务列表。\n\n参数：\n\n- superuser_qq：此群的 SUPERUSER，可以管理 Bot 在这个群的行为。可选参数，不填时则设置为使用此命令的人。\n\n#### 删除群\n\n命令：`@bot /bam/group/remove`\n\nSUPERUSER ONLY，GROUP ONLY。\n\n将当前群从服务列表中删除。\n\n#### 群列表\n\n命令：`/bam/group/list`\n\nSUPERUSER ONLY，PRIVATE ONLY。\n\n显示当前机器人服务的群列表。\n\n### 关注相关\n\n#### 添加关注\n\n命令：`[@bot] /bam/follower/add [qq_group_id] <bilibili_uid>`\n\nSUPERUSER ONLY, PRIVATE OR GROUP\n\n为群 `qq_group_id` 添加对 B 站用户 `bilibili_uid` 的监控。\n\n参数：\n\n- `qq_group_id`：操作群号。可选参数，如果在群聊中使用此命令则不能加此参数，默认为当前群。\n- `bilibili_uid`：B 站用户 UID，必填。\n\n注：`[@bot]` 表示在私聊中使用时不用(无法) at 机器人，下略。\n\n#### 删除关注\n\n命令：`[@bot] /bam/follower/remove [qq_group_id] <bilibili_uid>`\n\nSUPERUSER ONLY, PRIVATE OR GROUP\n\n为群 `qq_group_id` 删除对 B 站用户 `bilibili_uid` 的监控。\n\n参数：\n\n- `qq_group_id`：操作群号。可选参数，如果在群聊中使用此命令则不能加此参数，默认为当前群。\n- `bilibili_uid`：B 站用户 UID，必填。\n\n#### 群关注列表\n\n命令：`[@bot] /bam/follower/list [qq_group_id]`\n\nSUPERUSER ONLY, PRIVATE OR GROUP\n\n列出群 `qq_group_id` 的关注列表。\n\n参数：\n\n- `qq_group_id`：操作群号。可选参数，如果在群聊中使用此命令则不能加此参数，默认为当前群。\n\n### B 站相关\n\n#### 获取/更新用户数据\n\n命令：`[@bot] /bam/user/fetch <bilibili_uid>`\n\nSUPERUSER ONLY, PRIVATE OR GROUP\n\n获取或更新 B 站用户 `bilibili_uid` 的信息。\n\n参数：\n\n- `bilibili_uid`：B 站用户 UID，必填。\n\n#### 获取一个动态信息\n\n命令：`[@bot] /bam/act <bilibili_activity_id>`\n\nANYONE\n\n获取 B 站动态 `bilibili_activity_id` 的信息。\n\n参数：\n\n- `bilibili_activity_id`：B 站动态 ID。\n\n</details>\n\n## LICENSE\n\nMIT.\n\n[screenshot-live]: https://rikka.7sdre.am/files/af1c9c5a-5f8c-40df-b199-e97525368ec9.png\n[screenshot-act-normal]: https://rikka.7sdre.am/files/5350ce1c-63f6-4f43-abcc-004e9c722063.png\n[screenshot-act-repost]: https://rikka.7sdre.am/files/9c43a32b-2df7-4b93-be53-22c50a981c63.png\n',
    'author': '7sDream',
    'author_email': 'i@7sdre.am',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/7sDream/nonebot-plugin-bam',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
