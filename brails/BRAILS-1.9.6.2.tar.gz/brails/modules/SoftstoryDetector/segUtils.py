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

def encodeClass(df,className,fileName,fileNameReverse):
    classEncodes={}
    classEncodes_reverse={}
    for i,c in enumerate(list(df[className].unique())):
        classEncodes[c] = i+1
        classEncodes_reverse[i+1]=c
    print(classEncodes)
    with open(fileName, 'w') as fp:
        json.dump(classEncodes, fp)
    with open(fileNameReverse, 'w') as fp:
        json.dump(classEncodes_reverse, fp)
        
def writeanno(df, filename,tagName,classEncodeFile,imgDir='../'):
    images = []
    annotations = []
    
    
    imgID = 0
    imgList = []
    
    with open(classEncodeFile) as json_file:
        classEncode = json.load(json_file)
    
    for index, row in df.iterrows():

        category = row[tagName]
        #if category == "unknown":
        #    continue

        #categoryID = 1 if category=="reinforced" else 2
        categoryID = classEncode[category]

        w = int(row['width'])
        h = int(row['height'])

        #img_name = row['imgPath']
        #FolderID = row['FolderID']
        #imgPath = "/Users/simcenter/Files/Work/WorldBank/DRONE/SALINACRUZ/{}/{}".format(FolderID, img_name)
        imgPath = row['imgPath']
        imgName_new = imgPath
        #imgName_new = category + "/" + str(index+1)+".jpg"

        print(imgDir+imgPath)
        
        if not path.exists(imgDir+imgPath):
            continue     
            

        x1 = int(round(float(row['xtl'])))
        y1 = int(round(float(row['ytl'])))
        x2 = int(round(float(row['xbr'])))
        y2 = int(round(float(row['ybr'])))
        
  

        if imgPath not in imgList:
            imgList.append(imgPath)
            imgID += 1
            image = {"id" : imgID,
                    "file_name" : imgName_new,
                    "width": w,
                    "height": h,
                    "date_captured": "2020-10-25 01:26:40.419787",
                    "license": 1,
                    "coco_url": "",
                    "flickr_url": ""}
            images.append(image)
            currentImgID = imgID
        else: currentImgID = imgList.index(imgPath)+1





        try:

            segmentation =  [[x1,y1, x2,y1, x2,y2, x1,y2]]

            item = {
                "area" : w*h,
                "segmentation" : segmentation,
                "iscrowd" : 0,
                "image_id" : currentImgID,
                "bbox" : [x1,y1,x2-x1,y2-y1],
                'bbox_mode' : 4, # BoxMode.XYWHA_ABS
                
                "category_id" : categoryID,
                "id" : index+1
                #"size" : imgSize,
                #"name" : imgName_new,
                #"filename" : imgName_new,
                #"regions" : regions
            }
            annotations.append(item)
            
            #shutil.copyfile(imgPath, newDir+imgName_new) 
            
        except:
            #print(imgPath+' doesn\'t exit')
            #cmd = 'aws s3 cp s3://wbg-geography01/GEP/DRONE/SALINACRUZ/{}/{} {}\n'.format(FolderID,img_name, imgPath)
            #print(cmd)
            pass #print(imgPath)

    labels = {}
    labels["annotations"] = annotations
    labels["images"] = images
    labels["info"] = {
    "description": "Building Dataset",
    "url": ".",
    "version": "0.1.0",
    "year": 2020,
    "contributor": "charles",
    "date_created": "2020-04-25 01:29:34.597570"
    }
    
    labels["licenses"] = [
    {
    "id": 1,
    "name": ".",
    "url": "."
    }
    ]
    '''
    labels["categories"] = [
    {
    "id": 1,
    "name": "reinforced",
    "supercategory": "building"
    },
    {
    "id": 2,
    "name": "unreinforced",
    "supercategory": "building"
    }
    ]
    '''
    
    labels_categories = []
    for classN in classEncode.keys():
        c = {
            'id': classEncode[classN],
            'name': classN,
            'supercategory': 'building'
        }
        labels_categories.append(c)
    labels["categories"] = labels_categories

    with open(filename, 'w') as outfile:
        json.dump(labels, outfile)
    
    print(filename)
 


    
