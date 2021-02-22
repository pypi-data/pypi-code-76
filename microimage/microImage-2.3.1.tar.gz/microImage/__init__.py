import numpy as np
import os

import microImage.correction as corr
import microImage.image_classes as img
import microImage.input_output as io
import microImage.labelling as lbl
import microImage.modification as mod

##-\-\-\-\-\-\-\-\-\-\-\
## INPUT/OUTPUT FUNCTIONS
##-/-/-/-/-/-/-/-/-/-/-/

# ----------------------------------
# Open the image and return an array
def openImage(path):
    imageArray = io.loadImage(path)
    return imageArray

# ---------------------------------------
# Open the image and load it into a class
def loadImage(path, name = None):

    # Open the image
    imageArray = io.loadImage(path)

    # Extract the name of the file
    if name is None:
        a,name = os.path.split(path)
        if name == "":
            a,name = os.path.split(a)

    return img.getImageClass(imageArray, name=name)

# --------------------------
# Load an array into a class
def loadArray(array, name='Untitled'):
    return img.getImageClass(array, name=name)

# -----------------------------
# Save the image frame or stack
def saveImage(array, path, default=".tif", bit_depth=8, rescale=True):
    io.saveImage(array, path, default=default, bit_depth=bit_depth, rescale=rescale)

# -------------------------
# Save the array as a video
def saveVideo(array, path, fps=25, video_codec='libx264'):
    io.saveVideo(path, array, fps=fps, video_codec=video_codec)

##-\-\-\-\-\-\-\-\
## IMAGE CORRECTION
##-/-/-/-/-/-/-/-/

# ---------------------------------------
# Remove the background of an image stack
def backgroundCorrection(array, signed_bits=False, average='mean', correction='division'):

    # Apply the background correction
    corrected_array = corr.backgroundCorrection(array,
        signed_bits=signed_bits,
        average=average,
        correction=correction
        )

    return corrected_array

# ---------------------------------
# Correct the contrast of the image
def contrastCorrection(array, min=None, max=None, percentile=10, percentile_min=None, rescale=True):

    # Get the limits
    old_limits, new_limits = corr.setContrastCorrection(array,
        min=min,
        max=max,
        percentile=percentile,
        percentile_min=percentile_min,
        rescale=rescale
        )

    # Process the array
    corrected_array = corr.doContrastCorrection(array, old_limits, new_limits)

    return corrected_array

# -------------------------------------------------
# Display the pixel value distribution of the input
def showPVD(array, n_bins=1000, min=None, max=None, percentile=10, percentile_min=None, log_scale=None):
    corr.showPVDistribution(array, n_bins=n_bins, min=min, max=max, percentile=percentile, percentile_min=percentile_min, log_scale=log_scale)

##-\-\-\-\-\-\-\-\-\
## IMAGE MANIPULATION
##-/-/-/-/-/-/-/-/-/

# -------------------------------------
# Crop the image using the given points
def cropImage(array, top_left=(0,0), bottom_right=None):
    return mod.crop(array, top_left=top_left, bottom_right=bottom_right)

# ----------------------------
# Add time stamp on the frames
def addTime(array, time_unit='frame', time_scale=1, font_size=None, font='Arial.ttf', padding=10, position='top', white_text=False):
    return lbl.timeStamps(array, time_unit=time_unit, time_scale=time_scale, font_size=font_size, font=font, padding=padding, position=position, white_text=white_text)

# -------------------------------
# Add a scale bar on the frame(s)
def addBar(array, space_unit='px', space_scale=1, scale_length=20, thickness=20, padding=10, white_bar=False, add_text=False, font='Arial.ttf', font_size=None):

    # Process multiple frames
    if len(array.shape) == 3:
        new_array = []
        for frame in array:
            new_array.append( lbl.scaleBar(frame, space_unit=space_unit, space_scale=space_scale, scale_length=scale_length, thickness=thickness, padding=padding, white_bar=white_bar, add_text=add_text, font=font, font_size=font_size) )
        new_array = np.array(new_array)

    # Process single frame
    else:
        new_array = lbl.scaleBar(array, space_unit=space_unit, space_scale=space_scale, scale_length=scale_length, thickness=thickness, padding=padding, white_bar=white_bar, add_text=add_text, font=font, font_size=font_size)

    return new_array

##-\-\-\-\-\-\-\-\-\
## MONTAGE GENERATION
##-/-/-/-/-/-/-/-/-/

# -------------------------
# Generate an image montage
def makeMontage(array, frames=1, column=None, row=None, margin=0, white_margin=False):
    return lbl.makeMontage(array, frames=frames, column=column, row=row, margin=margin, white_margin=white_margin)
