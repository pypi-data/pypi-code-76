import os
def get_environ(req):
    env={}
    path = req.text.split()[1]
    par = dict(_parse_params(path))
    env['PATH'] = req.path.split('?')[0]
    env['PARAMS'] = par
    env['ENVIRON'] = dict(os.environ)
    return env
def _parse_params(url):
    if '?' in url:
        for i in range(len(url)):
            u = url[i]
            if u == '?':
                params = url[i:]
        for param in params.split('&'):
            yield param.split('=')