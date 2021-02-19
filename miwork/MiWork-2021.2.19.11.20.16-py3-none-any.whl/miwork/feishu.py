#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MiWork.
# @File         : feishu
# @Time         : 2021/1/28 7:42 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :
# 优化 print tab

from meutils.pipe import *
from miwork import OpenLark
from miwork.dt_enum import MessageType
import dataframe_image as dfi


class BotConf(BaseConfig):
    betterme: List[str] = []


class Feishu(object):

    def __init__(self, bot_name='betterme'):
        """

        :param bot_name: from zk
        """

        app_id, app_secret = BotConf.parse_zk('/mipush/bot').__getattribute__(bot_name)
        self.api = OpenLark(app_id=app_id, app_secret=app_secret)

        self.name2id = {chat.name: chat.chat_id for chat in self.chats}
        # self.chat_id = name2id[chat_name]
        # api.get_chat_info('oc_ea0c8c5a34480814ad8df126922021aa')
        # user_id, name = api.email_to_id('yuanjie@xiaomi.com')

    @property
    def chats(self):
        _, _, _chats = self.api.get_chat_list_of_bot()
        return _chats

    def send_by_image(self, chat_name='PUSH算法组', image="/Users/yuanjie/Desktop/qw.jpg"):

        image_key, url = self.api.upload_image(image)
        # api.get_image(image_key) # bytes
        content = {
            'image_key': image_key
        }
        return self.api.send_raw_message(
            open_chat_id=self.name2id.get(chat_name),
            msg_type=MessageType.image,
            content=content
        )

    def send_by_text(self, chat_name='PUSH算法组', text='这是一条文本', at_user='yuanjie@xiaomi.com'):
        '''

        :param text:
        :param at_user: all
        :return:
        '''
        if at_user:
            if at_user == 'all':
                at_user_id = 'all'
            else:
                at_user_id, name = self.api.email_to_id(at_user)

            content = {"text": f'<at user_id="{at_user_id}"> </at> {text}'}
        else:
            content = {"text": text}

        return self.api.send_raw_message(
            open_chat_id=self.name2id.get(chat_name),
            msg_type=MessageType.text,
            content=content
        )

    def send_by_post(self, chat_name='PUSH算法组', title='我是一个标题', text='我是一条文本', at_user='yuanjie@xiaomi.com'):
        """发送富文本信息

        {
            "tag": "a",
            "text": "超链接",
            "href": "http://www.feishu.cn"
        }

        {
            "tag": "text",
            "un_escape": True,
            "text": "第一行&nbsp;:"
        },
        """

        content = {"post": {"zh_cn": {
            "title": title,
            "content": [[]]
        }}}
        content['post']['zh_cn']['content'][0].append({'tag': 'text', 'text': text})

        if at_user:
            if at_user == 'all':
                at_user_id = 'all'
            else:
                at_user_id, name = self.api.email_to_id(at_user)

            content['post']['zh_cn']['content'][0].append({'tag': 'at', 'user_id': at_user_id})

        return self.api.send_raw_message(
            open_chat_id=self.name2id.get(chat_name),
            msg_type=MessageType.post,
            content=content
        )

    def send_by_card(self, chat='PUSH算法组',
                     title='我是一个标题',
                     text='我是一条文本',
                     md_text='我是一条md文本',
                     image='/Users/yuanjie/Desktop/lz.gif',
                     at_user='yuanjie@xiaomi.com'):
        """
        markdown: https://open.f.mioffice.cn/document/ukTMukTMukTM/uADOwUjLwgDM14CM4ATN
        """
        image_key, url = self.api.upload_image(image)

        content = {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": title
                }
            },

            "elements": [
                # https://open.f.mioffice.cn/document/ukTMukTMukTM/uUjNwUjL1YDM14SN2ATN
                {
                    "tag": "img",
                    # "title": {
                    #     "tag": "plain_text",
                    #     "content": "Block-img\n"
                    # },
                    "img_key": image_key,
                    "alt": {
                        "tag": "plain_text",
                        "content": "Block-img\n"
                    }
                },

                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": text

                    },
                    "fields": [
                        {
                            "is_short": False,
                            "text": {
                                "tag": "lark_md",
                                "content": md_text  # md
                            }
                        }
                    ]
                },
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "Read"
                            },
                            "type": "default"
                        }
                    ]
                }
            ]
        }

        return self.api.send_raw_message(
            open_chat_id=self.name2id.get(chat),
            msg_type=MessageType.card,
            content_key='card',
            content=content
        )

    def send_by_df_card(self, chat='PUSH算法组',
                        title='我是一个标题',
                        subtitle='我是个副标题',
                        df=None,
                        image_desc='我是一个副标题',  # alt
                        ):

        os.system('rm img.png')
        dfi.export(df, 'img.png', table_conversion='', max_rows=-1, max_cols=-1)
        image_key, url = self.api.upload_image('img.png')

        content = {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": title
                }
            },

            "elements": [

                {
                    "tag": "img",  # https://open.f.mioffice.cn/document/ukTMukTMukTM/uUjNwUjL1YDM14SN2ATN
                    "title": {
                        "tag": "plain_text",
                        "content": subtitle
                    },
                    "img_key": image_key,
                    "alt": {
                        "tag": "plain_text",
                        "content": image_desc
                    }
                },

                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "请查收"
                            },
                            "type": "default"
                        }
                    ]
                }
            ]
        }

        return self.api.send_raw_message(
            open_chat_id=self.name2id.get(chat),
            msg_type=MessageType.card,
            content_key='card',
            content=content
        )


# print(api.get_chat_list_of_user(user_access_token='t-e15083e6e2132cefc8c5133a7b4ba235127ec79f'))

# print(api.tenant_access_token)
# print(api.app_access_token)
# print(api.gen_oauth_url())
#
# api.get_approval_instance_code_list()
# api.mina_code_2_session()


# api.handle_card_message_callback()

# a = api.get_chat_info('oc_ea0c8c5a34480814ad8df126922021aa')
# print([member.open_id for member in a.members])

if __name__ == '__main__':
    # Feishu().send_by_card(md_text=pd.DataFrame(np.random.random((5, 5))).to_markdown())

    from meutils.pipe import *

    #
    # df = pd.DataFrame(np.random.random((10, 5)))
    # tb = Besttable.dfdraw(df)
    # print(tb)
    # # Feishu().send_by_text(text=df.to_string())
    # # Feishu().send_by_text(text=tb.replace('\n', '\r\n'))
    Feishu().send_by_df_card(df=pd.DataFrame(np.random.random((10, 10))))

    # Feishu().send_by_image('南京算法', '/Users/yuanjie/Desktop/lz.gif')
