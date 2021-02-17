# Copyright 2019 Tobias Höfer
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
"""Utils API"""
import numpy as np

import tensorflow as tf


def create_dataset(tfrecords,
                   buffer_size,
                   num_parallel_reads,
                   height,
                   width,
                   depth,
                   grid_h,
                   grid_w,
                   anchors,
                   labels,
                   seed,
                   batch_size,
                   prefetching=True,
                   cache=True):
    """Creates an optimized tf.data.Dataset object from a tfrecords file.

    Optimization steps:
        - prefetching: Prefetching overlaps the preprocessing and model
        execution of a training step. While the model is executing training step
        s, the input pipeline is reading the data for step s+1. Doing so reduces
        the step time to the maximum (as opposed to the sum) of the training and
        the time it takes to extract the data.

        - parallelize the map transformation.

    Returns:
        tfrecords file
    """
    raw_dataset = tf.data.TFRecordDataset(
        tfrecords, buffer_size=None, num_parallel_reads=num_parallel_reads)

    # pre-processing function but apply it in parallel on multiple samples.
    parsed_dataset = raw_dataset.map(
        lambda example: _parse_tfrecords(example, height, width, depth, grid_h,
                                         grid_w, anchors, labels),
        num_parallel_calls=tf.data.experimental.AUTOTUNE)

    parsed_dataset = parsed_dataset.shuffle(buffer_size, seed=seed)
    parsed_dataset = parsed_dataset.batch(batch_size)
    # Prefetching
    if prefetching:
        parsed_dataset = parsed_dataset.prefetch(tf.data.experimental.AUTOTUNE)

    if cache:
        # Apply time consuming operations before cache.
        parsed_dataset = parsed_dataset.cache()
    return parsed_dataset


def _parse_tfrecords(example, height, width, depth, grid_h, grid_w, anchors,
                     labels):
    # Create a dictionary describing the features.
    feature_description = {
        'height':
        tf.io.FixedLenFeature([], tf.int64, default_value=[-1]),
        'width':
        tf.io.FixedLenFeature([], tf.int64, default_value=[-1]),
        'depth':
        tf.io.FixedLenFeature([], tf.int64, default_value=[-1]),
        'num_objs':
        tf.io.FixedLenFeature([], tf.int64, default_value=[-1]),
        'image_raw':
        tf.io.FixedLenFeature([], tf.string, default_value=""),
        'bbox_xmin':
        tf.io.FixedLenSequenceFeature([],
                                      tf.float32,
                                      allow_missing=True,
                                      default_value=-1.0),
        'bbox_xmax':
        tf.io.FixedLenSequenceFeature([],
                                      tf.float32,
                                      allow_missing=True,
                                      default_value=-1.0),
        'bbox_ymin':
        tf.io.FixedLenSequenceFeature([],
                                      tf.float32,
                                      allow_missing=True,
                                      default_value=-1.0),
        'bbox_ymax':
        tf.io.FixedLenSequenceFeature([],
                                      tf.float32,
                                      allow_missing=True,
                                      default_value=-1.0),
        'class':
        tf.io.FixedLenSequenceFeature([],
                                      tf.string,
                                      allow_missing=True,
                                      default_value=""),
        'class_ids':
        tf.io.FixedLenSequenceFeature([],
                                      tf.int64,
                                      allow_missing=True,
                                      default_value=-1)
    }

    # TODO Single example vs. batch example
    example = tf.io.parse_single_example(example, feature_description)
    #example = tf.io.parse_example(example, feature_description)
    img = example["image_raw"]
    # Convert encoded jpeg bytes into tensors.
    img = tf.image.decode_jpeg(img, channels=depth)
    img = tf.cast(img, tf.float32)
    # Normalize img.
    img = img / 255.

    # Exract bounding box coordinates.
    bbox_xmin = example["bbox_xmin"]
    bbox_ymin = example["bbox_ymin"]
    bbox_xmax = example["bbox_xmax"]
    bbox_ymax = example["bbox_ymax"]

    bbox_xmin_xmax = tf.stack([bbox_xmin, bbox_xmax])
    bbox_ymin_ymax = tf.stack([bbox_ymin, bbox_ymax])
    coords = tf.stack([bbox_xmin_xmax, bbox_ymin_ymax])
    coords = tf.cast(coords, dtype=tf.float32)

    # Resize img and bb_coords accordingly.
    img, coords = _resize(img, coords, height, width)

    # Rescale to yolo grid & center coordinates
    coords = _rescale(coords, height, width, grid_h, grid_w)

    # Extract class idxs.
    classes = example["class"]
    num_objs = example["num_objs"]

    # Build label tensor use tf.py_function to use arbitrary python logic.
    #label = _build_tensor(coords, classes, grid_h, grid_w, anchors, class_idx, num_objs)
    label = tf.py_function(
        func=_build_yolo_label,
        inp=[grid_h, grid_w, anchors, coords, classes, labels, num_objs],
        Tout=tf.float32)

    return img, label


