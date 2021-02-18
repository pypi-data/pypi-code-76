# Copyright 2019 Kevin Hirschmann
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
# ==============================================================================

import tensorflow as tf
import cv2
import matplotlib.pyplot as plt


def construct_mined_triplets(inputs, ap_indices, an_indices):
    """
    Construct the mined triplets which are used for (Online) TripletLoss.

    Args:
        inputs (tf.tensor): inputs of the original TripletNet
        ap_indices (tf.tensor): indices [batch_size, 2] of anchor-positive pairs of mined triplets (will be set during training of TripletNet)
        an_indices (tf.tensor): indices [batch_size, 2] of anchor-negative pairs of mined triplets (will be set during training of TripletNet)

    Returns:
        selected_triplets (tf.tensor): 5D-tensor [batch_size, 3, h, w, c] containing each mined/selected triplet 
    """
    b, h, w, c = inputs.shape

    selected_triplets = tf.TensorArray(tf.float32, size=b)

    for i in range(inputs.shape[0]):
        triplet_ta = tf.TensorArray(
            tf.float32, size=3)  # tf.TensorArray for a single triplet

        anchor_index = ap_indices[i][0]
        pos_index = ap_indices[i][1]
        neg_index = an_indices[i][1]

        anchor = inputs[anchor_index]
        positive = inputs[pos_index]
        negative = inputs[neg_index]

        # Workaround for: tf.EagerTensor object does not support item assignment
        # use tf.TensorArray and tf.stack to fake correct tensor assignment
        triplet_ta = triplet_ta.write(0, anchor)
        triplet_ta = triplet_ta.write(1, positive)
        triplet_ta = triplet_ta.write(2, negative)

        triplet_ta = triplet_ta.stack(
        )  # stack array, result is a tensor [3, h, w, c]

        # add current Triplet to selected Triplet TensorArray
        selected_triplets = selected_triplets.write(i, triplet_ta)

    selected_triplets = selected_triplets.stack(
    )  # stack array, result is a tensor [batch_size, 3, h, w, c]

    return selected_triplets


def create_heatmap(image):
    """create heatmap of the activations of an image.

    Args:
        image (tf.tensor): tensor of a single image

    Return:
        heatmap (tf.tensor): heatmap of image activation
    """
    normalized = image / tf.reduce_max(image)
    normalized = tf.maximum(normalized, 0)

    # apply cv2 Color Map - cv2.COLORMAP_JET
    normalized = normalized * (1.0 - normalized)
    normalized = tf.cast(normalized, dtype=tf.uint8)

    heatmap = cv2.applyColorMap(normalized.numpy(), cv2.COLORMAP_JET)

    return tf.convert_to_tensor(heatmap)


def combine_heatmap_image(image, heatmap):
    """combine image and heatmap of image activations.

    Args:
        image (tf.tensor): tensor of the image
        heatmaps (tf.tensor): tensor of the image activation of an convolutional layer

    Returns:
        heatmap_image (tf.tensor): image with overlayed heatmap
    """
    heatmap_image = image * 0.7 + heatmap / 255 * 0.3
    return heatmap_image