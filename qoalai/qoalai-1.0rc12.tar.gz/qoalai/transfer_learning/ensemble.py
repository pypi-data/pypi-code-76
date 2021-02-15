'''
    File name: detector_utils.py
    Author: [Qoala DS Team]
    Date created: / /2019
    Date last modified: / /2019
    Python Version: >= 3.5
    qoalai version: v0.4.4
    License: MIT License
    Maintainer: [Mochammad F Rahman]
'''

import tensorflow as tf
from qoalai.transfer_learning.image_recognition import *


class Ensemble(): 
    """Class for ensembling two or more networks
    """    
    def __init__(self, classes,
                       ensemble_network = ['resnet', 'densenet'],
                       input_height = 300,
                       input_width = 300,
                       input_channel = 3,
                       tf_lite_architecture=False):
        """Ensemble Constructor
        
        Arguments:
            classes {[list of str]} -- the class list
        
        Keyword Arguments:
            ensemble_network {list} -- [description] (default: {['resnet', 'densenet']})
            input_height {int} -- [description] (default: {300})
            input_width {int} -- [description] (default: {300})
            input_channel {int} -- [description] (default: {3})
        """        
        self.classes = classes
        self.ensemble_networks = ensemble_network
        self.tf_lite_architecture = tf_lite_architecture
        
        if len(self.ensemble_networks) in [1, 2, 3]:
            #print ("==>> INFO: your networks are {} and {}".format(self.ensemble_networks[0], self.ensemble_networks[1]))

            self.input_height = input_height
            self.input_width = input_width
            self.input_channel = input_channel

            self.imrec = ImageRecognition(classes=self.classes,
                            input_height = self.input_height,
                            input_width = self.input_width, 
                            input_channel = self.input_channel)
            
            if self.tf_lite_architecture: 
                self.input_images = self.imrec.input_placeholder
            else: 
                self.input_string = tf.placeholder(tf.string, shape=[None], name='string_input')
                decode = lambda raw_byte_str: tf.image.resize_images(
                                                tf.cast(
                                                    tf.image.decode_jpeg(raw_byte_str, channels=3, name='decoded_image'),
                                                        tf.uint8), 
                                                [self.input_height, self.input_width])
                self.input_images = tf.map_fn(decode, self.input_string, dtype=tf.float32) / 255.0
                
        
        elif len(self.ensemble_networks) == 1: 
            print ("==>> WARNING: your network is only {}, Ensemble is combining TWO or more networks".format(self.ensemble_networks[0]))
        else: 
            print ("==>> WARNING: your networks are more than 2, This current version ONLY SUPPORTs 2 or 3 models ensemble")

    
    def do_ensemble(self, model_list,
                    model_result_path,
                    is_training=False):
        """[summary]
        
        Arguments:
            model_list {[type]} -- [description]
        
        Keyword Arguments:
            is_training {bool} -- [description] (default: {False})
        """
        network_output = {}
        network_vars = {} 
        savers = {}

        for i in self.ensemble_networks: 
            if i == 'densenet':
                network_output[i], _ = self.imrec.build_densenet_base(self.input_images,
                                                                dropout_rate = 0.20,
                                                                is_training = is_training,
                                                                top_layer_depth = 128) 
                network_vars[i] = tf.global_variables(scope='densenet121')

            elif i == 'resnet': 
                network_output[i], _ = self.imrec.build_resnetv2(self.input_images,
                                                            is_training=is_training,
                                                            top_layer_depth = 128) 
                network_vars[i] = tf.global_variables(scope='resnet_v2_101')

            elif i == 'inception': 
                network_output[i], _ = self.imrec.build_inceptionv4_basenet(self.input_images,
                                                            is_training=is_training,
                                                            final_endpoint='Mixed_7a', # 'Mixed_6a, Mixed_5a, Mixed_7a
                                                            top_layer_depth = 128) 
                network_vars[i] = tf.global_variables(scope='InceptionV4')
        
        self.out = tf.add_n(list(network_output.values())) / float(len(network_output)) #(network_output[self.ensemble_networks[0]] + network_output[self.ensemble_networks[1]]) / 2.
        print ("==>> INFO: Building networks success")
        
        session = tf.Session()
        saver_all = tf.train.Saver()
        for idx, i in enumerate(self.ensemble_networks): 
            savers[i] = tf.train.Saver(var_list=network_vars[i])
            #savers[i] = tf.train.Saver()
            print ("==========================")
            print (model_list[idx])
            print (len(network_vars[i]))
            print ("InceptionV4_1/batch_normalization_4/beta" in network_vars[i])
            for a in network_vars[i]: 
                print (a)
            print ("==========================")
            savers[i].restore(sess=session, save_path=model_list[idx])
        print ('==>> Load all wieghts success')

        ############  serving model procedure #################
        builder = tf.saved_model.builder.SavedModelBuilder(model_result_path)

        # Create aliase tensors
        # tensor_info_x: for input tensor
        # tensor_info_y: for output tensor
        if self.tf_lite_architecture: 
            tensor_info_x = tf.saved_model.utils.build_tensor_info(self.input_images)
        else: 
            tensor_info_x = tf.saved_model.utils.build_tensor_info(self.input_string)
        tensor_info_y = tf.saved_model.utils.build_tensor_info(self.out)

        # create prediction signature
        prediction_signature = tf.saved_model.signature_def_utils.build_signature_def(
                                inputs={'input': tensor_info_x},
                                outputs={'output': tensor_info_y},
                                method_name=tf.saved_model.signature_constants.PREDICT_METHOD_NAME)

        # build frozen graph
        legacy_init_op = tf.group(tf.tables_initializer(), name='legacy_init_op')
        builder.add_meta_graph_and_variables(session, [tf.saved_model.tag_constants.SERVING],
                                             signature_def_map={'serving_default':prediction_signature},
                                             legacy_init_op=legacy_init_op)
        builder.save()


