#Imports
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np

def plot_boxes(im, pred_boxes , pred_class , output): # Write the required arguments
  # The function should plot the predicted boxes on the images and save them.
  # Tip: keep the dimensions of the output image less than 800 to avoid RAM crashes.
  im = np.transpose(im , (1,2,0))
  print(im.shape)
  fig,ax = plt.subplots(1)
  ax.imshow(im)
  count = 0
  for box in pred_boxes:
    count = count + 1
    if count > 5:
      break
    rect = patches.Rectangle(box[0] , box[1][0]-box[0][0] , box[1][1]-box[0][1], linewidth=1 , edgecolor='r',facecolor='none')
    ax.add_patch(rect)
    plt.text(box[0][0] , box[0][1] , pred_class[count-1] ,color='r')

  plt.savefig(output)
  return