def downloadimages(df):

    for index, row in df.iterrows():

        imgPath = row['imgPath']

        # download from s3
        if not path.exists('../'+imgPath):
            cmd = 'aws s3 cp s3://wbg-geography01/GEP/'+imgPath+' ../'+imgPath
            os.system(cmd)
            print(' ../'+imgPath)


        

def getImgbyID(id,j):
  for img in j['images']:
    if img['id'] == id:
      return img['file_name'], img['height'],img['width']
  assert "didn't find file..."
    
def get_dataset_dicts(annofilename,cat='',imgDir='../'):

    #if name=='all': annofilename='labels_json/{}_test.json'.format(cat)
    #else: annofilename='labels_json/{}_test_{}.json'.format(cat,name)
    with open(annofilename) as f:
      j = json.load(f)
    
    #

    dataset_dicts = []
    for anno in j['annotations']:
      #print(anno)
      objs = []
      obj = {
                    "bbox": anno['bbox'],
                    "bbox_mode": BoxMode.XYWH_ABS,
                    "segmentation": anno['segmentation'],
                    "category_id": j['categories'][anno["category_id"]-1]['name'], #anno["category_id"],
                    "iscrowd": anno['iscrowd']
                }
      objs.append(obj)
      record = {}
      imgID = anno['image_id']
      imgName,h,w = getImgbyID(imgID,j)
      record["file_name"] = imgDir+imgName
      record["image_id"] = imgID
      record["height"] = h
      record["width"] = w
      record["annotations"] = objs
      dataset_dicts.append(record)
    return dataset_dicts


