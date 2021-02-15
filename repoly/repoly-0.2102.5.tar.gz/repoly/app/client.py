import requests


class Client:
    url: str = "http://localhost:5000/"

    def send(self, dic):
        response_login = requests.post(self.url + "/store", json=dic)
        print(response_login.json())
