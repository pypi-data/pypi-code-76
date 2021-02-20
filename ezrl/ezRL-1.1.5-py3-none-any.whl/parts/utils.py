
import sys
import cv2

# 画像の表示
def show_img(img, title_msg = "show_img"):
	cv2.imshow(title_msg, img)
	cv2.waitKey(0)