def _resize(img, coords, height, width):
    # x = x*w / W
    # y = y*h / H
    # Img
    old_height = tf.cast(tf.shape(img)[0], dtype=tf.float32)
    old_width = tf.cast(tf.shape(img)[1], dtype=tf.float32)

    img = tf.image.resize(img, (height, width))

    # Label
    x_coords = coords[0] * width / old_width
    x_coords = tf.math.maximum(tf.math.minimum(x_coords, width), 0)

    y_coords = coords[1] * height / old_height
    y_coords = tf.math.maximum(tf.math.minimum(y_coords, height), 0)

    coords = tf.stack([x_coords, y_coords])

    return img, coords


def _rescale(coords, height, width, grid_h, grid_w):
    # output label [x_center, y_center, w_center, h_center]
    x_mins = coords[0][0]
    x_maxs = coords[0][1]

    y_mins = coords[1][0]
    y_maxs = coords[1][1]

    x_center = 0.5 * (x_mins + x_maxs)
    x_center = x_center / (width / grid_w)

    y_center = 0.5 * (y_mins + y_maxs)
    y_center = y_center / (height / grid_h)

    w_center = (x_maxs - x_mins) / (width / grid_w)
    h_center = (y_maxs - y_mins) / (height / grid_h)

    coords = tf.stack([x_center, y_center, w_center, h_center])
    return coords


def _find_best_anchor(center_w, center_h, anchors, n_anchors):
    """The bounding boxes are often defined by 4 parameters:
    (xmin,ymin, width, height). When we calculate IoU between two bounding
    boxes, all we care is their width and height. The coordinates of a bounding
    box, xmin and ymin, are not of concern as we want to only compare the shapes
    of the bounding boxes. In otherwords, we can think that the xmin and ymin
    are shared by the two objects. Think of it as botch boxes share the same
    top-left corner.
    """
    # Holds IoU scores between the true label box and every prior anchor box.
    iou_scores = []
    # Get every second item, starting with index 0.
    anchor_widths = anchors[0::2]
    # Get every second item, starting with index 1.
    anchor_heights = anchors[1::2]
    for anchor in range(n_anchors):
        # Calculate width - intersection
        intersect_w = min(float(center_w), float(anchor_widths[anchor]))
        # Calculate height - intersection
        intersect_h = min(float(center_h), float(anchor_heights[anchor]))
        # Calculate area - intersection
        intersect_area = intersect_w * intersect_h
        union = float(
            center_w *
            center_h) + anchor_widths[anchor] * anchor_heights[anchor]
        iou_scores.append(intersect_area / union)

    # Index of best fit anchor box.
    max_iou_anchor_box = iou_scores.index(max(iou_scores))
    return max_iou_anchor_box


def _build_yolo_label(grid_h, grid_w, anchors, coords, classes, labels,
                      num_objs):
    n_anchors = int(len(anchors) / 2)
    yolo_label = np.zeros(
        [int(grid_h),
         int(grid_w), n_anchors, 5 + int(len(labels))])

    for obj in range(int(num_objs)):
        center_x = coords[0][obj]
        center_y = coords[1][obj]
        center_w = coords[2][obj]
        center_h = coords[3][obj]

        # Object midpoint is in cell (grid_x, grid_y).
        grid_x = int(np.floor(center_x))
        grid_y = int(np.floor(center_y))
        best_anchor = _find_best_anchor(center_w, center_h, anchors, n_anchors)
        # Box.
        yolo_label[grid_y, grid_x, best_anchor, 0:4] = [
            center_x, center_y, center_w, center_h
        ]
        # Set confidence to 1.
        yolo_label[grid_y, grid_x, best_anchor, 4:5] = 1
        # Class label to 1.
        class_idx = np.where(np.array(labels) == classes[obj])[0]
        yolo_label[grid_y, grid_x, best_anchor, 5 + class_idx] = 1

    return yolo_label
