#Imports
import numpy as np
import cv2
def plot_boxes(pred_class, pred_boxes,image, path, image_name, color = None):
  arr = image.astype('float32')
  arr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
  colorsarr = []
  if(color==None): 
    colorsarr =[(1.0,0,1.0),(0,1.0,1.0),(1.0,0,0),(0,0,1.0),(0,1.0,0)]
  else:
    colorsarr = [color,color,color,color,color]
  for idx,box in enumerate(pred_boxes):
    if(idx>=5):
      break
    arr = cv2.rectangle(arr, box[0], box[1], colorsarr[idx], 2)
    cv2.putText(arr, pred_class[idx], (box[0][0], max(box[0][1],20)), cv2.FONT_HERSHEY_DUPLEX, 1, colorsarr[idx], 2)
  cv2.imwrite(str(path+'/'+image_name+'.jpg'), 255*arr)
  return cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
  #cv2.imshow('Image',arr)
  #cv2.waitKey(100)
   # Write the required arguments

  # The function should plot the predicted boxes on the images and save them.
  # Tip: keep the dimensions of the output image less than 800 to avoid RAM crashes.
  
  