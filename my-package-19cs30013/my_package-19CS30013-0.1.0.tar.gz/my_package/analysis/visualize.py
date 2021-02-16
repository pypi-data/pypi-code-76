import random as rng
import cv2

def plot_boxes(item, name, outputs):
  
  img = item['image'].transpose((1, 2, 0))
  img *= 255/img.max()

  img_ = img.copy()

  for bbox in item['gt_bboxes']:
    cv2.rectangle(img_, (int(bbox[1]), int(bbox[2])), \
          (int(bbox[3]), int(bbox[4])), (0, 255, 0), 2)
    cv2.putText(img_, bbox[0], (int(bbox[1]), int(bbox[2]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,12), 2)
  
  if outputs:
    cv2.imwrite(outputs + '/' + name + '.jpg', img_)
  
  return img_