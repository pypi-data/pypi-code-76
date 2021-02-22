from .formats import *
from ..srv.version import version
class Response(object):
    def __init__(self, status, content_type=None, data=None, location=None, cookies=None, servername=version):
        self.status = status
        self.content_type = content_type
        self.data = data
        self.server = servername
        self.location = location
        if cookies is not None:
            self.cookies = ';'.join(key+'='+obj for key, obj in cookies.items())
        else:
            self.cookies = ''
    def __str__(self):
        if len(self.cookies)!=0:
            cookies = 'Set-Cookie: {}'.format(self.cookies)+"\r\n"
        else:
            cookies=''
        if self.status.startswith('3'):
            if self.location is None:
                raise Exception('Must mention Response.location in 3xx responses')
            return start_response.format_map(self.__dict__) + \
                location_header.format_map(self.__dict__) + \
                cookies + \
                end_response.format_map(self.__dict__) + self.data + '\r\n\r\n'
        if self.content_type is None:
            return start_response.format_map(self.__dict__) + \
                cookies + \
                end_response.format_map(self.__dict__) + "\r\n"
        return start_response.format_map(self.__dict__) + \
                cookies + \
                end_response.format_map(self.__dict__) + self.data + '\r\n\r\n'
    __repr__ = __str__