def plotfigs(dataset_dicts,name):
    plt.figure(figsize=(20, 20))
    for i,d in enumerate(random.sample(dataset_dicts, 9)):
        img = cv2.imread(d["file_name"])
        visualizer = Visualizer(img[:, :, ::-1], metadata=MetadataCatalog.get("checkLabels{}".format(name)), scale=1.0)
        visualizer._default_font_size = max(np.sqrt(visualizer.output.height * visualizer.output.width) // 90 *8, 10 // 1.0 * 8)
        vis = visualizer.draw_dataset_dict(d)
        
        #cv2_imshow(vis.get_image()[:, :, ::-1])
        ax = plt.subplot(3, 3, i + 1)
        plt.imshow(vis.get_image()[:, :, ::-1])
        plt.title(d["file_name"])
        plt.axis("off")
        
def read_anno(annofilename,cat):
    
    #maxNumPerCat = 100
    
    imgPath=[]

    width=[]
    height=[]
    xtl=[]
    ytl=[]
    xbr=[]
    ybr=[]

    category=[]
    
    #if name=='all': annofilename='labels_json/{}_test.json'.format(cat)
    #else: annofilename='labels_json/{}_test_{}.json'.format(cat,name)
    with open(annofilename) as f:
      j = json.load(f)
    
    numCat = len(j['categories'])
    catNumList = []
    [catNumList.append(0) for i in range(numCat)]
    

    dataset_dicts = []
    ll=j['annotations']
    #random.shuffle(ll) 
    for anno in ll:
      #print(anno)
      thisCatID = anno["category_id"]-1

      #if catNumList[thisCatID]>= maxNumPerCat: continue
      catNumList[thisCatID]=catNumList[thisCatID]+1
    
    
      objs = []
      obj = {
                    "bbox": anno['bbox'],
                    "bbox_mode": BoxMode.XYWH_ABS,
                    "segmentation": anno['segmentation'],
                    "category_id": j['categories'][anno["category_id"]-1]['name'], #anno["category_id"],
                    "iscrowd": anno['iscrowd']
                }
      objs.append(obj)
      record = {}
      imgID = anno['image_id']
      imgName,h,w = getImgbyID(imgID,j)
      
      imgPath.append(imgName)
      a,b,c,d=anno['bbox']

      width.append(w)
      height.append(h)
      xtl.append(a)
      ytl.append(b)
      xbr.append(c+a)
      ybr.append(d+b)
      #material
      category.append(j['categories'][anno["category_id"]-1]['name'])
      #condition
      #completeness
    imgPath
    df_tmpx = pd.DataFrame(list(zip(imgPath, width,height,xtl,ytl,xbr,ybr,category)),columns =['imgPath', 'width','height','xtl','ytl','xbr','ybr',cat]) 
    
    return df_tmpx

def read_anno_backup(name,cat):
    imgPath=[]

    width=[]
    height=[]
    xtl=[]
    ytl=[]
    xbr=[]
    ybr=[]

    category=[]
    

    with open('labels_json/{}_test_{}.json'.format(cat,name)) as f:
      j = json.load(f)

    dataset_dicts = []
    for anno in j['annotations']:
      #print(anno)
      objs = []
      obj = {
                    "bbox": anno['bbox'],
                    "bbox_mode": BoxMode.XYWH_ABS,
                    "segmentation": anno['segmentation'],
                    "category_id": j['categories'][anno["category_id"]-1]['name'], #anno["category_id"],
                    "iscrowd": anno['iscrowd']
                }
      objs.append(obj)
      record = {}
      imgID = anno['image_id']
      imgName,h,w = getImgbyID(imgID,j)
      
      imgPath.append(imgName)
      a,b,c,d=anno['bbox']

      width.append(w)
      height.append(h)
      xtl.append(a)
      ytl.append(b)
      xbr.append(c+a)
      ybr.append(d+b)
      #material
      category.append(j['categories'][anno["category_id"]-1]['name'])
      #condition
      #completeness
    imgPath
    df_tmpx = pd.DataFrame(list(zip(imgPath, width,height,xtl,ytl,xbr,ybr,category)),columns =['imgPath', 'width','height','xtl','ytl','xbr','ybr',cat]) 
    
    return df_tmpx


def plotfigs2(dataset_dicts,name,predictor,cfg,fontSize=5,alpha=0.1,threshold=0.7):
    
    
    plt.figure(figsize=(20, 40))
    for i,d in enumerate(random.sample(dataset_dicts, 8)):
        img = cv2.imread(d["file_name"])
        print(d["file_name"])
        #visualizer = Visualizer(img[:, :, ::-1], metadata=MetadataCatalog.get("checkLabels{}".format(name)), scale=1.0)
        visualizer = Visualizer(img[:, :, ::-1], metadata=MetadataCatalog.get('whatever'), scale=1.0)
        visualizer._default_font_size = max(np.sqrt(visualizer.output.height * visualizer.output.width) // 90 *fontSize, 10 // 1.0 * fontSize)
        #print(d)
        #annos = d.get("annotations", None)
        #print(annos)
        #labels = [x["category_id"] for x in annos]

        vis = visualizer.draw_dataset_dict(d,alpha=0.0)
        #cv2_imshow(vis.get_image()[:, :, ::-1])
        ax = plt.subplot(4, 4, 2*i + 1)
        plt.imshow(vis.get_image()[:, :, ::-1])
        #plt.title('Label')#d['annotations'][0]['category_id']
        plt.axis("off")
        
        outputs = predictor(img)
        v = Visualizer(img[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TEST[0]), scale=1)
        v._default_font_size = max(np.sqrt(v.output.height * v.output.width) // 90 *fontSize, 10 // 1.2 * fontSize)
        out = v.draw_instance_predictions(outputs["instances"].to("cpu"), alpha=alpha)
        
        ax = plt.subplot(4, 4, 2*i + 2)
        plt.imshow(out.get_image()[:, :, ::-1])
        #plt.title('Prediction')
        plt.axis("off")
        plt.rcParams['axes.xmargin'] = 0

def plotfigs3(dataset_dicts,name,predictor,cfg,cat,fontSize=5,alpha=0.1,threshold=0.7):
    
    if not os.path.exists('images/{}'.format(cat)):
        os.makedirs('images/{}'.format(cat))
    imgDir='images/{}/{}'

    
    for i,d in enumerate(random.sample(dataset_dicts, len(dataset_dicts))):

        print(d["file_name"])

        img = cv2.imread(d["file_name"])

        s = '-'.join(d["file_name"].split('/')[1:])
        newimg=imgDir.format(cat,s)

        if os.path.exists(newimg): continue

        plt.figure(figsize=(20, 10))

        #visualizer = Visualizer(img[:, :, ::-1], metadata=MetadataCatalog.get("checkLabels{}".format(name)), scale=1.0)
        visualizer = Visualizer(img[:, :, ::-1], metadata=MetadataCatalog.get('whatever'), scale=1.0)
        visualizer._default_font_size = max(np.sqrt(visualizer.output.height * visualizer.output.width) // 90 * fontSize, 10 // 1.0 * fontSize)
        #print(d)
        #annos = d.get("annotations", None)
        #print(annos)
        #labels = [x["category_id"] for x in annos]

        vis = visualizer.draw_dataset_dict(d, alpha=0.0)
        #cv2_imshow(vis.get_image()[:, :, ::-1])
        ax = plt.subplot(1,2, 1)
        plt.imshow(vis.get_image()[:, :, ::-1])
        #plt.title('Label')#d['annotations'][0]['category_id']
        plt.axis("off")
        
        outputs = predictor(img)
        v = Visualizer(img[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TEST[0]), scale=1)
        v._default_font_size = max(np.sqrt(v.output.height * v.output.width) // 90 *fontSize, 10 // 1.2 * fontSize)
        out = v.draw_instance_predictions(outputs["instances"].to("cpu"), alpha=alpha)
        
        ax = plt.subplot(1,2, 2)
        plt.imshow(out.get_image()[:, :, ::-1])
        #plt.title('Prediction')
        plt.axis("off")
        plt.rcParams['axes.xmargin'] = 0

        plt.savefig(newimg,bbox_inches='tight')



def registerdata(name,testAnno,imgDataDir):
    try:
        register_coco_instances(name, {}, testAnno, imgDataDir)
    except:
        name=name+str(random.randint(1,1e9))
        name=registerdata(name,testAnno,imgDataDir)

    return name

   
def predict(cat,trainjson,testjson,name,testdict,saveimages=False,lr=0.00025,imgDataDir = '../',fontSize=3,alpha=0.1,threshold=0.7,weights=''):
    #trainAnno='labels_json/use_train.json'
    #testAnno='labels_json/use_test_SalinaCruz_test.json'
    #testAnno='labels_json/use_test_Juchitan_test.json'
    trainAnno=trainjson#'labels_json/{}'.format(trainjson)
    testAnno=testjson#'labels_json/{}'.format(testjson)
    
    
    
    try: register_coco_instances("trainset", {}, trainAnno, imgDataDir)
    except: pass
    name = registerdata(name, testAnno, imgDataDir)

    NUM_WORKERS = 2
    IMS_PER_BATCH = 2
    BATCH_SIZE_PER_IMAGE = 128
    rootmodel = 'COCO-InstanceSegmentation'
    modelName='mask_rcnn_R_101_DC5_3x'
    modelPrefix=cat
    
    
    #lr=0.00025
    numiter=120000
    
    if weights=='':
        weights = "model/{}/{}_{}_{}_{}_{}_{}_{}_{}.pth".format(rootmodel,modelPrefix,trainAnno.split('/')[-1],lr,numiter,NUM_WORKERS, IMS_PER_BATCH, BATCH_SIZE_PER_IMAGE, modelName) 
    
    with open(testAnno) as f:
      j = json.load(f)
    
    numClasses = len(j['categories'])
    # configure 
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("{}/{}.yaml".format(rootmodel, modelName)))
    cfg.MODEL.WEIGHTS = weights
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7   # set the testing threshold 
    #cfg.MODEL.TENSOR_MASK.SCORE_THRESH_TEST = 0.8
    cfg.DATASETS.TEST = (name, )
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = numClasses
    cfg.MODEL.DEVICE='cpu' # run on cpu
    predictor = DefaultPredictor(cfg)

    for d in range(len(testdict)):
        l = testdict[d]['file_name'].split('/')
        l[0] = imgDataDir
        testdict[d]['file_name']='/'.join(l)
    
    MetadataCatalog.get(name).set(thing_classes=[j['categories'][i]['name'] for i in range(len(j['categories']))])
    #print(MetadataCatalog.get(name).thing_classes)
    if saveimages:
        plotfigs3(testdict,name,predictor,cfg,cat,fontSize=fontSize,alpha=alpha,threshold=threshold)
    else:
        plotfigs2(testdict,name,predictor,cfg,fontSize=fontSize,alpha=alpha,threshold=threshold)


def predictone(cat,trainjson,testjson,name,testdict,lr=0.00025,imgDataDir = '../', imgPath='',fontSize=5,alpha=0.1,threshold=0.7):
    #trainAnno='labels_json/use_train.json'
    #testAnno='labels_json/use_test_SalinaCruz_test.json'
    #testAnno='labels_json/use_test_Juchitan_test.json'
    trainAnno=trainjson#'labels_json/{}'.format(trainjson)
    
    
    try: register_coco_instances("trainset", {}, testjson, imgDataDir)
    except: pass

    NUM_WORKERS = 2
    IMS_PER_BATCH = 2
    BATCH_SIZE_PER_IMAGE = 128
    rootmodel = 'COCO-InstanceSegmentation'
    modelName='mask_rcnn_R_101_DC5_3x'
    modelPrefix=cat
    
    
    #lr=0.00025
    numiter=120000
    
    weights = "model/{}/{}_{}_{}_{}_{}_{}_{}_{}.pth".format(rootmodel,modelPrefix,trainAnno.split('/')[-1],lr,numiter,NUM_WORKERS, IMS_PER_BATCH, BATCH_SIZE_PER_IMAGE, modelName) 
    
    with open(testjson) as f:
      j = json.load(f)
    
    numClasses = len(j['categories'])
    # configure 
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("{}/{}.yaml".format(rootmodel, modelName)))
    cfg.MODEL.WEIGHTS = weights
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = threshold  # set the testing threshold 
    #cfg.MODEL.TENSOR_MASK.SCORE_THRESH_TEST = 0.8
    cfg.DATASETS.TEST = (name, )
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = numClasses
    cfg.MODEL.DEVICE='cpu' # run on cpu
    predictor = DefaultPredictor(cfg)


    
    MetadataCatalog.get(name).set(thing_classes=[j['categories'][i]['name'] for i in range(len(j['categories']))])



    if not os.path.exists('images/{}'.format(cat)):
        os.makedirs('images/{}'.format(cat))
    imgDir='images/{}/{}'



    if not os.path.exists(imgPath): 
        print(imgPath)
        print('Image doesn\'t exist.')
        return
    
    img = cv2.imread(imgPath)

    
    outputs = predictor(img)
    v = Visualizer(img[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TEST[0]), scale=1)
    v._default_font_size = max(np.sqrt(v.output.height * v.output.width) // 90 * fontSize, 10 // 1.2 * fontSize)
    out = v.draw_instance_predictions(outputs["instances"].to("cpu"), alpha=alpha)

    w2h = v.output.width / v.output.height
    plt.figure(figsize=(10, 10/w2h))
    plt.imshow(out.get_image()[:, :, ::-1])
    #plt.title('Prediction')
    plt.axis("off")
    plt.rcParams['axes.xmargin'] = 0

    l = imgPath.split('/')
    
    plt.savefig('-'.join(l[-4:]),bbox_inches='tight')