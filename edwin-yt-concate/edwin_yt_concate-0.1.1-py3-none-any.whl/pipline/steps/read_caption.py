from .step import Step

class ReadCaption(Step):
    def process(self, data, inputs, utils):
        for yt in data:
            if not utils.caption_file_exist(yt):
                continue
            captions={}
            with open(yt.caption_filepath, 'r') as f: #因為乎要檔案的main.py是不同資料夾要對path做處理
                # print(f)
                time_line = False
                time = None
                caption = None
                for line in f:
                    if '-->' in line:
                        time_line=True
                        time = line.strip()
                        continue
                    if time_line: #如果time_line是true那下一行就是字幕
                        caption = line.strip()
                        captions[caption] = time  #用字幕當key的原因是: 當用forloop字典時，return的值會是key
                        time_line = False
            yt.captions = captions

        return data