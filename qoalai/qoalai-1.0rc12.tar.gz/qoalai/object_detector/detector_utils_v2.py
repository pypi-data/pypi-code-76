'''
    File name: detector_utils.py
    Author: [DS Team]
    Date created: / /2019
    Date last modified: 16/08/2019
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
from qoalai.tensor_metrics import calculate_acc
from qoalai.tensor_losses import softmax_crosentropy_sum, sigmoid_crossentropy_sum, mse_loss_sum
from qoalai.tensor_losses import softmax_crosentropy_mean, sigmoid_crossentropy_mean, mse_loss_mean  
from .network import YoloNetwork 


class ObjectDetector(YoloNetwork): 
    def __init__(self, num_of_class,
                       input_height=416, 
                       input_width=416, 
                       grid_height1=32, 
                       grid_width1=32, 
                       grid_height2=16, 
                       grid_width2=16, 
                       grid_height3=8, 
                       grid_width3=8,
                       objectness_loss_alpha=2., 
                       noobjectness_loss_alpha=1., 
                       center_loss_alpha=1., 
                       size_loss_alpha=1., 
                       class_loss_alpha=1.,
                       add_modsig_toshape=True,
                       anchor = [(10, 13), (16, 30), (33, 23), (30, 61), (62, 45), (59, 119), (116, 90), (156, 198), (373, 326)],
                       dropout_rate = 0.0,
                       leaky_relu_alpha = 0.1,
                       threshold = 0.5,
                       convert_to_tflite=False,
                       is_multilabel=False,
                       multilabel_dict=None):
        """[summary]
        
        Arguments:
            num_of_class {int} -- the number of the class
        
        Keyword Arguments:
            input_height {int} -- [the height of input image in pixel] (default: {416})
            input_width {int} -- [the width of input image in pixel] (default: {416})
            grid_height1 {int} -- [the height of the 1st detector grid in pixel] (default: {32})
            grid_width1 {int} -- [the width of the 1st detector grid in pixel] (default: {32})
            grid_height2 {int} -- [the height of the 2nd detector grid in pixel] (default: {16})
            grid_width2 {int} -- [the width of the 2nd detector grid in pixel] (default: {16})
            grid_height3 {int} -- [the height of the 3rd detector grid in pixel] (default: {8})
            grid_width3 {int} -- [the width of the 3rd detector grid in pixel] (default: {8})
            objectness_loss_alpha {[float]} -- [the alpha for the objectness loss] (default: {2.})
            noobjectness_loss_alpha {[float]} -- [the alpha for the noobjectness loss] (default: {1.})
            center_loss_alpha {[float]} -- [the alpha for the center loss] (default: {1.})
            size_loss_alpha {[float]} -- [the alpha for the size loss] (default: {1.})
            class_loss_alpha {[float]} -- [the alpha for the class loss] (default: {1.})
            add_modsig_toshape{bool} -- ADD sigmoid modification to avoid nan loss or not
            anchor {list of tupple} -- [the list of tupple of the height and weight of anchors] (default: {[(10, 13), (16, 30), 
                                                                                                            (33, 23), (30, 61), 
                                                                                                            (62, 45), (59, 119), 
                                                                                                            (116, 90), (156, 198), 
                                                                                                            (373, 326)]})
            dropout_rate {float} -- the rate of the dropout
            leaky_relu_alpha {float} -- the alpha of leaky relu
            convert_to_tf_lite {bool} -- TF lite standard network or note
            is_multilabel {bool} -- multilable or not
            multilabel_dic -- python dictionary if multilble

        Returns:
            [type] -- [description]
        """      
        super(ObjectDetector, self).__init__(num_of_class,
                                                is_multilabel = is_multilabel,
                                                multilabel_dict = multilabel_dict,
                                                anchor = anchor, 
                                                dropout_val = 1. - dropout_rate,
                                                threshold= threshold,
                                                leaky_relu_alpha=leaky_relu_alpha,
                                                add_modsig_toshape = add_modsig_toshape,
                                                convert_to_tflite=convert_to_tflite)

        # ----------------------------- #
        # initialize all properties     #
        # - grid_relatif_width/height is the relative width/height of the grid to the image
        # - num_vertical/horizontal_grid is the number of vertical/horizontal grid in an image
        # - add_modsig_toshape is a boolean flag of adding modified sigmoid to the w/h 
        # ----------------------------- #
        self.input_height = input_height
        self.input_width = input_width
        
        self.grid_height = []
        self.grid_height.append(grid_height1)
        self.grid_height.append(grid_height2)
        self.grid_height.append(grid_height3)

        self.grid_width = []
        self.grid_width.append(grid_width1)
        self.grid_width.append(grid_width2)
        self.grid_width.append(grid_width3)
        
        self.grid_relatif_width = []
        self.grid_relatif_height = []
        for i in range (3):
            self.grid_relatif_width.append(self.grid_width[i] / self.input_width)
            self.grid_relatif_height.append(self.grid_height[i] / self.input_height)

        self.num_vertical_grid = []
        self.num_horizontal_grid = []
        for i in range(3):
            self.num_vertical_grid.append(int(math.floor(self.input_height/self.grid_height[i])))
            self.num_horizontal_grid.append(int(math.floor(self.input_width/self.grid_width[i])))

        self.grid_mask()

        self.objectness_loss_alpha = objectness_loss_alpha
        self.noobjectness_loss_alpha = noobjectness_loss_alpha
        self.center_loss_alpha = center_loss_alpha
        self.size_loss_alpha = size_loss_alpha
        self.class_loss_alpha = class_loss_alpha


    def grid_mask(self):
        """Method for creating the position mask of grids
        """
        self.grid_position_mask_onx_np = []
        self.grid_position_mask_ony_np = []
        self.grid_position_mask_onx = []
        self.grid_position_mask_ony = []

        for i in range(3):
            self.grid_position_mask_onx_np.append(np.zeros((1, self.num_vertical_grid[i] , self.num_horizontal_grid[i] , 1)))
            self.grid_position_mask_ony_np.append(np.zeros((1, self.num_vertical_grid[i] , self.num_horizontal_grid[i] , 1)))

            for j in range(self.num_vertical_grid[i]):
                for k in range(self.num_horizontal_grid[i]):
                    self.grid_position_mask_onx_np[i][:, j, k, :] = k
                    self.grid_position_mask_ony_np[i][:, j, k, :] = j

            self.grid_position_mask_onx.append(tf.convert_to_tensor(self.grid_position_mask_onx_np[i], dtype=tf.float32))
            self.grid_position_mask_ony.append(tf.convert_to_tensor(self.grid_position_mask_ony_np[i], dtype=tf.float32))


    def iou(self, bbox_pred, bbox_label):
        """[summary]
        
        Arguments:
            bbox_pred {[type]} -- [description]
            bbox_label {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        #------------------------------------------------------------------#
        # get the top left and bootom right of prediction result and label #
        # calculate the overlap and union                                  #
        # calculate the iou                                                #
        #------------------------------------------------------------------#
        x_topleft_pred = tf.maximum(bbox_pred[:, :, :, 0:1] - 0.5 * bbox_pred[:, :, :, 2:3], 0.0)
        y_topleft_pred = tf.maximum(bbox_pred[:, :, :, 1:2] - 0.5 * bbox_pred[:, :, :, 3:], 0.0)
        x_bottomright_pred = tf.minimum(bbox_pred[:, :, :, 0:1] + 0.5 * bbox_pred[:, :, :, 2:3], self.input_width)
        y_bottomright_pred = tf.minimum(bbox_pred[:, :, :, 1:2] + 0.5 * bbox_pred[:, :, :, 3:], self.input_height)

        x_topleft_label = tf.maximum(bbox_label[:, :, :, 0:1] - 0.5 * bbox_label[:, :, :, 2:3], 0.0)
        y_topleft_label = tf.maximum(bbox_label[:, :, :, 1:2] - 0.5 * bbox_label[:, :, :, 3:], 0.0)
        x_bottomright_label = tf.minimum(bbox_label[:, :, :, 0:1] + 0.5 * bbox_label[:, :, :, 2:3], self.input_width)
        y_bottomright_label = tf.minimum(bbox_label[:, :, :, 1:2] + 0.5 * bbox_label[:, :, :, 3:], self.input_height)

        x_overlap = tf.maximum((tf.minimum(x_bottomright_pred, x_bottomright_label) - tf.maximum(x_topleft_pred, x_topleft_label)), 0.0)
        y_overlap = tf.maximum((tf.minimum(y_bottomright_pred, y_bottomright_label) - tf.maximum(y_topleft_pred, y_topleft_label)), 0.0)
        overlap = x_overlap * y_overlap

        rect_area_pred = tf.abs(x_bottomright_pred - x_topleft_pred) * tf.abs(y_bottomright_pred - y_topleft_pred)
        rect_area_label = tf.abs(x_bottomright_label - x_topleft_label) * tf.abs(y_bottomright_label - y_topleft_label)
        union = rect_area_pred + rect_area_label - overlap
        the_iou = overlap / (union + 0.0001)

        return the_iou, overlap, union


    def average_iou(self, iou_map, objecness_label):
        """[summary]
        
        Arguments:
            iou_map {[type]} -- [description]
            objecness_label {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        iou = iou_map * objecness_label
        iou = tf.reduce_sum(iou)
        total_predictor = tf.reduce_sum(objecness_label)
        iou = iou / (total_predictor + 0.0001)
        return iou


    def object_accuracy(self, objectness_pred, objectness_label, noobjectness_label):
        """[summary]
        
        Arguments:
            objectness_pred {[type]} -- [description]
            objectness_label {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        objectness_mask = tf.math.greater(objectness_pred, tf.convert_to_tensor(np.array(self.threshold), tf.float32))
        objectness_mask = tf.cast(objectness_mask, tf.float32)
        delta = (objectness_label - objectness_mask) * objectness_label
        obj_acc = 1. - tf.reduce_sum(delta) / (tf.reduce_sum(objectness_label) + 0.0001)

        noobjecteness_mask = 1. - objectness_mask
        delta = (noobjectness_label - noobjecteness_mask) * noobjectness_label
        noobj_acc = 1. - tf.reduce_sum(delta) / (tf.reduce_sum(noobjectness_label) + 0.0001)
        return obj_acc, noobj_acc


    def yolo_loss(self, outputs: [], labels: []):
        """[summary]
        
        Arguments:
            outputs {[type]} -- [description]
            labels {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        self.all_losses = 0.0
        self.objectness_losses = 0.0
        self.noobjectness_losses = 0.0
        self.center_losses = 0.0
        self.size_losses = 0.0
        self.class_losses = 0.0

        if self.is_multilabel: 
            self.additional_class_losses = [] 
            additional_class_acc_total = []
            for i in self.multilabel_dict: 
                self.additional_class_losses.append(0.0)
                additional_class_acc_total.append(0.0)
        
        iou_total = 0.0
        obj_acc_total = 0.0
        noobj_acc_total = 0.0
        class_acc_total = 0.0
        
        #------------------------------------------------------#
        # For each anchor,                                     #
        # get the output results (objectness, x, y, w, h)      #
        #------------------------------------------------------#
        for i in range(3):
            output = outputs[i]
            label = labels[i]

            border_a = 0
            border_b = 3
            if i == 0:
                border_a = 6
                border_b = 9
            elif i == 1:
                border_a = 3
                border_b = 6

            for idx, val in enumerate(self.anchor[border_a:border_b]):
                if self.is_multilabel: 
                    base = idx * (5 + self.num_class + sum(self.multilabel_dict.values()))
                else: 
                    base = idx * (5 + self.num_class)
                
                # get objectness confidence
                objectness_pred_initial = tf.nn.sigmoid(output[:, :, :, (base + 4):(base + 5)])
                objectness_label = label[:, :, :, (base + 4):(base + 5)]
                objectness_pred = tf.multiply(objectness_pred_initial, objectness_label)

                # get noobjectness confidence
                noobjectness_pred = 1.0 - tf.nn.sigmoid(output[:, :, :, (base + 4):(base + 5)])
                noobjectness_label = 1.0 - objectness_label 
                noobjectness_pred = tf.multiply(noobjectness_pred, noobjectness_label)
                
                # get x values
                x_pred = tf.nn.sigmoid(output[:, :, :, (base + 0):(base + 1)])
                x_pred = tf.multiply(x_pred, objectness_label)
                x_pred = self.grid_position_mask_onx[i] + x_pred
                x_label = label[:, :, :, (base + 0):(base + 1)]
                x_label = self.grid_position_mask_onx[i] + x_label

                # get y value
                y_pred = tf.nn.sigmoid(output[:, :, :, (base + 1):(base + 2)])
                y_pred = tf.multiply(y_pred, objectness_label)
                y_pred = self.grid_position_mask_ony[i] + y_pred
                y_label = label[:, :, :, (base + 1):(base + 2)]
                y_label = self.grid_position_mask_ony[i] + y_label

                # get width values
                #--- yolo modification (10 / (1+e^{-0.1x}} - 5)
                w_pred = output[:, :, :, (base + 2):(base + 3)]
                if self.add_modsig_toshape:
                    w_pred = 6 /(1 + tf.exp(-0.2 * w_pred)) - 3
                w_label = label[:, :, :, (base + 2):(base + 3)]
                w_pred = tf.multiply(w_pred, objectness_label)
            
                # get height values
                #--- yolo modification (10 / (1+e^{-0.1x}} - 5)
                h_pred = output[:, :, :, (base + 3):(base + 4)]
                if self.add_modsig_toshape:
                    h_pred = 6 /(1 + tf.exp(-0.2 * h_pred)) - 3
                h_label = label[:, :, :, (base + 3):(base + 4)]
                h_pred = tf.multiply(h_pred, objectness_label)

                # get class value
                if self.is_multilabel: 
                    tmp_class_total = self.num_class #+ sum(self.multilabel_dict.values())
                else: 
                    tmp_class_total = self.num_class
                class_pred = output[:, :, :, (base + 5):(base + 5 + tmp_class_total)]
                class_pred = tf.multiply(class_pred, objectness_label)
                class_label = label[:, :, :, (base + 5):(base + 5 + tmp_class_total)]
                
                # claculate denomitaor
                objectness_denom = tf.reduce_sum(objectness_label) + 0.001
                noobjectness_denom = tf.reduce_sum(noobjectness_label) + 0.001

                # -------------------------------------------- #
                # IF this is a multilable detector             #
                # - get the number of properties               #
                # for each properties, get the class           #
                # -------------------------------------------- #
                if self.is_multilabel: 
                    additional_base = base + 5 + self.num_class
                    additional_class_pred = []
                    additional_class_label = []

                    for additional_class in self.multilabel_dict: 
                        member_num = int(self.multilabel_dict[additional_class])
                        tmp_pred = output[:, :, :, additional_base: (additional_base + member_num)]
                        tmp_pred = tf.multiply(tmp_pred, objectness_label)
                        tmp_label = label[:, :, :, additional_base: (additional_base + member_num)]
                        additional_class_pred.append(tmp_pred)
                        additional_class_label.append(tmp_label)
                        additional_base += member_num
                
                #----------------------------------------------#
                #              calculate the iou               #
                # 1. calculate pred bbox based on real ordinat #
                # 2. calculate the iou                         #
                #----------------------------------------------#
                x_pred_real = tf.multiply(self.grid_width[i] * x_pred, objectness_label)
                y_pred_real = tf.multiply(self.grid_height[i] * y_pred, objectness_label)
                w_pred_real = tf.multiply(val[0] * tf.math.exp(w_pred), objectness_label)
                h_pred_real = tf.multiply(val[1] * tf.math.exp(h_pred), objectness_label)
                pred_bbox = tf.concat([x_pred_real, y_pred_real, w_pred_real, h_pred_real], 3)

                x_label_real = tf.multiply(self.grid_width[i] * x_label, objectness_label)
                y_label_real = tf.multiply(self.grid_height[i] * y_label, objectness_label)
                w_label_real = tf.multiply(val[0] * tf.math.exp(w_label), objectness_label)
                h_label_real = tf.multiply(val[1] * tf.math.exp(h_label), objectness_label)
                label_bbox = tf.concat([x_label_real, y_label_real, w_label_real, h_label_real], 3)

                iou_map, overlap, union = self.iou(pred_bbox, label_bbox)

                #----------------------------------------------#
                #            calculate the losses              #
                # objectness, noobjectness, center & size loss #
                #----------------------------------------------#
                objectness_loss = self.objectness_loss_alpha * mse_loss_sum(objectness_pred, iou_map)/objectness_denom
                noobjectness_loss = self.noobjectness_loss_alpha * mse_loss_sum(noobjectness_pred, noobjectness_label)/noobjectness_denom
                ctr_loss = self.center_loss_alpha * (mse_loss_sum(x_pred, x_label) + mse_loss_sum(y_pred, y_label))/objectness_denom
                a = w_pred_real / self.grid_width[i]
                b = w_label_real / self.grid_width[i]
                c = h_pred_real / self.grid_height[i]
                d = h_label_real / self.grid_height[i]
                sz_loss =  self.size_loss_alpha * tf.sqrt(mse_loss_sum(a, b) + mse_loss_sum(c, d)) / objectness_denom

                if self.num_class == 1:
                    class_loss = self.class_loss_alpha * sigmoid_crossentropy_sum(class_pred, class_label)/objectness_denom
                else:
                    class_loss = self.class_loss_alpha * softmax_crosentropy_sum(class_pred, class_label)/objectness_denom

                # -------------------------------------------- #
                # IF this is a multilable detector             #
                # claculate additional class loss              #
                # -------------------------------------------- #
                if self.is_multilabel: 
                    additional_class_loss = []
                    for a, b in zip(additional_class_pred, additional_class_label):
                        additional_class_loss.append(self.class_loss_alpha * softmax_crosentropy_sum(a, b) / objectness_denom)
        
                total_loss = objectness_loss + \
                             noobjectness_loss + \
                             ctr_loss + \
                             sz_loss + \
                             class_loss
                
                if self.is_multilabel: 
                    total_loss += sum(additional_class_loss)
                
                self.all_losses = self.all_losses + total_loss
                self.objectness_losses = self.objectness_losses + objectness_loss
                self.noobjectness_losses = self.noobjectness_losses + noobjectness_loss
                self.center_losses = self.center_losses + ctr_loss
                self.size_losses = self.size_losses + sz_loss
                self.class_losses = self.class_losses + class_loss

                if self.is_multilabel: 
                    for a in range(len(additional_class_loss)): 
                        self.additional_class_losses[a] += additional_class_loss[a]
                
                avg_iou = self.average_iou(iou_map, objectness_label)
                obj_acc, noobj_acc = self.object_accuracy(objectness_pred_initial, 
                                                            objectness_label, 
                                                            noobjectness_label)

                if self.num_class == 1: 
                    class_acc = calculate_acc(tf.nn.sigmoid(class_pred), class_label)
                else: 
                    class_acc = calculate_acc(tf.nn.softmax(class_pred), class_label)
                
                if self.is_multilabel: 
                    for index, (a, b) in enumerate(zip(additional_class_pred, additional_class_label)):
                        additional_class_acc_total[index] += calculate_acc(a, b) *100

                iou_total = iou_total + avg_iou
                obj_acc_total = obj_acc_total + obj_acc
                noobj_acc_total = noobj_acc_total + noobj_acc
                class_acc_total = class_acc_total + class_acc
        
        self.iou_avg = iou_total / 9.  # 9==> num of anchors
        self.obj_acc_avg = obj_acc_total / 9.
        self.noobj_acc_avg = noobj_acc_total / 9.
        self.class_acc_avg = class_acc_total / 9.

        if self.is_multilabel: 
            self.additional_class_acc_avg = []
            for i in additional_class_acc_total: 
                self.additional_class_acc_avg.append(i/9.)

        return self.all_losses


    def read_yolo_labels(self, file_name: str):
        """[summary]
        
        Arguments:
            folder_path {[type]} -- [description]
            label_file_list {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """

        tmps = []
        for i in range(3):
            # -------------------------------------------- #
            # create the temporary detector array          #
            # IF this is multilabel detector, 
            # the depth = 3 * (5 + main class num + total all classes in other attributes)
            # -------------------------------------------- #
            # ex: main class male/female (2), 
            # additional attributes: age (adult/child, 2 classes) and use eye-glasses/not (2 classes)
            # so, the depth =  3 * (5 + 2 + (2 + 2))#
            # -------------------------------------------- #
            # 3 --> 3 anchor for each detector             #
            # 5 --> x, y, w, h, box confidence             #
            # -------------------------------------------- #
            if self.is_multilabel: 
                additional_class_num = sum(self.multilabel_dict.values())
                tmp = np.zeros((self.num_vertical_grid[i], 
                                self.num_horizontal_grid[i],  
                                int(len(self.anchor)/3) * ( 5 + self.num_class + additional_class_num)))
            else: 
                tmp = np.zeros((self.num_vertical_grid[i], 
                                self.num_horizontal_grid[i],  
                                int(len(self.anchor)/3) * (5 + self.num_class)))
            tmp[:, :, :] = 0.0

            # -------------------------------------------- #
            # read the .txt label of the image             #
            # - split the data based on the line           #
            # - each line represent 1 bbox, main class and additional class (if any)
            # - PARAM_NUM: the total parameters for 1 bbox or 1 label line
            # IF multilable : 
            # PARAM_NUM = x, y, w, h, main class, and aditional class
            # ELSE: 
            # PARAM_NUM = x, y, w, h, main class --> (5)   #
            #--------------------------------------------- #
            file = open(file_name, "r") 
            data = file.read()
            data = data.split()
            length = len(data)

            PARAM_NUM = 5 
            if self.is_multilabel: 
                PARAM_NUM = 5 + len(list(self.multilabel_dict.keys()))
            line_num = int(length/PARAM_NUM)

            #--------------------------------------------- #
            # for each line,                               #
            # extract main class, x, y, w, h               #
            # IF multilable:                               #
            # extract the additional class index           #
            #--------------------------------------------- #
            c = []
            x = []
            y = []
            w = []
            h = []

            if self.is_multilabel: 
                additional_c = {}
                for val in self.multilabel_dict: 
                    additional_c[val] = []

            for j in range (line_num):
                c.append(int(float(data[j*PARAM_NUM + 0])))
                x.append(float(data[j*PARAM_NUM + 1]))
                y.append(float(data[j*PARAM_NUM + 2]))
                w.append(float(data[j*PARAM_NUM + 3]))
                h.append(float(data[j*PARAM_NUM + 4]))

                if self.is_multilabel: 
                    base = 5
                    for val in self.multilabel_dict: 
                        additional_c[val].append(float(data[j*PARAM_NUM + base]))
                        base += 1

            file.close()
            
            #----------------------------------------------------------------#
            #   this part is getting the position of object in certain grid  #
            #----------------------------------------------------------------#
            border_a = 0
            border_b = 3
            if i == 0:
                border_a = 6
                border_b = 9
            elif i == 1:
                border_a = 3
                border_b = 6

            for idx_anchor, j in enumerate(self.anchor[border_a: border_b]):
                if self.is_multilabel: 
                    base = (5 + self.num_class + sum(self.multilabel_dict.values())) * idx_anchor
                else:
                    base = (5+self.num_class) * idx_anchor

                for index, (k, l, m, n, o) in enumerate(zip(x, y, w, h, c)):
                    cell_x = int(math.floor(k / float(1.0 / self.num_horizontal_grid[i])))
                    cell_y = int(math.floor(l / float(1.0 / self.num_vertical_grid[i])))
                    tmp [cell_y, cell_x, base + 0] = (k - (cell_x * self.grid_relatif_width[i])) / self.grid_relatif_width[i]  				# add x center values
                    tmp [cell_y, cell_x, base + 1] = (l - (cell_y * self.grid_relatif_height[i])) / self.grid_relatif_height[i]				# add y center values
                    tmp [cell_y, cell_x, base + 2] = math.log(m * self.input_width/j[0])										    # add width width value
                    tmp [cell_y, cell_x, base + 3] = math.log(n * self.input_height/j[1])								            # add height value
                    tmp [cell_y, cell_x, base + 4] = 1.0																				    # add objectness score
                    for p in range(self.num_class):
                        if p == o:
                            tmp [cell_y, cell_x, base + 5 + p] = 1.0

                    if self.is_multilabel: 
                        additional_base = base + 5 + self.num_class 
                        for val in self.multilabel_dict: 
                            for p in range(int(self.multilabel_dict[val])): 
                                if p == additional_c[val][index]: 
                                    tmp [cell_y, cell_x, additional_base + p] = 1.0
                            
                            additional_base = additional_base + int(self.multilabel_dict[val])    

                    #if idx_anchor ==2: 
                    #    print (tmp[cell_y, cell_x, :])
                    
            tmps.append(tmp)
        return tmps


    def nms(self, batch, confidence_threshold=0.5, overlap_threshold=0.5):
        """[summary]
        
        Arguments:
            self {[type]} -- [description]
        
        Keyword Arguments:
            confidence_threshold {float} -- [description] (default: {0.5})
            overlap_threshold {float} -- [description] (default: {0.5})
        
        Returns:
            [type] -- [description]
        """
        result_box = []
        result_conf = []
        result_class = []
        result_class_prob = []
        final_box = []
        
        for boxes in batch:
            mask = boxes[:, 4] > confidence_threshold
            boxes = boxes[mask, :] 
            classes = np.argmax(boxes[:, 5:], axis=-1)
            classes = classes.astype(np.float32).reshape((classes.shape[0], 1))
            classes_prob = np.max(boxes[:, 5:], axis=-1)
            classes_prob = classes_prob.astype(np.float32).reshape((classes_prob.shape[0], 1))
            boxes = np.concatenate((boxes[:, :5], classes, classes_prob), axis=-1)

            boxes_dict = dict()
            for cls in range(self.num_class):
                mask = (boxes[:, 5] == cls)
                mask_shape = mask.shape
                
                if np.sum(mask.astype(np.int)) != 0:
                    class_boxes = boxes[mask, :]
                    boxes_coords = class_boxes[:, :4]
                    boxes_ = boxes_coords.copy()
                    boxes_[:, 2] = (boxes_coords[:, 2] - boxes_coords[:, 0])
                    boxes_[:, 3] = (boxes_coords[:, 3] - boxes_coords[:, 1])
                    boxes_ = boxes_.astype(np.int)
                    
                    boxes_conf_scores = class_boxes[:, 4:5]
                    boxes_conf_scores = boxes_conf_scores.reshape((len(boxes_conf_scores)))
                    the_class = class_boxes[:, 5:]
                    the_class_prob = class_boxes[:, 6:]

                    result_box.extend(boxes_.tolist())
                    result_conf.extend(boxes_conf_scores.tolist())
                    result_class.extend(the_class.tolist())
                    result_class_prob.extend(the_class_prob.tolist())
        
        indices = cv2.dnn.NMSBoxes(result_box, result_conf, confidence_threshold, overlap_threshold)
        for i in indices:
            i = i[0]
            box = result_box[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            conf = result_conf[i]
            the_class = result_class[i][0]
            the_class_prob = result_class_prob[i][0]
            final_box.append([left, top, width, height, conf, the_class, the_class_prob])
        return final_box

    def nms_ml(self, batch, main_class_num, multilabel_dict, confidence_threshold=0.5, overlap_threshold=0.5):
        """[summary]
        
        Arguments:
            self {[type]} -- [description]
        
        Keyword Arguments:
            confidence_threshold {float} -- [description] (default: {0.5})
            overlap_threshold {float} -- [description] (default: {0.5})
        
        Returns:
            [type] -- [description]
        """
        result_box = []
        result_conf = []
        result_class = []
        result_class_prob = []
        final_box = []
        result_class_ml = []
        
        for boxes in batch:
            mask = boxes[:, 4] > confidence_threshold
            boxes = boxes[mask, :] 
            classes = np.argmax(boxes[:, 5:5+main_class_num], axis=-1)
            classes = classes.astype(np.float32).reshape((classes.shape[0], 1))
            classes_prob = np.max(boxes[:, 5:5+main_class_num], axis=-1)
            classes_prob = classes_prob.astype(np.float32).reshape((classes_prob.shape[0], 1))
            boxes_new = np.concatenate((boxes[:, :5], classes, classes_prob), axis=-1)

            for i in multilabel_dict: 
                base = 5+main_class_num
                tmp = np.argmax(boxes[:, base:base + multilabel_dict[i]], axis=-1)
                tmp = tmp.astype(np.float32).reshape((tmp.shape[0], 1))
                tmp_prob = np.max(boxes[:, base:base + multilabel_dict[i]], axis=-1)
                tmp_prob = tmp_prob.astype(np.float32).reshape((classes_prob.shape[0], 1))
                boxes_new = np.concatenate((boxes_new, tmp, tmp_prob), axis=-1)
                base = base + multilabel_dict[i]

            boxes_dict = dict()
            for cls in range(self.num_class):
                mask = (boxes_new[:, 5] == cls)
                mask_shape = mask.shape
                
                if np.sum(mask.astype(np.int)) != 0:
                    class_boxes = boxes_new[mask, :]
                    boxes_coords = class_boxes[:, :4]
                    boxes_ = boxes_coords.copy()
                    boxes_[:, 2] = (boxes_coords[:, 2] - boxes_coords[:, 0])
                    boxes_[:, 3] = (boxes_coords[:, 3] - boxes_coords[:, 1])
                    boxes_ = boxes_.astype(np.int)
                    
                    boxes_conf_scores = class_boxes[:, 4:5]
                    boxes_conf_scores = boxes_conf_scores.reshape((len(boxes_conf_scores)))
                    the_class = class_boxes[:, 5:6]
                    the_class_prob = class_boxes[:, 6:7]
                    the_additional_class = class_boxes[:, 7:]

                    result_box.extend(boxes_.tolist())
                    result_conf.extend(boxes_conf_scores.tolist())
                    result_class.extend(the_class.tolist())
                    result_class_prob.extend(the_class_prob.tolist())
                    result_class_ml.extend(the_additional_class.tolist())
        
        indices = cv2.dnn.NMSBoxes(result_box, result_conf, confidence_threshold, overlap_threshold)
        for i in indices:
            i = i[0]
            box = result_box[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            conf = result_conf[i]
            the_class = result_class[i][0]
            the_class_prob = result_class_prob[i][0]
            the_additional_class = result_class_ml[i]
            final_box.append([left, top, width, height, conf, the_class, the_class_prob, the_additional_class])
        return final_box

         




