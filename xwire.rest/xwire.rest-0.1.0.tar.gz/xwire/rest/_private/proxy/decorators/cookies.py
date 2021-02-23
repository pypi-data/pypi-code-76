def cookies(func):
    func.__proxy_cookies = True
    return func
