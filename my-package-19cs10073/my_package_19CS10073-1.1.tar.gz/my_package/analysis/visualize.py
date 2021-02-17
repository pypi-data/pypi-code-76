#Imports
import numpy as np
import cv2

def plot_boxes(pred_class, pred_boxes, image, path, image_name, color = (0,0,1.0)):
    # converting image numpy array to float for drawing bboxes
    image_f = image.astype('float32')

    # converting from RGB to BGR for using opencv
    image_f = cv2.cvtColor(image_f, cv2.COLOR_RGB2BGR)

    # drawing the top 5 predicted bounding boxes
    for item_number, bbox in enumerate(pred_boxes):
        if(item_number >= 5):
            break
        image_f = cv2.rectangle(image_f, bbox[0], bbox[1], color, 2)
        cv2.putText(image_f, pred_class[item_number], (bbox[0][0], max(bbox[0][1],20)), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    
    # saving image in outputs folder
    cv2.imwrite(str(path + '\\' + image_name + '.jpg'), 255*image_f)

    # converting from BGR to RGB
    return cv2.cvtColor(image_f, cv2.COLOR_BGR2RGB)
  
  # The function should plot the predicted boxes on the images and save them.
  # Tip: keep the dimensions of the output image less than 800 to avoid RAM crashes.