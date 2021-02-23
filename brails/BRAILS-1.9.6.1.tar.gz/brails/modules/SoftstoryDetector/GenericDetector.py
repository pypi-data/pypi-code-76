# -*- coding: utf-8 -*-
"""
/*------------------------------------------------------*
|                         BRAILS                        |
|                                                       |
| Author: Charles Wang,  UC Berkeley, c_w@berkeley.edu  |
|                                                       |
| Date:    02/13/2021                                   |
*------------------------------------------------------*/
"""

import json 
import xmltodict 
import glob
import os
import subprocess
import numpy as np
import xml.etree.ElementTree as ET
import pandas as pd
from os import path
import json
import random
from detectron2.structures import BoxMode
from detectron2.data.datasets import register_coco_instances
import pandas as pd

# import some common libraries
import numpy as np
import cv2
import random
from cv2 import imshow

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
import matplotlib.pyplot as plt



from detectron2.data.datasets import register_coco_instances
from detectron2.engine import DefaultTrainer

import glob
import random
from detectron2.structures import BoxMode
from detectron2.data.catalog import DatasetCatalog

class GenericDetector:
    """ A Generic Object Detector. """

    def __init__(self, modelName=None, classNames=None, resultFile='preds.csv', workDir='tmp', printRes=True):
        '''
        modelFile: path to the model
        classNames: a list of classnames
        '''

        if not os.path.exists(workDir): os.makedirs(workDir)

        if not modelName:

            modelName = 'myCoolModelv0.1'
            print('You didn\'t specify modelName, a default one is assigned {}.'.format(modelName))

        modelFile = os.path.join(workDir,'{}.pth'.format(modelName))
        modelDetailFile = os.path.join(workDir,'{}.json'.format(modelName))

        self.workDir = workDir
        self.modelFile = modelFile
        self.classNames = classNames
        self.resultFile = resultFile
        self.modelName = modelName
        self.modelDetailFile = modelDetailFile
        self.printRes = printRes

        if os.path.exists(modelFile):
            print('Model found locally: {} '.format(modelFile))
            self.loadModel(modelFile)
            print('Model loaded.')
            
            # check if a local definition of the model exists.
            if os.path.exists(self.modelDetailFile):
                with open(self.modelDetailFile) as f:
                    self.classNames = json.load(f)['classNames']
                    print('Class names found in the detail file: {} '.format(self.classNames))

        else:
            print('Model file {} doesn\'t exist locally. You are going to train your own model.'.format(modelFile))


    def loadModel(self, weights):
        '''
        weights (str) : .pth
        '''

        numClasses = 2

        # configure 
        cfg = get_cfg()
        cfg.merge_from_file(model_zoo.get_config_file("{}/{}.yaml".format('COCO-InstanceSegmentation', 'mask_rcnn_R_101_DC5_3x')))
        cfg.MODEL.WEIGHTS = weights
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7   # set the testing threshold 
        #cfg.DATASETS.TEST = (name, )
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = numClasses
        cfg.MODEL.DEVICE='cpu' # run on cpu
        self.predictor = DefaultPredictor(cfg)


        #return self.predictor

        #MetadataCatalog.get(name).set(thing_classes=[])




    def predictOne(self,imagePath):

        img = image.load_img(imagePath, target_size=(256, 256))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        prediction = self.model.predict(x)
        prob = max(prediction[0])
        prediction = np.argmax(prediction[0])
        if self.classNames: prediction = self.classNames[prediction]

        if os.path.getsize(imagePath)/1024 < 9: # small image, likely to be empty
            #print("{imagePath} is blank. No predictions.")
            #return [imagePath,None, None]
            print("Image :  {}     Class : {} ({}%)".format(imagePath, prediction, str(round(0*100,2)))) 
            return [imagePath,prediction,0]
        else:
            print("Image :  {}     Class : {} ({}%)".format(imagePath, prediction, str(round(prob*100,2)))) 
            return [imagePath,prediction,prob]

    def predictMulti(self,imagePathList):
        predictions = []
        probs = []
        for imagePath in imagePathList:
  
            img = image.load_img(imagePath, target_size=(256, 256))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            prediction = self.model.predict(x)
            if os.path.getsize(imagePath)/1024 < 9: # small image, likely to be empty
                probs.append(0)
            else:
                probs.append(max(prediction[0]))
            prediction = np.argmax(prediction[0])
            if self.classNames: prediction = self.classNames[prediction]
            predictions.append(prediction)

        if self.printRes:
            for img, pred, prob in zip(imagePathList, predictions, probs): 
                print("Image :  {}     Class : {} ({}%)".format(img, pred, str(round(prob*100,2)))) 

        df = pd.DataFrame(list(zip(imagePathList, predictions, probs)), columns =['image', 'prediction', 'probability']) 
        df.to_csv(self.resultFile, index=False)
        print('Results written in file {}'.format(self.resultFile))

        return df
    
    def predict(self,image):
        if type(image) is list: pred = self.predictMulti(image)
        elif type(image) is str: pred = self.predictOne(image)
        else: 
            print("The parameter of this function should be string or list.")
            pred = []
        return pred


    def save(self, newModelName=None):
        if newModelName != None: 
            newFileName = os.path.join(self.workDir,'{}.pth'.format(newModelName))
        else:
            newFileName = self.modelFile
        self.model.save(newFileName) 
        print('Model saved at ', newFileName)



def main():
    pass

if __name__ == '__main__':
    main()




