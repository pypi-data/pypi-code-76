import numpy as np
import logging


def _image_value_trimmer(image_stack):
    logging.info("Trimming brightest pixels")
    new_stack = image_stack[:, :, :]
    median_std = np.median([np.std(image) for image in image_stack])
    median_median = np.median(image_stack)
    new_max = median_median + 2.5 * median_std
    return np.clip(new_stack, 0, new_max)


def exposure_correct(images, exposure_minmax, brightfield_image_list):
    """
    Cockpit saves some exposure min/max data which they use to
    correct exposure when displaying it. This function uses this
    to correct for the exposure.
    """
    logging.info("Applying exposure correction")
    images_min = images[brightfield_image_list].min()
    images_max = images[brightfield_image_list].max()
    images_range = images_max - images_min
    corrected_images = []
    for i in brightfield_image_list:
        exp_min = exposure_minmax[i, 0]
        exp_max = exposure_minmax[i, 1]
        exp_range = exp_max - exp_min

        normalisation_coefficient = images_range / exp_range

        unbiased_img = (images[i, :, :] - exp_min) * normalisation_coefficient
        corrected_images.append(unbiased_img)
    return corrected_images


def normalise_to_datatype(corrected_images, datatype, trim=True):
    logging.info("Re-scaling images to %s", datatype)
    # Trim images before correction to avoid any speckles
    # leading to the entire image to be quite dark:
    if trim: corrected_images = _image_value_trimmer(corrected_images)

    corrected_images = np.asarray(corrected_images).astype('f')  # Convert to float for rescaling
    # Move minimum value of all corrected images to 0:
    corrected_min = corrected_images.min()
    corrected_images -= corrected_min
    # Convert values to float and rescale so the maximum
    # is set by datatype:
    corrected_max = corrected_images.max()
    # New max should be 1 less than the max allowed by datatype
    # so that the background (max) can be made transparent without losing data
    new_max = (np.iinfo(datatype).max - 1)
    rescaled_images = corrected_images * (new_max / corrected_max)
    
    return rescaled_images

def cast_to_dtype(image, data_type):
    try:
        dtype = np.dtype(data_type)
        if np.issubdtype(dtype, np.integer) and np.issubdtype(image.dtype, np.floating):
            dtype_info = np.iinfo(dtype)
            # Round min/max to avoid this warning when the issue is just going to be rounded away.
            img_min, img_max = round(image.min()), round(image.max())
            if dtype_info.min > img_min:
                logging.warning(
                    "Image min %f below %s minimum of %i, values below this will be cut off",
                    img_min, dtype, dtype_info.min)
                _conditional_replace(image, dtype_info.min, lambda x: x < dtype_info.min)
            if dtype_info.max < img_max:
                logging.warning(
                    "Image max %f above %s maximum of %i, values above this will be cut off",
                    img_max, dtype, dtype_info.max)
                _conditional_replace(image, dtype_info.max, lambda x: x > dtype_info.max)
        return np.around(image, decimals=0).astype(dtype)
    except Exception:
        logging.error("Invalid data type given: %s aka %s. Saving with default data type.", data_type, dtype)
    return image

def _conditional_replace(array, replacement, condition_func):
    array[condition_func(array)] = replacement
