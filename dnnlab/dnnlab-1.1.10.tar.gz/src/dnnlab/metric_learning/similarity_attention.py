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
"""
Similarity Attention for Triplet Network.
For a detailed explanation see: Learning Similarity Attention - https://arxiv.org/pdf/1911.07381.pdf
"""

import tensorflow as tf
import matplotlib.pyplot as plt


class SimilarityAttention(tf.keras.Model):
    def __init__(self, encoder: tf.keras.Model, alpha, beta):
        """
        Similarity Attention

        Attributes:
            encoder (keras.model): Basic nn encoder/feature extractor
            alpha (float): factor used for soft-masking the images, internally this a learnable parameter
            beta (float): fctor used for soft-masking the images, internally this a leranable parameter
        """
        super(SimilarityAttention, self).__init__()
        self.encoder = encoder
        self.alpha = tf.Variable(
            alpha, name="sim_alpha",
            trainable=True)  # declare as trainable variable
        self.beta = tf.Variable(
            beta, name="sim_beta",
            trainable=True)  # declare as trainable variable

    def extract_features(self, triplet, training):
        """Extract features of one mined triplet.
        Calls forward path of the encoder to get veature vectors and feature maps of the encoder for a given triplet
        consisting of one anchor, one positive and one negative sample

        Args:
            triplet (tf.tensor): mined triplet consisting of anchor, positive, negative

        Returns:
            feature_vectors (tf.tensor): feature vectors of the encoder forward path
            feature_maps (tf.tensor): feature maps of the last convolution layer of the encoder
        """
        feature_vectors, feature_maps = self.encoder(triplet,
                                                     training=training)

        return feature_vectors, feature_maps

    def construct_weight_vectors(self, feature_vectors):
        """Construct similarity weight vector w.

        Args:
            feature_vectors (tf.tensor): feature vectors of a given triplet
       
        Returns: 
            w (tf.tensor): weight vector of similarity learning
        """

        # split feature vectors
        f_a, f_p, f_n = feature_vectors[0], feature_vectors[
            1], feature_vectors[2]

        #  w_p = 1 - |f_a - f_p|, w_n = |f_a - f_n|
        w_p_diff = f_a - f_p

        w_p = 1 - tf.abs(w_p_diff)

        w_n_diff = f_a - f_n
        w_n = tf.abs(w_n_diff)

        # construct a single weight vector w = wp * wn,
        # where * denotes the element-wise product operation
        w = w_p * w_n

        return w

    def compute_sample_scores(self, weight_vector, feature_vectors):
        '''Compute sample scores s_a, s_p, s_n which are scalar values.

        Args:
            weight_vector (tf.tensor): weight vector w
            feature_vectors (tf.tensor): feature vectors of a given triplet

 
        Returns: 
            s_a (tf.tensor): sample score for anchor
            s_p (tf.tensor): sample score for positive
            s_n (tf.tensor): sample score for negative
        '''
        # split feature vectors
        f_a, f_p, f_n = feature_vectors[0], feature_vectors[
            1], feature_vectors[2]

        # weight_vector and f_a are 1D-Tensors/Vectors of shape (n,)
        s_a = tf.tensordot(weight_vector, f_a, 1)
        s_p = tf.tensordot(weight_vector, f_p, 1)
        s_n = tf.tensordot(weight_vector, f_n, 1)

        return s_a, s_p, s_n

    def get_attention_map(self, gradient_tape, feature_maps, sample_scores,
                          triplet_part):
        """Compute the attention map for a singe sample (anchor or positive or negative) of a triplet.

        Args:
            gradient_tape (tf.GradientTape): gradient tape used to caluclate the gradients of the forward path
            feature_maps (tf.tensor): feature maps of the triplet
            sample_scores (tf.tensor, tf.tensor, tf.tensor): sample scores s_a, s_p, s_n
            triplet_part (String): which part of the triplet - "anchor", "positive", "negative" 

        Returns:
            attention_map (tf.tensor): attention map (h, w) of the choosen triplet part
        """
        index = None
        if triplet_part == "anchor":
            index = 0

        elif triplet_part == "positive":
            index = 1

        elif triplet_part == "negative":
            index = 2

        # get correct sample score
        sample_score = sample_scores[index]

        # get attention maps
        grads = gradient_tape.gradient(sample_score, feature_maps)[index]
        feature_map = feature_maps[index]

        # do GAP like in GradCAM

        alpha = tf.reduce_mean(grads, axis=(0, 1))

        # attention map of (h, w)
        attention_map = tf.reduce_sum(tf.multiply(alpha, feature_map), axis=-1)

        # apply ReLU to attention map
        attention_map = tf.nn.relu(attention_map)

        return attention_map

    def get_attention_maps(self, gradient_tape, feature_maps, sample_scores):
        """Compute attention map for each part of a triplet.

        Args:
            gradient_tape (tf.GradientTape): gradient tape used to caluclate the gradients of the forward path
            feature_maps (tf.tensor): feature maps of the triplet
            sample_scores (tf.tensor, tf.tensor, tf.tensor): sample scores s_a, s_p, s_n

         Returns:
            attention_map_a (tf.tensor): attention map (h, w) of anchor
            attention_map_p (tf.tensor): attention map (h, w) of positive
            attention_map_n (tf.tensor): attention map (h, w) of negative
        """
        attention_map_a = self.get_attention_map(gradient_tape=gradient_tape,
                                                 feature_maps=feature_maps,
                                                 sample_scores=sample_scores,
                                                 triplet_part="anchor")

        attention_map_p = self.get_attention_map(gradient_tape=gradient_tape,
                                                 feature_maps=feature_maps,
                                                 sample_scores=sample_scores,
                                                 triplet_part="positive")

        attention_map_n = self.get_attention_map(gradient_tape=gradient_tape,
                                                 feature_maps=feature_maps,
                                                 sample_scores=sample_scores,
                                                 triplet_part="negative")

        return attention_map_a, attention_map_p, attention_map_n

    def mask_image(self, attention_map, image):
        """Soft-masking of an image with the corresponding attention map.

        Args:
            attention_map_a (tf.tensor): attention map (h, w) of anchor or positive or negative
            image (tf.tensor): image data of anchor or positive or negative

        Returns:
            image_hat (tf.tensor): soft-masked image
            attention_map (tf.tensor): interpolated/resized/rescaled attention map - only used for drawing
        """
        h, w, c = image.shape

        # add dimension because tf.image.resize need a 3d (height, width, channel) or 4d input of (batch, heigth, width, channel)
        attention_map = tf.expand_dims(attention_map, 2)

        # resize attention map to same height and width as the image
        attention_map = tf.image.resize(images=attention_map,
                                        size=[h, w],
                                        method="bilinear")

        # calc sigma(M_i)
        temp = self.alpha * (attention_map - self.beta)
        sigma = tf.nn.sigmoid(temp)

        # perform soft masking
        image_hat = image * (1 - sigma)

        # remove added dimension with value 1 from attention maps
        attention_map = tf.squeeze(attention_map, axis=2)

        return image_hat, attention_map

    def mask_images(self, attention_map_a, attention_map_p, attention_map_n,
                    data):
        """Soft-masking the images of a triplet.

        Args:
            attention_map_a (tf.tensor): attention map (h, w) of anchor
            attention_map_p (tf.tensor): attention map (h, w) of positive
            attention_map_n (tf.tensor): attention map (h, w) of negative
            data (tf.tensor): image data of a triplet consisting of anchor, positive, negative

        Returns:
            a_hat (tf.tensor): soft-masked anchor
            p_hat (tf.tensor): soft-masked positive
            n_hat (tf.tensor); soft-masked negative
            a_map (tf.tensor): attention map anchor
            p_map (tf.tensor): attention map positive
            n_map (tf.tensor): attention map negative
        """
        data_a = data[0]
        data_p = data[1]
        data_n = data[2]

        a_hat, a_map = self.mask_image(attention_map=attention_map_a,
                                       image=data_a)
        p_hat, p_map = self.mask_image(attention_map=attention_map_p,
                                       image=data_p)
        n_hat, n_map = self.mask_image(attention_map=attention_map_n,
                                       image=data_n)

        return a_hat, p_hat, n_hat, a_map, p_map, n_map

    def forward_masked_images(self, triplets, training):
        """Feed masked triplets through forward path of triplet network

        Args:
            triplets (tf.tensor): tensor of soft-masked triplets

        Returns:
            feature_vectors_ta (tf.tensor): feature vectors of masked triplets for similarity loss calculation
        """
        b = triplets.shape[0]

        feature_vectors_ta = tf.TensorArray(tf.float32, size=b)

        for i in range(b):
            feature_vectors_hat, _ = self.extract_features(triplets[i],
                                                           training=training)
            feature_vectors_ta = feature_vectors_ta.write(
                i, feature_vectors_hat)

        feature_vectors_ta = feature_vectors_ta.stack()
        return feature_vectors_ta

    def call(self, mined_triplets, training):
        """Peform Similarity Attention Learning.

        Args:
            mined_triplets (tf.tensor):  tensor of the selected triplets
            training (bool): determine if training or evaluation phase

        Returns:
            feature_vectors_hat (tf.tensor): feature vectors of masked triplets for similarity loss calculation
            all_triplets_hat (tf.tensor): tensor containg masked images for each triplet batch
            all_triplets_att (tf.tensor): tensor containg attention maps for each triplet batch

        """
        selected_triplets = mined_triplets

        b, t, h, w, c = selected_triplets.shape

        all_triplets_hat = tf.TensorArray(tf.float32, size=b)

        all_triplets_att = tf.TensorArray(tf.float32, size=b)

        for i in range(b):
            selected = selected_triplets[i]

            triplet_hat = tf.TensorArray(tf.float32, size=t)

            triplet_att = tf.TensorArray(tf.float32, size=t)

            with tf.GradientTape(persistent=True) as tape:

                # get feature vectors and feature maps for current triplet
                feature_vectors, feature_maps = self.extract_features(
                    selected, training=training)

                # construct weight vector
                weight_vector = self.construct_weight_vectors(
                    feature_vectors=feature_vectors)

                # compute sample scores
                s_a, s_p, s_n = self.compute_sample_scores(
                    weight_vector=weight_vector,
                    feature_vectors=feature_vectors)

            # compute attention maps
            am_anchor, am_positive, am_negative = self.get_attention_maps(
                gradient_tape=tape,
                feature_maps=feature_maps,
                sample_scores=(s_a, s_p, s_n))

            # soft mask images
            a_hat, p_hat, n_hat, a_map, p_map, n_map = self.mask_images(
                attention_map_a=am_anchor,
                attention_map_p=am_positive,
                attention_map_n=am_negative,
                data=selected)

            # construct tensor of triplet_hats
            triplet_hat = triplet_hat.write(0, a_hat)
            triplet_hat = triplet_hat.write(1, p_hat)
            triplet_hat = triplet_hat.write(2, n_hat)

            triplet_hat = triplet_hat.stack()  # (3, h , w, 3)

            all_triplets_hat = all_triplets_hat.write(i, triplet_hat)

            # construct tensor of triplet attention maps
            triplet_att = triplet_att.write(0, a_map)
            triplet_att = triplet_att.write(1, p_map)
            triplet_att = triplet_att.write(2, n_map)

            triplet_att = triplet_att.stack()  # (3, h, w)

            all_triplets_att = all_triplets_att.write(i, triplet_att)

        all_triplets_hat = all_triplets_hat.stack()  # (b, 3, h, w, 3)

        all_triplets_att = all_triplets_att.stack()  # (b, 3, h, w)

        # forward masked images
        feature_vectors_hat = self.forward_masked_images(
            triplets=all_triplets_hat, training=training)

        return feature_vectors_hat, all_triplets_hat, all_triplets_att
