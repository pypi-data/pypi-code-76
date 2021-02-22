import json, re
from enum import Enum
from sanic import response
from .log_helper import LogHelper
from .common import StaticVariable

Log = LogHelper()


# param_conf = StaticVariable().getParam('param_conf')


class ParamReg:
    Mobile = r"^1([358][0-9]|4[579]|66|7[0135678]|9[89])[0-9]{8}$"  # 手机号码
    # 中国电信号段
    #
    # 133、149、153、173、177、180、181、189、199
    # 中国联通号段
    # 130、131、132、145、155、156、166、175、176、185、186
    # 中国移动号段
    # 134(0 - 8)、135、136、137、138、139、147、150、151、152、157、158、159、178、182、183、184、187、188、198
    # 其他号段
    # 14
    # 号段以前为上网卡专属号段，如中国联通的是145，中国移动的是147等等。
    # 虚拟运营商
    # 电信：1700、1701、1702
    # 移动：1703、1705、1706
    # 联通：1704、1707、1708、1709、171

    Telephone = r"^0\d{2,3}-\d{7,8}$"  # 固定电话

    Chinese = r"^[\u4e00-\u9fa5]+$"  # 中

    Email = r"^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"  # 邮箱

    Number = r"^[0-9]+$"  # 数字

    Letter = r"^[A-Za-z]+$"  # 字母

    Letter_Number = r"^[A-Za-z0-9]+$"  # 数字或字母

    Card_No = r"^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$"  # 身份证号


# 0非必填 1必填
class Param:
    def __init__(self, request):
        content_type = request.content_type if request.content_type else ""
        self._param = request.args if request.method == "GET" or "multipart/form-data" in content_type else request.json
        self.req = request

    def checkParam(self, key, code, checkFormatReg=None):
        if self._param is None:
            raise RuntimeError({"rtnCode": "1000", "rtnMsg": key + "参数不存在"})
        else:
            param = self._param.get(key)
            if not isinstance(param, str):
                param = json.dumps(param, ensure_ascii=False) if param is not None else None
            if param is None:
                if code == 1:
                    raise RuntimeError(
                        {"rtnCode": "1000", "rtnMsg": key + "参数不存在"})
                else:
                    return ""
            else:
                if code == 1:
                    if len(param) == 0:
                        raise RuntimeError(
                            {"rtnCode": "1000", "rtnMsg": key + "参数不存在"})
                    else:
                        if checkFormatReg is None:
                            return param
                        else:
                            result = re.match((checkFormatReg), param)
                            # print(result, param)
                            if result:
                                return param
                            else:
                                raise RuntimeError(
                                    {"rtnCode": "1000", "rtnMsg": key + "参数格式错误"})
                else:
                    return param

    def Response(self, rtn_code, rtnDesc="", Body=None):
        if not isinstance(rtnDesc, str):
            rtnDesc = '-'.join([str(v) for v in rtnDesc.args])
        rtnObj = rtn_code.value[0]
        rtnObj["rtnDesc"] = rtnDesc
        if Body is not None:
            rtnBody = {
                "head": rtnObj,
                "body": Body
            }
        else:
            rtnBody = {
                "head": rtnObj
            }
        if "0000" == rtnObj.get("rtnCode"):
            Log.info(f"{self.req.url} 0000 {rtnBody}")
        elif "1000" == rtnObj.get("rtnCode"):
            Log.warning(f"{self.req.url} 1000 {rtnBody}")
        else:
            Log.error(f"{self.req.url} {rtnObj.get('rtnCode')} {rtnBody}")
        return response.json(status=200, body=rtnBody, dumps=json.dumps, default=str)

    def HandleParam(self, ParamStr, *OtherKey):
        RealParam = {k: self.checkParam(k, v) for (k, v) in ParamStr.items()}
        if OtherKey:
            if OtherKey[0]:
                OtherParam = {k: v for (k, v) in self._param.items() if k in OtherKey[0]}
            else:
                OtherParam = {k: v for (k, v) in self._param.items() if k not in ParamStr.keys()}
        else:
            OtherParam = {k: v for (k, v) in self._param.items() if k not in ParamStr.keys()}
        return RealParam, OtherParam


class rtnCode(Enum):
    Success = {"rtnCode": "0000", "rtnMsg": "操作成功", "rtnDesc": ""},
    Failure = {"rtnCode": "1000", "rtnMsg": "操作失败", "rtnDesc": ""},
    ParamError = {"rtnCode": "1001", "rtnMsg": "缺少参数/参数错误/参数格式错误"},
    BizParamError = {"rtnCode": "1002", "rtnMsg": "业务参数异常"},
    # Auth
    AuthError = {"rtnCode": "2000", "rtnMsg": "接口授权信息异常"},
    PermissionError = {"rtnCode": "2001", "rtnMsg": "权限不足"},
    TokenError = {"rtnCode": "2002", "rtnMsg": "token异常"},
    SignatureError = {"rtnCode": "2003", "rtnMsg": "signature异常"},
    # 补充异常
    DBError = {"rtnCode": "3001", "rtnMsg": "数据库异常"},
    OutsideApiError = {"rtnCode": "4001", "rtnMsg": "外部接口访问异常"},
    # Other
    OtherError = {"rtnCode": "9999", "rtnMsg": "其他异常"},
    TipError = {"rtnCode": "xxxx", "rtnMsg": "异常提示"},
