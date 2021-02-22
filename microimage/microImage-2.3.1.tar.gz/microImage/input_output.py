import ffmpeg
from glob import glob
import numpy as np
import os
from PIL import Image, ImageSequence
import pims
from skimage import io

import microImage.correction as corr

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# ----------------------------------------------------
# Check that the extensions in the list are authorized
def _check_extensions(list, extensions=['.tif','.png','.bmp','.gif','.jpg']):

    new_list = []

    # Process all the items of the list
    for file in list:
        file_name, file_extension = os.path.splitext(file)

        # Save in the new list on if the extension is authorized
        if file_extension in extensions:
            new_list.append(file)

    # Check that the new list is not empty
    if len(new_list) == 0:
        raise Exception('The directory does not contain any valid file.')
    else:
        return new_list

# ------------------------------
# Open all the files in a folder
def _open_folder(path):

    # Check all the files in the folder
    file_in_folder = glob( os.path.join(path, '*.*') )

    # Check that the files in the folder can be opened
    file_in_folder = _check_extensions(file_in_folder)
    _, file_extension = os.path.splitext(file_in_folder[0])

    # Open all the images
    sequence = pims.ImageSequence( os.path.join(path, '*'+file_extension) )

    return np.array(sequence)

# ----------------------
# Open the selected file
def _open_file(path):

    # Check the extension of the given file
    file_path = _check_extensions( [path] )
    path = file_path[0]

    # Load the image(s)
    sequence = Image.open(path)

    # Deal with stacks (.tif) and animations (.gif)
    if 'n_frames' in dir(sequence):

        # Extract all frames
        stack = []
        for frame in ImageSequence.Iterator(sequence):
            stack.append( np.copy(np.array(frame)) )

        imageArray = np.array(stack)

    # Convert simple image type
    else:
        imageArray = np.array(sequence)

        # Format the shape of all image arrays
        imageArray = np.reshape( imageArray, (1, *imageArray.shape) )

    return imageArray

# ----------------------------------------
# Add an extension to the file if required
def _add_extension(path, default=".tif"):

    # Separate the name and extension
    name, extension = os.path.splitext(path)

    # Add extension if missing
    if extension == "":
        path_a, path_b = os.path.split(path)

        if path_b == "":
            path = path_a + default
        else:
            path += default

    return path

# ------------------------------------
# Convert the image type and bit depth
def _convert_bit_depth(array, bit_depth=8, rescale=True):

    # Check the bit depth
    if bit_depth not in [8,16]:
        raise Exception('The selected bit depth ('+str(bit_depth)+') is not supported. Please select any of the following (8/16)')

    # Get the parameters for the conversion
    data_types = {8:np.uint8, 16:np.uint16}
    data_type = data_types[bit_depth]

    new_limits = (0, 2**bit_depth - 1)

    # Check for rescale of old min value
    if rescale:
        old_min = np.amin(array)
    else:
        old_min = 0

    # Check for rescale of old max value
    if array.dtype in [data_types[d] for d in list(data_types.keys())] and not rescale:
        old_max = np.iinfo(array.dtype).max

    else:
        old_max = np.amax(array)

    old_limits = (old_min, old_max)
    new_array = corr._rescale_array(array, old_limits, new_limits)

    return new_array.astype(data_type)

# -------------------------
# Save a single frame image
def _save_frame(array, path):

    # Check the extension of the given file
    path = _check_extensions( [path] )[0]

    # Generate the image file
    io.imsave(path, array)

# ---------------------
# Save a whole sequence
def _save_stack(array, path):

    # Check the extension of the given file
    path = _check_extensions( [path], extensions=['.gif','.tif'] )[0]

    # Generate a .gif animation
    if os.path.splitext(path)[1] == '.gif':

        # Check that .gif are only saved in 8 bits
        if array.dtype != np.uint8:
            raise Exception('.gif animations can only be saved in 8 bits format.')

        im = [Image.fromarray(img) for img in array]
        im[0].save(path, save_all=True, append_images=im[1:])

    # Generate a .tif stack
    else:
        io.imsave(path, array)

# ----------------------------------
# Convert an array into a video file
def _convert_to_RGB(array):

    # Check the bit depth
    if array.dtype != np.uint8:
        array = _convert_bit_depth(array, bit_depth=8, rescale=True)

    # Add new channels
    if len(array.shape) != 4:
        arrays = [array for _ in range(3)]
        array = np.stack(arrays, axis=3)

    return array

# --------------------------------
# Save the array into a video file
def _save_video(path, array, fps=25, video_codec='libx264'):

    # Check the extension of the given file
    path = _check_extensions( [path], extensions=['.mp4'] )[0]

    # Get the informations from the array
    n,height,width,channels = array.shape

    # Initialize the process
    process = ffmpeg.input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height))
    process = ffmpeg.output(process, path, pix_fmt='yuv420p', vcodec=video_codec, r=fps)
    process = ffmpeg.overwrite_output(process)
    process = ffmpeg.run_async(process, pipe_stdin=True)

    # Save all the frames
    for frame in array:
        process.stdin.write( frame.tobytes() )

    # Terminate the process
    process.stdin.close()
    process.wait()

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ----------------------------------
# Load an image, a stack or a folder
def loadImage(path):

    # Check if it is a folder
    if os.path.isdir(path):
        imageArray = _open_folder(path)

    # Check if it is a file
    elif os.path.isfile(path):
        imageArray = _open_file(path)

    # Abort if the file is not recognized
    else:
        raise Exception('The input path is neither a file nor a directory.')

    # Return the appropriate object
    return imageArray

# ----------------------
# Save an image or stack
def saveImage(array, path, default=".tif", bit_depth=8, rescale=True):

    # Check the extension
    path = _add_extension(path, default=default)

    # Convert the type
    array = _convert_bit_depth(array, bit_depth=bit_depth, rescale=rescale)

    # Save a single frame
    if len(array.shape) == 2 or array.shape[0] == 1:
        _save_frame(array, path)

    # Save a stack or animation
    else:
        _save_stack(array, path)

# -------------------------
# Save the array as a video
def saveVideo(file_name, array, fps=25, video_codec='libx264'):

    # Convert the array to the correct format
    array = _convert_to_RGB(array)

    # Create the video
    _save_video(file_name, array, fps=fps, video_codec=video_codec)
