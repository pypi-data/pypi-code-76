from tencentcloud.sms.v20190711 import sms_client, models as sms_models
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common import credential
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.profile.client_profile import ClientProfile
import json
import time
import random
import logging


class tencent_duan_xin:
    """
    腾讯短信发送
    """

    def __init__(self, secret_id: str, secret_key: str, sms_template_id: str, sms_signiture: str, sms_sdk_appid: str, sms_code_espired_time: int,  resend_time: int):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.sms_template_id = sms_template_id
        self.sms_signiture = sms_signiture
        self.sms_sdk_appid = sms_sdk_appid
        self.sms_code_espired_time = sms_code_espired_time
        self.sms_resend_time = resend_time
        self.vertification_codes = {}

    def gen_verification_code(self, openid: str) -> int:
        """
        生成对应appid的验证码，并纪录其对应关系和失效时间
            @openid:str:目标用户的openid
            @espire_time:int:超时时间
            @resend_time:int:重复发送时间间隔，用于判定是否重新发送验证码，如果验证码发送还在cd状态则不发送验证码，返回0
            @return:int:6位验证码，如果为0表示不需要重新发送验证码
        """
        # 规范时间为秒
        espired_time = int(self.sms_code_espired_time) * 60
        resend_time = int(self.sms_resend_time) * 60

        # 用户可能在时间间隔内发送了多次验证码，前面发送的验证码如果未超时尚可使用
        self.vertification_codes[openid] = self.vertification_codes.get(openid) or [
        ]
        code_list: list = self.vertification_codes[openid]
        cur_time = time.time()

        # 删除过期的验证码，计算出最新的验证码
        i = 0
        newest_time = 0
        while i < len(code_list):
            if code_list[i]['espired_time'] > newest_time:
                newest_time = code_list[i]['espired_time']

            if cur_time >= code_list[i]['espired_time']:
                code_list.pop(i)
                i -= 1
            i += 1

        # 检测是否尚在cd计时中
        if cur_time - (newest_time - espired_time + resend_time) < resend_time:
            return 0

        # 生成验证码并缓存过期时间
        code = random.randint(100000, 999999)
        self.vertification_codes[openid].append({
            "code": code,
            "espired_time": time.time() + espired_time
        })

        # 返回验证码
        return code

    def check_vertification_code(self, openid: str, code: str) -> int:
        """
        检测用户输入的code是否正确
            @openid:str:目标用户
            @code:str:用户输入的code
            @return: 0 表示匹配成功，1表示验证码超时，2表示匹配失败
        """
        code_list = self.vertification_codes.get(openid)
        if code_list is None:
            return 2

        cur_time = time.time()
        for code_data in code_list:
            if cur_time <= code_data['espired_time'] and code == str(code_data['code']):
                self.vertification_codes[openid].clear()
                return 0

        self.vertification_codes[openid].clear()

        return 2

    def send_vertification_code(self, openid: str, phone: str, code: str) -> dict:
        """
        发送短信验证码,并记录该用户的验证码，和失效时间
            @openid:目标用户ID
            @phone:目标手机号码
            @code:验证码
            @return:dict:腾讯接口的返回值
        例如：
            send_vertification_code('xxx','15200001111','1234')
            {
                "Response": {
                    "SendStatusSet": [{
                        "SerialNo": "2104:167949002415940010463502127",
                        "PhoneNumber": "+8615200001111",
                        "Fee": 1,
                        "SessionContext": "",
                        "Code": "Ok",
                        "Message": "send success",
                        "IsoCode": "CN"}],
                    "RequestId": "10024749-d20c-4ad8-b5ff-99e0d5d0f13c"
                }
            }
        """
        try:
            cred = credential.Credential(self.secret_id, self.secret_key)
            httpProfile = HttpProfile()
            httpProfile.endpoint = "sms.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = sms_client.SmsClient(cred, "ap-beijing", clientProfile)

            req = sms_models.SendSmsRequest()
            req.PhoneNumberSet = [f"86{phone}"]
            req.TemplateID = self.sms_template_id
            req.Sign = self.sms_signiture
            req.SmsSdkAppid = self.sms_sdk_appid
            req.TemplateParamSet = [str(code), str(self.sms_code_espired_time)]
            resp = client.SendSms(req)
            resp_json_string = resp.to_json_string()
            logging.info(resp_json_string)
            return json.loads(resp_json_string)
        except TencentCloudSDKException as err:
            logging.error(err)
