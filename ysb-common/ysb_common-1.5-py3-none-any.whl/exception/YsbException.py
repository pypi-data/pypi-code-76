class YsbException(Exception):
    """
    自定义异常类
    """

    def __init__(self, code, msg, error_code, error_info):
        """

        :param code: "0"-成功， “-1”-失败
        :param msg:
        :param error_code: "0"=成功,"-1"=程序异常,可以进行重试, "1"=业务异常
        :param error_info:
        """
        self.code = code
        self.msg = msg
        self.error_code = error_code
        self.error_info = error_info

    #类中调用方式如下
    # try:
    #     if "异常情况":
    #         raise YsbException("-1", "失败", "1", "异常信息")
    # except YsbException as e:
    #     print("返回信息：", {"CODE": e.code, "MSG": e.msg, "ERROR_CODE": e.error_code, "ERROR_INFO": e.error_info})
