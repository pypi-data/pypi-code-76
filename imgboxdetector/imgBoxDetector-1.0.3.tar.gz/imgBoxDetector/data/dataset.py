#Imports
import json
from PIL import Image, ImageOps
from numpy import asarray 
import numpy as np

class Dataset(object):
	'''
        A class for the dataset that will return data items as per the given index
	'''

	def __init__(self, annotation_file, transforms = None):
		'''
            Arguments:
            annotation_file: path to the annotation file
            transforms: list of transforms (class instances)
                        For instance, [<class 'RandomCrop'>, <class 'Rotate'>]
		'''
		
		self.annotation_file = annotation_file
		
		if transforms==None:
			self.transforms = []
		else:
			self.transforms = transforms

		self.dataPoints = []
		fin = open(self.annotation_file,"r")
		
		for line in fin:
			self.dataPoints.append(json.loads(line.strip('\n')))

		fin.close()


	def __len__(self):
		'''
		    return the number of data points in the dataset
		'''
		return self.dataPoints.size
        

	def __getitem__(self, idx):
		'''
			return the dataset element for the index: "idx"
			Arguments:
				idx: index of the data element.

			Returns: A dictionary with:
				image: image (in the form of a numpy array) (shape: (3, H, W))
				gt_bboxes: N X 5 array where N is the number of bounding boxes, each 
							consisting of [class, x1, y1, x2, y2]
							x1 and x2 lie between 0 and width of the image,
							y1 and y2 lie between 0 and height of the image.

			You need to do the following, 
			1. Extract the correct annotation using the idx provided.
			2. Read the image and convert it into a numpy array (wont be necessary
				with some libraries). The shape of the array would be (3, H, W).
			3. Scale the values in the array to be with [0, 1].
			4. Create a dictonary with both the image and annotations
			4. Perform the desired transformations.
			5. Return the transformed image and annotations as specified.
		'''
		img_path = self.dataPoints[idx]['img_fn']
		img = np.array(Image.open("./data/" + img_path))

		# print(type(img))
		for transform in self.transforms:
			img = transform(img)
		
		print(type(img))
		img = img.transpose(2, 0, 1).astype('float')
		img /= 255

		ret = {}
		ret['image'] = img
		ret['bboxes'] = self.dataPoints[idx]['bboxes']
		
		return ret

# dataset = Dataset("/home/anish/Software Development Lab/Assignment-3/CS29006_SW_Lab_Spr2021/Python_DS_Assignment/AssignmentQs2/data/annotations.jsonl")
# Image.fromarray((dataset[0]['image']*255).transpose(2,1,0).astype(np.uint8)).show()
