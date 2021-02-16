import json
import numpy as np
import cv2

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
        self.transforms = transforms
        with open(annotation_file) as f:
            lines = f.readlines()
            self.data = []
            for line in lines:
                self.data.append(json.loads(line))
        

    def __len__(self):
        '''
            return the number of data points in the dataset
        '''
        return len(self.data)
        

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
        img = cv2.imread("data/" + self.data[idx]['img_fn'], cv2.IMREAD_COLOR)
        
        arr = np.asarray( img, dtype="float32" )
        arr = np.transpose(arr, (2, 0, 1))
        arr *= 1.0/arr.max()
        
        gt_bboxes = []
        for box in self.data[idx]['bboxes']:
            bbox = []
            bbox.append(box['category'])
            for cord in box['bbox']:
                bbox.append(cord)
            gt_bboxes.append(bbox)

        for transfrom in self.transforms:
            arr = transfrom(arr)
        
        obj = {}
        obj['image'] = arr
        obj['gt_bboxes'] = gt_bboxes

        return obj


        