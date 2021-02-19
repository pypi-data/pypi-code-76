import requests
import time
import logging
import base64
import json
import hashlib
import copy
from Crypto.Cipher import AES
from l0n0lhttputils.util import random_string


class wx_xcx_pay:
    def __init__(self, appid: str, mch_id: str, mch_secret: str, spbill_create_ip: str, pay_notify_url: str):
        """
        @appid:小程序ID
        @mch_id:商户号
        @mch_secret:商户号密码
        @spbill_create_ip:调用微信支付API的机器IP，支持IPV4和IPV6两种格式的IP地址。
        @pay_notify_url:异步接收微信支付结果通知的回调地址，通知url必须为外网可访问的url，不能携带参数。
        """
        self.appid = appid
        self.mch_id = mch_id
        self.mch_secret = mch_secret
        self.spbill_create_ip = spbill_create_ip
        self.pay_notify_url = pay_notify_url

    def pay_sign(self, params: dict) -> dict:
        """
        对微信支付的参数进行签名
            @params:dict:参数
            @return:dict:增加sign字段
        """
        keys = sorted(params)

        # 对参数按照key=value的格式，并按照参数名ASCII字典序排序如下：
        stringA = '&'.join(f"{key}={params[key]}" for key in keys)

        # 拼接API密钥：
        mch_sercret_key = self.mch_secret
        stringSignTemp = stringA + \
            f"&key={mch_sercret_key}"  # 注：key为商户平台设置的密钥key

        # md5签名
        sign = hashlib.md5(stringSignTemp).digest().upper()

        # 放入参数中
        params['sign'] = sign

        return params

    def request_pay(self, desc, out_trade_no, total_fee, openid):
        """
        向微信发起统一支付请求
            @desc:str:商品描述
            @out_trade_no:str:订单号
            @total_fee:int:费用(单位：分)
            @openid:str:用户openid
            @return:str:{"errMsg": "OK", "prepay_id": jret['prepay_id']}
        """
        # 构建微信支付统一下单参数
        params = {
            # 小程序ID
            "appid": self.appid,
            # 商户号
            "mch_id": self.mch_id,
            # 随机字符串，长度要求在32位以内
            "nonce_str": random_string(32),
            # 商品简单描述
            "body": desc,
            # 商户系统内部订单号，要求32个字符内，只能是数字、大小写字母_-|*且在同一个商户号下唯一
            "out_trade_no": str(out_trade_no),
            # 订单总金额，单位为分
            "total_fee": total_fee,
            # 支持IPV4和IPV6两种格式的IP地址。调用微信支付API的机器IP
            "spbill_create_ip": self.spbill_create_ip,
            # 异步接收微信支付结果通知的回调地址，通知url必须为外网可访问的url，不能携带参数。
            "notify_url": self.pay_notify_url,
            # 交易类型
            "trade_type": "JSAPI",
            # trade_type=JSAPI，此参数必传，用户在商户appid下的唯一标识。
            "openid": openid
        }

        # 签名
        params = self.pay_sign(params)

        # 向微信发起请求
        url = "https://api.mch.weixin.qq.com/pay/unifiedorder"

        ret = requests.get(url, params=params)

        if ret.status_code != 200:
            logging.error("[request_pay]Try start pay error!")
            return {"errMsg": "请求微信开始支付失败"}

        jret: dict = ret.json()

        if jret["return_code"] != "SUCCESS":
            return_msg = jret['return_msg']
            logging.error(f"[request_pay]{return_msg}")
            return {"errMsg": f"[request_pay]{return_msg}"}

        # 验证签名，防止中间人攻击
        copy_ret: dict = copy.deepcopy(jret)
        copy_ret.pop('sign')
        copy_ret = self.pay_sign(copy_ret)

        if copy_ret['sign'] != jret['sign']:
            logging.error(f"[request_pay]微信返回签名错误")
            return {"errMsg": f"微信返回签名错误"}

        if jret['result_code'] != "SUCCESS":
            return_msg = jret['err_code_des']
            logging.error(f"[request_pay]{return_msg}")
            return {"errMsg": f"{return_msg}"}

        return {"errMsg": "OK", "prepay_id": jret['prepay_id']}

    def get_order_status(self, out_trade_no: str) -> dict:
        """
        查询订单支付状态
            @out_trade_no:str:订单号
            @return:dict:订单支付成功返回dict，否则返回None
        """
        params = {
            "appid": self.appid,
            "mch_id": self.mch_id,
            "out_trade_no": out_trade_no,
            "nonce_str": random_string(32)
        }
        params = self.pay_sign(params)

        url = "https://api.mch.weixin.qq.com/pay/orderquery"

        ret = requests.get(url, params=params)

        if ret.status_code != 200:
            logging.error("[get_order_status] Network error!")
            return {"errMsg": "[get_order_status] Network error!"}

        jret = ret.json()

        return self.check_order_status(jret)

    def check_order_status(self, jret: dict):
        """
        检测支付结果
            @jret:支付结果
            @return:支付成功返回jret，失败返回None
        """
        # 查看支付结果
        if jret['return_code'] != "SUCCESS":
            err_msg = jret['return_msg']
            logging.error(f"[get_order_status]{err_msg}")
            return {"errMsg": f"[get_order_status]{err_msg}"}

        # 验证签名，防止中间人攻击
        copy_ret: dict = copy.deepcopy(jret)
        copy_ret.pop('sign')
        copy_ret = self.pay_sign(copy_ret)

        if copy_ret['sign'] != jret['sign']:
            logging.error(f"[get_order_status]wechat return error")
            return {"errMsg": f"[get_order_status]wechat return error"}

        if jret['result_code'] != "SUCCESS":
            err_msg = jret['err_code_des']
            logging.error(f"[get_order_status]{err_msg}")
            return {"errMsg": f"[get_order_status]{err_msg}"}

        # 查看订单是否成功
        if jret['trade_state'] != "SUCCESS":
            return

        return {"errMsg": "OK", "jret": jret}


