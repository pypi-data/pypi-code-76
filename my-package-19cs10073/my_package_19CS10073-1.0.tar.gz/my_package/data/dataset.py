#Imports
import numpy as np
import json
from matplotlib import image
from matplotlib import pyplot
from pathlib import Path
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
        self.transforms = transforms
        self.data_list = []
        with open(self.annotation_file) as f:
            for line in f:
                img_data = json.loads(line)
                gt_bboxes = np.array([])
                
                for item in img_data['bboxes']:
                    item_info = np.append(item['category_id'], item['bbox'])
                    if(len(gt_bboxes) == 0):
                        gt_bboxes = item_info
                        gt_bboxes = gt_bboxes.reshape(1,5)
                    else:
                        gt_bboxes = np.vstack((gt_bboxes,item_info))
                
                p = Path(annotation_file)
                dir_data = str(p.parent.absolute())
                img = image.imread(dir_data + '\\' + img_data['img_fn'])
                
                img = np.interp(img, (img.min(), img.max()), (0, +1))
                
                if(self.transforms != None):
                    for transform in self.transforms:
                        img = transform(img)
                
                img = np.transpose(img, (2,0,1))
                
                self.data_list.append([img, gt_bboxes])
        

    def __len__(self):
        '''
            return the number of data points in the dataset
        '''
        return len(self.data_list)
        

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
        D = {}
        D['image'] = self.data_list[idx][0]
        D['annotations'] = self.data_list[idx][1]
        return D

        