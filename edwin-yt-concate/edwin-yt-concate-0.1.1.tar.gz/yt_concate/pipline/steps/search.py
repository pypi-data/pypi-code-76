from .step import Step
from model.found import Found


class Search(Step):
    def process(self, data, input, utils):
        search_word = input['search_word']
        found = []
        for yt in data:
            captions = yt.captions
            if not captions:
                continue

            for caption in captions:
                if search_word in caption:
                    time = captions[caption]
                    f = Found(yt, caption, time)
                    found.append(f)  # 因為append一次只能放一個東西，所以要用tuple傳
        print(len(found))
        return found
