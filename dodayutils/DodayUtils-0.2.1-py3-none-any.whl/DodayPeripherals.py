import logging
import sys, os
import time
import json
from DodayUtils._exceptions import *
from DodayUtils._dwrappers import *
from DodayUtils.OrderInfo import *
from PIL import Image, ImageDraw, ImageFont

import cups
import glob
import re
import subprocess
from ctypes import *

from reportlab.lib import utils
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

# Helper functions for merging pictures
#----------------------------------------------------------------------
def d2250print(func):
	# d2250 printing function wrapper
	@dutils
	def handle_d2250_print(*args, **kwargs):
		# clean tmp filepath
		files = glob.glob(args[0].d2250_tmpfile_path+'/*')
		safe_remove_set = {".pdf", ".png", ".jpg"}
		# guard for specific filetype
		for f in files:
			if f[-4:] in safe_remove_set:
				os.remove(f)

		tmp_fp, job_name = func(*args, **kwargs)
		args[0].send_to_d2250(tmp_fp, job_name, printer_name=kwargs["printer_name"])

	return handle_d2250_print

class StickerFormat:
	def __init__(self, sticker_lines=[], **kwargs):
		self.sticker_width = kwargs.get("sticker_width", 380)
		self.sticker_height = kwargs.get("sticker_height", 300)
		self.default_font_path = kwargs["default_font_path"]
		self.sticker_lines = copy.deepcopy(sticker_lines)
		logging.info("[StickerFormat] Init sticker lines: "+ str(self.sticker_lines))

		self.edge_space = kwargs.get("edge_space", 10)
		self.small_font = self.get_d2250_font(23)
		self.default_font = self.get_d2250_font(35)
		self.big_font = self.get_d2250_font(40)
		self.left_header = kwargs.get("left_header", "")
		self.right_header = kwargs.get("right_header", "")

		a = self.spread_string(self.left_header, self.right_header, self.default_font)
		# Header
		self.append({"string": self.spread_string(self.left_header, self.right_header, self.default_font), 
			"font": "default_font"})
		self.add_repeat_char("-", "small_font")
		# self.add_repeat_char(" ", "small_font")

	def __len__(self):
		return len(self.sticker_lines)

	def __iter__(self):
		for line in self.sticker_lines:
			yield line

	def __getitem__(self, key):
		return getattr(self, key)

	def __setitem__(self, key, value):
		setattr(self, key, value)

	def __add__(self, other):
		return StickerFormat(sticker_lines=self["sticker_lines"]+other["sticker_lines"])

	def get_d2250_font(self, size):
		return ImageFont.truetype(self.default_font_path, size)

	def add_repeat_char(self, character, font):
		cstr = ""
		while getattr(self,font).getsize(cstr)[0] < self.sticker_width-self.edge_space:
			cstr += character

		self.append({"string": cstr[:-1], "font": "small_font"})

	def append(self, item, delimiter=None, end_header=False):
		"""
		Add lines for sticker
		"""
		assert type(item) == dict 
		# Mandatory keys
		for key in ("string", "font"):
			if key not in item:
				raise DodayUtilError("Sticker Line Format Incorrect")

		try:
			item["font"] = getattr(self, item["font"])
		except:
			raise DodayUtilError("No Such Font")

		item["color"] = (0, 0, 0)
		if self.sticker_lines == []:
			item["pos"] = (8, 10)
			self.sticker_lines.append(item)
		elif end_header:
			item["pos"] = (8, self.sticker_height - item["font"].getsize(item["string"])[1] - \
				self.v_offset(item["font"]))
			self.sticker_lines.append(item)
		else:
			str_list = self.split_string(item["font"], item["string"], delimiter=delimiter)
			last_line = self.sticker_lines[-1]
			for str_line in str_list:
				current_line = item.copy()
				current_line["string"] = str_line
				vertical_pos = last_line["pos"][1] + last_line["font"].getsize(last_line["string"])[1]\
					- self.v_offset(current_line["font"])
				current_line["pos"] = (8, vertical_pos)
				self.sticker_lines.append(current_line)
				last_line = current_line.copy()

	def spread_string(self, left, right, font, start_width=40):
		"""
		This is the function to spread the string
		out to the left and right. 
		"""
		header_list = [left]
		header_list.extend([" " for _ in range(start_width - len(left) - len(right))])
		header_list.append(right)
		res_str = "".join(header_list)
		if font.getsize(res_str)[0] > self.sticker_width-self.edge_space:
			return self.spread_string(left, right, font, start_width-1)
		return res_str

	def find_all(self, string, delimiter):
		"""
		Helper function to find all the delimiter
		in the string. 
		"""
		start = 0
		while True:
			start = string.find(delimiter, start)
			if start == -1: return
			yield start
			start += len(delimiter) # use start += 1 to find overlapping matches

	def split_string(self, font, string, delimiter=None):
		"""
		This is the function to find the best way to split
		the string into possible ways that fits the sticker
		"""
		if font.getsize(string)[0] < self.sticker_width-self.edge_space:
			# This is base case. If the entire string fits
			return [string]

		if delimiter:
			idx = -1
			reverse_dindex_list = list(self.find_all(string, delimiter))[::-1]
			for dindex in reverse_dindex_list:
				if font.getsize(string[:dindex])[0] < self.sticker_width-self.edge_space:
					# If the string gets in the range of the sticker
					idx = dindex
					break

			return [string[:dindex]] + self.split_string(font, string[dindex:],delimiter=delimiter)

		else:
			idx = -1
			for i in range(len(string), -1, -1):
				if font.getsize(string[:i])[0] < self.sticker_width-self.edge_space:
					# If the string gets in the range of the sticker
					idx = i
					break

			return [string[:idx]] + self.split_string(font, string[idx:])

	def v_offset(self, font):
		if font == self.small_font:
			return 10
		else:
			return -2

