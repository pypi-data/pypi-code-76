from .step import Step
from pytube import YouTube
from .settings import VIDEOS_DIR

class DownloadVideos(Step):
    def process(self, data, input, utils):
        # print(len(data))
        yt_set = set([found.yt for found in data])  #set會把重複的去掉
        print('videos to download= ',len(yt_set))
        for yt in yt_set:
            url = yt.url 
            
            if utils.video_file_exist(yt):
                print(f'found existing video file for{url}, skipping')
                continue

            print('downloading: ',url)
            YouTube(url).streams.first().download(output_path=VIDEOS_DIR, filename=yt.id)
        return data
