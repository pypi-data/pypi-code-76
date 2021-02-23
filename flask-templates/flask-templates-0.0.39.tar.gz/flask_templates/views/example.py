# -*- coding: utf-8 -*-
"""
------------------------------------------------------------------
    File Name:              example
    Description:            
    Author:                 hzy
    date:                   2019/8/24
------------------------------------------------------------------
    Change Activity:
                            2019/8/24
------------------------------------------------------------------
"""
from flask_templates.common.logger import logger

__author__ = 'hzy'

import time
from flask_templates.views import api
from flask_templates.views.base import check_request_params
from flask_templates.service.example import index


@api.route('/')
@check_request_params(auth=True)
def example_index(**kwargs):
    """
/**
* showdoc
* @catalog 测试文档/用户相关
* @title 用户登录
* @description 用户登录的接口
* @method get
* @url https://www.showdoc.cc/home/user/login
* @header token 可选 string 设备token
* @param username 必选 string 用户名
* @param password 必选 string 密码
* @param name 可选 string 用户昵称
* @return {"error_code":0,"data":{"uid":"1","username":"12154545","name":"吴系挂","groupid":2,"reg_time":"1436864169","last_login_time":"0"}}
* @return_param groupid int 用户组id
* @return_param name string 用户昵称
* @remark 这里是备注信息
* @number 99
*/
    Parameters
    ----------
    kwargs

    Returns
    -------

    """
    logger.error('333')
    return index(**kwargs)



if __name__ == "__main__":
    start_t = time.time()

    pass

    print("use time: %s" % (time.time() - start_t))
