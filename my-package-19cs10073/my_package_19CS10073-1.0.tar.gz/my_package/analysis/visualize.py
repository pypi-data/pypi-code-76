#Imports
import numpy as np
import cv2

def plot_boxes(pred_class, pred_boxes, image, path, image_name, color = (0,0,1.0)):
    image_f = image.astype('float32')
    image_f = cv2.cvtColor(image_f, cv2.COLOR_RGB2BGR)
    
    for idx, box in enumerate(pred_boxes):
        if(idx>=5):
            break
        image_f = cv2.rectangle(image_f, box[0], box[1], color, 2)
        cv2.putText(image_f, pred_class[idx], (box[0][0], max(box[0][1],20)), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    
    cv2.imwrite(str(path+'/'+image_name+'.jpg'), 255*image_f)
    
    return cv2.cvtColor(image_f, cv2.COLOR_BGR2RGB)
  
  # The function should plot the predicted boxes on the images and save them.
  # Tip: keep the dimensions of the output image less than 800 to avoid RAM crashes.