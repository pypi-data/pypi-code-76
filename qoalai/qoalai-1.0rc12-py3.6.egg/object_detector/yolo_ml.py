'''
    File name: yolo.py
    Author: [DS Team]
    Date created: / /2019
    Date last modified: 17/08/2019
    Python Version: >= 3.5
    qoalai version: v0.4.4
    License: MIT License
    Maintainer: [DS Team]
'''
import cv2
import json
import math
import random
import numpy as np
import tensorflow as tf
from qoalai.tensor_operations import *
from qoalai.object_detector.detector_utils_v2 import ObjectDetector
from comdutils.file_utils import get_filenames


# =============================================== #
# This class is the child of ObjectDetector class #
# in qoalai_tensor.object_detector.detector_utils #
# =============================================== #
class Yolo(ObjectDetector):
    def __init__(self, 
                 num_of_class,
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
                 dropout_rate = 0.8,
                 leaky_relu_alpha = 0.1,
                 threshold = 0.5, 
                 convert_to_tflite=False,
                 is_multilabel = False,
                 multilabel_dict = None):
        """[summary]
        
        Arguments:
            label_folder_path {[type]} -- [description]
            dataset_folder_path {[type]} -- [description]
        
        Keyword Arguments:
            input_height {int} -- [description] (default: {512})
            input_width {int} -- [description] (default: {512})
            grid_height {int} -- [description] (default: {128})
            grid_width {int} -- [description] (default: {128})
            output_depth {int} -- [description] (default: {5})
            objectness_loss_alpha {[type]} -- [description] (default: {1.})
            noobjectness_loss_alpha {[type]} -- [description] (default: {1.})
            center_loss_alpha {[type]} -- [description] (default: {0.})
            size_loss_alpha {[type]} -- [description] (default: {0.})
            class_loss_alpha {[type]} -- [description] (default: {0.})
        """

        super(Yolo, self).__init__(num_of_class=num_of_class,
                                    input_height=input_height, 
                                    input_width=input_width, 
                                    grid_height1=grid_height1, 
                                    grid_width1=grid_width1, 
                                    grid_height2=grid_height2, 
                                    grid_width2=grid_width2, 
                                    grid_height3=grid_height3, 
                                    grid_width3=grid_height3,
                                    objectness_loss_alpha=objectness_loss_alpha, 
                                    noobjectness_loss_alpha=noobjectness_loss_alpha, 
                                    center_loss_alpha=center_loss_alpha, 
                                    size_loss_alpha=size_loss_alpha, 
                                    class_loss_alpha=class_loss_alpha,
                                    add_modsig_toshape=add_modsig_toshape,
                                    anchor = anchor,
                                    dropout_rate = dropout_rate,
                                    leaky_relu_alpha = leaky_relu_alpha,
                                    threshold=threshold,
                                    convert_to_tflite=convert_to_tflite,
                                    is_multilabel=is_multilabel,
                                    multilabel_dict=multilabel_dict)

        self.input_placeholder = tf.placeholder(tf.float32, shape=(None, self.input_height, self.input_width, 3))
        self.lr_placeholder = tf.placeholder(tf.float32, shape=[])
        if self.is_multilabel: 
            self.output_placeholder1 = tf.placeholder(tf.float32, shape=(None, 13, 13, 3*(5 + num_of_class + sum(multilabel_dict.values()) )))
            self.output_placeholder2 = tf.placeholder(tf.float32, shape=(None, 26, 26, 3*(5 + num_of_class + sum(multilabel_dict.values()) )))
            self.output_placeholder3 = tf.placeholder(tf.float32, shape=(None, 52, 52, 3*(5 + num_of_class + sum(multilabel_dict.values()) )))
        else: 
            self.output_placeholder1 = tf.placeholder(tf.float32, shape=(None, 13, 13, 3*(5 + num_of_class)))
            self.output_placeholder2 = tf.placeholder(tf.float32, shape=(None, 26, 26, 3*(5 + num_of_class)))
            self.output_placeholder3 = tf.placeholder(tf.float32, shape=(None, 52, 52, 3*(5 + num_of_class)))

        self.optimizer = None
        self.session = None
        self.saver_partial = None
        self.saver_all = None

        self.train_losses = []
        self.o_losses = []
        self.no_losses = []
        self.ct_losses = []
        self.sz_losses = []
        self.cls_losses = []


    def read_target(self, file_path):
        """[summary]
        
        Arguments:
            file_path {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        target = self.read_yolo_labels(file_path)
        return target


    def build_net(self, input_tensor, 
                  network_type='big', 
                  is_training=False):
        """[summary]
        
        Arguments:
            input_tensor {[type]} -- [description]
        
        Keyword Arguments:
            network_type {str} -- [description] (default: {'big'})
            is_training {bool} -- [description] (default: {False})
        """
        with tf.variable_scope('yolo_v3_model'):
            self.build_yolov3_net2(inputs=input_tensor, 
                                        network_type=network_type, 
                                        is_training=is_training)


    def batch_generator(self, batch_size, dataset_path, message):
        """Train Generator
        
        Arguments:
            batch_size {integer} -- the size of the batch
            image_name_list {list of string} -- the list of image name
        """
        label_folder_path = dataset_path + "labels/"
        dataset_folder_path = dataset_path + "images/"
        dataset_file_list = get_filenames(dataset_folder_path)
        random.shuffle(dataset_file_list)
        
        print ("------------------------INFO-------------------")
        print ("Image Folder: " + dataset_folder_path)
        print ("Number of Image: " + str(len(dataset_file_list)))
        print ("-----------------------------------------------")

        # Infinite loop.
        idx = 0
        while True:
            x_batch = []
            y_pred1 = []
            y_pred2 = []
            y_pred3 = []

            for i in range(batch_size):
                if idx >= len(dataset_file_list):
                    random.shuffle(dataset_file_list)
                    print ("==>>> INFO: your " + message +" dataset is reshuffled again", idx)
                    idx = 0
                try:
                    tmp_x = cv2.imread(dataset_folder_path + dataset_file_list[idx])
                    tmp_x = cv2.cvtColor(tmp_x, cv2.COLOR_BGR2RGB)
                    tmp_x = cv2.resize(tmp_x, (self.input_width, self.input_height))
                    tmp_x = tmp_x.astype(np.float32) / 255.
                    tmp_y = self.read_target(label_folder_path + dataset_file_list[idx].split('.j')[0] + ".txt")
                    x_batch.append(tmp_x)
                    y_pred1.append(tmp_y[0])
                    y_pred2.append(tmp_y[1])
                    y_pred3.append(tmp_y[2])
                except Exception as e:
                    print ("---------------------------------------------------------------")
                    print ("WARNING: the " + str(e))
                    print ("---------------------------------------------------------------")

                idx += 1
            yield (np.array(x_batch), [np.array(y_pred1), np.array(y_pred2), np.array(y_pred3)])


    def __draw_rect_wrap(self, bbox, img):
        for i in bbox:
            img = cv2.rectangle(img, (i[0], i[1]), (i[2], i[3]), (0, 255, 255), 1) 
        return img


    def visualize_label(self, labels, image): 
        """[summary]

        Arguments:
            labels {[type]} -- label list (3 labels for yolo)
            image {[type]} -- numpy uint8

        Returns:
            [type] -- [description]
        """        
        images = []

        for idx, i in enumerate(labels): 
            tmps = []

            for j in range(3): 
                base = j * (5+self.num_class)
                tmp = i[:, :, base:base + 5+self.num_class]
                tmps.append(tmp)

            for idy, j in enumerate(tmps): 
                mask = j[:, :, 4:5].astype(np.bool)
                grid_size = self.grid_width[idx]

                centerx = (j[:, :, 0:1] + self.grid_position_mask_onx_np[idx][0, :, :, :]) * grid_size
                centery = (j[:, :, 1:2] + self.grid_position_mask_ony_np[idx][0, :, :, :]) * grid_size
                centerx = centerx[mask].astype(np.int32)
                centery = centery[mask].astype(np.int32)

                if idx == 0: 
                    base = 6
                elif idx == 1: 
                    base = 3
                else: 
                    base = 0
                sizex = np.exp(j[:, :, 2:3][mask]) * self.anchor[base + idy][0]
                sizey = np.exp(j[:, :, 3:4][mask]) * self.anchor[base + idy][1]

                x1 = (centerx - 0.5 * sizex).astype(np.int32).reshape((centerx.shape[0], 1))
                x2 = (centerx + 0.5 * sizex).astype(np.int32).reshape((centerx.shape[0], 1))
                y1 = (centery - 0.5 * sizey).astype(np.int32).reshape((centerx.shape[0], 1))
                y2 = (centery + 0.5 * sizey).astype(np.int32).reshape((centerx.shape[0], 1))
                bbox = np.concatenate([x1, y1, x2, y2], axis=-1)

                sliced_cls = []
                for t in range(self.num_class): 
                    tt = j[:, :, 5+t:5+t+1][mask]
                    tt = np.reshape(tt, (tt.shape[0], 1))
                    sliced_cls.append(tt)
                class_ = np.concatenate(sliced_cls, axis=-1)
                class_ = np.argmax(class_, axis=-1)

                tmp_img = image.copy()
                for a, b, c in zip(centerx, centery, class_): 
                    cv2.circle(tmp_img,(a, b), 5, (0,255,0), -1)
                    cv2.putText(tmp_img, str(c), (a,b), cv2.FONT_HERSHEY_SIMPLEX, 1, (100,255,255))

                tmp_img = self.__draw_rect_wrap(bbox, tmp_img)
                images.append(tmp_img)

        return images


    def optimize(self, subdivisions, 
                 iterations, 
                 best_loss, 
                 train_generator, 
                 val_generator, save_path):
        """[summary]
        
        Arguments:
            subdivisions {[type]} -- [description]
            iterations {[type]} -- [description]
            best_loss {[type]} -- [description]
            train_generator {[type]} -- [description]
            val_generator {[type]} -- [description]
            save_path {[type]} -- [description]
        """
        best_loss = best_loss
        learning_rate = 0.0001
        #nonnan_count = 0
        #notsaved_time = 0
        
        for i in range(iterations):
            sign = '-'
            tmp_all = [] 
            tmp_obj = [] 
            tmp_noobj = [] 
            tmp_ctr = [] 
            tmp_sz = [] 
            tmp_class = [] 

            if self.is_multilabel: 
                tmp_additional_class = {}
                for val in self.multilabel_dict: 
                    tmp_additional_class[val] = []

            # ---------------------------------- #
            # Training Data                      #
            # ---------------------------------- #
            for j in range (subdivisions):
                x_train, y_train = next(train_generator)
                
                feed_dict = {}
                feed_dict[self.input_placeholder] = x_train
                feed_dict[self.output_placeholder1] = y_train[0]
                feed_dict[self.output_placeholder2] = y_train[1]
                feed_dict[self.output_placeholder3] = y_train[2]
                total, obj, noobj, ctr, size, class_l, iou_avg, obj_acc, noobj_acc, class_acc = self.session.run([self.all_losses, 
                                                            self.objectness_losses, 
                                                            self.noobjectness_losses, 
                                                            self.center_losses, 
                                                            self.size_losses,
                                                            self.class_losses,
                                                            self.iou_avg,
                                                            self.obj_acc_avg,
                                                            self.noobj_acc_avg,
                                                            self.class_acc_avg], feed_dict)

                if math.isnan(obj) or math.isnan(noobj) \
                    or math.isnan(ctr) or math.isnan(size) \
                    or math.isnan(class_l): 
                    print("===============>><<==================") 
                    print ("NAN Loss was found")
                    print ('obj loss: {}, no-obj loss: {}, ctr loss: {}, size loss: {}, class loss: {}'.format(obj, noobj, ctr, size, class_l))
                    print("===============>><<==================") 
                    #if learning_rate >= 1e-6: 
                    #    learning_rate = learning_rate - 0.01 * learning_rate
                    self.saver_all.restore(self.session, save_path)
                """
                else: 
                    nonnan_count += 1
                    if nonnan_count >= 100: 
                        learning_rate = learning_rate + 0.001 * learning_rate
                        nonnan_count = 0
                """
                if self.is_multilabel:
                    additional_ls = self.session.run(self.additional_class_losses, feed_dict)
                    for index, val in enumerate(self.multilabel_dict): 
                        tmp_additional_class[val].append(additional_ls[index])

                    additional_acc = self.session.run(self.additional_class_acc_avg, feed_dict)
                
                feed_dict[self.lr_placeholder] = learning_rate
                self.session.run(self.optimizer, feed_dict=feed_dict)

                tmp_all.append(total)
                tmp_obj.append(obj)
                tmp_noobj.append(noobj)
                tmp_ctr.append(ctr)
                tmp_sz.append(size)
                tmp_class.append(class_l)
                
                if self.is_multilabel: 
                    print ("> Train sub", j, ': iou: ', round(iou_avg*100, 1), 
                            'obj acc: ', round(obj_acc*100, 1), 'noobj acc: ', round(noobj_acc*100, 1), 
                            'main-cls-acc: ', round(class_acc*100, 1), "additional-cls-acc: ", additional_acc, 
                            'lr: ', learning_rate)
                else: 
                    print ("> Train sub", j, ': iou: ', round(iou_avg*100, 1), 
                            'obj acc: ', round(obj_acc*100, 1), 'noobj acc: ', round(noobj_acc*100, 1), 
                            'class acc: ', round(class_acc*100, 1), 'lr: ', learning_rate)
                
            # ------------------------------- #
            # validating the data             #
            # ------------------------------- #
            x_val, y_val = next(val_generator)
            val_feed_dict = {}
            val_feed_dict[self.input_placeholder] = x_val
            val_feed_dict[self.output_placeholder1] = y_val[0]
            val_feed_dict[self.output_placeholder2] = y_val[1]
            val_feed_dict[self.output_placeholder3] = y_val[2]
            total_val, _, _, _, _, _, iou_avg_val, obj_acc_val, noobj_acc_val, class_acc_val = self.session.run([self.all_losses, 
                                                        self.objectness_losses, 
                                                        self.noobjectness_losses, 
                                                        self.center_losses, 
                                                        self.size_losses,
                                                        self.class_losses,
                                                        self.iou_avg,
                                                        self.obj_acc_avg,
                                                        self.noobj_acc_avg,
                                                        self.class_acc_avg], val_feed_dict)
            
            total = sum(tmp_all)/(len(tmp_all) + 0.001)
            obj =  sum(tmp_obj)/(len(tmp_obj) + 0.001)
            noobj = sum(tmp_noobj)/(len(tmp_noobj) + 0.001)
            ctr = sum(tmp_ctr)/(len(tmp_ctr) + 0.001)
            size = sum(tmp_sz)/(len(tmp_sz) + 0.001)
            class_l = sum(tmp_class)/(len(tmp_class) + 0.001)

            if self.is_multilabel: 
                additional_l = {}
                for val in self.multilabel_dict: 
                    additional_l[val] = sum(tmp_additional_class[val])/len(tmp_additional_class[val])
            
            self.train_losses.append(total)
            self.o_losses.append(obj)
            self.no_losses.append(noobj)
            self.ct_losses.append(ctr)
            self.sz_losses.append(size)
            self.cls_losses.append(class_l)
            
            # ------------------------------- #
            # save the model                  #
            # ------------------------------- #
            if best_loss > total_val:
                best_loss = total_val
                sign = "************* model saved"
                self.saver_all.save(self.session, save_path)
                #notsaved_time = 0
            
            print ("> Val epoch :", 'iou: ', round(iou_avg_val*100, 3), 
                    'obj acc: ', round(obj_acc_val*100, 3), 'noobj acc: ', round(noobj_acc_val*100, 3), 
                    'main-cls-acc: ', round(class_acc_val*100, 3))
            
            print ('eph: ', i, 'ttl-loss: ', round(total, 2), 'obj-loss: ', round(obj*100, 2), 
                    'noobj-loss: ', round(noobj*100, 2), 'ctr-loss: ', round(ctr*100, 2), 
                    'size-loss: ', round(size*100, 2),  'main-cls-loss: ', round(class_l*100, 2), sign)
            
            if self.is_multilabel: 
                print ("      additional-cls-loss: ", additional_l)

    
    def check_val_data(self, val_generator):
        """[summary]
        
        Arguments:
            val_generator {[type]} -- [description]
        """
        x_val, y_val = next(val_generator)
        val_feed_dict = {}
        val_feed_dict[self.input_placeholder] = x_val
        val_feed_dict[self.output_placeholder1] = y_val[0]
        val_feed_dict[self.output_placeholder2] = y_val[1]
        val_feed_dict[self.output_placeholder3] = y_val[2]
        total, obj, noobj, ctr, size, class_l, iou_avg_val, obj_acc_val, noobj_acc_val, class_acc_val = self.session.run([self.all_losses, 
                                                    self.objectness_losses, 
                                                    self.noobjectness_losses, 
                                                    self.center_losses, 
                                                    self.size_losses,
                                                    self.class_losses,
                                                    self.iou_avg,
                                                    self.obj_acc_avg,
                                                    self.noobj_acc_avg,
                                                    self.class_acc_avg], val_feed_dict)

        print ("> iou: ", round(iou_avg_val*100, 3), 'obj acc: ', round(obj_acc_val*100, 3), 
                'noobj acc: ', round(noobj_acc_val*100, 3), 'class acc: ', round(class_acc_val*100, 3))

        print ('ttl loss: ', round(total, 2), 'obj loss: ', round(obj*100, 2), 
                'noobj loss: ', round(noobj*100, 2), 'ctr loss: ', round(ctr*100, 2), 
                'size loss: ', round(size*100, 2),  round(class_l*100, 2))
    


    
