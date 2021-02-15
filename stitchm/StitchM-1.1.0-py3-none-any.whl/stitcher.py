import numpy as np
import logging

from .edge_definer import image_edge_definer
from .image_normaliser import exposure_correct, normalise_to_datatype, cast_to_dtype


class Stitcher():

    def __init__(self, datatype="uint16"):
        '''Default datatype="uint16"'''
        self.dtype = np.dtype(datatype)
        self.brightfield_list = []

    def make_mosaic(self, unstitched, filter=True, normalise=True):
        logging.info("Creating mosaic")
        if unstitched.img_count == unstitched.images.shape[0]:
            if filter:
                self.brightfield_list = self._find_brightfield_images(unstitched.img_count, unstitched.exposure_minmax)
            else:
                self.brightfield_list = [i for i in range(unstitched.img_count)]
            # create new large array and load data into it from mosaic:
            mosaic_size = (unstitched.boundaries[1, 0] - unstitched.boundaries[0, 0],
                         unstitched.boundaries[1, 1] - unstitched.boundaries[0, 1])
            
            # If we are not normalising, fill with zero values rather than max
            fill_value = np.iinfo(self.dtype).max * normalise
            mosaic_array = np.full(mosaic_size, fill_value, dtype=self.dtype)
            
            if normalise:
                # Apply exposure correction
                images = exposure_correct(unstitched.images, unstitched.exposure_minmax, self.brightfield_list)
            else:
                # Filter out unwanted images
                images = unstitched.images[self.brightfield_list]
            
            # Convert to numpy array
            images = np.asarray(unstitched.images[self.brightfield_list])

            if normalise:
                # Rescale max/min to fit data type
                images = normalise_to_datatype(images, self.dtype, trim=True)
            
            # Cast to output data type
            preprocessed_images = cast_to_dtype(images, self.dtype)

            for i in range(len(self.brightfield_list)):
                start, end = image_edge_definer(
                    unstitched.pix_positionlist[self.brightfield_list[i], :],
                    unstitched.boundaries,
                    unstitched.pix2edge
                    )
                # Array needs to be transposed for python versus dv.
                # This rotates each image so they line up correctly
                mosaic_array[start[0]:end[0], start[1]:end[1]] = preprocessed_images[i, :, :].T
            # Rotate back and flip
            return np.flip(mosaic_array.T, 0)
        else:
            logging.error("Number of images doesn't match between files")
            raise AssertionError("Number of images doesn't match between files")

    def get_brightfield_list(self):
        return self.brightfield_list

    @staticmethod
    def _find_brightfield_images(img_count, minmax):
        # This returns a list of "good" images i.e. not fluorescent images
        # This is based on the min/max values of fluorescent images being
        # significantly lower than the std deviation of all the images.
        # This will fail if there are too many fl images to bf images.
        median_max = np.median(minmax[:, 1])
        std_max = np.std(minmax[:, 1])
        image_list = []
        for i in range(img_count):
            if minmax[i, 1] > median_max - std_max:
                image_list.append(i)
            else:
                logging.info("Median of image %i (counted from 0) is not within the minimum threshold", i)
        if len(image_list) > img_count / 2:
            return image_list
        return range(0, img_count)
