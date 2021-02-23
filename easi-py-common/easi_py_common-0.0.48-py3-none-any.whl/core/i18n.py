import os
from enum import Enum
from inspect import isfunction
from typing import Optional, List

import yaml
from addict import Dict

from easi_py_common.core.error import ServiceException
from easi_py_common.core.sql_alchemy import db
from flask import current_app, request, Flask

LANG_ZH = 'zh'

LANG_CN = 'cn'
LANG_EN = 'en'
LANG_JA = 'ja'
LANG_MS = 'ms'

LANG_LIST = []


def verify_language(lang) -> bool:
    if not lang:
        return False
    return lang in LANG_LIST


def get_header_language() -> str:
    lang = None

    if current_app.header_language_function is not None:
        func_lang = current_app.header_language_function()
        if verify_language(func_lang):
            lang = func_lang

    if not lang:
        header_lang = request.headers.get(current_app.header_language_name)
        if verify_language(header_lang):
            lang = header_lang

    if not lang:
        lang = current_app.i18n_language_default or LANG_EN

    if lang == LANG_ZH:
        lang = LANG_CN

    lang = current_app.i18n_language_mapping.get(lang) or lang
    return lang


def verify_auto_language(lang: Optional[str]) -> str:
    if verify_language(lang):
        return lang
    return get_header_language()


def verify_default_language(lang: str, default_lang: str = LANG_EN) -> str:
    if verify_language(lang):
        return lang
    if verify_language(default_lang):
        return default_lang
    return LANG_EN


def trans_data(data_cn, data_en, lang=None):
    lang = verify_auto_language(lang)
    if lang in (LANG_CN, LANG_ZH):
        return data_cn

    return handle_lang_en_val(data_en, data_cn)


def trans(data, data_key, lang=None):
    lang = verify_auto_language(lang)

    if not isinstance(data, (dict, db.Model)):
        return ''

    if isinstance(data, db.Model):
        data = data.__dict__

    return trans_data(data.get(data_key), data.get('{}_en'.format(data_key)), lang=lang)


def tt(translate_key: str, lang: Optional[str] = None) -> Dict:
    """
    1. 指定返回参数值。两个参数都不能为空,语言为空则返回中文内容

    :param translate_key: 参数。解析 en.yml cn.yml 语言配置文件, 只需要传入 translate_key, 自动返回该配置文件下该 key 的字典
    :param lang: 指定的具体语言
    :return:
    """
    return current_app.i18n.get(verify_auto_language(lang), Dict()).get(translate_key, Dict())


def t(translate_key=None, lang=None, data=None, data_key=None, data_cn=None, data_en=None):
    """
    1. 指定返回参数值。两个参数都不能为空,语言为空则返回中文内容

    :param translate_key: 参数。解析 en.yml cn.yml 语言配置文件, 只需要传入 translate_key, 自动返回该配置文件下该 key 的字典
    :param lang: 指定的具体语言
    :param data:
    :param data_key:
    :param data_cn:
    :param data_en:
    :return:
    """
    lang = verify_auto_language(lang)
    if translate_key:
        return tt(translate_key, lang=lang)

    if data_cn is not None or data_en is not None:
        return trans_data(data_cn, data_en, lang=lang)

    return trans(data, data_key, lang=lang)


def is_empty(string):
    if string is None:
        return True

    if type(string) == str:
        return len(string.strip()) == 0
    else:
        return False


def handle_lang_en_val(en_val, zh_val):
    """
    如果英文为空会返回中文
    :param en_val:
    :param zh_val:
    :return:
    """
    return zh_val if is_empty(en_val) else en_val


class BaseErrorCode(Enum):

    def __get_code(self):
        code = 400
        def_msg = ''
        if isinstance(self.value, int):
            code = self.value
        elif isinstance(self.value, tuple):
            code, def_msg = self.value
        return code, def_msg

    def __get_code_message(self):
        code, def_msg = self.__get_code()
        return code, t(self.error_code_prefix()).get(self.name) or def_msg

    def error_code_prefix(self):
        return 'error_code'

    def build_exception(self):

        code, msg = self.__get_code_message()
        return ServiceException(code=code, msg=msg)

    def build_invalid_params_exception(self, msg):
        code, def_msg = self.__get_code()
        return ServiceException(code=code, msg=msg or def_msg)


def init_app(app: Flask, lang_list: List[str], header_language_name: str = 'language',
             header_language_function=None, i18n_language_default: str = None, i18n_language_mapping: dict = None):
    if header_language_function and not isfunction(header_language_function):
        raise ServiceException(code=400, msg='header_language_function 不是  function')

    if not lang_list:
        lang_list = [LANG_CN, LANG_EN, LANG_JA, LANG_MS]

    app_path = os.path.dirname(app.root_path)
    lang_map = {}
    for lang in lang_list:
        lang_yml_path = os.path.join(app_path, 'common/i18n/{}.yml'.format(lang))
        with open(lang_yml_path) as lang_yml_file:
            lang_yml = yaml.load(lang_yml_file, Loader=yaml.FullLoader)
            lang_map[lang] = Dict(lang_yml)
            if lang not in LANG_LIST:
                LANG_LIST.append(lang)

    app.i18n = lang_map
    app.header_language_name = header_language_name
    app.header_language_function = header_language_function
    app.i18n_language_default = i18n_language_default if i18n_language_default in lang_list else LANG_EN
    app.i18n_language_mapping = i18n_language_mapping or dict()
