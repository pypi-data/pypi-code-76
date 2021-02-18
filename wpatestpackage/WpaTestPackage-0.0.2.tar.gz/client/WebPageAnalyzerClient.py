import json

import requests

class WebPageAnalyzerClient:
    host = "localhost"
    port = "8086"

    def set_host(self,host):
        self.host=host

    def set_port(self,port):
        self.port=port

    def get_host(self, host):
        return self.host

    def get_port(self, port):
        return self.port

    def initializeWebPageAnalyzer(self):
        status=False
        proxyURL= self.host + ":" + self.port
        response = requests.post("http://"+proxyURL+"/api/v1/initialize",headers={"content-type":"json"})
        if response.status_code==200:
            status = True
        return status

    def scanPage(self, PageDetails, url):
        status = False
        proxyURL = self.host + ":" + self.port
        response = requests.post("http://" + proxyURL + "/api/v1/scanPage",
                                 data=json.dumps(PageDetails.__dict__),
                                 headers={"content-type": "application/json"},
                                 params={"url": url})
        if response.status_code == 200:
            status = True
        return status

    def stopPageAnalyzer(self):
        status = False
        proxyURL = self.host + ":" + self.port
        response = requests.post("http://" + proxyURL + "/api/v1/stop",
                                 headers={"content-type": "json"})
        if response.status_code == 200:
            status = True
        return status