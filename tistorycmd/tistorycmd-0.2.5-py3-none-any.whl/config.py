import json, os

home_dir = os.path.expanduser('~')
base_dir = home_dir + os.sep + '.tistorycmd'
config_file = base_dir + os.sep + 'config.json'
config_json = dict()
config_json['blog_name'] = ''
config_json['app_id'] = ''
config_json['secret_key'] = ''
config_json['access_code'] = ''
config_json['access_token'] = ''

config = ''

if not os.path.exists(base_dir):
    os.makedirs(base_dir)

if not os.path.exists(config_file):
    with open(config_file, 'w', encoding='utf-8') as make_file:
        json.dump(config_json, make_file, indent="\t")

with open(config_file, 'r') as f:
    config = json.load(f)


def set_config():
    with open(config_file, 'w', encoding='utf-8') as make_file:
        json.dump(config, make_file, indent="\t")


def reset_access_token():
    print('==================ERROR==================')
    print('token이 만료되었습니다.')
    config['access_code'] = ''
    config['access_token'] = ''
    set_config()
    exit(1)


if ( (not config['app_id']) or (not config['secret_key']) ):
    print('==================USAGE==================')
    print('app_id, secret_key 은(는) 필수 설정 입니다.')
    print('https://www.tistory.com/guide/api/manage/register 에서 확인가능')
    print('README.md 설명 참고')
    print('==================input==================')
    if (not config['app_id']):
        config['app_id'] = input("app_id : ")
    if (not config['secret_key']):
        config['secret_key'] = input("secret_key : ")
    set_config()