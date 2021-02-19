
async def request_tornado_repeat_request(request_fuc, retry_code_range_list=((599, 600)), max_request_count=5):
    from tornado.simple_httpclient import HTTPError
    # 为了安装这个包的时候，tornado不是必须的
    for i in range(max_request_count):
        res = await request_fuc()
        code = res.code
        is_match = False
        for code_range in retry_code_range_list:
            if code >= code_range[0] and code < code_range[1]:
                is_match = True
                break
        if is_match:
            if i < max_request_count - 1:
                continue
            else:
                raise HTTPError(res.code)
        else:
            return res


def request_requests_reapeat_request(request_func, max_request_count=5, timeout=(5, 20)):
    from requests.exceptions import ConnectionError, ReadTimeout
    for i in range(max_request_count):
        try:
            res = request_func()
            return res
        except ConnectionError:
            if i < max_request_count - 1:
                continue
            else:
                raise
        except ReadTimeout:
            if i < max_request_count - 1:
                continue
            else:
                raise