class D2250_sticker:
	def __init__(self, **configs):
		self.sticker_width = 380 #mm
		self.sticker_height = 300 #mm
		self.default_font_path = configs["default_font_path"]
		self.d2250_tmpfile_path = configs["d2250_tmpfile_path"]

	def init_d2250_printer_driver(self, **configs):
		pass

	def send_to_d2250(self, tmp_folder_path, job_name, printer_name="ARGOX_D2-250_PPLB"):
		# send filename to d2250 printer and print it out.
		conn = cups.Connection()

		# TODO: In the future we can save a copy of output pdf
		# for logging purposes
		outputPdfName = "output_sticker"
		pathToSavePdfTo = tmp_folder_path
		pathToPictures = tmp_folder_path
		splitType = "none"
		numberOfEntitiesInOnePdf = 1
		listWithImagesExtensions = ["png", "jpg"]
		picturesAreInRootFolder = True
		nameOfPart = "volume"
		self.unite_pictures_into_pdf(outputPdfName, pathToSavePdfTo, pathToPictures, splitType, numberOfEntitiesInOnePdf, listWithImagesExtensions, picturesAreInRootFolder, nameOfPart)
		conn.printFile(printer_name,tmp_folder_path+"/output_sticker.pdf",job_name,{})

	def save_img_to_location(self, img, fn):
		# This is the function to save file to location
		img.save(fn)

	def sorted_nicely(self, l):
		""" 
		# http://stackoverflow.com/questions/2669059/how-to-sort-alpha-numeric-set-in-python
	 
		Sort the given iterable in the way that humans expect.
		""" 
		convert = lambda text: int(text) if text.isdigit() else text 
		alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
		return sorted(l, key = alphanum_key)

	#----------------------------------------------------------------------
	def unite_pictures_into_pdf(self, outputPdfName, pathToSavePdfTo, pathToPictures, splitType, numberOfEntitiesInOnePdf, listWithImagesExtensions, picturesAreInRootFolder, nameOfPart):
		
		if numberOfEntitiesInOnePdf < 1:
			print("Wrong value of numberOfEntitiesInOnePdf.")
			return
		if len(listWithImagesExtensions) == 0:
			print("listWithImagesExtensions is empty.")
			return
		
		
		if picturesAreInRootFolder == False:
			foldersInsideFolderWithPictures = self.sorted_nicely(glob.glob(pathToPictures + "/*/"))
			if len(foldersInsideFolderWithPictures) != 0:
				picturesPathsForEachFolder = []
				for iFolder in foldersInsideFolderWithPictures:
					picturePathsInFolder = []
					for jExtension in listWithImagesExtensions:
						picturePathsInFolder.extend(glob.glob(iFolder + "*." + jExtension))
					picturesPathsForEachFolder.append(self.sorted_nicely(picturePathsInFolder))
				if splitType == "folder":
					numberOfFoldersAdded = 0;
					for iFolder in picturesPathsForEachFolder:
						if (numberOfFoldersAdded % numberOfEntitiesInOnePdf) == 0:
							endNumber = numberOfFoldersAdded + numberOfEntitiesInOnePdf
							if endNumber > len(picturesPathsForEachFolder):
								endNumber = len(picturesPathsForEachFolder)
							filename = []
							if numberOfEntitiesInOnePdf > 1:
								filename = os.path.join(pathToSavePdfTo, outputPdfName + "_" + nameOfPart + "_" + str(numberOfFoldersAdded + 1) + '-' + str(endNumber) + "_of_" + str(len(picturesPathsForEachFolder)) + ".pdf")
							elif numberOfEntitiesInOnePdf == 1:
								filename = os.path.join(pathToSavePdfTo, outputPdfName + "_" + nameOfPart + "_" + str(numberOfFoldersAdded + 1) + "_of_" + str(len(picturesPathsForEachFolder)) + ".pdf")
							c = canvas.Canvas(filename)
						for jPicture in iFolder:
							img = utils.ImageReader(jPicture)
							imagesize = img.getSize()
							c.setPageSize(imagesize)
							c.drawImage(jPicture, 0, 0)
							c.showPage()
						numberOfFoldersAdded += 1
						if (numberOfFoldersAdded % numberOfEntitiesInOnePdf) == 0:
							c.save()
							print("created", filename)
					if (numberOfFoldersAdded % numberOfEntitiesInOnePdf) != 0:
							c.save()
							print("created", filename)
				elif splitType == "picture":
					numberOfPicturesAdded = 0;
					totalNumberOfPictures = 0;
					for iFolder in picturesPathsForEachFolder:
						totalNumberOfPictures += len(iFolder)
					for iFolder in picturesPathsForEachFolder:
						for jPicture in iFolder:
							if (numberOfPicturesAdded % numberOfEntitiesInOnePdf) == 0:
								endNumber = numberOfPicturesAdded + numberOfEntitiesInOnePdf
								if endNumber > totalNumberOfPictures:
									endNumber = totalNumberOfPictures
								filename = []
								if numberOfEntitiesInOnePdf > 1:
									filename = os.path.join(pathToSavePdfTo, outputPdfName + "_" + nameOfPart + "_" + str(numberOfPicturesAdded + 1) + '-' + str(endNumber) + "_of_" + str(totalNumberOfPictures) + ".pdf")
								elif numberOfEntitiesInOnePdf == 1:
									filename = os.path.join(pathToSavePdfTo, outputPdfName + "_" + nameOfPart + "_" + str(numberOfPicturesAdded + 1) + "_of_" + str(totalNumberOfPictures) + ".pdf")
								c = canvas.Canvas(filename)
							img = utils.ImageReader(jPicture)
							imagesize = img.getSize()
							c.setPageSize(imagesize)
							c.drawImage(jPicture, 0, 0)
							c.showPage()
							numberOfPicturesAdded += 1
							if (numberOfPicturesAdded % numberOfEntitiesInOnePdf) == 0:
								c.save()
								print("created", filename)
					if (numberOfPicturesAdded % numberOfEntitiesInOnePdf) != 0:
							c.save()
							print("created", filename)
				elif splitType == "none":
					filename = os.path.join(pathToSavePdfTo, outputPdfName + ".pdf")
					c = canvas.Canvas(filename)
					for iFolder in picturesPathsForEachFolder:
						for jPicture in iFolder:
							img = utils.ImageReader(jPicture)
							imagesize = img.getSize()
							c.setPageSize((38*mm, 30*mm))
							c.scale(0.27, 0.27)
							c.drawImage(jPicture, 0, 0)
							c.showPage()
					c.save()
					print("created", filename)
				else:
					print("Wrong splitType value")
			else:
				print("No pictures found.")
			return
			
		if picturesAreInRootFolder == True:
			picturesInsideFolderWithPictures = []
			for iExtension in listWithImagesExtensions:
				picturesInsideFolderWithPictures.extend(glob.glob(pathToPictures + "/*." + iExtension))
			picturesInsideFolderWithPictures = self.sorted_nicely(picturesInsideFolderWithPictures)
			if len(picturesInsideFolderWithPictures) != 0:
				if splitType == "picture":
					numberOfPicturesAdded = 0
					totalNumberOfPictures = len(picturesInsideFolderWithPictures)
					for iPicture in picturesInsideFolderWithPictures:
						if (numberOfPicturesAdded % numberOfEntitiesInOnePdf) == 0:
							endNumber = numberOfPicturesAdded + numberOfEntitiesInOnePdf
							if endNumber > totalNumberOfPictures:
								endNumber = totalNumberOfPictures
							filename = []
							if numberOfEntitiesInOnePdf > 1:
								filename = os.path.join(pathToSavePdfTo, outputPdfName + "_" + nameOfPart + "_" + str(numberOfPicturesAdded + 1) + '-' + str(endNumber) + "_of_" + str(totalNumberOfPictures) + ".pdf")
							elif numberOfEntitiesInOnePdf == 1:
								filename = os.path.join(pathToSavePdfTo, outputPdfName + "_" + nameOfPart + "_" + str(numberOfPicturesAdded + 1) + "_of_" + str(totalNumberOfPictures) + ".pdf")
							c = canvas.Canvas(filename)
						img = utils.ImageReader(iPicture)
						imagesize = img.getSize()
						c.setPageSize(imagesize)
						c.drawImage(iPicture, 0, 0)
						c.showPage()
						numberOfPicturesAdded += 1
						if (numberOfPicturesAdded % numberOfEntitiesInOnePdf) == 0:
							c.save()
							print("created", filename)
					if (numberOfPicturesAdded % numberOfEntitiesInOnePdf) != 0:
						c.save()
						print("created", filename)
				elif splitType == "none":
					filename = os.path.join(pathToSavePdfTo, outputPdfName + ".pdf")
					c = canvas.Canvas(filename)
					for iPicture in picturesInsideFolderWithPictures:
						img = utils.ImageReader(iPicture)
						imagesize = img.getSize()
						c.setPageSize((38*mm, 30*mm))
						c.scale(0.27, 0.27)
						c.drawImage(iPicture, 0, 0)
						c.showPage()
					c.save()
					print("created", filename)
				else:
					print("Wrong splitType value")
			else:
				print("No pictures found.")
			return

	@d2250print
	def print_order_sticker(self, order_info, printer_name="ARGOX_D2-250_PPLB", **kwargs):
		# print order sticker. order info class.
		for i in range(len(order_info)):
			img = Image.new('RGB', (self.sticker_width, self.sticker_height), color = (255, 255, 255))
			d = ImageDraw.ImageDraw(img)
			
			# Generate Sticker
			sf = StickerFormat(default_font_path=self.default_font_path, 
				left_header="編號%s"%str(order_info["serial_number"]), right_header="%02d/%02d"%(i+1, len(order_info)))
			
			# Handle special day
			if "special day" in order_info.orders[i].title:
				title_str = order_info.orders[i].title + "@ "+str(order_info.orders[i]["基底"]).replace("[", "").replace("]", "")
			else:
				title_str = order_info.orders[i].title
			sf.append({"string": "{} - ${}".format(title_str,str(order_info.orders[i]["final_price"])), "font": "big_font"})
			sf.add_repeat_char(" ", "small_font")

			sf.append({"string": "選配: "+order_info.orders[i].get_options_str(), "font": "default_font"}, delimiter=',')
			# Handle bottom header string
			if not kwargs.get("store_str_bottom", True):
				left_bottom = " "
			else:
				left_bottom = OrderInfo.getStoreStr(order_info["store_id"])

			if not kwargs.get("store_phone_bottom", True):
				right_bottom = " "
			else:
				right_bottom = OrderInfo.getStorePhone(order_info["store_id"])

			sf.append({"string": sf.spread_string(left_bottom, right_bottom, sf.small_font),"font": "small_font"}, end_header=True)

			self.img_draw_string(d, sf)

			img_fp = self.d2250_tmpfile_path+"/img_%s_%d.png"%(order_info["order_id"], i)
			self.save_img_to_location(img, img_fp)

		return self.d2250_tmpfile_path, "D2250-"+order_info["order_id"]

	@d2250print
	def print_inventory_sticker(self, inventory_item, printer_name="ARGOX_D2-250_PPLB", **kwargs):
		# print inventory sticker. inventory item.
		for i in range(inventory_item.subitems_count):
			img = Image.new('RGB', (self.sticker_width, self.sticker_height), color = (255, 255, 255))
			d = ImageDraw.ImageDraw(img)

			sf = StickerFormat(default_font_path=self.default_font_path, 
				left_header="庫存%s"%inventory_item.invid, right_header="%02d/%02d"%(i, inventory_item.subitems_count))
			sf.append({"string": inventory_item.name, "font": "big_font"})
			sf.add_repeat_char(" ", "small_font")
			sf.append({"string": "進貨日期 : {}".format(inventory_item.made_date), "font": "default_font"})
			sf.append({"string": "有效期限 : {}".format(inventory_item.expirary_date), "font": "default_font"})
			sf.append({"string": sf.spread_string(inventory_item.upstream_name, inventory_item.upstream_phone, sf.small_font),
				"font": "small_font"}, end_header=True)
			self.img_draw_string(d, sf)

			img_fp = self.d2250_tmpfile_path+"/img_%s_%d.png"%(food_item.invid, i)
			self.save_img_to_location(img, img_fp)

		return self.d2250_tmpfile_path, "D2250-"+food_item.invid

	@d2250print
	def print_food_sticker(self, food_item, printer_name="ARGOX_D2-250_PPLB", **kwargs):
		# This is for printing food sticker. With expirary date
		for i in range(food_item.subitems_count):
			img = Image.new('RGB', (self.sticker_width, self.sticker_height), color = (255, 255, 255))
			d = ImageDraw.ImageDraw(img)

			sf = StickerFormat(default_font_path=self.default_font_path, 
				left_header="庫存%s"%food_item.invid, right_header="%02d/%02d"%(i, food_item.subitems_count))
			sf.append({"string": food_item.name, "font": "big_font"})
			sf.add_repeat_char(" ", "small_font")
			sf.append({"string": "製造日期 : {}".format(food_item.made_date), "font": "default_font"})
			sf.append({"string": "有效期限 : {}".format(food_item.expirary_date), "font": "default_font"})
			sf.append({"string": sf.spread_string(food_item.upstream_name, food_item.upstream_phone, sf.small_font),
				"font": "small_font"}, end_header=True)
			self.img_draw_string(d, sf)

			img_fp = self.d2250_tmpfile_path+"/img_%s_%d.png"%(food_item.invid, i)
			self.save_img_to_location(img, img_fp)

		return self.d2250_tmpfile_path, "D2250-"+food_item.invid

	def print_test(self, sticker_format):
		"""
		This is for testing only. Example code exist. 
		"""
		img = Image.new('RGB', (self.sticker_width, self.sticker_height), color = (255, 255, 255))
		d = ImageDraw.ImageDraw(img)
		self.img_draw_string(d, sticker_format)
		img_fp = self.d2250_tmpfile_path+"/img.png"
		self.save_img_to_location(img, img_fp)

	@dutils
	def img_draw_string(self, imgdraw, sticker_format, **kwargs):
		"""
		This is the function to draw the sticker
		string on the image canvas. 
		"""
		for line in sticker_format:
			imgdraw.text(line["pos"], line["string"], font=line["font"], fill=line["color"])

