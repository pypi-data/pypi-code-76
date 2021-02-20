
import sys
import cv2
# 共通部品 [utils.py]
from .parts.utils import show_img

# 画像の表示
def show_img(img, title_msg = "show_img"):
	cv2.imshow(title_msg, img)
	cv2.waitKey(0)
