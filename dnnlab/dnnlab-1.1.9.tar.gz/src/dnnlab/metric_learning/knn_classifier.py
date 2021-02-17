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
# =============================================================================
"""
k-NN (k-NearestNeighbor) classifier.

we are going to extract the features extracted from the CNN, the last layer of
CNN is supposed to learn a good representation of image and accordingly could have 
adjusted the weights why should not obtain these features, and feed them to some other 
Machine Learning Models like SVM, KNN etc.
"""

import tensorflow as tf


class KNNClassifier:
    def __init__(self, k=1, labels=None):
        self.k = 1
        self.labels = labels

    def distance_metric(self, embeddings_train, embeddings_test):
        """Generate the euclidean distance matrix.
        Compare each test sample with all train samples. 

        Args:
            embeddings_train (tf.tensor): training embeddings [b_train, h, w, c]
            embeddings_test (tf.tensor): test embeddings [b_test, h, w, c]

        Returns:
            distance_matrix (tf.tensor): distance matrix [b_test, b_train] between the train and test embeddings 
        """
        test_shape = embeddings_test.shape
        dm_ta = tf.TensorArray(tf.float32, size=test_shape[0])

        print(test_shape)
        for b in range(test_shape[0]):
            dist = tf.sqrt(
                tf.reduce_sum(tf.square(
                    tf.subtract(embeddings_train, embeddings_test[b])),
                              axis=[1, 2, 3]))
            print(dist.shape)
            dm_ta = dm_ta.write(b, dist)

        dm_ta = dm_ta.stack()
        print("DM_TA", dm_ta)
        return dm_ta

    def get_k_nearest_neighbors(self, embeddings_train, embeddings_test):
        """k-nearest neighbors.

        Args:
            embeddings_train (tf.tensor): embeddings of training samples
            embeddings_test (tf.tensor): embeddings of test samples

        Returns:
            labels_test (tf.tensor): predicted labels of test samples

        """
        # Calculates the distance from the test instances against the training data.
        distances = self.distance_metric(embeddings_train=embeddings_train,
                                         embeddings_test=embeddings_test)

        # Negating the distances
        # this is a trick because tensorflow hast top_k API and no closes_k or reverse=True api
        neg_distances = tf.negative(distances)

        # return the k values and indices from the leas distant nodes
        values, indices = tf.nn.top_k(neg_distances, self.k)

        # gather the classes using the indexes in the label tensor
        labels_neighbours = tf.gather(self.labels, indices)

        # Since the class is discrete we cast it into an int32.
        labels_neighbours = tf.cast(labels_neighbours, tf.int32)

        # We aggregate sums of the values and calculate how many values from each class is there on the neighbourhood.
        # (i.e. creates a tensor with the count on each index for each class)
        label_counts = tf.math.bincount(labels_neighbours)
        print("LC: ", label_counts)

        #Gets the index (i.e. corresponding class) of the test samples with the max count.
        labels_test = tf.argmax(label_counts)
        print("LT: ", labels_test)

        return labels_test
