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
"""Image Input Pipeline API.

TODO example name as key parameters.
Creates a tf.datset from tfrecords containing two images.
"""
import tensorflow as tf


def create_dataset(tfrecords,
                   buffer_size,
                   num_parallel_reads,
                   height,
                   width,
                   depth,
                   seed,
                   batch_size,
                   keys,
                   encoding=True,
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
    if encoding:
        parsed_dataset = raw_dataset.map(
            lambda example: _parse_tfrecords_encoded(example, height, width,
                                                     depth, keys),
            num_parallel_calls=tf.data.experimental.AUTOTUNE)
    else:
        parsed_dataset = raw_dataset.map(
            lambda example: _parse_tfrecords_raw(example, height, width, depth,
                                                 keys),
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


def _parse_tfrecords_encoded(example, height, width, depth, keys):
    # Create a dictionary describing the features.
    feature_description = {
        keys[0]: tf.io.FixedLenFeature([], tf.string, default_value=""),
        keys[1]: tf.io.FixedLenFeature([], tf.string, default_value="")
    }

    # TODO Single example vs. batch example
    example = tf.io.parse_single_example(example, feature_description)
    img_source = example[keys[0]]
    # Convert encoded jpeg bytes into tensors.
    img_source = tf.image.decode_jpeg(img_source, channels=depth)
    img_source = tf.cast(img_source, tf.float32)
    # Normalize img.
    if tf.math.reduce_max(img_source) > 1.0:
        img_source = img_source / 255.
    img_source = tf.image.resize(img_source, (height, width))

    img_target = example[keys[1]]
    # Convert encoded jpeg bytes into tensors.
    img_target = tf.image.decode_jpeg(img_target, channels=depth)
    img_target = tf.cast(img_target, tf.float32)
    # Normalize img.
    img_target = img_target / 255.

    img_target = tf.image.resize(img_target, (height, width))

    return img_source, img_target


def _parse_tfrecords_raw(example, height, width, depth, keys):
    # Create a dictionary describing the features.
    feature_description = {
        keys[0]: tf.io.FixedLenFeature([], tf.string, default_value=""),
        keys[1]: tf.io.FixedLenFeature([], tf.string, default_value=""),
        "height": tf.io.FixedLenFeature([], tf.int64),
        "width": tf.io.FixedLenFeature([], tf.int64),
        "depth": tf.io.FixedLenFeature([], tf.int64, default_value=[1])
    }

    # TODO Single example vs. batch example
    example = tf.io.parse_single_example(example, feature_description)

    # Get imgs as raw bytes.
    img_source = example[keys[0]]
    img_target = example[keys[1]]

    # Decode raw bytes to numbers.
    img_source = tf.io.decode_raw(img_source, tf.uint8)
    img_source = tf.cast(img_source, tf.float32)

    img_target = tf.io.decode_raw(img_target, tf.uint8)
    img_target = tf.cast(img_target, tf.float32)

    # Restore spatial resolution of images.
    height_orig = tf.cast(example['height'], tf.int32)
    width_orig = tf.cast(example['width'], tf.int32)
    # Defaults to grayscale if feature is missing in example. Doesnt work TODO
    # depth = tf.cast(example['depth'], tf.int32)
    depth_orig = 1

    image_shape = tf.stack([height_orig, width_orig, depth_orig])
    label_shape = tf.stack([height_orig, width_orig, depth_orig])

    img_source = tf.reshape(img_source, image_shape)
    img_target = tf.reshape(img_target, label_shape)

    img_source = tf.cast(img_source, tf.float32)
    img_target = tf.cast(img_target, tf.float32)

    # Normalize images.
    if tf.math.reduce_max(img_source) > 1.0:
        img_source = img_source / 255.

    if tf.math.reduce_max(img_target) > 1.0:
        img_target = img_target / 255.

    # Rescale images.
    img_source = tf.image.resize(img_source, (height, width))
    img_target = tf.image.resize(img_target, (height, width))

    return img_source, img_target