class DodayPeripherals:
	"""
	This is the class for DoDay inventory
	management. One instance for a store or a kitchen. 
	"""
	@dutils 
	def __init__(self, init_peripherals=["D2250_sticker"], doday_api_lib=None, **configs):
		self.terminate_qr_process = False
		if doday_api_lib:
			self.doday_lib = cdll.LoadLibrary(doday_api_lib)
			self.doday_lib.minc_init_api()
		else:
			self.doday_lib = None

		for mod in init_peripherals:
			setattr(self, mod, eval(mod)(**configs))

	@dutils
	def order_print(self, order_info, **kwargs):
		"""
		This is the function to print the order
		"""
		# This is the assertion of doday lib existence
		assert self.doday_lib != None

		self.doday_lib.minc_print_order(*order_info.toprinterargs())

	@dutils
	def cli_normal_call(self, param=[], **kwargs):
		"""
		This is the function to do the normal
		cli call
		"""
		return subprocess.check_output(param) 

	@dutils
	def cli_call_scripts(self, file_path, param=[], **kwargs):
		"""
		This is the function to help call the
		script via cli. 
		"""
		if param != []:
			output = subprocess.check_output(['bash', file_path]+param)
		else:
			output = subprocess.check_output(['bash', file_path]) # with args:  subprocess.call(['./test.sh', 'param1', 'param2'])
		return output

	# CV2 related functions
	# ---------------------------
	@dutils
	def img_qr_scan_init(self, **kwargs):
		# The these two only if needed. 
		import cv2
		import pyzbar.pyzbar as pyzbar

	@dutils
	def decodeDisplay(self, imagex1, **kwargs):
		"""
		This is used to decode the qr image data
		to barcode data. 
		"""
		# 轉為灰度影象
		gray = cv2.cvtColor(imagex1, cv2.COLOR_BGR2GRAY)
		barcodes = pyzbar.decode(gray)

		try:
			barcode = barcodes[0]
		except:
			return ""

		barcodeData = barcode.data.decode("utf-8")
		
		return barcodeData

	@dutils
	def get_qr_scan_data(self, tout, **kwargs):
		"""
		This is the main function that the checkin front end should
		call. It turns on the camera and scan the qr code and extract
		the data for checkin functionality.  
		"""
		self.terminate_qr_process = False

		# Capture frame
		cap = cv2.VideoCapture(0, cv2.CAP_V4L)
		cv2.waitKey(10)
		data = None

		tout_start_time = time.time()
		while True:
			_, inputImage = cap.read()
			cv2.waitKey(50)

			data = decodeDisplay(inputImage)
			
			if self.terminate_qr_process:
				logging.info("manual terminate qr loop")
				cv2.waitKey(1)
				cap.release()
				data = "Terminated"

			# payment timeout -> set to timeout
			if time.time() - tout_start_time >= tout:
				break

			if len(data)>0:
				break

			cv2.waitKey(1)

		cap.release()
		return data

	@dutils
	def get_qr_scan_data_com(self, tout, **kwargs):
		"""
		This is the main function that the checkin front end should
		call. It turns on the camera and scan the qr code and extract
		the data for checkin functionality.  
		"""
		self.terminate_qr_process = False

		tout_start_time = time.time()
		while True:
			qrcode_str = create_string_buffer(b'\000' * 32)
			self.doday_lib.minc_read_qrcode(c_int(5), qrcode_str)
			data = qrcode_str.value.decode('utf-8')
			
			if self.terminate_qr_process:
				logging.info("manual terminate qr loop")
				data = "Terminated"

			# payment timeout -> set to timeout
			if time.time() - tout_start_time >= tout:
				break

			if len(data)>0:
				break

		return data











