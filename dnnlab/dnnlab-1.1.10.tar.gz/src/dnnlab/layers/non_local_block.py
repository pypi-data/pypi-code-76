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
"""Both convolutional and recurrent operations are building blocks that process
one local neighborhood at a time. In this paper, we present non-local operations
as a generic family of building blocks for capturing long-range dependencies.
Inspired by the classical non-local means method in computer vision,
our non-local operation computes the response at a position as a weighted sum of
the features at all positions. This building block can be plugged into many
computer vision architectures.

Paper: https://arxiv.org/abs/1711.07971, https://arxiv.org/abs/1805.08318
TODO(visualize attention maps)
"""

import tensorflow as tf


class NonLocalBlock(tf.keras.layers.Layer):
    """The non-local behavior is due to the fact that all postions are
    considered in the operation. As a comparison, a convolutional operation sums
    up the weighted input in a local neighborhood. The non-local operation is
    also different from a fully connected layer. This block computes responses
    based on relationships between different locations, whereas a fully
    connected layer uses learned weights. Furtheremore it allows variable input
    sizes and maintains the corresponding size in the output. A non-local
    builidng block can be used together with convolutional/recurrent layers.
    It can be added into the earlier part of deep neural networks, unlike fully
    connected layers that are often used in the end to decrease the number of
    parameters and increase numerical performance. This allows us to build a
    richer hierarchy that combines both non-local and local information."""
    def __init__(self, reduction_ratio=8, visualize_attention_map=False):
        super(NonLocalBlock, self).__init__()
        self.reduction_ratio = reduction_ratio
        self.visualize_attention_map = visualize_attention_map
        # Scale parameter which is multiplied to attention map.

    def get_config(self):
        config = super().get_config().copy()
        config.update({
            'reduction_ratio': self.reduction_ratio,
            'visualize_attention_map': self.visualize_attention_map,
        })
        return config

    def build(self, input_shape):
        self.gamma = self.add_weight(self.name + '_gamma',
                                     shape=(),
                                     initializer=tf.initializers.Zeros)
        self.filter_size = input_shape[3]

        self.f = tf.keras.layers.Conv2D(filters=self.filter_size /
                                        self.reduction_ratio,
                                        kernel_size=(1, 1),
                                        strides=(1, 1),
                                        use_bias=False)
        self.g = tf.keras.layers.Conv2D(filters=self.filter_size /
                                        self.reduction_ratio,
                                        kernel_size=(1, 1),
                                        strides=(1, 1),
                                        use_bias=False)
        self.h = tf.keras.layers.Conv2D(filters=self.filter_size /
                                        self.reduction_ratio,
                                        kernel_size=(1, 1),
                                        strides=(1, 1),
                                        use_bias=False)
        self.v = tf.keras.layers.Conv2D(filters=self.filter_size,
                                        kernel_size=(1, 1),
                                        strides=(1, 1),
                                        use_bias=False)

    def call(self, input):
        """For simplicity, f & g & h are linear embeddings (1x1 convolutions
        with linear activations). The main difference between the dot product
        and embedded Gaussian is the presence of softmax, which plays the role
        of an activation function."""
        # C = Channels; C´= C/reduction_ratio; N = Width * Height
        # Query: 1x1 conv to transform x to feature space f.
        query = self.f(input)  # [bs, h, w, c']
        # Key:  1x1 conv to transform x to feature space g.
        key = self.g(input)  # [bs, h, w, c']
        # Value: 1x1 conv to transform x to feature space h.
        value = self.h(input)  # [bs, h, w, c']

        # Score function for feature similarity (dot product).
        beta = tf.matmul(self._hw_flatten(key),
                         self._hw_flatten(query),
                         transpose_b=True)  # [bs, N, N]
        # Softmax activation.
        beta = tf.nn.softmax(beta)  # [bs, N, N]

        # Multiply activation to value feature maps.
        o = tf.matmul(beta, self._hw_flatten(value))  # [bs, N, c']
        o = tf.reshape(o, shape=tf.shape(value))  # [bs, h, w, c']
        # Use last 1x1 convolution to increase channels to match input.
        o = self.v(o)  # [bs, h, w, c]

        # In addition, we further multiply the output of the attention layer by
        # a scale parameter and add back the input feature map.
        y = self.gamma * o + input

        return y

    @staticmethod
    def _hw_flatten(x):
        # Flattens H*W
        return tf.reshape(x,
                          shape=[
                              tf.shape(x)[0],
                              tf.shape(x)[1] * tf.shape(x)[2],
                              tf.shape(x)[3]
                          ])
