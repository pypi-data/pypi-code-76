from dotenv import load_dotenv  # 讓程式到.env檔找變數

import os  # 到系統的環境變數那邊，添加API_KEY的環境變數，環境變數需要重新讀取

load_dotenv()
API_KEY = os.getenv('API_KEY')
# print(API_KEY)


VIDEO_LIST_FILENAME = ''
DOWNLOADS_DIR = 'downloads'
VIDEOS_DIR =os.path.join(DOWNLOADS_DIR,'videos')  #or DOWNLOADS+'/videos'
CAPTIONS_DIR = os.path.join(DOWNLOADS_DIR,'captions')
OUTPUTS_DIR = 'outputs'