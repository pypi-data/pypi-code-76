""" Tool "imgaug" is used for data/image augmentation
see https://imgaug.readthedocs.io/en/latest/source/installation.html for reference

API: https://imgaug.readthedocs.io/en/latest/source/api_imgaug.html

Install:
Prerequisites: 
- pip install opencv-python-headless --upgrade
- pip install opencv-contrib-python-headless --upgrade

- Conda
    - conda config --add channels conda-forge
    - conda install imgaug
    - pip install imagecorruptions
- Pip
    - pip install imgaug
    - pip install imagecorruptions
"""

from imgaug import augmenters as iaa
import imgaug as ia
import numpy as np
import tensorflow as tf


class YoloAugmentation:
    """ Example usage of YoloAugmentation

    1) create YoloAugmentation object
    ya = dnnlab.input_pipeline.data_augmentation.YoloAugmentation(img_width=WIDTH, img_height=HEIGHT, grid_w=GRID_W, grid_h=GRID_H)

    2) create list of wanted augmentations. You can choose betwenn rotate, shift in x direction, shift in y direction
       every augmentation needs a pair of 2 values in a shape 
       (max negative value, max positive value) from which the values for each augmentation step are randomly selected
    aug_list = [("rotate", (-10,10)), ("shiftx", (-20, 20)), ("shifty", (-20, 20))]

    3) setup augmentation operations with augmentation list
    ya.setup(aug_list)

    4) augment dataset 
    training_data = ya.augment_data(training_data, batch_size=BATCH_SIZE, increase_dataset=False, buffer_size=BUFFER_SIZE, seed=SEED,
                                        prefetching=True, cache=True)
    """
    def __init__(self, img_width, img_height, grid_w, grid_h):
        """ YoloAugmentation class.

        Args:
            img_width (int): width of images
            img_height (int): width of images
            grid_w (int): number of grids in x direction
            grid_h (int): number of grids in y direction
        """
        self.img_width = img_width
        self.img_height = img_height
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.augmenters = iaa.OneOf([])  # imgaug.augmenters.meta

        self.factor_h = self.img_height / self.grid_h
        self.factor_w = self.img_width / self.grid_w

    def convert_to_imgaug_bboxes(self, labels):
        """ convert yolo bboxes to imgaug bboxes

        Args:
            labels (np.array): labels array with x_center, y_center, w_center, h_center, objectiveness, classes
        
        Returns:
            augmentation_bboxes (imgaug.bboxes): converted bboxes
            aug_indecs (list): inidices list of converted boxes
        """
        # labes: (BS,GRID,GRID,ANCHORS,(x,y,w,h,objectivness,n_classes))
        # x_center, y_center, w_center, h_center
        batches, gh, gw, anchors, boxes = labels.shape

        augmentation_bboxes = []
        aug_indices = []
        for b in range(batches):
            boxes = []
            batch_indices = []
            for h in range(gh):
                for w in range(gw):
                    for a in range(anchors):
                        if labels[
                                b, h, w, a,
                                4] == 1:  # if objectiveness is 1, then it's a label/bbox
                            box = labels[
                                b, h, w, a, 0:
                                4]  # x_center, y_center, w_center, h_center

                            x1, y1, x2, y2 = self.inverse_rescale(box)

                            bbox = ia.BoundingBox(x1=x1, y1=y1, x2=x2, y2=y2)
                            boxes.append(bbox)
                            batch_indices.append((b, h, w, a))
            augmentation_bboxes.append(boxes)
            aug_indices.append(batch_indices)
        return augmentation_bboxes, aug_indices

    def convert_to_yolo_bboxes(self, boxes, indices, labels):
        """ convert imgaug bboxes to yolo bboxes

        Args:
            boxes (list(imgaug bboxes)): converted  imgaug bboxes
            indices (list): inidices list of converted boxes
            labels (np.array): array of origin yolo labels/bboxes
        
        Returns:
            labels (np.array): array of origin yolo labels/bboxes with augmented values
        """

        for batch_boxes, batch_indices, batch_labels in zip(
                boxes, indices, labels):
            for img_boxes, img_indices in zip(batch_boxes, batch_indices):

                # convert x_min, y_min, x_max, y_min to center_x, center_y, center_width, center_height
                # Imgaug BBoxes have built in attributes/methods for this
                center_x = img_boxes.center_x / self.factor_w
                center_y = img_boxes.center_y / self.factor_h
                width = img_boxes.width / self.factor_w
                height = img_boxes.height / self.factor_h

                b, h, w, a = img_indices[0], img_indices[1], img_indices[
                    2], img_indices[3]

                # assing center x, y, width, height to labels
                labels[b, h, w, a, 0] = center_x
                labels[b, h, w, a, 1] = center_y
                labels[b, h, w, a, 2] = width
                labels[b, h, w, a, 3] = height

        return labels

    def inverse_rescale(self, box):
        """inverse function of input_pipeline.yolo's rescale method
        Convert x_center, y_center, w_center, h_center back to x_min, y_min, x_max, y_max.
        This is needed to setup Imaug Bboxes for augmentation.

        Args:
            box (np.array): yolo bounding box coordinates
        
        Returns:
            x_min (float): 
            y_min (float):
            x_max (float):
            y_max (float):
        """
        # code inverse function of _rescale from yolo-input pipeline to
        # get correct coordinates and not grid specific values

        # rescale center coords
        x_center = box[0] * self.factor_w
        y_center = box[1] * self.factor_h
        w_center = box[2] * self.factor_w
        h_center = box[3] * self.factor_h

        # recalculate x's and y's coordinates
        x_min = x_center - 0.5 * w_center
        x_max = 2 * x_center - x_min

        y_min = y_center - 0.5 * h_center
        y_max = 2 * y_center - y_min

        return x_min, y_min, x_max, y_max

    def add_rotation(self, angles):
        """ add Rotation Augmentation operation to list of augmenters

        Args:
            angles (pair): pair of max negative angle and max positive angle
        """
        rot_op = iaa.Rotate(angles)
        self.augmenters.add(rot_op)

    def add_shift_x(self, pixels):
        """ add Shift-X Augmentation operation to list of augmenters

        Args:
            angles (pair): pair of max negative pixel and max positive pixel
        """
        shift_op = iaa.TranslateX(px=pixels)
        self.augmenters.add(shift_op)

    def add_shift_y(self, pixels):
        """ add Shift-Y Augmentation operation to list of augmenters

        Args:
            angles (pair): pair of max negative pixel and max positive pixel
        """
        shift_op = iaa.TranslateY(px=pixels)
        self.augmenters.add(shift_op)

    def setup(self, op_pairs):
        """ setup choosen augmentation operations with parameters.

        Args:
            op_pairs [(op_name (string), op_values (int, int)), (op_name (string), op_values (int, int))]
        """
        if op_pairs is None:
            self.augmenters.add(iaa.Identity())
        else:
            for op in op_pairs:
                name = op[0]
                values = op[1]

                if name == "rotate":
                    self.add_rotation(angles=values)
                if name == "shiftx":
                    self.add_shift_x(pixels=values)
                if name == "shifty":
                    self.add_shift_y(pixels=values)

    def augment_data(self,
                     dataset,
                     buffer_size,
                     seed,
                     batch_size,
                     increase_dataset=False,
                     prefetching=True,
                     cache=True):
        """ perform augmetation on a dataset

        Args:
            dataset (tf.dataset): tf.Dataset with shape(None, width, height, depth)
            buffer_size (int): representing the maximum number of elements that will be buffered when prefetching.
            seed (int): representing the random seed that will be used to create the distribution
            batch_size (int): batch size
            increase_dataset (bool): determine if origin dataset and augmented dataset are concatenated
            prefetching (bool): determine if prefetching is On or Off
            cache (bool): determine if cache is On or Off
        """

        i = 0 # index for stacking augmented images and labels
        for elements in dataset:
            images = elements[0].numpy()
            labels = elements[1].numpy()

            bboxes, indices = self.convert_to_imgaug_bboxes(labels)
            aug_imgs, aug_bboxes = self.augmenters(images=images,
                                            bounding_boxes=bboxes)
            aug_labels = self.convert_to_yolo_bboxes(aug_bboxes, indices, labels)

            if i==0: # first iteration to init array stack
                stacked_aug_imgs = aug_imgs 
                stacked_aug_labels =  aug_labels
            else: # after first itreation stack (in batch dimension) aug_imgs and aug_labels
                stacked_aug_imgs = np.vstack((stacked_aug_imgs, aug_imgs))
                stacked_aug_labels = np.vstack((stacked_aug_labels, aug_labels))

            i+=1 # update index

        # create tf.data.Dataset from numpy-arrays
        aug_dataset = tf.data.Dataset.from_tensor_slices((stacked_aug_imgs, stacked_aug_labels))
        aug_dataset = aug_dataset.batch(batch_size)

        # concat origin dataset and augmented dataset if increase_dataset=True
        # else just use aug_dataset
        if increase_dataset:
            result_dataset = dataset.concatenate(aug_dataset)
        else:
            result_dataset = aug_dataset

        result_dataset = result_dataset.shuffle(buffer_size, seed=seed)

        # Prefetching
        if prefetching:
            result_dataset = result_dataset.prefetch(
                tf.data.experimental.AUTOTUNE)
        # Cache
        if cache:
            # Apply time consuming operations before cache.
            result_dataset = result_dataset.cache()

        return result_dataset
