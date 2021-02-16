#Imports
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
from PIL.Image import fromarray

def plot_boxes(im , pred_boxes, pred_class, name): # Write the required arguments

  # The function should plot the predicted boxes on the images and save them.
  # Tip: keep the dimensions of the output image less than 800 to avoid RAM crashes.
  im = np.transpose(im,(1,2,0))
  # im = fromarray(im)

  # Create figure and axes
  fig, ax = plt.subplots(1)

  # Display the image
  ax.imshow(im)

  # Create a Rectangle patch
  mina = min(5,len(pred_boxes))
  for i in range(mina):
    box = pred_boxes[i]
    width = box[1][0]-box[0][0]
    height = box[1][1]-box[0][1]
    rect = patches.Rectangle(box[0], width, height, linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(rect)
    plt.text(box[0][0],box[0][1],pred_class[i],color = 'r')

  plt.savefig(name)

  # Add the patch to the Axes
  



