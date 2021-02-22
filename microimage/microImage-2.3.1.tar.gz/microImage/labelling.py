import math
import matplotlib.font_manager as fontman
import numpy as np
import os
from PIL import ImageFont, Image, ImageDraw

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

#-------------------
# Find font location
def _find_font(fontName = 'Arial.ttf'):

    # Look for the font location on the computer
    matches = list(filter(lambda path: fontName in os.path.basename(path), fontman.findSystemFonts()))

    return matches[0]

#-------------------------------------------
# Determine the font size for the image text
def _get_font_size(text, fontPath, sizeLimit):

    # Initialise the function
    fontSize = 1
    font = ImageFont.truetype(fontPath, fontSize)

    # Loop until the size is found
    while font.getsize(text)[0] < sizeLimit:
        fontSize += 1
        font = ImageFont.truetype(fontPath, fontSize)

    return fontSize - 1

#-------------------------------
# Find the closes squared number
def _closest_square(number):

    # Initialise
    i = 0
    j = 1
    top_square = 0

    # Search for the pairs of numbers surrounding the reference
    while top_square < number:

        # Calculate the number
        i += 1
        j += 1
        bottom_square = i ** 2
        top_square = j ** 2

    # Select the one closest to the number
    if abs(number - i**2) < abs(number - j**2):
        return i
    else:
        return j

# -----------------------
# Generate the frame list
def _get_frame_list(nbr_frames, frames=1):

    # Process in case of frame separation
    if type(frames) == int:
        frame_list = list( range(0, nbr_frames, frames) )

    # Process in case of a list of frames
    elif type(frames) == list:
        frame_max = max(frames)
        if frame_max >= nbr_frames:
            raise Exception("Indices in the frame list are higher than the number of frame in the array ("+str(nbr_frames)+").")
        else:
            frame_list = frames

    # Raise an error otherwise
    else:
        raise Exception("Frame selection for montage can only be either an integer or a list of integers.")

    return frame_list

# -------------------------------------------------------
# Get the properties of the table for the montage display
def _get_table_properties(frames, column=None, row=None):

    # Get the number of frames
    n_frames = len(frames)

    # No informations given
    if column is None and row is None:
        column = _closest_square( n_frames )

    # Get the missing number
    if row is None and column is not None:
        row = math.ceil( n_frames / column)
    elif column is None and row is not None:
        column = math.ceil( n_frames / row)

    # Rewrite the list if different
    else:
        max_frames = column * row
        if n_frames > max_frames:
            frames = frames[0:max_frames]

    return frames, column, row

# ------------------
# Create the montage
def _do_montage(montageArray, imageArray, frame_list, column, margin=0):

    # Extract the image size
    height, width = imageArray.shape[1], imageArray.shape[2]

    # Loop over all the frames to add
    for i, frame in enumerate(frame_list):

        # Get the index of the array in the table
        row_id = i // column
        column_id = i % column

        # Get the indices of the pixel in the wide array
        xPixelStart = column_id * (width + margin)
        xPixelStop = xPixelStart + width
        yPixelStart = row_id * (height + margin)
        yPixelStop = yPixelStart + height

        # Copy the images into the new array
        montageArray[yPixelStart:yPixelStop,xPixelStart:xPixelStop] = imageArray[frame]

    return montageArray

# ----------------------------------------
# Format the text to display on the frames
def _format_time_text(n_frames, time_scale=1, time_unit='frame'):

    # Generate the time values
    time_values = np.arange(n_frames) * time_scale

    # Generate the text list
    time_text = [ "{0:.3f}".format(t) + ' ' + time_unit for t in list(time_values) ]

    return time_text

# ----------------------------------------
# Generate the text array to add on frames
def _generate_scale_text(scale_text, bar_position, image_size, font='Arial.ttf', padding=10, font_size=None, bar_length=20):

    # Get the font path
    fontPath = _find_font(fontName = font)

    # Get the size limit
    yPosition, xPosition = bar_position

    # Get the font size
    if font_size is None:
        font_size = _get_font_size(scale_text, fontPath, bar_length)

    # Calculate the position from the top edge of the image
    textFont = ImageFont.truetype(fontPath, font_size)
    textSize = textFont.getsize(scale_text)

    topPosition = yPosition - (padding + textSize[1])
    leftPosition = xPosition

    # Generate the image to draw
    textImage = Image.new('L', image_size, color=(0))

    # Draw the text on the image
    textDrawing = ImageDraw.Draw(textImage)
    textDrawing.text((leftPosition,topPosition), scale_text, fill=(255), font=textFont)

    return np.array(textImage)

