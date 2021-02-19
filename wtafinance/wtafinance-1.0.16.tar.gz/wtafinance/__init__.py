def initConfig():
    url = "http://127.0.0.1:8000/app_finance/getcodeconfig"
    import requests,json
    res = requests.get(url, timeout=60)
    ClassCodeConfig.config = json.loads(res.text)

class ClassCodeConfig():
    config = []

initConfig()


if __name__ == '__main__':
    con = ClassCodeConfig.config
    print(con)