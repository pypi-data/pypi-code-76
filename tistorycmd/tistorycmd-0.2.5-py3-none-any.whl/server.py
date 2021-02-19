import http.server
import threading
import urllib.parse
from . import config


class Server(http.server.BaseHTTPRequestHandler):
    """HTTP 요청을 처리하는 클래스"""

    def do_GET(self):
        url_parsed = urllib.parse.urlparse(self.path)
        dict_query = urllib.parse.parse_qs(url_parsed.query)

        config.config['access_code'] = dict_query['code'][0]
        config.set_config()

        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

        response_html = b"""<html>
                            <head><title>Tistory-cli</title></head>
                            <body>
                            <h1>Successfully Got the Access Token</h1>
                            <p>Just go back to your terminal :)</p>
                            </body>
                            </html>"""
        self.wfile.write(response_html)

        killer = threading.Thread(target=self.server.shutdown, daemon=True)
        killer.start()


if __name__ == "__main__":
    # 요청받을 주소 (요청을 감시할 주소)
    address = ('localhost', 5000)

    # 요청 대기하기
    listener = http.server.HTTPServer(address, Server)
    print(f'http://{address[0]}:{address[1]} 주소에서 요청 대기중...')
    listener.serve_forever()