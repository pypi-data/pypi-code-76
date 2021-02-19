#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : feishu_bot_app
# @Time         : 2021/1/28 8:32 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :

"""
todo:
增加卡片@
增加get/post发送消息
"""
from fastapi import FastAPI
from starlette.requests import Request
import pandas as pd
from miwork.feishu import Feishu
from meutils.http_utils import request
from meutils.log_utils import logger4feishu

app = FastAPI()

fs = Feishu()


@app.post("/hive/{chat}/{title}")
async def hive_http_callback(request: Request, chat, title, at_users=None, image_desc='我是个数据框'):
    """at_users逗号分割

    数据工厂http回调
    """
    data_str = dict(await request.form()).get('data', '')
    if data_str:
        data = eval(data_str)
        df = pd.DataFrame(data[1:], columns=data[0])
    else:
        df = pd.DataFrame()

    fs.send_by_df_card(
        chat=chat,
        title=title,
        subtitle='',
        df=df.to_dict('r'),
        image_desc=image_desc
    )

    # fs.send_by_card(
    #     chat=chat,  # 'PUSH算法组',
    #     title=title,
    #     text=df.to_string(index=True),
    #     md_text="",
    #     at_user=at_users.split(',')[0] if at_users else None  # card 增加@
    # )


@app.get("/common/{chat}/{title}")
def send_by_card_get(request: Request, chat, title):
    """
    /common/PUSH算法组/我是个标题?text=我是条内容
    """
    input = dict(request.query_params)
    text = input.get('text', '')

    fs.send_by_card(chat=chat, title=title, text="", md_text=text)


@app.post("/common/{chat}/{title}")
def send_by_card_post(chat, title, kwargs: dict):
    text = kwargs.get('text', '')

    fs.send_by_card(chat=chat, title=title, text="", md_text=text)


# wehooks
@app.post("/wehook")
def wehook(kwargs: dict):
    """wehooks 内网穿透 解决网络不通的问题

    body = {

        'url': 'wehook_url',

        'post': {'title': '我是个标题', 'text': '我是条内容'}

    }

    """
    url = kwargs.get('url')
    post = kwargs.get('post')
    return request(url, json=post)


# card
@app.post("/image")
def send_df(kwargs: dict):
    """目前支持dataframe发送

    body = {

        "chat": "PUSH算法组",

        "title": "我是个标题",

        "subtitle": "我是个副标题",

        "image_desc": "我是个数据框",

        "df_json": [{"a": 1, "b": 2}]

    }

    """

    df = pd.DataFrame(kwargs.get('df_json'))

    fs.send_by_df_card(chat=kwargs.get('chat', 'PUSH算法组'),
                       title=kwargs.get('title', '我是一个标题'),
                       subtitle=kwargs.get('subtitle', ''),
                       df=df,
                       image_desc=kwargs.get('image_desc', '我是个数据框'))


@app.get("/logger/{title}")
def logger_get(request: Request, title):
    kwargs = dict(request.query_params)

    logger4feishu(title, kwargs.get('text', '我是个log'))


@app.post("/logger")
def logger_post(kwargs: dict):
    """
    {

        "title": "我是个标题",

        "text": "我是个log",

    }

    """
    logger4feishu(title=kwargs.get('title', '我是个标题'), text=kwargs.get('text', '我是个log'))


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0')
