#Imports
import jsonlines
from PIL import Image
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
        self.annotation_file=annotation_file
        if transforms==None:
            self.transforms = []
        else:
            self.transforms = transforms
        self.image_paths = []
        self.bboxes = []
        with jsonlines.open(annotation_file) as fl:
            for line in fl.iter():
                self.image_paths.append(line['img_fn'])
                self.bboxes.append(line['bboxes'])
        

    def __len__(self):
        '''
            return the number of data points in the dataset
        '''
        return len(self.annotation_file) 

        

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
        edit_path = "/Users/satvikb/SELab/PythonDS/AssignmentQs2/data/"
        image = Image.open(edit_path + self.image_paths[idx])
        
        for x in self.transforms:
            image = x(image)
            
        gt_bboxes = []
        for x in self.bboxes[idx]:
            arr = []
            arr.append(x['category'])
            arr = [*arr, *x['bbox']]
            gt_bboxes.append(arr)
        
        imageArr = np.array(image)
        imageArr = imageArr.transpose(2,0,1).astype('float32')
        imageArr/=255.0
        return {"image" : imageArr, "gt_bboxes" : gt_bboxes}
        
        

        