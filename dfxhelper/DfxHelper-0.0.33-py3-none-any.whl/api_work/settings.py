from dfx_utils.klass_helper import BaseData, SuperDict


class ApiSetting(SuperDict):
    def __init__(self, api_name: str, request_url: str, method: str, *args, **kwargs):
        super(ApiSetting, self).__init__(*args, **kwargs)
        self.data = BaseData()
        self.method = method.lower()
        self.api_name = api_name
        self.request_url = request_url

    def __getitem__(self, item):
        key = f'{self.api_name}.{item}'
        return super(ApiSetting, self).__getitem__(key)

    def __setitem__(self, key, value):
        key = f'{self.api_name}.{key}'
        return super(ApiSetting, self).__setitem__(key, value)

    def add(self, **kwargs):
        """ 添加数据 """
        self.data.add(**kwargs)

    def reset(self):
        """ 清除已有数据 """
        self.data = BaseData()

    def data_rule(self, key, rule, required=True):
        """ 添加数据规则 """
        tmp_key = f'data.{key}'
        self[tmp_key] = (rule, required)

    def __add_rule(self, typ, args: list):
        self[typ] = args

    def header_rule(self, *args):
        """ 添加 header 规则 """
        self.__add_rule('header', args)

    def param_rule(self, *args):
        """ 添加 param 规则 """
        self.__add_rule('param', args)

    def __check_data(self, data, setting: SuperDict = None, ret_data: dict = dict()):
        """ 检查 post data """
        tmp_data = ret_data
        for key, val in setting.items():
            if isinstance(val, dict):
                tmp_data[key] = tmp_data.get(key, {})
                self.__check_data(data, setting=val, ret_data=tmp_data[key])
            else:
                if not getattr(data, key) and val[-1]:
                    raise Exception(f'{self.api_name}: data({key}) not found')
                elif getattr(data, key).__class__.__name__ not in val[0] and val[-1]:
                    raise Exception(f'{self.api_name}: data({key}) need {val[0]}, found {type(getattr(data, key))}')
                tmp_data[key] = getattr(data, key)
        return ret_data

    def __check(self, typ, data: BaseData):
        """ 检查 param 和 header """
        ret_data = BaseData()
        for item in self.get(typ, []):
            value = getattr(data, item)
            if value is None:
                raise Exception(f'{self.api_name}: {typ}({item}) not found')
            ret_data.add(**{item: value})
        return ret_data()

    def __check_param(self, data: BaseData):
        """ 检查 param """
        param_key = f'{self.api_name}.param'
        return self.__check(param_key, data)

    def __check_header(self, data: BaseData):
        """ 检查 header """
        header_key = f'{self.api_name}.header'
        return self.__check(header_key, data)

    def __call__(self):
        """ 检查并返回 param/header/data """
        headers = self.__check_header(self.data)
        param = self.__check_param(self.data)
        key = f'{self.api_name}.data'
        ret_data = self.__check_data(self.data, self.get(key, {}))
        ret_data = {k: v for k, v in ret_data.items() if v is not None}
        return param, headers, ret_data


class ApiSettingManager(dict):
    def __init__(self, base_url: str = None, name: str = None):
        self.name = name
        self.base_url = base_url

    def __call__(self, api_name, path, method) -> ApiSetting:
        """ 创建并记录 api setting """
        request_url = f'{self.base_url}{path}'
        key = f'{self.name}.{api_name}'
        self[key] = ApiSetting(key, request_url, method)
        return self[api_name]

    def __getitem__(self, item):
        key = f'{self.name}.{item}'
        return super(ApiSettingManager, self).__getitem__(key)
