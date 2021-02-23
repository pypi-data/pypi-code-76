class Params:
    """
    汇总展示项目中统一公共的配置参数
    命名方式：参照常量的命名方式，统一大写。
    调用方式：类名.字段名。Params.RETURN_CODE_SUCCESS
    """

    # 通用返回值，异常错误返回-1
    RETURN_CODE_ERROR = '-1'
    # 通用返回值，正常返回0
    RETURN_CODE_SUCCESS = '0'

    '''
    任务类型---常量定义
    '''
    LX_JCFW_CODE = '01'  # 基础服务类型
    LX_SBCXFW_CODE = '02'  # 申报查询服务接口类型
    LX_QCFW_CODE = '03'  # 期初服务接口类型
    LX_FPCX_CODE = '10'  # 发票查询类型
    LX_JTFW_CODE = '04'  # 截图服务类型
    LX_MMYZ_CODE = '06'  # 密码验证对应的类型
    LX_PLSB_CODE = '07'  # 批量申报对应的类型
    LX_YDSSB_CODE = '08'  # 引导式申报对应的类型
    LX_SBZF_CODE = '11'  # 申报作废类型

    # 截图保存图片路径
    IMAGE_URL = './taxService/imgCut/'
