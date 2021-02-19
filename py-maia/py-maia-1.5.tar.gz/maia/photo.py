import requests
import shutil


class Photo:
    def __init__(self, path):
        self.path = path

    def download(self, site):
        response = requests.get(site)
        if response.status_code == 200:
            with open(self.path, 'wb') as file:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, file)
            return True
