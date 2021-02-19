from .step import Step
from model.yt import YT


class InitializeYT(Step):
    def process(self, data, input, utils):
        
        return [YT(url) for url in data]  #為了要用utils的方法，所以傳進去，但是因為設計、易讀、效能上的考量所以先不這樣做