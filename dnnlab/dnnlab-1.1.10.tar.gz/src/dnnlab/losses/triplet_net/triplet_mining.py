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
###Triplet Loss
A triplet consists of an anchor a, a positive p of the same class as the anchor
and a negative n of a different class. For some distance on the embedding space
d, the loss of a triplet (a,p,n) is:
    L = max( d(a,p) - d(a,n) + margin, 0)
We minimize this loss, which pushes d(a,p) to 0 and d(a,n) to be greater than
d(a,p) + margin. As soon as n becomes an "eays negative", the loss becomes zero.


### Triplet Mining
There are 3 categories of triplets:
- easy triplets: triplets which have a loss of 0, because d(a,p) + margin < d(a,n)
- hard triplets: triplets where the negative is closer to anchor than the positive, i.e d(a,n) < d(a,p)
- semi-hard triplets: triplets where the negative is not closer to the anchor than the positive,
                      but which still have positive loss: d(a,p) < d(a,n) < d(a,p) + margin
Each of these definitions depend on where the negative is, relatively to the anchor and positive.
Therefore, we can extend these 3 categories to the negatives: hard negative, semi-hard negative or easy negatives.

### Offline and Online triplet mining
Some triplets are more useful than others. How to sample or "mine" these triplets.

# OFFLINE:
The first way to produce triplets is to find them offline, at the beginning of each epoch 
for instance. We compute all the embeddings on the training set, and then only select HARD or 
SEMI-HARD triplets; avoid the EASY triplets because their loss is 0. We can then train one epoch on these triplets.
Concretely, we would produce a list of triplets
(i,j,k). We would then create batches of these triplets of size B, which means we will have to compute 3*B
embeddings to get the B triplets, compute the loss of these B triplets and then backpropagate into the network.

Overall this technique is not very efficient since we need to do a full pass on the training set to generate triplets. 
It also requires to update the offline mined triplets regularly.

# ONLINE:
The idea here is to compute useful triplets on the fly, for each batch of inputs.
Given a batch of B examples (for instance B images of faces), we compute the B embeddings and 
we then can find a maximum of B^3 triplets.
Of course, most of these triplets are not valid (i.e. they don’t have 2 positives and 1 negative).

This technique gives you more triplets for a single batch of inputs, and doesn’t require any offline mining. 
It is therefore much more efficient.


### Stategies in online mining
In online mining, we have computed a batch of  B embeddings from a batch of B inputs. 
Now we want to generate triplets from these B embeddings.
Whenever there are the 3 indices i,j,k, if example i and j have the same label but are distinct,
and example k has a different label, it is a valid triplet (i,j,k).
What remains here is to have a good strategy to pick triplets among the valid ones on which to compute the loss.

Suppose you have a batch if samples/images of input size B = P * K, composed of P different image classes 
and K images of each class. A typical value is K = 4.
There are two strategies:
# batch all:
select all the valid triplets, and average the loss on the hard and semi-hard triplets
    - a crucial point here is to not take into acount the eays triplets (those with loss 0), as averaging
      on them would make the overall loss very small --> weak learning and weight updates
    - produces a total of PK(K-1)(PK-K) triplets (PK anchors, K-1 possible positives per anchor, PK-K possible negatives)

# batch hard:
for each anchor, select the harest positive (biggest distance d(a,p)) and the hardest negative among the batch
    - this produces PK triplets
    - the selected triplets are the hardest among the batch

The batch hard strategy yields the best performance.
However it really depends on the dataset and should be decided by comparing performance.



Steps to define Online Triplet Loss and Mining:
1. select mining strategy: batch all, batch hard

Steps to define Offline Triplet Loss and Mining:
1. select triplet category: easy, hard, semi-hard
2. compute the valid triplets


