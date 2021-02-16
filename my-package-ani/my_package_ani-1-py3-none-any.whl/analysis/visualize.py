# Imports
from PIL import Image, ImageDraw
import numpy as np

def show_boxes(img, bboxes, labels, out):  # Write the required arguments
	# The function should plot the predicted boxes on the images and save them.
	# Tip: keep the dimensions of the output image less than 800 to avoid RAM crashes.

	img =Image.fromarray( np.uint8(np.transpose(img, (1, 2, 0))*255))
	for i in range(min(len(bboxes), 5)):
		ImageDraw.Draw(img).rectangle(bboxes[i],width=2,outline='blue')
		ImageDraw.Draw(img).text(bboxes[i][0],labels[i],fill='orange')
	img.save(out)
