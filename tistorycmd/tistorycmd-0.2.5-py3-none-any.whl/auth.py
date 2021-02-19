import json, os, requests, sys, urllib
import webbrowser
from .server import *
from . import config


class Auth:
    def __init__(self):
        if((not config.config['app_id']) or (not config.config['secret_key'])):
            print('==================Error==================')
            print('config.json app_id 랑 secret_key 설정필요합니다.')
            print('https://www.tistory.com/guide/api/manage/register 에서 확인가능')
            print('README.md 설명 참고')
            exit(1)

        if (not config.config['access_code']):
            self.get_authorize()

        if (not config.config['access_token']):
            self.get_access_token()

        if (not config.config['blog_name']):
            self.get_blog_name()

    def get_authorize(self):
        """
        client_id=[App id]&redirect_uri=[앱등록에서 입력한 redirect url]&response_type=code&state=someValue
        :return: null
        """
        params = {'client_id':config.config['app_id'], 'redirect_uri':'http://localhost:5000/callback', 'response_type':'code', 'state':'someValue'}
        webbrowser.open('https://www.tistory.com/oauth/authorize?' + urllib.parse.urlencode(params))

        address = ('localhost', 5000)
        listener = http.server.HTTPServer(address, Server)
        print(f'http://{address[0]}:{address[1]} 주소에서 요청 대기중...')
        listener.serve_forever()

    def get_access_token(self):
        """
        client_id=[App id]&client_secret=[Secret key]&redirect_uri=[앱등록에서 입력한 redirect url]&code=[access_code]&grant_type=authorization_code
        :return: null
        """
        params = {'client_id': config.config['app_id'], 'client_secret': config.config['secret_key'], 'redirect_uri': 'http://localhost:5000/callback', 'code': config.config['access_code'],'grant_type': 'authorization_code'}

        try:
            # 토큰 받아오기
            res = requests.get('https://www.tistory.com/oauth/access_token?' + urllib.parse.urlencode(params))
            config.config['access_token'] = res.text.split('=')[1]
            config.set_config()
        except:
            # 토큰 초기화
            config.reset_access_token()

    def get_blog_name(self):
        url = 'https://www.tistory.com/apis/blog/info'
        data = {'access_token': config.config['access_token'], 'output': 'json'}
        res = requests.get(url, params=data)
        if res.status_code == 200:
            config.config['blog_name'] = res.json()["tistory"]["item"]["blogs"][0]["name"]   # 블로그명 불러오기
            config.set_config()  # 설정 저장

        else:
            json_text = json.dumps(res.json(), indent=4, ensure_ascii=False)
            print(json_text)


if __name__ == "__main__":
    auth = Auth()