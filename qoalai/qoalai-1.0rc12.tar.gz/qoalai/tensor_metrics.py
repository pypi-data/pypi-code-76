'''
    File name: tensor_metrics.py
    Author: [Mochammad F Rahman]
    Date created: / /2018
    Date last modified: 17/07/2019
    Python Version: >= 3.5
    Qoalai version: v0.4.1
    License: MIT License
    Maintainer: [Mochammad F Rahman]
'''

import tensorflow as tf 
import numpy as np


def calculate_acc(input_tensor, label, threshold=0.5):
    """[summary]
    
    Arguments:
        input_tensor {[type]} -- [description]
        label {[type]} -- [description]
    
    Keyword Arguments:
        threshold {float} -- [description] (default: {0.5})
    
    Returns:
        [type] -- [description]
    """
    mask = tf.math.reduce_sum(label, axis=-1)
    total_obj = tf.math.reduce_sum(label)
    input_tensor = tf.math.argmax(input_tensor, axis=-1)
    label = tf.math.argmax(label, axis=-1)
    correctness = tf.cast(tf.math.equal(input_tensor, label), tf.float32) 
    correctness = correctness * mask
    acc = tf.reduce_sum(correctness) / (total_obj + 0.01) 
    return acc


    """
    mask = tf.fill(tf.shape(label), 1.)
    input_tensor = tf.reshape(input_tensor, [tf.shape(input_tensor)[0], -1])
    label = tf.reshape(label, [tf.shape(label)[0], -1])

    input_tensor = tf.math.greater(input_tensor, tf.convert_to_tensor(np.array(threshold), tf.float32))
    input_tensor = tf.cast(input_tensor, tf.float32)
    label = tf.math.greater(label, tf.convert_to_tensor(np.array(threshold), tf.float32))
    label = tf.cast(label, tf.float32)

    error = tf.reduce_sum(tf.abs(input_tensor - label)) / (tf.reduce_sum(mask) + 0.0001)
    acc = 1. - error
    return acc
    """