class wx_gzh:
    def __init__(self, gzh_appid, gzh_secret):
        self.gzh_appid = gzh_appid
        self.gzh_secret = gzh_secret
        self.access_tokens = {}
        self.jssdk_access_token = {}
        self.jssdk_ticket = None

    def get_access_token(self, code):
        """
        获取用户token
            @code:用户授权code
            @return
                access_token 网页授权接口调用凭证,注意：此access_token与基础支持的access_token不同
                expires_in	access_token接口调用凭证超时时间，单位（秒）
                refresh_token 用户刷新access_token
                openid 用户唯一标识，请注意，在未关注公众号时，用户访问公众号的网页，也会产生一个用户和公众号唯一的OpenID
                scope 用户授权的作用域，使用逗号（,）分隔
        """
        # 向微信验证用户的code是否正确，并获取用户的openid
        check_result = requests.get("https://api.weixin.qq.com/sns/oauth2/access_token", params={
            'appid': self.gzh_appid,
            "secret": self.gzh_secret,
            "code": code,
            "grant_type": 'authorization_code'
        })

        # 判断验证时网络是否正常
        if check_result.status_code != 200:
            logging.error("向微信获取access_token发生网络错误")
            return {"errMsg": "向微信获取access_token发生网络错误"}

        # 获取微信的验证结果，openid
        json_value = check_result.json()
        if json_value.get("errcode"):
            return {"errMsg": "验证失败"}

        # 设置过期时间
        json_value['end_time'] = time.time() + json_value['expires_in']
        json_value['refresh_end_time'] = time.time() + 30 * 86400
        self.access_tokens[json_value['openid']] = json_value

        return {"errMsg": "OK", "data": json_value}

    def refresh_access_token(self, openid):
        """
        刷新用户token
            @openid:str:用户openid
            @return:
                access_token 网页授权接口调用凭证,注意：此access_token与基础支持的access_token不同
                expires_in	access_token接口调用凭证超时时间，单位（秒）
                refresh_token	用户刷新access_token
                openid	用户唯一标识
                scope	用户授权的作用域，使用逗号（,）分隔
                错误时微信会返回JSON数据包如下（示例为code无效错误）:
                {"errcode":40029,"errmsg":"invalid code"}
        """
        token_data = self.access_tokens.get(openid)
        if token_data is None:
            return {"errMsg": "用户不存在"}

        refresh_token_end_time = token_data['refresh_end_time']
        if time.time() >= refresh_token_end_time:
            return {"errMsg": "token过期"}

        # 刷新用户的
        check_result = requests.get("https://api.weixin.qq.com/sns/oauth2/refresh_token", params={
            'appid': self.gzh_appid,
            "refresh_token": token_data['refresh_token'],
            "grant_type": 'refresh_token'
        })

        # 判断验证时网络是否正常
        if check_result.status_code != 200:
            logging.error("[refresh_access_token] 向微信刷新access_token发生网络错误")
            return {"errMsg": "向微信刷新access_token发生网络错误"}

        # 获取微信的验证结果,openid
        json_value = check_result.json()
        if json_value.get("errcode"):
            return {"errMsg": "失败"}

        # 设置过期时间
        json_value['end_time'] = time.time() + json_value['expires_in']

        # 刷新缓存
        self.access_tokens[openid] = json_value

        return {"errMsg": "OK", "data": json_value}

    def get_user_info(self, openid):
        """
        获取用户数据
            @openid:str:用户的openid
            @return
                openid	用户的唯一标识
                nickname	用户昵称
                sex	用户的性别，值为1时是男性，值为2时是女性，值为0时是未知
                province	用户个人资料填写的省份
                city	普通用户个人资料填写的城市
                country	国家，如中国为CN
                headimgurl	用户头像，最后一个数值代表正方形头像大小（有0、46、64、96、132数值可选，0代表640*640正方形头像），用户没有头像时该项为空。若用户更换头像，原有头像URL将失效。
                privilege	用户特权信息，json 数组，如微信沃卡用户为（chinaunicom）
                unionid	只有在用户将公众号绑定到微信开放平台帐号后，才会出现该字段。
                错误时微信会返回JSON数据包如下（示例为openid无效）:
                {"errcode":40003,"errmsg":" invalid openid "}
        """
        # 获取token
        token_data = self.access_tokens.get(openid)
        if token_data is None:
            return {"errMsg": "获取token失败"}

        # 查看token是否过期
        if time.time() >= token_data['end_time']:
            token_data = self.refresh_access_token(openid)

        # 刷新失败
        if token_data is None:
            return {"errMsg": "刷新失败"}

        # 查看scope
        if "snsapi_userinfo" not in token_data['scope']:
            return {"errMsg": "查看scope失败"}

        # 获取用户信息
        check_result = requests.get("https://api.weixin.qq.com/sns/userinfo", params={
            'lang': "zh_CN",
            "access_token": token_data['access_token'],
            "openid": openid
        })

        # 判断验证时网络是否正常
        if check_result.status_code != 200:
            logging.error("[get_user_info] 向微信请求用户数据发生网络错误")
            return {"errMsg": "向微信请求用户数据发生网络错误"}

        # 获取微信的验证结果,openid
        json_value = check_result.json()
        if json_value.get("errcode"):
            return {"errMsg": "微信的验证失败"}

        return {"errMsg": "OK", "data": json_value}

    def get_jssdk_ticket(self):
        # 检测是否有token或者token是否过期
        if not self.jssdk_access_token.get("token") or time.time() - self.jssdk_access_token["timestamp"] >= self.jssdk_access_token['expires_in']:
            # 向微信请求token
            ret = requests.get("https://api.weixin.qq.com/cgi-bin/token", params={
                "grant_type": "client_credential",
                "appid": self.gzh_appid,
                "secret": self.gzh_secret
            })

            if ret.status_code != 200:
                logging.error(
                    "[get_jssdk_ticket] 向微信请求jssdk access_token发生网络错误")
                return {"errMsg": "向微信请求jssdk access_token发生网络错误"}


            # 缓存token
            self.jssdk_access_token = ret.json()

            # 处理错误
            if self.jssdk_access_token.get("errmsg"):
                return {"errMsg": self.jssdk_access_token.get("errmsg")}

            # 设置时间戳
            self.jssdk_access_token["timestamp"] = time.time()

        # 查看ticket是否过期
        if self.jssdk_ticket is None or time.time() - self.jssdk_ticket['timestamp'] >= self.jssdk_ticket['expires_in']:
            # 通过token获取 jsapi_ticket
            ret = requests.get("https://api.weixin.qq.com/cgi-bin/ticket/getticket", params={
                "access_token": self.jssdk_access_token['access_token'],
                "type": "jsapi"
            })

            # 检测网络是否时报
            if ret.status_code != 200:
                logging.error("wx_token get jsapi_ticket error!")
                return {"errMsg": "get jsapi_ticket error!"}

            # 如果失败，返回失败
            ret = ret.json()
            if ret['errcode'] != 0:
                logging.error("wx_token get jsapi_ticket error!")
                return {"errMsg": "get jsapi_ticket error!"}

            # 缓存ticket
            del ret['errcode']  # 删除没用的量
            del ret['errmsg']  # 删除没用的量

            # 缓存
            self.jssdk_ticket = ret
            self.jssdk_ticket['timestamp'] = time.time()

        return {"errMsg": "OK", "data": self.jssdk_ticket}


class wx_data_crypt:
    def __init__(self, appId, sessionKey):
        self.appId = appId
        self.sessionKey = sessionKey

    def decrypt(self, encryptedData: str, iv: str) -> dict:
        # base64 decode
        sessionKey = base64.b64decode(self.sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))

        if decrypted['watermark']['appid'] != self.appId:
            raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]
