import time
import uuid
import json
import logging
import hashlib
from aiohttp import web
from aiohttp.web import Request


class token_mgr:
    def __init__(self):
        self.user_token = {}
        self.token_user = {}
        self.token_timestamp = {}
        self.timer = 0
        self.espire_time = 120

    def gen_token(self, target_id: str):
        """
        根据target_id生成csrf_token
            @target_id:str:目标target_id
            @return:str:目标用户的token
        """
        # 删除以前的token，最多有两个token
        self.user_token[target_id] = self.user_token.get(target_id) or []
        pre_tokens: list = self.user_token[target_id]
        if len(pre_tokens) >= 2:
            token = pre_tokens.pop(0)
            self.token_user.pop(token)
            self.token_timestamp.pop(token)

        # 生成新的token
        token = str(uuid.uuid4())
        while self.token_user.get(token):
            token = str(uuid.uuid4())

        # token缓存
        self.token_user[token] = target_id
        self.token_timestamp[token] = time.time() + self.espire_time
        return token

    def remove_token(self, token:str, target_id:str=None):
        """
        删除token
            @token:str:token
            @target_id:str:目标ID
        """
        if target_id is None:
            target_id = self.token_user.get(token)
        if target_id is None:
            return

        self.user_token[target_id] = self.user_token.get(target_id) or []
        
        try:
            self.user_token[target_id].remove(token)
        except:
            pass
        del self.token_user[token]
        del self.token_timestamp[token]

    def check_token(self, token):
        """
        根据token获取用户的target_id
            @token:str:用户的token
            @return:target_id:str
        """
        timestamp = self.token_timestamp.get(token)
        if timestamp is None:
            return

        target_id = self.token_user.get(token)
        if target_id is None:
            return

        cur_time = time.time()
        if cur_time >= timestamp:
            self.remove_token(token, target_id)
            return

        self.token_timestamp[token] = cur_time + self.espire_time

        return target_id

    def update_token(self, elapse):
        """
        更新删除过期的token
        """
        self.timer += elapse
        if self.timer < 1:
            return
        self.timer = 0

        remove_list = []

        cur_time = time.time()
        for token, stamp in self.token_timestamp.items():
            if cur_time >= stamp:
                remove_list.append(token)

        for token in remove_list:
            self.remove_token(token)


def check_token(tmgr: token_mgr):
    """
    csrf token验证装饰器
    """
    def g(func):
        async def f(request: Request):
            if "token" not in request.headers:
                return web.json_response({"errMsg": "######"}, headers={
                    "token": "error",
                    "Access-Control-Allow-Origin": "*"
                })
            token = request.headers["token"]
            openid = tmgr.check_token(token)
            if openid is None:
                return web.json_response({"errMsg": "######"}, headers={
                    "token": "error",
                    "Access-Control-Allow-Origin": "*"
                })
            setattr(request, "openid", openid)
            md5value = hashlib.md5(openid.encode('utf8'))
            setattr(request, "id", md5value.hexdigest())
            if request.headers['content-type'] == 'application/json':
                setattr(request, "jsonvalue", await request.json())
                logging.info(msg=json.dumps(request.jsonvalue, indent="\t"))
            return await func(request)
        return f
    return g
