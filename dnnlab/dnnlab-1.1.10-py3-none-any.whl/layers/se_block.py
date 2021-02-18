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
"""SE Block as a new architectural unit with the goal of improving the quality
of representations produced by a network by explicitly modelling the
interdependencies between the channels of its convolutional features. To this
end, SE Blocks introduce a mechanism that allows the network to perform feature
recalibration, through which it can learn to use global information to
selectively emphasise informative features and suppress less useful ones.

Paper: https://arxiv.org/pdf/1709.01507.pdf
"""
import tensorflow as tf


class SEBlock(tf.keras.layers.Layer):
    """Squeeze-and-Excitation Block."""
    def __init__(self, reduction_ratio=16):
        super(SEBlock, self).__init__()
        self.reduction_ratio = reduction_ratio

    def build(self, input_shape):
        self.filter_size = input_shape[3]
        self.se_shape = (1, 1, self.filter_size)
        self.dense_1 = tf.keras.layers.Dense(self.filter_size /
                                             self.reduction_ratio,
                                             activation="relu",
                                             use_bias=False)
        self.dense_2 = tf.keras.layers.Dense(self.filter_size,
                                             activation="sigmoid",
                                             use_bias=False)

    def call(self, input):
        net = input
        # Squeeze
        net = tf.keras.layers.GlobalAveragePooling2D()(net)
        net = tf.keras.layers.Reshape(self.se_shape)(net)
        # Excitaiton
        net = self.dense_1(net)
        net = self.dense_2(net)
        return tf.keras.layers.multiply([net, input])
