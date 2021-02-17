# Copyright 2020 Tobias Höfer
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
"""Implements  a morphological layer that learns the rank of a rank filter operation."""
import numpy as np
import tensorflow as tf


class Morph2D(tf.keras.layers.Layer):
    """Encapsulates both a state (weights) and a transformation from inputs to
    outputs."""
    def __init__(self, filters=1, **kwargs):
        """Define state and do all input-independent initualization.

        Args:
            se (tensor): Structuring element. Defaults to np.ones((3,3)).
        """
        super(Morph2D, self).__init__(name="")
        self.filters = filters

    def get_config(self):
        """Defines state to enable model_load()."""
        config = super().get_config().copy()
        config.update({
            "filters": self.filters,
            "se": self.se,
            "se_size": self.se_size,
            "rank": self.ranks
        })
        return config

    def compute_output_shape(self, input_shape):
        """This transformation ."""
        return [input_shape[0], input_shape[1], input_shape[2], self.filters]

    def build(self, input_shape):
        # SE: [se_height, se_width, in_channels, out_channels]
        self.se = tf.ones([3, 3, input_shape[-1], self.filters],
                          dtype=tf.float32)
        self.se_size = self.se.get_shape()
        self.se_h = self.se_size[0]
        self.se_w = self.se_size[1]
        self.se_in_ch = self.se_size[2]
        self.se_out_ch = self.se_size[3]

        #rank_init = tf.random_uniform_initializer()
        rank_init = tf.random_normal_initializer()
        # Define rank vector as learnable weight.
        self.ranks = tf.Variable(initial_value=rank_init(shape=(
            self.filters,
            self.se_w * self.se_h * self.se_in_ch,
        ),
                                                         dtype="float32"),
                                 trainable=True,
                                 name="rank")
        #self.alpha = tf.Variable(initial_value=rank_init(shape=(
        #                        self.filters, 1),
        #                        dtype="float32"),
        #                        trainable=True,
        #                        name="alpha")

    def call(self, inputs):
        """Define transformation from inputs to outputs."""
        inputs = tf.cast(inputs, tf.float32)
        batch_dim = tf.shape(inputs)[0]
        img_h = tf.shape(inputs)[1]
        img_w = tf.shape(inputs)[2]
        #img_h = inputs.shape[1]
        #img_w = inputs.shape[2]
        #print(img_h)

        # Returns a 4-D Tensor of the same type as the input. Extracted batches
        # are stacked in the last dimension.
        image_patches = tf.image.extract_patches(
            inputs,
            sizes=[1, self.se_h, self.se_w, 1],
            strides=[1, 1, 1, 1],
            rates=[1, 1, 1, 1],
            padding="SAME")
        # Reshape patches to vectors.
        shape = tf.convert_to_tensor([
            batch_dim, 1, img_h * img_w, self.se_h * self.se_w * self.se_in_ch
        ])
        image_patches = tf.reshape(image_patches, shape)

        # Reshape structuring element to vector.
        se = tf.reshape(
            self.se,
            [1, 1, self.se_h * self.se_w * self.se_in_ch, self.se_out_ch])
        se = tf.transpose(se, [0, 3, 1, 2])
        se = tf.tile(se, [batch_dim, 1, 1, 1])

        # Process structuring element with patches.
        mul_1 = tf.multiply(image_patches, se)

        # Non-linear sort operation of processed patches.
        sorted_list = tf.sort(mul_1, axis=-1, direction="ASCENDING")

        # Transform rank vector to probabilities.
        ranks = tf.nn.softmax(self.ranks)
        # beta params
        #ranks = tf.exp(self.beta*self.ranks[filter])
        # / tf.reduce_sum(tf.exp(self.beta*self.ranks[filter]),axis=-1)

        # Multiply rank probabilities with sorted list. Only element at given
        # rank is active.
        mul_2 = tf.multiply(sorted_list, ranks)

        # Compute sum over rank * SL(se * patch).
        result = tf.reduce_sum(sorted_list, 3)

        # Reshape results
        result = tf.reshape(
            result,
            [batch_dim, inputs.shape[1], inputs.shape[1], self.se_out_ch])

        return result
