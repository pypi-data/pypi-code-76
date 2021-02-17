# coding=utf8

__author__ = 'Alexander.Li'

import json
import aioredis
import asyncio
import logging
import traceback
from typing import List, Any
from pydantic import BaseModel, Field

MESSAGE_TYPE_REPLY = 'reply'


class Message(BaseModel):
    to: str = Field('', title="收件人")
    tp: str = Field('', title="消息类型")
    rms: List[str] = Field('', title="删除消息id列表")
    payload: dict = Field({}, title="内容")
    np: int = Field(0, title="是否要推送")


def message_id(message_obj: dict) -> str:
    return message_obj['id']


class MessageList(BaseModel):
    msgs: List[dict] = Field([], title="消息列表")


GLOBAL_CHN = "g:chn"


def p_key(key: str) -> str:
    return f"p1:{key}"


class PersistedRmq(object):
    redis_uri: str
    client_types: []
    dispatch_conn: aioredis.connection
    command_conn: aioredis.connection
    connections: dict
    running: bool

    @classmethod
    def init(cls, uri, client_types) -> "PersistedRmq":
        cls.redis_uri = uri
        return cls(client_types)

    def __init__(self, client_types):
        self.connections = {}
        self.running = True
        self.client_types = client_types

    async def start(self):
        self.dispatch_conn = await aioredis.create_redis_pool(self.__class__.redis_uri)
        self.command_conn = await aioredis.create_redis_pool(self.__class__.redis_uri)

    async def close(self):
        self.running = False
        await self.dispatch_conn.unsubscribe(GLOBAL_CHN)
        self.dispatch_conn.close()
        await self.dispatch_conn.wait_closed()
        self.command_conn.close()
        await self.command_conn.wait_closed()
        logging.error("Redis connection连接已关闭")

    async def get_persisted_message(self, chn: str, message_id: str):
        logging.error(f'will load:{chn} {message_id}')
        return await self.command_conn.hget(p_key(chn), message_id)

    async def persisted_message(self, chn: str, message_id: str, text_message: str):
        return await self.command_conn.hset(p_key(chn), message_id, text_message)

    async def unread_all(self, chn):
        return await self.command_conn.hgetall(p_key(chn))

    async def comfirm_issued(self, chn: str,  message_ids=[]):
        for message_id in message_ids:
            persisted_key = p_key(chn)
            await self.command_conn.hdel(persisted_key, message_id)
            logging.error(f'del old message: {message_id}')

    async def push(self, key, payload):
        await self.command_conn.lpush(key, payload)

    def channel_reactor(self):
        asyncio.get_running_loop().create_task(self.wait_trans_message())

    async def wait_trans_message(self):
        chs = await self.dispatch_conn.subscribe(GLOBAL_CHN)
        logging.error(f'subscribe chn:{GLOBAL_CHN}')
        while self.running:
            if await chs[0].wait_message():
                message = await chs[0].get()
                message_str = str(message, encoding='utf8')
                target, message_id = message_str.split(':')
                if target in self.connections:
                    socks: dict = self.connections[target]
                    bad_socks = []
                    for cid, sock in socks.items():
                        try:
                            msg = await self.get_persisted_message(target, message_id)
                            message_payload = json.loads(str(msg, encoding='utf8'))
                            messages = MessageList(msgs=[message_payload, ])
                            # payload = json.dumps({'msgs': [json.loads(str(msg, encoding='utf8')), ]})
                            payload = messages.json()
                            await sock.send_text(payload)
                            logging.error('msg 已经下发给了:%s', target)
                        except Exception as ex:
                            logging.error(f'error:{ex}')
                            logging.error("连接已经中断")
                            bad_socks.append((target, cid))
                    for t, c_id in bad_socks:
                        del self.connections[t][c_id]

    async def on_accept_socket(self, chn, cid, sock, after_dispached=None):
        # 添加连接到本地连接池
        if chn not in self.connections:
            self.connections[chn] = {cid: sock}
        else:
            self.connections[chn][cid] = sock
        # 查找有没有老数据需要下发
        old_messages = await self.unread_all(chn)
        if old_messages:
            try:
                msgs = []
                for k, v in old_messages.items():
                    msgs.append(json.loads(v))
                await sock.send_text(json.dumps({'msgs': msgs}))
                logging.error('旧 msg 已经下发给了:%s', chn)
            except Exception as ex:
                logging.error(f'error1:{traceback.print_exc()}')
                # 如果无法下发就说明连接断了，直接退出，并将连接从池里退出
                del self.connections[chn][cid]
                return
        while True:
            try:
                message = await sock.receive_text()
                message_obj = Message().parse_raw(message)
                message_type = message_obj.tp
                if message_type == MESSAGE_TYPE_REPLY:
                    message_ids = message_obj.rms
                    logging.error(f'reply: {message_ids}')
                    await self.comfirm_issued(chn, message_ids=message_ids)
                else:
                    await self.publish(message_obj.to, message_obj.payload)
                    if after_dispached:
                        await after_dispached(self, message_obj.to, message_obj)
            except Exception as ex:
                # 读取数据失败，标示连接中断了
                logging.error(f'error:{ex} {chn} 断开了连接')
                #logging.error(f'error2:{traceback.print_exc()}')
                del self.connections[chn][cid]
                return

    async def publish(self, to_chn: str, message_obj: dict):
        msg_id = message_id(message_obj)
        dispatch_message = ":".join([to_chn, msg_id])
        await self.persisted_message(to_chn, msg_id, json.dumps(message_obj))
        await self.dispatch_conn.publish(GLOBAL_CHN, dispatch_message)

