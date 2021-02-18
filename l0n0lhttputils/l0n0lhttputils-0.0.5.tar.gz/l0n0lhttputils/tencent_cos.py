# -*- coding:UTF-8 -*-
# 作者: l0n0l
# 时间: 2020/09/22 周二
# 点: 18:00:55

# 描述: 腾讯 对象存储
from tencentcloud.sms.v20190711 import sms_client, models as sms_models
from tencentcloud.sts.v20180813 import sts_client, models as sts_models
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common import credential
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.profile.client_profile import ClientProfile
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos import streambody
import json
import logging


class cos_bucket:
    def __init__(self, bucket_name, region, secret_id, secret_key):
        self.bucket = bucket_name
        self.region = region
        self.secret_id = secret_id
        self.secret_key = secret_key

    def get_temp_secret(self, openid: str, statement: dict, duration: int = 1800):
        """
        获取临时访问凭证
            @openid:str:用户的openid
            @statement:dict:权限分配参数{
                "前缀":"rwx" r表示读，w表示写，x表示删除
            }
            @duration:int:密钥时常，默认为None
            @return:dict:访问权限密钥 
        """
        try:
            bucket = self.bucket
            appid = str(bucket[(bucket.rfind('-') + 1):]).strip()
            statements = []
            for prefix, priveleges in statement.items():
                actions = []
                if 'r' in priveleges:
                    actions.append("name/cos:GetObject")
                    actions.append("name/cos:GetBucket")
                if 'w' in priveleges:
                    actions.append("name/cos:PutObject")
                    actions.append("name/cos:PostObject")
                    actions.append("name/cos:putObjectCopy")
                if 'x' in priveleges:
                    actions.append("name/cos:DeleteObject")
                    actions.append("name/cos:DeleteMultipleObjects")
                statements.append({
                    "effect": "allow",
                    "action": actions,
                    "resource": [f"qcs::cos::uid/{appid}:{bucket}/{prefix}/*"]
                })
            cred = credential.Credential(
                self.secret_id, self.secret_key)
            httpProfile = HttpProfile()
            httpProfile.endpoint = f"sts.ap-beijing.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = sts_client.StsClient(
                cred, self.region, clientProfile)

            req = sts_models.GetFederationTokenRequest()
            req.DurationSeconds = duration
            req.Name = openid

            req.Policy = json.dumps({
                "version": "2.0",
                "statement": statements
            })
            resp = client.GetFederationToken(req)
            resp_json_string = resp.to_json_string()
            logging.info(resp_json_string)
            return json.loads(resp_json_string)
        except TencentCloudSDKException as err:
            logging.error("[get_temp_secret]" + err)

    def __get_cos_client(self) -> CosS3Client:
        """
        创建对象存储客户端
            @return:CosS3Client:对象存储客户端
        """
        cos_config = CosConfig(
            Region=self.region,
            Secret_id=self.secret_id,
            Secret_key=self.secret_key)

        return CosS3Client(cos_config)

    def put(self, key: str, value: str) -> dict:
        """
        在存储桶放入数据
            @key:str:数据的key
            @value:str:数据的值
            @return:dict:上传成功返回的结果，包含ETag等信息.
        例子：
            1.
            with open('test.txt', 'rb') as fp:
                response = put('test.txt',fp)
                print (response['ETag'])
            2.
            response = put('test.txt','12312312312')
            print (response['ETag'])
        """
        try:
            client = self.__get_cos_client()
            return client.put_object(self.bucket, value, key)
        except Exception as err:
            logging.error("[cos_put]" + str(err))

    def get(self, key: str) -> dict:
        """
        从存储桶中拿数据
            @key:str:数据的key
            @return:dict:下载成功返回的结果,包含Body对应的StreamBody,可以获取文件流或下载文件到本地.
        例子：
            response = get('test.txt') 
            response['Body'].get_raw_stream.read()
        """
        try:
            client = self.__get_cos_client()
            ret = client.get_object(self.bucket, key)
            body: streambody.StreamBody = ret['Body']
            return body.get_raw_stream().read()
        except Exception as err:
            logging.info("[cos_get]" + str(err))

    def delete(self, key: str) -> dict:
        """
        从存储桶中删除数据
            @bucket:str:存储桶
            @key:str:数据的key
            @return:dict:
        例子：
            response =delete('test.txt') 
        """
        try:
            client = self.__get_cos_client()
            return client.delete_object(self.bucket, key)
        except Exception as err:
            logging.error("[cos_delete]" + str(err))

    def deletes(self, keys: str) -> dict:
        """
        从存储桶中删除数据
            @bucket:str:存储桶
            @keys:list:数据的key
            @return:dict:
        例子：
            response = deletes(['key1','key2','key3'])
        """
        try:
            objects = {"Quiet": "true", "Object": []}
            for key in keys:
                objects['Object'].append({"Key": key})
            client = self.__get_cos_client()
            return client.delete_objects(self.bucket, objects)
        except Exception as err:
            logging.error("[cos_delete]" + str(err))
