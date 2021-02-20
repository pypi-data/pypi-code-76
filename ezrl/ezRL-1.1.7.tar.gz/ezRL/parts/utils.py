
import sys
import cv2

# 画像の表示
def show_img(img, title_msg = "show_img", waitKey = True, ratio = 1.0):
	resized_img = cv2.resize(img, None, fx = ratio, fy = ratio, interpolation = cv2.INTER_CUBIC)
	cv2.imshow(title_msg, resized_img)
	if waitKey is True: cv2.waitKey(0)
