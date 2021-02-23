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

from brails.modules.ModelZoo import zoo
import wget 
import os
from brails.modules.SoftstoryDetector.GenericDetector import *
import pandas as pd

class SoftstoryDetector(GenericDetector):
    """ Softstory Detector. """


    def __init__(self, modelName=None, classNames=None, resultFile='softstory2_preds.csv', workDir='tmp', printRes=True):
        '''
        modelFile: path to the model
        classNames: a list of classnames
        '''

        if not os.path.exists(workDir): os.makedirs(workDir)

        fileURL = zoo['softstory']['fileURL']
        
        if not classNames:
            classNames = zoo['softstory']['classNames']

        if not modelName:
            modelName = 'softstory_seg_v1.0'
            print('A default softstory model will be used: {}.'.format(modelName))

        modelFile = os.path.join(workDir,'{}.pth'.format(modelName))


        if not os.path.exists(modelFile): # download
            print('Downloading the model ...')
            downloadedModelFile = wget.download(fileURL, out=modelFile)

        GenericDetector.__init__(self, modelName=modelName, classNames=classNames, resultFile=resultFile, printRes=printRes)

    def detectOne(self, imagePath):

        img = cv2.imread(str(imagePath))
        outputs = self.predictor(img)
        instances = outputs["instances"].to("cpu")   

        # area:   instances[0].pred_masks.sum()
        if len(instances)>0:
            preds = instances.pred_classes.tolist() # 0: others ; 1:softstory
            scores = instances.scores.tolist()
            areas = [int(instances.pred_masks[i].sum()) for i in range(len(instances))]
            i = areas.index(max(areas))
            return preds[i], scores[i]

        return None, None

    def detect(self, images):
        preds, scores = [], []
        if isinstance(images, str):
            p, s = self.detectOne(images)
            preds.append(p)
            scores.append(s)
        elif isinstance(images, list):
            for img in images:
                p, s = self.detectOne(img)
                preds.append(p)
                scores.append(s)
                
        else: pass

        df = pd.DataFrame(list(zip(images, preds, scores)), columns =['image', 'prediction', 'probability']) 
        df.to_csv(self.resultFile, index=False)
        print('Results written in file {}'.format(self.resultFile))

        return df


        

if __name__ == '__main__':
    main()






