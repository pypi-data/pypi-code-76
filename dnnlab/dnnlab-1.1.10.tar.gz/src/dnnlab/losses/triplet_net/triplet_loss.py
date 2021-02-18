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
"""Define Triplet Net Loss functions."""
import tensorflow as tf

from dnnlab.losses.triplet_net.triplet_mining import batch_hard_triplet_loss


class TripletLoss():
    """Standard TripletLoss.
    """
    def __init__(self, margin):
        super().__init__()
        self.margin = margin

    def call(self, embeddings, targets):
        """Calculate standard TripletLoss for triplets which are sampled via
        input pipeline.
        L = max( d(a,p) - d(a,n) + margin, 0)

        Args:
            embeddings (tf.tensor): embeddings of the encoder forward path
            targest (tf.tensor): labels

        Returns:
            loss (tf.tensor): TripletLoss of the embeddings and corresponding
                labels.
        """
        anchor = embeddings[0]
        positive = embeddings[1]
        negative = embeddings[2]

        ap_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, positive)),
                                axis=-1)
        an_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, negative)),
                                axis=-1)

        basic_loss = tf.add(tf.subtract(ap_dist, an_dist), self.margin)
        loss = tf.reduce_sum(tf.maximum(basic_loss, 0.0))

        return tf.math.reduce_mean(loss)


# omoindrot
class TripletBatchHardLoss():
    """TripletBatchHardLoss is one variant of TripletLoss with Online
        TripletMining.
    """
    def __init__(self, margin=1.0):
        self.margin = margin

    def call(self, embeddings, targets):
        """Calculate TripletBatchHardLoss with "batch hard" triplet mining.

         Args:
            embeddings (tf.tensor): embeddings of the encoder forward path
            targets (tf.tensor): labels

        Returns:
            loss (tf.tensor): TripletBatchHardLoss of the mined triplets and
                corresponding labels.
        """
        return batch_hard_triplet_loss(labels=targets,
                                       embeddings=embeddings,
                                       margin=self.margin)


class SimilarityLoss():
    """SimilarityLoss for learning similarity attention.
    """
    def call(self, feature_vectors):
        """Calculate SimilarityLoss for TripletNet with similarity attention.

        Args:
            feature_vectors (tf.tensor[batch_size, 3, num_features]):

        Returns:
            loss (tf.tensor): SimilarityLoss of similarity attention of
                batch-hard-mined triplets.
        """

        # feature vectors have shape (batch_size, 3, num_features)
        # therefore a single triplet has shape (3, num_features)
        f_a = feature_vectors[:, 0, :]
        f_p = feature_vectors[:, 1, :]
        f_n = feature_vectors[:, 2, :]

        euclidean_ap = tf.math.reduce_euclidean_norm(f_a - f_p)
        euclidean_an = tf.math.reduce_euclidean_norm(f_a - f_n)
        loss_sm = tf.abs(euclidean_ap - euclidean_an)

        return loss_sm


class OverallSimilarityLoss():
    """Overall training object of TripletNet + SimiliarityAttention.
    L = loss_ml + gamma * loss_sm
    The SimilarityLoss is weighted by a factor gamma.
    """
    def __init__(self, gamma=0.5):
        """
        gamma is a weight factor for the SimilarityLoss
        """
        self.gamma = gamma

    def call(self, loss_ml, loss_sm):
        """Calculate OverallSimilarityLoss.

        Args:
            loss_ml (tf.tensor): loss of standalone TripletNet
            loss_sm (tf.tensor): SimilarityLoss

        Returns:
            overall_all (tf.tensor): combined loss of TripletNet-Loss and
                weighted SimilarityLoss.
        """
        overall_loss = loss_ml + self.gamma * loss_sm
        return overall_loss
