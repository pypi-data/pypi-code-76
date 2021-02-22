reply_format = '''\
HTTP/1.1 {status}\r\n\
Server: {server}\r\n\
Cache-Control: no-store\r\n\
Connection: keep-alive\r\n\
Content-Type: {content_type};charset=utf-8\r\n\r\n\
{data}\r\n\r\n'''
start_response = '''\
HTTP/1.1 {status}\r\n\
Server: {server}\r\n\
'''
location_header = 'Location: {location}\r\n'
end_response = '''\
Cache-Control: no-store\r\n\
Connection: keep-alive\r\n\
Content-Type: {content_type};charset=utf-8\r\n\r\n\
'''
redirect_format = '''\
HTTP/1.1 {status}\r\n\
Server: {server}\r\n\
Location: {location}\r\n\
Cache-Control: no-store\r\n\
Connection: keep-alive\r\n\
Content-Type: {content_type};charset=utf-8\r\n\r\n'''
no_data_format = '''\
HTTP/1.1 {status}\r\n\
Server: {server}\r\n\
Cache-Control: no-store\r\n\
Connection: keep-alive\r\n\r\n\
'''