"""

import tensorflow as tf


def pairwise_distances(feature, squared=False):
    """Computes the pairwise distance matrix of all possible image pairs with numerical stability.
    output[i, j] = || feature[i, :] - feature[j, :] ||_2

    D_ij = || x_i - x_j ||^2_2
    or:
    D_ij = (x_i - x_j)^T (x_i - x_j) = || x_i ||^2_2 - 2(x_i)^T x_j + || x_j ||^2_2

    Args:
      feature (tf.tensor): 2-D Tensor of size [number of data, feature dimension].
      squared (boolean): Boolean, whether or not to square the pairwise distances.

    Returns:
      pairwise_distances (tf.tensor): 2-D Tensor of size [number of data, number of data].
    """
    pairwise_distances_squared = tf.math.add(
        tf.math.reduce_sum(tf.math.square(feature), axis=[1], keepdims=True),
        tf.math.reduce_sum(
            tf.math.square(tf.transpose(feature)), axis=[0],
            keepdims=True)) - 2.0 * tf.matmul(feature, tf.transpose(feature))

    # set small negatives to zero to have numerical inaccuracies
    pairwise_distances_squared = tf.math.maximum(pairwise_distances_squared,
                                                 0.0)

    # create mask where the zero distances are placed
    error_mask = tf.math.less_equal(pairwise_distances_squared, 0.0)

    # Optionally take the sqrt
    if squared:
        pairwise_distances = pairwise_distances_squared
    else:
        # Because the gradient of sqrt is infinite when distances == 0.0 (ex: on the diagonal)
        # we need to add a small epsilon where distances == 0.0
        pairwise_distances = tf.math.sqrt(
            pairwise_distances_squared +
            tf.cast(error_mask, dtype=tf.float32) * 1e-16)

    # Undo conditionally adding 1e-16.
    pairwise_distances = tf.math.multiply(
        pairwise_distances,
        tf.cast(tf.math.logical_not(error_mask), dtype=tf.float32))

    # Explicitly set diagonals to zero.
    num_data = tf.shape(feature)[0]
    mask_offdiagonals = tf.ones_like(pairwise_distances) - tf.linalg.diag(
        tf.ones([num_data]))
    pairwise_distances = tf.math.multiply(pairwise_distances,
                                          mask_offdiagonals)

    return pairwise_distances


"""
To compute the hardest positive, we begin with the pairwise distance matrix. We then get a 2D mask of the valid
pairs (a,p) (i.e. a != p and a and p have same labels) and put to 0 any element outside of the mask.
The last step is just to take the maximum distance over each row of this modified distance matrix.
The results should be a valid pair (a,p) since invalid elements are set to 0.
"""


def _get_anchor_positive_triplet_mask(labels):
    """
        Return a 2D mask where mask[a, p] is True iff a and p are distinct and have same label.

        Args:
            labels (tf.tensor): tf.int32 `Tensor` with shape [batch_size]
        Returns:
            mask (tf.tensor): tf.bool `Tensor` with shape [batch_size, batch_size]
        """
    # check that i and j are distinct
    indices_equal = tf.cast(tf.eye(tf.shape(labels)[0]), tf.bool)
    indices_not_equal = tf.logical_not(indices_equal)

    # check if label[i] == labels[j]
    # uses broadcasting where the 1st argument has shape (1, batch_size) and the 2nd (batch_size, 1)
    labels_equals = tf.equal(tf.expand_dims(labels, 0),
                             tf.expand_dims(labels, 1))

    # combine the two masks
    mask = tf.logical_and(indices_not_equal, labels_equals)

    return mask


"""
The hardest negative is similar but a bit trickier to compute. Here we need to get the minimum distance
for each row, so we cannot set to 0 the invalid pairs (a,n) (invalid if a and n have the same label).
Our trick here is for each row to add the maximum value to the invalide pairs (a,n). We then take the
minimum over each row. The result should be a valid pair (a,n) since invalid elements are set to the 
maximum value.
"""


def _get_anchor_negative_triplet_mask(labels):
    """
        Return a 2D mask where mask[a, n] is True iff a and n have distinct labels.

        Args:
            labels (tf.tensor): tf.int32 `Tensor` with shape [batch_size]
        Returns:
            mask (tf.tensor): tf.bool `Tensor` with shape [batch_size, batch_size]
        """
    # check if labels[i] !0 labels[j]
    # uses broadcasting where the 1st argument has shape (1, batch_size) and the 2nd (batch_size, 1)
    labels_equal = tf.equal(tf.expand_dims(labels, 0),
                            tf.expand_dims(labels, 1))

    mask = tf.logical_not(labels_equal)

    return mask


# only used for batch_all_triplet_loss
def _get_triplet_mask(labels):
    """
        Return a 3D mask where mask[a, p, n] is True iff the triplet (a, p, n) is valid.

        A triplet (i, j, k) is valid if:
            - i, j, k are distinct
            - labels[i] == labels[j] and labels[i] != labels[k]
        Args:
            labels (tf.tensor): tf.int32 `Tensor` with shape [batch_size]

        Returns:
            maks (tf.tensor): boolean mask of valid triplets
        """
    # check that i, j and k are distinct
    indices_equal = tf.cast(tf.eye(tf.shape(labels)[0]), tf.bool)
    indices_not_equal = tf.logical_not(indices_equal)

    i_not_equal_j = tf.expand_dims(indices_not_equal, 2)
    i_not_equal_k = tf.expand_dims(indices_not_equal, 1)
    j_not_equal_k = tf.expand_dims(indices_not_equal, 0)

    distinct_indices = tf.logical_and(
        tf.logical_and(i_not_equal_j, i_not_equal_k), j_not_equal_k)

    # check if labels[i] == labels[j] and labels[i] != labels[k]
    label_equal = tf.equal(tf.expand_dims(labels, 0),
                           tf.expand_dims(labels, 1))
    i_equal_j = tf.expand_dims(label_equal, 2)
    i_equal_k = tf.expand_dims(label_equal, 1)

    valid_labels = tf.logical_and(i_equal_j, tf.logical_not(i_equal_k))

    # combine the two masks
    mask = tf.logical_and(distinct_indices, valid_labels)

    return mask


def batch_all_triplet_loss(labels, embeddings, margin, squared=False):
    """Build the triplet loss over a batch of embeddings.

    Generate all the valid triplets and average the loss over the positive ones.

    Args:
        labels (tf.tensor): labels of the batch, of size (batch_size,)
        embeddings (tf.tensor): tensor of shape (batch_size, embed_dim)
        margin (float): margin for triplet loss
        squared (boolean): Boolean. If true, output is the pairwise squared euclidean distance matrix.
                 If false, output is the pairwise euclidean distance matrix.

    Returns:
        triplet_loss (tf.tensor): scalar tensor containing the triplet loss
    """
    # TODO
    pass


"""
for each anchor, select the hardest positive (biggest distance d(a,p)) and 
the hardest negative (smallest distance d(a,n)) among the batch
- this produces P*K triplets
- the selected triplets are the hardest among the batch
"""


def batch_hard_triplet_loss(labels, embeddings, margin, squared=False):
    """
        Build the triplet loss over a batch of embeddings.

        For each anchor, we get the hardest positive and hardest negative to form a triplet.
        Args:
            labels (tf.tensor): labels of the batch, of size (batch_size,)
            embeddings (tf.tensor): tensor of shape (batch_size, embed_dim)
            margin (float): margin for triplet loss
            squared (boolean): Boolean. If true, output is the pairwise squared euclidean distance matrix.
                    If false, output is the pairwise euclidean distance matrix.
        Returns:
            triplet_loss (tf.tensor): scalar tensor containing the triplet loss
        """
    # get the pairwise distance matrix
    pairwise_dist = pairwise_distances(embeddings, squared=squared)

    # for each anchor, get the hardest positive
    # first, we need to get a mask for every valide positive (they should have same label)
    mask_anchor_positive = _get_anchor_positive_triplet_mask(labels)
    mask_anchor_positive = tf.cast(mask_anchor_positive, dtype=tf.float32)

    # We put to 0 any element where (a, p) is not valid (valid if a != p and label(a) == label(p))
    anchor_positive_dist = tf.multiply(mask_anchor_positive, pairwise_dist)

    # shape (batch_size, 1)
    hardest_positive_dist = tf.reduce_max(anchor_positive_dist,
                                          axis=1,
                                          keepdims=True)

    # get indices of the hardest anchor positive pairs
    hardest_ap_indices = tf.where(
        tf.equal(hardest_positive_dist, anchor_positive_dist))

    # for each anchor, get the hardest negative
    # first, we need to get a mask for every valid negative (they should have different labels)
    mask_anchor_negative = _get_anchor_negative_triplet_mask(labels)
    mask_anchor_negative = tf.cast(mask_anchor_negative, dtype=tf.float32)

    # we add the maximum value in each row to the invalid negatives (label(a) == label(n))
    max_anchor_negative_dist = tf.reduce_max(pairwise_dist,
                                             axis=1,
                                             keepdims=True)
    anchor_negative_dist = pairwise_dist + max_anchor_negative_dist * (
        1.0 - mask_anchor_negative)

    # shape (batch_size,)
    hardest_negative_dist = tf.reduce_min(anchor_negative_dist,
                                          axis=1,
                                          keepdims=True)

    # get indices of hardest anchor negative pairs
    hardest_an_indices = tf.where(
        tf.equal(hardest_negative_dist, anchor_negative_dist))

    # Combine biggest d(a, p) and smallest d(a, n) into final triplet loss
    triplet_loss = tf.maximum(
        hardest_positive_dist - hardest_negative_dist + margin, 0.0)

    # Get final mean triplet loss
    triplet_loss = tf.reduce_mean(triplet_loss)

    return triplet_loss, hardest_ap_indices, hardest_an_indices
