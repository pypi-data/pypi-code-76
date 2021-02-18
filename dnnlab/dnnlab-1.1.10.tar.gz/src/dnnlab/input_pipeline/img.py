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

Creates a tf.datset from tfrecords containing a single image in 1 example.
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
                   prefetching=True,
                   cache=True,
                   key="image_raw"):
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
        lambda example: _parse_tfrecords(example, height, width, depth, key),
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


def _parse_tfrecords(example, height, width, depth, key):
    # Create a dictionary describing the features.
    feature_description = {
        'height': tf.io.FixedLenFeature([], tf.int64, default_value=[-1]),
        'width': tf.io.FixedLenFeature([], tf.int64, default_value=[-1]),
        'depth': tf.io.FixedLenFeature([], tf.int64, default_value=[-1]),
        key: tf.io.FixedLenFeature([], tf.string, default_value=""),
    }

    # TODO Single example vs. batch example
    example = tf.io.parse_single_example(example, feature_description)
    #example = tf.io.parse_example(example, feature_description)
    img = example[key]
    # Convert encoded jpeg bytes into tensors.
    img = tf.image.decode_jpeg(img, channels=depth)
    img = tf.cast(img, tf.float32)
    # Normalize img.
    img = img / 255.

    img = tf.image.resize(img, (height, width))

    return img
