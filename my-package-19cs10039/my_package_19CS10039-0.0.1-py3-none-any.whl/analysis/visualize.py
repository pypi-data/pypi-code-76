#Imports
import json
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def plot_boxes(image_dict, image, location = None, saver = 0): # Write the required arguments
	# The function should plot the predicted boxes on the images and save them.
	# Tip: keep the dimensions of the output image less than 800 to avoid RAM crashes.

	num_of_bboxes = len(image_dict['bboxes'])
	if num_of_bboxes > 5:
		num_of_bboxes = 5
	
	for j in image_dict['bboxes']: # for one bbox
		x_min, y_min, x_max, y_max = j['bbox']
		shape = [(x_min, y_min), (x_max, y_max)]
		drawer = ImageDraw.Draw(image)   
		drawer.rectangle(shape, outline ="red", width=5)
		my_font = ImageFont.truetype('arial.ttf', 20)
		drawer.text((x_min,y_min), j['category'], font=my_font, fill = (255, 255, 0))
	if saver == 1:
		image.save(location + image_dict['img_fn'].split('/')[-1])
	return image