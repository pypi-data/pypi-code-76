#Imports
from PIL import ImageDraw, Image, ImageFont

def plot_boxes(image, path, boxes, filename): # Write the required arguments

  # The function should plot the predicted boxes on the images and save them.
  # Tip: keep the dimensions of the output image less than 800 to avoid RAM crashes.
  
  font = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 25)
  image = Image.fromarray(image)
  image_d = ImageDraw.Draw(image)
  for i, box in enumerate(boxes[:5]):
    box_t = tuple(box)
    image_d.rectangle(box_t, outline="blue")
    image_d.text((box[1][0], box[1][1]), filename[i], fill = 'red', font = font, stroke_width = 1)
  pth = path
  image.save(fp = pth)
  return image