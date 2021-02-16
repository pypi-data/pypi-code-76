# Imports
import json
from my_package.data.transforms.rotate import RotateImage
from os import stat_result
import numpy as np
from PIL import Image


class Dataset(object):
    '''
        A class for the dataset that will return data items as per the given index
    '''
    result = []
    trans_list = []
    gen_path = None

    def __init__(self, annotation_file, transforms=None):
        '''
            Arguments:
            annotation_file: path to the annotation file
            transforms: list of transforms (class instances)
                        For instance, [<class 'RandomCrop'>, <class 'Rotate'>]
        '''
        with open(annotation_file) as f:
            self.result = [json.loads(lo) for lo in f.readlines()]
        self.trans_list = transforms
        self.gen_path = annotation_file.strip()
        self.gen_path = self.gen_path.split('/')
        self.gen_path = self.gen_path[:-1]
        self.gen_path = '/'.join(self.gen_path)
        if(self.gen_path[-1] == '/'):
            self.gen_path -= '/'
        print(f'general path to imgs dir {self.gen_path}')

    def __len__(self):
        '''
            return the number of data points in the dataset
        '''
        return len(self.result)

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
        output = {}
        json_data = self.result[idx]
        og_image = np.asarray(Image.open(f'{self.gen_path}/{json_data["img_fn"]}'))
        n_image = og_image
        # self.trans_list=[RotateImage(0)]+self.trans_list
        for x in self.trans_list:
            n_image = x(n_image)
        output["bboxes"] = json_data["bboxes"]
        # last mai H,w,3 ko 3,H,W bana dena
        # print(f'old shape-> {n_image.shape}')
        n_image = np.transpose(n_image, (2, 0, 1))/255

        # print(f'new shape-> {n_image.shape}')
        output["img"] = n_image
        return output
