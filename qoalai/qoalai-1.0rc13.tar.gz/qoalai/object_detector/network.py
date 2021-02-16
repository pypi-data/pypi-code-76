'''
    File name: network.py
    Author: [DS Team]
    Date created: / /2020
    Date last modified: 
    Python Version: >= 3.5
    qoalai version: v0.4
    License: MIT License
    Maintainer: [DS Team]
'''

import os
import cv2
import math
import numpy as np
from os import walk
import tensorflow as tf 
from qoalai.tensor_operations import *



class YoloNetwork(object): 
    def __init__(self,
                    num_class,
                    is_multilabel,
                    multilabel_dict,
                    anchor, 
                    dropout_val = 0.85,
                    threshold = 0.5,
                    leaky_relu_alpha = 0.1,
                    add_modsig_toshape = True,
                    convert_to_tflite=False): 

        self.num_class = num_class
        self.is_multilabel = is_multilabel
        self.multilabel_dict = multilabel_dict 
        self.anchor = anchor
        self.dropout_val = 0.8
        self.threshold = threshold
        self.leaky_relu_alpha = leaky_relu_alpha
        self.add_modsig_toshape = add_modsig_toshape
        self.lite = convert_to_tflite

        self.FILTER_128 = 128
        self.FILTER_256 = 256
        self.FILTER_512 = 512
        self.FILTER_1024 = 1024 

    
    def fixed_padding(self, inputs, 
                        kernel_size, 
                        data_format):
        """ResNet implementation of fixed padding.
        Pads the input along the spatial dimensions independently of input size.

        Args:
            inputs: Tensor input to be padded.
            kernel_size: The kernel to be used in the conv2d or max_pool2d.
            data_format: The input format.
        Returns:
            A tensor with the same format as the input.
        """
        pad_total = kernel_size - 1
        pad_beg = pad_total // 2
        pad_end = pad_total - pad_beg

        if data_format == 'channels_first':
            padded_inputs = tf.pad(inputs, [[0, 0], [0, 0],
                                            [pad_beg, pad_end],
                                            [pad_beg, pad_end]])
        else:
            padded_inputs = tf.pad(inputs, [[0, 0], [pad_beg, pad_end],
                                            [pad_beg, pad_end], [0, 0]])
        return padded_inputs 

        
    def darknet53_residual_block(self, inputs, 
                                    filters, 
                                    training, 
                                    data_format, 
                                    stride=1, 
                                    name='res'):
        """[summary]
        Arguments:
            inputs {[tensor]} -- input tensor
            filters {[tensor]} -- the filter tensor
            training {[bool]} -- the phase, training or not
            data_format {[string]} -- channel first or not
        
        Keyword Arguments:
            stride {int} -- [the strides] (default: {1})
            name {str} -- [the additional name for all tensors in this block] (default: {'res'})
        
        Returns:
            [type] -- [description]
        """
        shortcut = inputs
        
        inputs = new_conv2d_layer(input=inputs, 
                        filter_shape=[1, 1, inputs.get_shape().as_list()[-1], filters], 
                        name = name + '_input_conv1', 
                        dropout_val= self.dropout_val, 
                        activation = 'LRELU',  
                        padding=('SAME' if stride == 1 else 'VALID'), 
                        strides=[1, stride, stride, 1],  
                        is_training=training,
                        use_bias=False,
                        use_batchnorm=True)
        
        inputs = new_conv2d_layer(input=(inputs if stride == 1 else self.fixed_padding(inputs, 3, 'channels_last')), 
                        filter_shape=[3, 3, inputs.get_shape().as_list()[-1], shortcut.get_shape().as_list()[-1]], 
                        name = name + '_input_conv2', 
                        dropout_val= self.dropout_val, 
                        activation = 'LRELU',
                        padding=('SAME' if stride == 1 else 'VALID'), 
                        strides=[1, stride, stride, 1], 
                        data_type=tf.float32, 
                        is_training=training,
                        use_bias=False,
                        use_batchnorm=True)

        inputs += shortcut
        return inputs


    def darknet53(self, inputs, training, data_format, network_type):
        """[summary]
        
        Arguments:
            inputs {tensor} -- the input tensor
            training {bool} -- the phase, training or not
            data_format {string} -- channel_first or not
        
        Returns:
            [type] -- [description]
        """
        inputs = new_conv2d_layer(input=inputs, 
                        filter_shape=[3, 3, inputs.get_shape().as_list()[-1], 32], 
                        name = 'main_input_conv1', 
                        dropout_val= self.dropout_val, 
                        activation = 'LRELU',
                        padding='SAME', 
                        strides=[1, 1, 1, 1], 
                        data_type=tf.float32, 
                        is_training=training,
                        use_bias=False,
                        use_batchnorm=True)

        inputs = new_conv2d_layer(input=self.fixed_padding(inputs, 3, 'channels_last'), 
                        filter_shape=[3, 3, inputs.get_shape().as_list()[-1], 64], 
                        name = 'main_input_conv2', 
                        dropout_val= self.dropout_val, 
                        activation = 'LRELU',
                        padding='VALID', 
                        strides=[1, 2, 2, 1], 
                        is_training=training,
                        use_bias=False,
                        use_batchnorm=True)

        inputs = self.darknet53_residual_block(inputs=inputs, 
                                            filters=32, 
                                            training=training,
                                            data_format=data_format, 
                                            name='res1')

        inputs = new_conv2d_layer(input=self.fixed_padding(inputs, 3, 'channels_last'), 
                        filter_shape=[3, 3, inputs.get_shape().as_list()[-1], 128], 
                        name = 'main_input_conv3', 
                        dropout_val= self.dropout_val, 
                        activation = 'LRELU',
                        padding='VALID', 
                        strides=[1, 2, 2, 1], 
                        data_type=tf.float32, 
                        is_training=training,
                        use_bias=False,
                        use_batchnorm=True)

        for i in range(2):
            inputs = self.darknet53_residual_block(inputs, 
                                                filters=64,
                                                training=training,
                                                data_format=data_format, 
                                                name='res' + str(i+1))
            
        inputs = new_conv2d_layer(input=self.fixed_padding(inputs, 3, 'channels_last'), 
                        filter_shape=[3, 3, inputs.get_shape().as_list()[-1], 256], 
                        name = 'main_input_conv4', 
                        dropout_val= self.dropout_val, 
                        activation = 'LRELU',
                        padding='VALID', 
                        strides=[1, 2, 2, 1],  
                        data_type=tf.float32, 
                        is_training=training,
                        use_bias=False,
                        use_batchnorm=True)

        return_vars = None
        if network_type == 'special':
            return_vars = tf.global_variables(scope='yolo_v3_model')
        elif network_type == 'very_small':
            return_vars = tf.global_variables(scope='yolo_v3_model')

        for i in range(8):
            inputs = self.darknet53_residual_block(inputs, 
                                                filters=self.FILTER_128,
                                                training=training,
                                                data_format=data_format, 
                                                name='res' + str(i+3))

        route1 = inputs
        inputs = new_conv2d_layer(input=self.fixed_padding(inputs, 3, 'channels_last'), 
                        filter_shape=[3, 3, inputs.get_shape().as_list()[-1], self.FILTER_512], 
                        name = 'main_input_conv5', 
                        dropout_val= self.dropout_val, 
                        activation = 'LRELU',
                        padding='VALID', 
                        strides=[1, 2, 2, 1], 
                        data_type=tf.float32, 
                        is_training=training,
                        use_bias=False,
                        use_batchnorm=True)
        
        for i in range(8):
            inputs = self.darknet53_residual_block(inputs, 
                                                filters=self.FILTER_256,
                                                training=training,
                                                data_format=data_format, 
                                                name='res' + str(i+11))

        route2 = inputs
        inputs = new_conv2d_layer(input=self.fixed_padding(inputs, 3, 'channels_last'), 
                        filter_shape=[3, 3, inputs.get_shape().as_list()[-1], self.FILTER_1024], 
                        name = 'main_input_conv6', 
                        dropout_val= self.dropout_val, 
                        activation = 'LRELU', 
                        padding='VALID', 
                        strides=[1, 2, 2, 1],  
                        data_type=tf.float32, 
                        is_training=training,
                        use_bias=False,
                        use_batchnorm=True)

        for i in range(4):
            inputs = self.darknet53_residual_block(inputs, filters=self.FILTER_512,
                                            training=training,
                                            data_format=data_format, name='res' + str(i+19))
        return route1, route2, inputs, return_vars


    def yolo_convolution_block(self, inputs, filters, training, data_format):
        """[summary]
        
        Arguments:
            inputs {[type]} -- [description]
            filters {[type]} -- [description]
            training {[type]} -- [description]
            data_format {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        inputs = new_conv2d_layer(input=inputs, 
                        filter_shape=[1, 1, inputs.get_shape().as_list()[-1], filters], 
                        name = 'main_input_conv7', 
                        dropout_val= self.dropout_val, 
                        activation = 'LRELU',
                        padding='SAME', 
                        strides=[1, 1, 1, 1],
                        data_type=tf.float32, 
                        is_training=training,
                        use_bias=False,
                        use_batchnorm=True)
    
        inputs = new_conv2d_layer(input=inputs, 
                        filter_shape=[3, 3, inputs.get_shape().as_list()[-1], 2*filters], 
                        name = 'main_input_conv8', 
                        dropout_val= self.dropout_val, 
                        activation = 'LRELU',
                        padding='SAME', 
                        strides=[1, 1, 1, 1],
                        data_type=tf.float32, 
                        is_training=training,
                        use_bias=False,
                        use_batchnorm=True)
        
        inputs = new_conv2d_layer(input=inputs, 
                        filter_shape=[1, 1, inputs.get_shape().as_list()[-1], filters], 
                        name = 'main_input_conv9', 
                        dropout_val= self.dropout_val, 
                        activation = 'LRELU',
                        padding='SAME', 
                        strides=[1, 1, 1, 1],
                        data_type=tf.float32,   
                        is_training=training,
                        use_bias=False,
                        use_batchnorm=True)
        
        inputs = new_conv2d_layer(input=inputs, 
                        filter_shape=[3, 3, inputs.get_shape().as_list()[-1], 2*filters], 
                        name = 'main_input_conv10', 
                        dropout_val= self.dropout_val, 
                        activation = 'LRELU',
                        padding='SAME', 
                        strides=[1, 1, 1, 1],
                        data_type=tf.float32, 
                        is_training=training,
                        use_bias=False,
                        use_batchnorm=True)
        
        inputs = new_conv2d_layer(input=inputs, 
                        filter_shape=[1, 1, inputs.get_shape().as_list()[-1], filters], 
                        name = 'main_input_conv11', 
                        dropout_val= self.dropout_val, 
                        activation = 'LRELU',
                        padding='SAME', 
                        strides=[1, 1, 1, 1], 
                        data_type=tf.float32, 
                        is_training=training,
                        use_bias=False,
                        use_batchnorm=True)

        route = inputs
        inputs = new_conv2d_layer(input=inputs, 
                        filter_shape=[3, 3, inputs.get_shape().as_list()[-1], 2*filters], 
                        name = 'main_input_conv12', 
                        dropout_val= self.dropout_val, 
                        activation = 'LRELU',
                        padding='SAME', 
                        strides=[1, 1, 1, 1],
                        data_type=tf.float32, 
                        is_training=training,
                        use_bias=False,
                        use_batchnorm=True)
                    
        return route, inputs

    
    def yolo_layer(self, inputs, n_classes, 
                    anchors, img_size, data_format):
        """Creates Yolo final detection layer.

        Detects boxes with respect to anchors.

        Args:
            inputs: Tensor input.
            n_classes: Number of labels.
            anchors: A list of anchor sizes.
            img_size: The input size of the model.
            data_format: The input format.

        Returns:
            Tensor output.
        """
        # ----------------------------- #
        # get the num of anchor         #
        # get the grid shape (hxw)      #
        # ----------------------------- #
        n_anchors = len(anchors)
        shape = inputs.get_shape().as_list()
        grid_shape = shape[2:4] if data_format == 'channels_first' else shape[1:3]

        # ----------------------------- #
        # reshape the tensor to:        #
        # batch x (num of anchor . h . w) x (5 + num of classes)
        # strides -> int(the image input / grid)
        # strides -> horizontal and vertical stride 
        # ----------------------------- #
        if data_format == 'channels_first':
            inputs = tf.transpose(inputs, [0, 2, 3, 1])
        inputs = tf.reshape(inputs, [-1, n_anchors * grid_shape[0] * grid_shape[1],
                                    5 + n_classes])

        strides = (img_size[0] // grid_shape[0], img_size[1] // grid_shape[1])

        # ----------------------------- #
        # split the tensor to           #
        # center, shape, confidence, class
        # center: SILL RELATIVE to the GRID
        # create an x ofset tensor based on grid position
        # create an y ofset tensor based on grid position
        # center = (ofset tensor + center) * stride
        # ----------------------------- #
        box_centers, box_shapes, confidence, classes = \
                    tf.split(inputs, [2, 2, 1, n_classes], axis=-1)

        x = tf.range(grid_shape[0], dtype=tf.float32)
        y = tf.range(grid_shape[1], dtype=tf.float32)
        x_offset, y_offset = tf.meshgrid(x, y)
        x_offset = tf.reshape(x_offset, (-1, 1))
        y_offset = tf.reshape(y_offset, (-1, 1))
        x_y_offset = tf.concat([x_offset, y_offset], axis=-1)
        x_y_offset = tf.tile(x_y_offset, [1, n_anchors])
        x_y_offset = tf.reshape(x_y_offset, [1, -1, 2])
        box_centers = tf.nn.sigmoid(box_centers)
        box_centers = (box_centers + x_y_offset) * strides

        # ----------------------------- #
        # shape = exp(shape) * anchor
        # box confidence = sigmoid(conf)
        # classes = sigmoid(classes)
        # final -> concat all
        # ----------------------------- #
        anchors = tf.tile(anchors, [grid_shape[0] * grid_shape[1], 1])
        if self.add_modsig_toshape:
            box_shapes = 6 /(1 + tf.exp(-0.2 * box_shapes)) - 3
        box_shapes = tf.exp(box_shapes) * tf.to_float(anchors)
        confidence = tf.nn.sigmoid(confidence)
        classes = tf.nn.sigmoid(classes)
        inputs = tf.concat([box_centers, box_shapes,
                            confidence, classes], axis=-1)
        return inputs


    def upsample(self, inputs, out_shape, data_format):
        """Upsamples to `out_shape` using nearest neighbor interpolation.
        
        Arguments:
            inputs {[type]} -- [description]
            out_shape {[type]} -- [description]
            data_format {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        if data_format == 'channels_first':
            inputs = tf.transpose(inputs, [0, 2, 3, 1])
            new_height = out_shape[3]
            new_width = out_shape[2]
        else:
            new_height = out_shape[2]
            new_width = out_shape[1]

        inputs = tf.image.resize_nearest_neighbor(inputs, (new_height, new_width)) #tf.compat.v1.image.resize_nearest_neighbor(inputs, (new_height, new_width))
        if data_format == 'channels_first':
            inputs = tf.transpose(inputs, [0, 3, 1, 2])
        return inputs


    def build_boxes(self, inputs):
        """Computes top left and bottom right points of the boxes.
        
        Arguments:
            inputs {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        center_x, center_y, width, height, confidence, classes = \
            tf.split(inputs, [1, 1, 1, 1, 1, -1], axis=-1)

        if self.num_class == 1:
            classes = tf.nn.sigmoid(classes)
        else:
            classes = tf.nn.softmax(classes)

        top_left_x = center_x - width / 2
        top_left_y = center_y - height / 2
        bottom_right_x = center_x + width / 2
        bottom_right_y = center_y + height / 2 
        
        if self.lite:
            '''
            boxes = tf.concat([top_left_x, top_left_y,
                        bottom_right_x, bottom_right_y,
                        confidence, classes], axis=-1)
            tmp_boxes = boxes[:, :, :-(self.num_class + 1)]
            self.selected_indices = tf.image.non_max_suppression(tmp_boxes[0, :],
                                                                tf.squeeze(confidence[0, :]),
                                                                max_output_size = 15,
                                                                iou_threshold=0.5,
                                                                score_threshold=float('-inf'),
                                                                name=None)
            self.selected_boxes = tf.gather(boxes, self.selected_indices, axis=1)
            
            results = {} 
            results['detection_boxes'] = tf.concat([top_left_x, top_left_y, bottom_right_x, bottom_right_y], axis = -1)
            results['detection_classes'] = classes
            results['detection_scores'] = confidence
            return results
            '''
            boxes = tf.concat([top_left_x, top_left_y,
                        bottom_right_x, bottom_right_y,
                        confidence, classes], axis=-1)
            return boxes

        else: 
            selected_mask = tf.math.greater(confidence, tf.convert_to_tensor(np.array(self.threshold), tf.float32))
            total_num = tf.reduce_sum(tf.cast(selected_mask, tf.float32))
            
            #----------------------------------#
            # Remove some bbox with confidence lower than thd       
            #----------------------------------#
            confidence = tf.boolean_mask(confidence, selected_mask, axis=None)
            classes = tf.boolean_mask(classes, tf.squeeze(selected_mask, 2), axis=0)
            top_left_x = tf.boolean_mask(top_left_x, selected_mask, axis=None)
            top_left_y = tf.boolean_mask(top_left_y, selected_mask, axis=None)
            bottom_right_y = tf.boolean_mask(bottom_right_y, selected_mask, axis=None)
            bottom_right_x = tf.boolean_mask(bottom_right_x, selected_mask, axis=None)
            
            confidence = tf.reshape(tensor=confidence, shape=(-1, total_num, 1))
            classes = tf.reshape(tensor=classes, shape=(-1, total_num, self.num_class))
            top_left_x = tf.reshape(tensor=top_left_x, shape=(-1, total_num, 1))
            top_left_y = tf.reshape(tensor=top_left_y, shape=(-1, total_num, 1))
            bottom_right_x = tf.reshape(tensor=bottom_right_x, shape=(-1, total_num, 1))
            bottom_right_y = tf.reshape(tensor=bottom_right_y, shape=(-1, total_num, 1))

            boxes = tf.concat([top_left_x, top_left_y,
                        bottom_right_x, bottom_right_y,
                        confidence, classes], axis=-1)
            return boxes


    def build_yolov3_net(self, inputs, network_type, is_training):
        """method for building yolo-v3 network
        
        Returns:
            [type] -- [description]
        """
        model_size = (416, 416)
        data_format = 'channels_last'

        self.network_type = network_type
        if self.network_type == 'special': 
            self.FILTER_128 = 32
            self.FILTER_256 = 32
            self.FILTER_512 = 32
            self.FILTER_1024 = 32
        elif self.network_type == 'very_small': 
            self.FILTER_128 = 64
            self.FILTER_256 = 64
            self.FILTER_512 = 64
            self.FILTER_1024 = 64

        if self.network_type == 'special' or \
            self.network_type == 'very_small':
            route1, route2, inputs, self.yolo_special_vars = darknet53(inputs, 
                                                                        training=is_training,
                                                                        data_format=data_format, 
                                                                        network_type=network_type)
            self.yolo_very_small_vars = self.yolo_special_vars
        else:
            route1, route2, inputs, _ = self.darknet53(inputs, 
                                                    training=is_training,
                                                    data_format=data_format, 
                                                    network_type=network_type)

        self.YOLO_CONV_FILTERS = {}
        if self.network_type == 'big':
            self.YOLO_CONV_FILTERS['a'] = 512
            self.YOLO_CONV_FILTERS['b'] = 256
            self.YOLO_CONV_FILTERS['c'] = 128
        elif network_type == 'medium':
            self.YOLO_CONV_FILTERS['a'] = 512
            self.YOLO_CONV_FILTERS['b'] = 128
            self.YOLO_CONV_FILTERS['c'] = 128
        elif network_type == 'small':
            self.YOLO_CONV_FILTERS['a'] = 256
            self.YOLO_CONV_FILTERS['b'] = 128
            self.YOLO_CONV_FILTERS['c'] = 128
        elif network_type == 'very_small':
            self.YOLO_CONV_FILTERS['a'] = 128
            self.YOLO_CONV_FILTERS['b'] = 64
            self.YOLO_CONV_FILTERS['c'] = 64
        elif network_type == 'special':
            self.YOLO_CONV_FILTERS['a'] = 64
            self.YOLO_CONV_FILTERS['b'] = 32
            self.YOLO_CONV_FILTERS['c'] = 32

        self.yolo_small_vars = tf.global_variables(scope='yolo_v3_model')
        route, inputs = self.yolo_convolution_block(inputs, 
                                                filters=self.YOLO_CONV_FILTERS['a'], 
                                                training=is_training,
                                                data_format=data_format)
        inputs_detect1 = inputs
        inputs = new_conv2d_layer(input=route, 
                    filter_shape=[1, 1, route.get_shape().as_list()[-1], 256], 
                    name = 'main_input_conv13', 
                    dropout_val= self.dropout_val, 
                    activation = 'LRELU',
                    padding='SAME', 
                    strides=[1, 1, 1, 1], 
                    data_type=tf.float32, 
                    is_training=is_training,
                    use_bias=False,
                    use_batchnorm=True)

        upsample_size = route2.get_shape().as_list()
        inputs = self.upsample(inputs, 
                            out_shape=upsample_size,
                            data_format=data_format)
        axis = 3
        inputs = tf.concat([inputs, route2], axis=axis)

        self.yolo_medium_vars = tf.global_variables(scope='yolo_v3_model')
        route, inputs = self.yolo_convolution_block(inputs, 
                                                filters=self.YOLO_CONV_FILTERS['b'],  
                                                training=is_training,
                                                data_format=data_format)

        inputs_detect2 = inputs
        inputs = new_conv2d_layer(input=route, 
                                    filter_shape=[1, 1, route.get_shape().as_list()[-1], 128], 
                                    name = 'main_input_conv14', 
                                    dropout_val= self.dropout_val, 
                                    activation = 'LRELU',
                                    padding='SAME', 
                                    strides=[1, 1, 1, 1],
                                    data_type=tf.float32,
                                    is_training=is_training,
                                    use_bias=False,
                                    use_batchnorm=True)
        upsample_size = route1.get_shape().as_list()

        inputs = self.upsample(inputs, 
                            out_shape=upsample_size,
                            data_format=data_format)
        inputs = tf.concat([inputs, route1], axis=axis)
        route, inputs = self.yolo_convolution_block(inputs, 
                                                filters=self.YOLO_CONV_FILTERS['c'], 
                                                training=is_training,
                                                data_format=data_format)

        self.yolo_big_vars = tf.global_variables(scope='yolo_v3_model')
        self.yolo_vars = tf.global_variables(scope='yolo_v3_model')

        inputs_detect3 = inputs

        if self.is_multilabel: 
            total_properties = 6 #sum(self.multilabel_dict.values)
            OUTPUT_DEPTH = int(len(self.anchor)/3 * (5 + self.num_class + total_properties))
        else: 
            OUTPUT_DEPTH = int(len(self.anchor)/3 * (5 + self.num_class))
        
        self.detect1 = tf.layers.conv2d(inputs_detect1, 
                                    filters=OUTPUT_DEPTH,
                                    kernel_size=1, 
                                    strides=1, 
                                    use_bias=True,
                                    data_format=data_format)
     
        self.detect2 = tf.layers.conv2d(inputs_detect2, 
                                    filters=OUTPUT_DEPTH,
                                    kernel_size=1, 
                                    strides=1, 
                                    use_bias=True,
                                    data_format=data_format)

        self.detect3 = tf.layers.conv2d(inputs_detect3, 
                                    filters=OUTPUT_DEPTH,
                                    kernel_size=1, 
                                    strides=1, 
                                    use_bias=True,
                                    data_format=data_format)

        """  
        self.detect1 = new_conv2d_layer(input=inputs_detect1, 
                                    filter_shape=[1, 1, inputs_detect1.get_shape().as_list()[-1], OUTPUT_DEPTH], 
                                    name = 'detect1_conv', 
                                    dropout_val= self.dropout_val, 
                                    activation = 'None',
                                    padding='VALID', 
                                    strides=[1, 1, 1, 1],
                                    is_training=is_training,
                                    use_bias=True,
                                    use_batchnorm=False)
        self.detect2 = new_conv2d_layer(input=inputs_detect2, 
                                    filter_shape=[1, 1, inputs_detect2.get_shape().as_list()[-1], OUTPUT_DEPTH], 
                                    name = 'detect2_conv', 
                                    dropout_val= self.dropout_val, 
                                    activation = 'None',
                                    padding='VALID', 
                                    strides=[1, 1, 1, 1],
                                    is_training=is_training,
                                    use_bias=True,
                                    use_batchnorm=False)
        self.detect3 = new_conv2d_layer(input=inputs_detect3, 
                                    filter_shape=[1, 1, inputs_detect3.get_shape().as_list()[-1], OUTPUT_DEPTH], 
                                    name = 'detect2_conv', 
                                    dropout_val= self.dropout_val, 
                                    activation = 'None',
                                    padding='VALID', 
                                    strides=[1, 1, 1, 1],
                                    is_training=is_training,
                                    use_bias=True,
                                    use_batchnorm=False)
        """
        self.output_list = [self.detect1, self.detect2, self.detect3]
        
        combine_box1 = self.yolo_layer(self.detect1, 
                                n_classes=self.num_class,
                                anchors=self.anchor[6:9],
                                img_size=model_size,
                                data_format=data_format)
        combine_box2 = self.yolo_layer(self.detect2, 
                                n_classes=self.num_class,
                                anchors=self.anchor[3:6],
                                img_size=model_size,
                                data_format=data_format)
        combine_box3 = self.yolo_layer(self.detect3, 
                                n_classes=self.num_class,
                                anchors=self.anchor[0:3],
                                img_size=model_size,
                                data_format=data_format)
        
        if self.lite: 
            inputs = combine_box1
        else: 
            inputs = tf.concat([combine_box1, combine_box2, combine_box3], axis=1)
        self.boxes_dicts = self.build_boxes(inputs)


    def build_yolov3_net2(self, inputs, network_type, is_training):
        """method for building yolo-v3 network
        
        Returns:
            [type] -- [description]
        """
        print ("=====================================")
        print ("Using Old Version")
        print ("=====================================")
        model_size = (416, 416)
        max_output_size = 10
        data_format = 'channels_last'


        # -------------------------------------------- #
        # Function for giving hard padding             #
        # It is applied on original yolo network       #
        # -------------------------------------------- #
        def fixed_padding(inputs, 
                          kernel_size, 
                          data_format):
            """ResNet implementation of fixed padding.
            Pads the input along the spatial dimensions independently of input size.

            Args:
                inputs: Tensor input to be padded.
                kernel_size: The kernel to be used in the conv2d or max_pool2d.
                data_format: The input format.
            Returns:
                A tensor with the same format as the input.
            """
            pad_total = kernel_size - 1
            pad_beg = pad_total // 2
            pad_end = pad_total - pad_beg

            if data_format == 'channels_first':
                padded_inputs = tf.pad(inputs, [[0, 0], [0, 0],
                                                [pad_beg, pad_end],
                                                [pad_beg, pad_end]])
            else:
                padded_inputs = tf.pad(inputs, [[0, 0], [pad_beg, pad_end],
                                                [pad_beg, pad_end], [0, 0]])
            return padded_inputs
        
        # --------------------------------------- #
        # For building darknet 53 residual block  #
        # --------------------------------------- #           
        def darknet53_residual_block(inputs, 
                                     filters, 
                                     training, 
                                     data_format, 
                                     stride=1, 
                                     name='res'):
            """[summary]
            Arguments:
                inputs {[tensor]} -- input tensor
                filters {[tensor]} -- the filter tensor
                training {[bool]} -- the phase, training or not
                data_format {[string]} -- channel first or not
            
            Keyword Arguments:
                stride {int} -- [the strides] (default: {1})
                name {str} -- [the additional name for all tensors in this block] (default: {'res'})
            
            Returns:
                [type] -- [description]
            """
            shortcut = inputs
            
            inputs = new_conv2d_layer(input=inputs, 
                            filter_shape=[1, 1, inputs.get_shape().as_list()[-1], filters], 
                            name = name + '_input_conv1', 
                            dropout_val= self.dropout_val, 
                            activation = 'LRELU', 
                            lrelu_alpha= self.leaky_relu_alpha, 
                            padding=('SAME' if stride == 1 else 'VALID'), 
                            strides=[1, stride, stride, 1],  
                            is_training=training,
                            use_bias=False,
                            use_batchnorm=True)
            
            inputs = new_conv2d_layer(input=(inputs if stride == 1 else fixed_padding(inputs, 3, 'channels_last')), 
                            filter_shape=[3, 3, inputs.get_shape().as_list()[-1], shortcut.get_shape().as_list()[-1]], 
                            name = name + '_input_conv2', 
                            dropout_val= self.dropout_val, 
                            activation = 'LRELU',
                            lrelu_alpha=self.leaky_relu_alpha, 
                            padding=('SAME' if stride == 1 else 'VALID'), 
                            strides=[1, stride, stride, 1],
                            data_type=tf.float32,  
                            is_training=training,
                            use_bias=False,
                            use_batchnorm=True)

            inputs += shortcut
            return inputs
        
        # ------------------------------------- #
        # function for building main darknet 53 #
        # ------------------------------------- #
        def darknet53(inputs, training, data_format, network_type):
            """[summary]
            
            Arguments:
                inputs {tensor} -- the input tensor
                training {bool} -- the phase, training or not
                data_format {string} -- channel_first or not
            
            Returns:
                [type] -- [description]
            """
            inputs = new_conv2d_layer(input=inputs, 
                            filter_shape=[3, 3, inputs.get_shape().as_list()[-1], 32], 
                            name = 'main_input_conv1', 
                            dropout_val= self.dropout_val, 
                            activation = 'LRELU',
                            lrelu_alpha=self.leaky_relu_alpha,  
                            padding='SAME', 
                            strides=[1, 1, 1, 1],
                            data_type=tf.float32,  
                            is_training=training,
                            use_bias=False,
                            use_batchnorm=True)

            inputs = new_conv2d_layer(input=fixed_padding(inputs, 3, 'channels_last'), 
                            filter_shape=[3, 3, inputs.get_shape().as_list()[-1], 64], 
                            name = 'main_input_conv2', 
                            dropout_val= self.dropout_val, 
                            activation = 'LRELU',
                            lrelu_alpha=self.leaky_relu_alpha,  
                            padding='VALID', 
                            strides=[1, 2, 2, 1],
                            data_type=tf.float32,  
                            is_training=training,
                            use_bias=False,
                            use_batchnorm=True)

            inputs = darknet53_residual_block(inputs, 
                                              filters=32, 
                                              training=training,
                                              data_format=data_format, 
                                              name='res1')

            inputs = new_conv2d_layer(input=fixed_padding(inputs, 3, 'channels_last'), 
                            filter_shape=[3, 3, inputs.get_shape().as_list()[-1], 128], 
                            name = 'main_input_conv3', 
                            dropout_val= self.dropout_val, 
                            activation = 'LRELU',
                            lrelu_alpha=self.leaky_relu_alpha, 
                            padding='VALID', 
                            strides=[1, 2, 2, 1],
                            data_type=tf.float32,  
                            is_training=training,
                            use_bias=False,
                            use_batchnorm=True)

            for i in range(2):
                inputs = darknet53_residual_block(inputs, 
                                                  filters=64,
                                                  training=training,
                                                  data_format=data_format, 
                                                  name='res' + str(i+1))
                
            inputs = new_conv2d_layer(input=fixed_padding(inputs, 3, 'channels_last'), 
                            filter_shape=[3, 3, inputs.get_shape().as_list()[-1], 256], 
                            name = 'main_input_conv4', 
                            dropout_val= self.dropout_val, 
                            activation = 'LRELU',
                            lrelu_alpha=self.leaky_relu_alpha, 
                            padding='VALID', 
                            strides=[1, 2, 2, 1],
                            data_type=tf.float32,  
                            is_training=training,
                            use_bias=False,
                            use_batchnorm=True)

            filter_128 = 128
            filter_256 = 256
            filter_512 = 512
            filter_1024 = 1024
            return_vars = None
            if network_type == 'special':
                filter_128 = 32
                filter_256 = 32
                filter_512 = 32
                filter_1024 = 32
                return_vars = tf.global_variables(scope='yolo_v3_model')
            elif network_type == 'very_small':
                filter_128 = 64
                filter_256 = 64
                filter_512 = 64
                filter_1024 = 64
                return_vars = tf.global_variables(scope='yolo_v3_model')

            for i in range(8):
                inputs = darknet53_residual_block(inputs, 
                                                  filters=filter_128,
                                                  training=training,
                                                  data_format=data_format, 
                                                  name='res' + str(i+3))

            route1 = inputs
            inputs = new_conv2d_layer(input=fixed_padding(inputs, 3, 'channels_last'), 
                            filter_shape=[3, 3, inputs.get_shape().as_list()[-1], filter_512], 
                            name = 'main_input_conv5', 
                            dropout_val= self.dropout_val, 
                            activation = 'LRELU',
                            lrelu_alpha=self.leaky_relu_alpha,
                            padding='VALID', 
                            strides=[1, 2, 2, 1],
                            data_type=tf.float32,  
                            is_training=training,
                            use_bias=False,
                            use_batchnorm=True)
            
            for i in range(8):
                inputs = darknet53_residual_block(inputs, 
                                                  filters=filter_256,
                                                  training=training,
                                                  data_format=data_format, 
                                                  name='res' + str(i+11))

            route2 = inputs
            inputs = new_conv2d_layer(input=fixed_padding(inputs, 3, 'channels_last'), 
                            filter_shape=[3, 3, inputs.get_shape().as_list()[-1], filter_1024], 
                            name = 'main_input_conv6', 
                            dropout_val= self.dropout_val, 
                            activation = 'LRELU',
                            lrelu_alpha=self.leaky_relu_alpha, 
                            padding='VALID', 
                            strides=[1, 2, 2, 1],
                            data_type=tf.float32,  
                            is_training=training,
                            use_bias=False,
                            use_batchnorm=True)

            for i in range(4):
                inputs = darknet53_residual_block(inputs, filters=filter_512,
                                                training=training,
                                                data_format=data_format, name='res' + str(i+19))
            return route1, route2, inputs, return_vars
        
        #---------------------------------------- 
        def yolo_convolution_block(inputs, filters, training, data_format):
            """[summary]
            
            Arguments:
                inputs {[type]} -- [description]
                filters {[type]} -- [description]
                training {[type]} -- [description]
                data_format {[type]} -- [description]
            
            Returns:
                [type] -- [description]
            """
            inputs = new_conv2d_layer(input=inputs, 
                            filter_shape=[1, 1, inputs.get_shape().as_list()[-1], filters], 
                            name = 'main_input_conv7', 
                            dropout_val= self.dropout_val, 
                            activation = 'LRELU',
                            lrelu_alpha=self.leaky_relu_alpha,
                            padding='SAME', 
                            strides=[1, 1, 1, 1],
                            data_type=tf.float32,  
                            is_training=training,
                            use_bias=False,
                            use_batchnorm=True)
        
            inputs = new_conv2d_layer(input=inputs, 
                            filter_shape=[3, 3, inputs.get_shape().as_list()[-1], 2*filters], 
                            name = 'main_input_conv8', 
                            dropout_val= self.dropout_val, 
                            activation = 'LRELU',
                            lrelu_alpha=self.leaky_relu_alpha,
                            padding='SAME', 
                            strides=[1, 1, 1, 1],
                            data_type=tf.float32,  
                            is_training=training,
                            use_bias=False,
                            use_batchnorm=True)
            
            inputs = new_conv2d_layer(input=inputs, 
                            filter_shape=[1, 1, inputs.get_shape().as_list()[-1], filters], 
                            name = 'main_input_conv9', 
                            dropout_val= self.dropout_val, 
                            activation = 'LRELU',
                            lrelu_alpha=self.leaky_relu_alpha,
                            padding='SAME', 
                            strides=[1, 1, 1, 1],
                            data_type=tf.float32,  
                            is_training=training,
                            use_bias=False,
                            use_batchnorm=True)
            
            inputs = new_conv2d_layer(input=inputs, 
                            filter_shape=[3, 3, inputs.get_shape().as_list()[-1], 2*filters], 
                            name = 'main_input_conv10', 
                            dropout_val= self.dropout_val, 
                            activation = 'LRELU',
                            lrelu_alpha=self.leaky_relu_alpha, 
                            padding='SAME', 
                            strides=[1, 1, 1, 1],
                            data_type=tf.float32,  
                            is_training=training,
                            use_bias=False,
                            use_batchnorm=True)
            
            inputs = new_conv2d_layer(input=inputs, 
                            filter_shape=[1, 1, inputs.get_shape().as_list()[-1], filters], 
                            name = 'main_input_conv11', 
                            dropout_val= self.dropout_val, 
                            activation = 'LRELU',
                            lrelu_alpha=self.leaky_relu_alpha, 
                            padding='SAME', 
                            strides=[1, 1, 1, 1],
                            data_type=tf.float32,  
                            is_training=training,
                            use_bias=False,
                            use_batchnorm=True)

            route = inputs
            inputs = new_conv2d_layer(input=inputs, 
                            filter_shape=[3, 3, inputs.get_shape().as_list()[-1], 2*filters], 
                            name = 'main_input_conv12', 
                            dropout_val= self.dropout_val, 
                            activation = 'LRELU',
                            lrelu_alpha=self.leaky_relu_alpha, 
                            padding='SAME', 
                            strides=[1, 1, 1, 1],
                            data_type=tf.float32,  
                            is_training=training,
                            use_bias=False,
                            use_batchnorm=True)
                        
            return route, inputs
        
        #-----------------------------------#
        def yolo_layer(inputs, n_classes, anchors, img_size, data_format):
            """Creates Yolo final detection layer.

            Detects boxes with respect to anchors.

            Args:
                inputs: Tensor input.
                n_classes: Number of labels.
                anchors: A list of anchor sizes.
                img_size: The input size of the model.
                data_format: The input format.

            Returns:
                Tensor output.
            """
            
            n_anchors = len(anchors)
            shape = inputs.get_shape().as_list()
            grid_shape = shape[2:4] if data_format == 'channels_first' else shape[1:3]
            if data_format == 'channels_first':
                inputs = tf.transpose(inputs, [0, 2, 3, 1])

            strides = (img_size[0] // grid_shape[0], img_size[1] // grid_shape[1])

            if self.is_multilabel: 
                inputs = tf.reshape(inputs, [-1, n_anchors * grid_shape[0] * grid_shape[1], 5 + n_classes + sum(self.multilabel_dict.values())])
                box_centers, box_shapes, confidence, classes = tf.split(inputs, [2, 2, 1, n_classes + sum(self.multilabel_dict.values())], axis=-1)
            else: 
                inputs = tf.reshape(inputs, [-1, n_anchors * grid_shape[0] * grid_shape[1], 5 + n_classes])
                box_centers, box_shapes, confidence, classes = tf.split(inputs, [2, 2, 1, n_classes], axis=-1)

            x = tf.range(grid_shape[0], dtype=tf.float32)
            y = tf.range(grid_shape[1], dtype=tf.float32)
            x_offset, y_offset = tf.meshgrid(x, y)
            x_offset = tf.reshape(x_offset, (-1, 1))
            y_offset = tf.reshape(y_offset, (-1, 1))
            x_y_offset = tf.concat([x_offset, y_offset], axis=-1)
            x_y_offset = tf.tile(x_y_offset, [1, n_anchors])
            x_y_offset = tf.reshape(x_y_offset, [1, -1, 2])
            box_centers = tf.nn.sigmoid(box_centers)
            box_centers = (box_centers + x_y_offset) * strides

            anchors = tf.tile(anchors, [grid_shape[0] * grid_shape[1], 1])
            if self.add_modsig_toshape:
                box_shapes = 6 /(1 + tf.exp(-0.2 * box_shapes)) - 3
            box_shapes = tf.exp(box_shapes) * tf.to_float(anchors)
            confidence = tf.nn.sigmoid(confidence)
            inputs = tf.concat([box_centers, box_shapes,
                                confidence, classes], axis=-1)

            return inputs

        #---------------------------------------------#
        def upsample(inputs, out_shape, data_format):
            """Upsamples to `out_shape` using nearest neighbor interpolation.
            
            Arguments:
                inputs {[type]} -- [description]
                out_shape {[type]} -- [description]
                data_format {[type]} -- [description]
            
            Returns:
                [type] -- [description]
            """
            if data_format == 'channels_first':
                inputs = tf.transpose(inputs, [0, 2, 3, 1])
                new_height = out_shape[3]
                new_width = out_shape[2]
            else:
                new_height = out_shape[2]
                new_width = out_shape[1]

            inputs = tf.image.resize_nearest_neighbor(inputs, (new_height, new_width))
            if data_format == 'channels_first':
                inputs = tf.transpose(inputs, [0, 3, 1, 2])
            return inputs
        
        #------------------------------------------------#
        def build_boxes(inputs):
            """Computes top left and bottom right points of the boxes.
            
            Arguments:
                inputs {[type]} -- [description]
            
            Returns:
                [type] -- [description]
            """
            center_x, center_y, width, height, confidence, classes_all = \
                tf.split(inputs, [1, 1, 1, 1, 1, -1], axis=-1)

            additional_class = []
            if self.is_multilabel: 
                classes = classes_all[:, :, :self.num_class]
                base = self.num_class

                for i in self.multilabel_dict.values(): 
                    additional_class.append(tf.nn.softmax(classes_all[:, :, base:base + i]))
                    base = base + i
            else: 
                classes = classes_all

            if self.num_class == 1:
                classes = tf.nn.sigmoid(classes)
            else:
                classes = tf.nn.softmax(classes)

            top_left_x = center_x - width / 2
            top_left_y = center_y - height / 2
            bottom_right_x = center_x + width / 2
            bottom_right_y = center_y + height / 2 
            
            if self.lite:
                '''
                boxes = tf.concat([top_left_x, top_left_y,
                            bottom_right_x, bottom_right_y,
                            confidence, classes], axis=-1)
                tmp_boxes = boxes[:, :, :-(self.num_class + 1)]
                self.selected_indices = tf.image.non_max_suppression(tmp_boxes[0, :],
                                                                    tf.squeeze(confidence[0, :]),
                                                                    max_output_size = 15,
                                                                    iou_threshold=0.5,
                                                                    score_threshold=float('-inf'),
                                                                    name=None)
                self.selected_boxes = tf.gather(boxes, self.selected_indices, axis=1)
                
                results = {} 
                results['detection_boxes'] = tf.concat([top_left_x, top_left_y, bottom_right_x, bottom_right_y], axis = -1)
                results['detection_classes'] = classes
                results['detection_scores'] = confidence
                return results
                '''
                boxes = tf.concat([top_left_x, top_left_y,
                            bottom_right_x, bottom_right_y,
                            confidence, classes], axis=-1)
                return boxes

            else: 
                selected_mask = tf.math.greater(confidence, tf.convert_to_tensor(np.array(self.threshold), tf.float32))
                total_num = tf.reduce_sum(tf.cast(selected_mask, tf.float32)) 
                
                #----------------------------------#
                # Remove some bbox with confidence lower than thd       
                #----------------------------------#
                confidence = tf.boolean_mask(confidence, selected_mask, axis=None)
                classes = tf.boolean_mask(classes, tf.squeeze(selected_mask, 2), axis=0)
                top_left_x = tf.boolean_mask(top_left_x, selected_mask, axis=None)
                top_left_y = tf.boolean_mask(top_left_y, selected_mask, axis=None)
                bottom_right_y = tf.boolean_mask(bottom_right_y, selected_mask, axis=None)
                bottom_right_x = tf.boolean_mask(bottom_right_x, selected_mask, axis=None)
                
                confidence = tf.reshape(tensor=confidence, shape=(-1, total_num, 1))
                classes = tf.reshape(tensor=classes, shape=(-1, total_num, self.num_class))
                top_left_x = tf.reshape(tensor=top_left_x, shape=(-1, total_num, 1))
                top_left_y = tf.reshape(tensor=top_left_y, shape=(-1, total_num, 1))
                bottom_right_x = tf.reshape(tensor=bottom_right_x, shape=(-1, total_num, 1))
                bottom_right_y = tf.reshape(tensor=bottom_right_y, shape=(-1, total_num, 1))

                for idx, i in enumerate(additional_class): 
                    tmp = tf.boolean_mask(i, tf.squeeze(selected_mask, 2), axis=0)
                    additional_class[idx] = tf.reshape(tensor=tmp, shape=(-1, total_num, list(self.multilabel_dict.values())[idx]))

                boxes = tf.concat([top_left_x, top_left_y,
                            bottom_right_x, bottom_right_y,
                            confidence, classes] + additional_class, axis=-1)

                return boxes
        #--------------------------------------------------#

        #----------------------------------#
        #     Network Type Choiches        #
        #----------------------------------#
        filters = {}
        if network_type == 'big':
            filters['a'] = 512
            filters['b'] = 256
            filters['c'] = 128
        elif network_type == 'medium':
            filters['a'] = 512
            filters['b'] = 128
            filters['c'] = 128
        elif network_type == 'small':
            filters['a'] = 256
            filters['b'] = 128
            filters['c'] = 128
        elif network_type == 'very_small':
            filters['a'] = 128
            filters['b'] = 64
            filters['c'] = 64
        elif network_type == 'special':
            filters['a'] = 64
            filters['b'] = 32
            filters['c'] = 32
        #---------------------------------#
        if network_type == 'special' or network_type == 'very_small':
            route1, route2, inputs, self.yolo_special_vars = darknet53(inputs, 
                                                                     training=is_training,
                                                                     data_format=data_format, 
                                                                     network_type=network_type)
            self.yolo_very_small_vars = self.yolo_special_vars
        else:
            route1, route2, inputs, _ = darknet53(inputs, 
                                                  training=is_training,
                                                  data_format=data_format, 
                                                  network_type=network_type)

        #-------------------------------------#
        #     get yolo small variables        #
        #-------------------------------------#
        self.yolo_small_vars = tf.global_variables(scope='yolo_v3_model')
        route, inputs = yolo_convolution_block(inputs, 
                                                filters=filters['a'], 
                                                training=is_training,
                                                data_format=data_format)
        inputs_detect1 = inputs

        inputs = new_conv2d_layer(input=route, 
                    filter_shape=[1, 1, route.get_shape().as_list()[-1], 256], 
                    name = 'main_input_conv13', 
                    dropout_val= self.dropout_val, 
                    activation = 'LRELU',
                    lrelu_alpha=self.leaky_relu_alpha,
                    padding='SAME', 
                    strides=[1, 1, 1, 1],
                    data_type=tf.float32,  
                    is_training=is_training,
                    use_bias=False,
                    use_batchnorm=True)

        upsample_size = route2.get_shape().as_list()
        inputs = upsample(inputs, 
                            out_shape=upsample_size,
                            data_format=data_format)
        axis = 3
        inputs = tf.concat([inputs, route2], axis=axis)

        #-------------------------------------#
        #     get yolo medium variables       #
        #-------------------------------------#
        self.yolo_medium_vars = tf.global_variables(scope='yolo_v3_model')
        route, inputs = yolo_convolution_block(inputs, 
                                                filters=filters['b'],  
                                                training=is_training,
                                                data_format=data_format)
        inputs_detect2 = inputs
        
        inputs = new_conv2d_layer(input=route, 
                                    filter_shape=[1, 1, route.get_shape().as_list()[-1], 128], 
                                    name = 'main_input_conv14', 
                                    dropout_val= self.dropout_val, 
                                    activation = 'LRELU',
                                    lrelu_alpha=self.leaky_relu_alpha,
                                    padding='SAME', 
                                    strides=[1, 1, 1, 1],
                                    data_type=tf.float32,  
                                    is_training=is_training,
                                    use_bias=False,
                                    use_batchnorm=True)
        
        upsample_size = route1.get_shape().as_list()
        inputs = upsample(inputs, 
                            out_shape=upsample_size,
                            data_format=data_format)
        inputs = tf.concat([inputs, route1], axis=axis)
        route, inputs = yolo_convolution_block(inputs, 
                                                filters=filters['c'], 
                                                training=is_training,
                                                data_format=data_format)
        inputs_detect3 = inputs

        #-------------------------------------#
        #       get yolo big variables        #
        #       get yolo all variables        #
        #-------------------------------------#
        self.yolo_big_vars = tf.global_variables(scope='yolo_v3_model')
        self.yolo_vars = tf.global_variables(scope='yolo_v3_model')


        if self.is_multilabel: 
            total_properties = 6 #sum(self.multilabel_dict.values)
            OUTPUT_DEPTH = int(len(self.anchor)/3 * (5 + self.num_class + total_properties))
        else: 
            OUTPUT_DEPTH = int(len(self.anchor)/3 * (5 + self.num_class))

        """
        self.detect1 = tf.layers.conv2d(inputs_detect1, 
                                    filters=OUTPUT_DEPTH,
                                    kernel_size=1, 
                                    strides=1, 
                                    use_bias=True,
                                    data_format=data_format)
     
        self.detect2 = tf.layers.conv2d(inputs_detect2, 
                                    filters=OUTPUT_DEPTH,
                                    kernel_size=1, 
                                    strides=1, 
                                    use_bias=True,
                                    data_format=data_format)

        self.detect3 = tf.layers.conv2d(inputs_detect3, 
                                    filters=OUTPUT_DEPTH,
                                    kernel_size=1, 
                                    strides=1, 
                                    use_bias=True,
                                    data_format=data_format)
        """
        self.detect1 = new_conv2d_layer(input=inputs_detect1, 
                                    filter_shape=[1, 1, inputs_detect1.get_shape().as_list()[-1], OUTPUT_DEPTH], 
                                    name = 'detect1_conv', 
                                    dropout_val= self.dropout_val, 
                                    activation = 'None',
                                    padding='VALID', 
                                    strides=[1, 1, 1, 1],
                                    is_training=is_training,
                                    use_bias=True,
                                    use_batchnorm=False)
        self.detect2 = new_conv2d_layer(input=inputs_detect2, 
                                    filter_shape=[1, 1, inputs_detect2.get_shape().as_list()[-1], OUTPUT_DEPTH], 
                                    name = 'detect2_conv', 
                                    dropout_val= self.dropout_val, 
                                    activation = 'None',
                                    padding='VALID', 
                                    strides=[1, 1, 1, 1],
                                    is_training=is_training,
                                    use_bias=True,
                                    use_batchnorm=False)
        self.detect3 = new_conv2d_layer(input=inputs_detect3, 
                                    filter_shape=[1, 1, inputs_detect3.get_shape().as_list()[-1], OUTPUT_DEPTH], 
                                    name = 'detect2_conv', 
                                    dropout_val= self.dropout_val, 
                                    activation = 'None',
                                    padding='VALID', 
                                    strides=[1, 1, 1, 1],
                                    is_training=is_training,
                                    use_bias=True,
                                    use_batchnorm=False)
        self.output_list = [self.detect1, self.detect2, self.detect3]

        combine_box1 = yolo_layer(self.detect1, 
                                n_classes=self.num_class,
                                anchors=self.anchor[6:9],
                                img_size=model_size,
                                data_format=data_format)
        combine_box2 = yolo_layer(self.detect2, 
                                n_classes=self.num_class,
                                anchors=self.anchor[3:6],
                                img_size=model_size,
                                data_format=data_format)
        combine_box3 = yolo_layer(self.detect3, 
                                n_classes=self.num_class,
                                anchors=self.anchor[0:3],
                                img_size=model_size,
                                data_format=data_format)
        
        if self.lite: 
            inputs = combine_box1
        else: 
            inputs = tf.concat([combine_box1, combine_box2, combine_box3], axis=1)
        self.boxes_dicts = build_boxes(inputs)













