import os
from pipline.steps.settings import CAPTIONS_DIR
from pipline.steps.settings import DOWNLOADS_DIR
from pipline.steps.settings import VIDEOS_DIR
from pipline.steps.settings import VIDEO_LIST_FILENAME
from pipline.steps.settings import OUTPUTS_DIR

class Utils:
    def __init__(self):
        pass

    def get_video_list_filepath(self, channel_id):
        return os.path.join(DOWNLOADS_DIR, channel_id+'.txt')

    def create_dirs(self):
        os.makedirs(DOWNLOADS_DIR, exist_ok=True)  # 如果資料夾存在是OK的
        os.makedirs(CAPTIONS_DIR, exist_ok=True)
        os.makedirs(VIDEOS_DIR, exist_ok=True)
        os.makedirs(OUTPUTS_DIR,exist_ok=True)
    def video_list_file_exists(self, channel_id):
        path = self.get_video_list_filepath(channel_id)
        return os.path.exists(path) and os.path.getsize(path)>0

    def caption_file_exist(self, yt):  # 檢查文字檔案存不存在，避免一值重複跑
        # 避免之前為下載到
        return os.path.exists(yt.caption_filepath) and os.path.getsize(yt.caption_filepath) > 0

    def video_file_exist(self,yt):
        filepath = yt.video_filepath
        return os.path.exists(filepath) and os.path.getsize(filepath) > 0

    def get_output_filepath(self, channel_id,search_word):
        filename = channel_id+'_'+search_word+'.mp4'
        return os.path.join(OUTPUTS_DIR,filename)
