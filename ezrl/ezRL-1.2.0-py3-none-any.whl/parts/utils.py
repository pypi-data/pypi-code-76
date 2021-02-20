
import sys
import copy

# 画像の表示
def show_img(img, title_msg = "show_img", waitKey = True, ratio = 1.0):
	import cv2
	resized_img = cv2.resize(img, None, fx = ratio, fy = ratio, interpolation = cv2.INTER_CUBIC)
	cv2.imshow(title_msg, resized_img)
	if waitKey is True: cv2.waitKey(0)

# 画像を透過して合成
def transparent_mix(base_img, mix_image, transparent_color):
	import numpy as np
	# 真っ黒の画像を作成
	gen_black = lambda: np.zeros(base_img.shape, dtype = np.uint8)
	# 画像のコピー
	cp = copy.deepcopy
	# 透過マスクの作成
	tp = np.array(transparent_color, dtype = np.uint8)[None, None, :]
	raw_mask = gen_black()
	raw_mask[mix_image == tp] = 1
	sum_mask = np.sum(raw_mask, axis = 2)
	mask_2d = (sum_mask == 3)
	mask = (np.tile(mask_2d[:,:,None], (1,1,3)) == False)
	# 合成
	img_0, img_1 = cp(base_img), cp(mix_image)
	img_0[mask] = 0
	img_1[mask == False] = 0
	mixed_img = img_0 + img_1
	return mixed_img

# タイルを並べた画像の作成 [ezRL]
class TileArt:
	# 初期化処理
	def __init__(self,
		canvas_size,	# キャンバスの大きさ
		tile_file_dic,	# タイル名と画像ファイルパスの対応辞書
		transparent_color = (255, 0, 255),	# 透過色の指定 (b,g,r)
		window_title = "TileArt"
	):
		import cv2
		# 画像の読み込み
		self.tile_img_dic = {
			tile_name: cv2.imread(tile_file_dic[tile_name])	# 画像読み込み
			for tile_name in tile_file_dic
		}
		# 様々なパラメータを保持
		self.canvas_size = canvas_size	# キャンバスの大きさ
		self.transparent_color = transparent_color	# 透過色の指定 (b,g,r)
		self.window_title = window_title
	# タイルを並べた画像の作成
	def gen_img(self, tile_ls, show_flag = False, ratio = 1.0, interpolation = None):
		import cv2
		import numpy as np
		# 補完のデフォルト値
		if interpolation is None: interpolation = cv2.INTER_NEAREST
		# キャンバスの作成
		x_canvas_size, y_canvas_size = self.canvas_size
		img = np.zeros((y_canvas_size, x_canvas_size, 3), dtype = np.uint8)
		# layer順にソート (安定ソート)
		sorted_tile_ls = sorted(tile_ls, key = lambda e: e["layer"])
		# タイルを並べる
		for tile in sorted_tile_ls:
			px, py = tile["pos"]
			x_size, y_size = tile["size"]
			texture = tile["texture"]
			raw_tile_img = self.tile_img_dic[texture]
			# 画像を伸縮する
			tile_img = cv2.resize(raw_tile_img, (x_size, y_size), interpolation = interpolation)
			# 画像を透過して合成
			base_img = img[py:py+y_size,px:px+x_size,:]
			mixed_img = transparent_mix(base_img, tile_img, self.transparent_color)	# 画像を透過して合成
			img[py:py+y_size,px:px+x_size,:] = mixed_img
		# 画像の表示 (show_flagがTrueの時)
		if show_flag is True: show_img(img, ratio)	# 画像の表示
		# 出来上がった画像を返す
		return img