# ----------------------------------------
# Generate the text array to add on frames
def _generate_time_text(time_list, image_size, font='Arial.ttf', padding=10, font_size=None, position='bottom'):

    # Get the font path
    fontPath = _find_font(fontName = font)

    # Get the size limit
    height, width = image_size
    sizeLimit = width - 2*padding

    # Get the font size
    longestName = max(time_list, key=len)
    if font_size is None:
        font_size = _get_font_size(longestName, fontPath, sizeLimit)

    # Calculate the position from the top edge of the image
    textFont = ImageFont.truetype(fontPath, font_size)
    textSize = textFont.getsize(longestName)

    if position == 'top':
        topPosition = padding
    else:
        topPosition = height - (padding + textSize[1])

    # Process all the frames
    text_array = []
    for time in time_list:

        # Generate the image to draw
        textImage = Image.new('L', image_size, color=(0))

        # Draw the text on the image
        textDrawing = ImageDraw.Draw(textImage)
        textDrawing.text((padding,topPosition), time, fill=(255), font=textFont)

        text_array.append( np.copy( np.array(textImage) ) )

    return np.array(text_array)

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ----------------------------
# Add a scale bar to the image
def scaleBar(array, space_unit='px', space_scale=1, scale_length=20, thickness=20, padding=10, white_bar=False, add_text=False, font='Arial.ttf', font_size=None):

    # Duplicate
    imageArray = np.copy(array)

    # Get the scale bar length in px
    if space_unit.lower() not in ['px','pixel']:
        bar_length = scale_length * space_scale
    else:
        bar_length = scale_length

    # Get the limits of the bar
    xMax = array.shape[-1] - padding
    yMax = array.shape[-2] - padding
    xMin = xMax - bar_length
    yMin = yMax - thickness
    xMin, xMax, yMin, yMax = int(xMin), int(xMax), int(yMin), int(yMax)

    # Set the color of the bar
    if white_bar:
        color = np.iinfo(imageArray.dtype).max
    else:
        color = 0

    # Edit the array
    imageArray[yMin:yMax, xMin:xMax] = color

    # Add the text if required
    if add_text:

        # Generate the text
        scale_text = str(scale_length) + ' ' + space_unit

        # Generate the array
        textArray = _generate_scale_text(scale_text, (yMin, xMin), (array.shape[-2], array.shape[-1]), font=font, padding=padding, font_size=font_size, bar_length=bar_length)

        # Apply the text
        imageArray[textArray == 255] = color

    return imageArray

# -------------------------
# Add time stamps on frames
def timeStamps(array, time_unit='frame', time_scale=1, font_size=None, font='Arial.ttf', padding=10, position='bottom', white_text=False):

    # Duplicate
    imageArray = np.copy(array)

    # Get the texts to print
    time_list = _format_time_text(imageArray.shape[0], time_scale=time_scale, time_unit=time_unit)

    # Generate the text array to print
    textArray = _generate_time_text(time_list, (imageArray.shape[1], imageArray.shape[2]), padding=padding, font=font, font_size=font_size, position=position)

    # Select the text color
    if white_text:
        color = np.iinfo(imageArray.dtype).max
    else:
        color = 0

    # Copy the text on the image
    for i, textToAdd in enumerate(textArray):
        imageArray[i][textToAdd == 255] = color

    return imageArray

# -----------------
# Produce a montage
def makeMontage(imageArray, frames=1, column=None, row=None, margin=0, white_margin=False):

    # Format the list of frames to be saved
    frame_list = _get_frame_list(imageArray.shape[0], frames=frames)

    # Get the table rows and columns
    frame_list, column, row = _get_table_properties(frame_list, column=column, row=row)

    # Generate the empty montage array
    height = row * imageArray.shape[1] + (row-1) * margin
    width = column * imageArray.shape[2] + (column-1) * margin
    montageArray = np.zeros((height, width), imageArray.dtype)

    # Initialise the background for margin
    if white_margin:
        montageArray[:] = np.iinfo(imageArray.dtype).max

    # Populate the montage array
    montageArray = _do_montage(montageArray, imageArray, frame_list, column, margin=margin)

    return montageArray
