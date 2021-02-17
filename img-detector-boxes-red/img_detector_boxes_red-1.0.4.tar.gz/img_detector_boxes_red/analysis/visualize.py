#Imports
from PIL import ImageDraw, Image, ImageFont
def plot_boxes(image, path, boxes, filename): # Write the required arguments

  # The function should plot the predicted boxes on the images and save them.
  # Tip: keep the dimensions of the output image less than 800 to avoid RAM crashes.
  font = ImageFont.load_default()
  img = Image.fromarray(image)
  drawImg = ImageDraw.Draw(img)
  for i,box in enumerate(boxes[:5]):
    tupleBox=tuple(box)
    drawImg.rectangle(tupleBox, outline="blue")
    drawImg.text((box[0][0], box[0][1]-25), filename[i], fill = "red", font = font, stroke_width = 25)
  pth = path
  img.save(fp=pth)
  return img  
  
