import json
from flask import abort, Response
from .tools import handle_abnormal


class Parameter():
    def __init__(self, request):
        self.method = request.method  # 请求方法
        self.headers = dict(request.headers)  # 请求头
        # GET方法的取参
        self.param_url = request.args.to_dict()
        # 非GET方法取值
        try:
            self.param_json = json.loads(
                request.get_data(as_text=True)
            )
        except json.decoder.JSONDecodeError:
            self.param_json = {}
        # 表单提交取值
        self.param_form = request.form

    def get_content(self) -> dict:
        return {
            'method': self.method,
            'headers': self.headers,
            'param_url': self.param_url,
            'param_json': self.param_json,
            'param_form': self.param_form
        }

    def verification(self, checking: dict, verify: dict, optional: dict = {}, null_value: bool = False) -> dict:
        for opt_k, opt_v in optional.items():
            # 没有选填参数时，填充预设的默认值
            if not checking.__contains__(opt_k):
                checking[opt_k] = opt_v
        if not set(verify.keys()).issubset(set(checking.keys())):
            json_data = {'All Parameters': {}, 'Optional': optional}
            for k, v in verify.items():
                json_data['All Parameters'][k] = str(v)
            handle_abnormal(
                message='请求参数不完整',
                status=400,
                other={'prompt': json_data}
            )
        for _k, _v in checking.items():
            try:
                str_data = None
                if type(_v) != verify[_k]:
                    str_data = f'参数 {_k} 应该是 {verify[_k]} 类型'
                if not null_value and verify[_k] == str and not optional.__contains__(_k):
                    if not _v.strip():
                        str_data = f'参数 {_k} 不能是空字符串'
                if str_data:
                    handle_abnormal(
                        message='请求参数类型校验失败',
                        status=400,
                        other={'prompt': str_data}
                    )
            except KeyError as err:
                handle_abnormal(
                    message='有多余的请求参数',
                    status=400,
                    other={'prompt': str(err)}
                )
        return checking
