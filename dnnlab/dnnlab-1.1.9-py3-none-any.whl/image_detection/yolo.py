# Copyright 2019 Tobias Höfer
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
YOLOv2
-------------
+ Batch Normalization to feature extractor model - no need for dropout
+ Convolutional With Anchor Boxes (fully convolutional)
+ Dimension Clusters
+ Direct location prediction

YOLOv2 uses a few tricks to improve training and increase performance.
Like Overfeat and SSD we use a fully-convolutional model, but we still train on
whole images, not hard negatives. Like Faster R-CNN we adjust priors on bounding
boxes instead of predicting the width and height outright. However, we still
predict the x and y coordinates directly. The full details are in the paper.
"""
import logging
import os
import time
from datetime import datetime

import tensorflow as tf

from dnnlab.errors.dnnlab_exceptions import ModelNotCompiledError
from dnnlab.losses import yolo_loss
from dnnlab.losses import extract_model_output, extract_label, yolo_grid
from dnnlab.utils.coco_map import compute_coco_metrics

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # FATAL
logging.getLogger("tensorflow").setLevel(logging.FATAL)


class YOLO():
    """Implements a yolo learning model.

        Typical usage example:

        feature_extractor -> keras.model (pretrained or from scratch) /
                             final output_layer should have fixed
                             spatial resolution:
                                (grid_size, grid_size, num_channels)
                             but num_channels can vary.

        # Define forward path.
        # TODO: only allows symmetric grid.
        GRID_H = 13
        GRID_W = 13
        ANCHORS = np.array([
                        4.0, 2.0,
                        2.0, 4.0,
                        2.0, 2.0,
                        8.0, 1.0
                    ])
        LABELS = ["foo", "bar"]

        feature_extractor = tf.keras.models....
        yolo = dnnlab.image_detection.YOLO(feature_extractor, GRID_H, GRID_W,
                                       ANCHORS, LABELS)

        # Define optimizer.
        yolo.compile(optimizer="adam", lr=1e-4)

        # Start training process.
        yolo.fit(training_data, validation_data, EPOCHS, BATCH_SIZE,LEN_DATASET)

        # Export h5 model.
        yolo.export()

        use yolo.restore("relative_path_to_logs") to continue training after
        a break.


    Attributes:
        feature_extractor (keras.model): Basic nn feature extractor.
        grid_h (int): Grid size.
        grid_w (int): Grid size.
        anchors (np.array): List of w,h of prior bounding boxes.
        boxes(int): Number of prior defined bounding boxes.
        class_list (int): Labels as a list of strings.
        n_classes(int): Number of different classes.
        optimizer(keras.optimizers): Learning algorithm instance.
        complete_model(keras.model): Feature extractor + classification head.
        init_timestamp (str): Acts as a unique folder identifier.
        logdir (str): Top level logdir.
        tensorboard (str): Path to tensorboard summary files.
        ckpt_dir (str): Path to ckpt files.
        ckpt_manager (tf.train.CheckpointManager): Deletes old checkpoints.
        checkpoint (tf.train.Checkpoint): Groups trackable objects, saving and
            restoring them.
        colors (tf.constant): Color of predicted bounding boxes.
    """
    def __init__(self,
                 feature_extractor,
                 grid_h,
                 grid_w,
                 anchors,
                 class_list,
                 complete_model=None):
        """Inits YOLO with a predefined keras model. A complete model is a
        neural net consisting of a feature extractor (body) and a yolo
        classification head. If only a feature extractor is given YOLO will
        automatically append a corresponding classification head depending on
        a grid size, the number of prior anchor boxes and the number of classes.

        Args:
            feature_extractor (keras.model): Basic nn feature extractor.
            grid_h (int): Grid size.
            grid_w (int): Grid size.
            anchors (np.array): List of w,h of prior bounding boxes.
            class_list (list): Labels as a list of strings.
            complete_model (keras.model, optional): Feature extractor +
                classification head.. Defaults to None.
        """
        self.feature_extractor = feature_extractor
        self.grid_h = grid_h
        self.grid_w = grid_w
        self.anchors = anchors
        self.boxes = len(anchors) // 2
        self.class_list = class_list
        self.n_classes = len(class_list)
        self.category_list = self._list_to_dict()
        self.optimizer = None
        self.complete_model = complete_model
        if self.complete_model is None:
            self.model = self._append_classifier()
        else:
            self.model = self.complete_model
        self.init_timestamp = "YOLO-" + datetime.now().strftime(
            "%d%m%Y-%H%M%S")
        self.logdir = os.path.join("logs", self.init_timestamp)
        self.tensorboard = os.path.join(self.logdir, "tensorboard")
        self.ckpt_dir = os.path.join(self.logdir, "ckpts")
        self.ckpt_manager = None
        self.checkpoint = None
        self.colors = tf.constant([(253, 165, 15)], dtype=tf.float32) / 255.

    def _list_to_dict(self):
        category_list = []
        for counter, item in enumerate(self.class_list):
            category_list.append({"id": counter, "name": item})
        return category_list

    def summary(self):
        """Returns a keras model summary on it underlying yolo model."""
        return self.model.summary()

    def predict(self,
                img,
                text_format=True,
                max_number_bb=100,
                iou_threshold=0.4,
                class_conf_threshold=0.25):
        """Performs an inference step (prediction) with yolo specific
        post-processing. After the prediction, the output is filtered by
        class_confidence below class_conf_threshold:
            class_confidence = box_confidence * class probability
        and a multiclass non-max suppression with iou_threshold and a maximal
        number of returning boundind boxes.
        If text_format is true, this method returns a dict.
        If text_format is false, this method return the input image with
        its predicted bounding boxes (tensor).

        Args:
            img: Image to perform prediction on.
            text_format (bool, optional): Ouput format. Defaults to True.
            max_number_bb (int, optional): Maximum of predicted bounding boxes.
                Defaults to 100.
            iou_threshold (float, optional): Used in NMS. Defaults to 0.4.
            class_conf_threshold (float, optional): Used before NMS.
                Defaults to 0.25.
        """
        prediction = self.model.predict(img)
        selected_boxes, selected_confidence, selected_classes = self.decode_yolo_output(  # pylint:disable=line-too-long
            prediction,
            self.anchors,
            max_number_bb=max_number_bb,
            iou_threshold=iou_threshold,
            class_conf_threshold=class_conf_threshold)

        if text_format:
            result = []
            for obj, cl, box in zip(selected_confidence, selected_classes,
                                    selected_boxes):
                item = {}
                item["Class"] = self.class_list[tf.cast(cl, dtype=tf.int32)]
                item["Confidence"] = obj
                item["Box"] = box
                result.append(item)
            return result

        # Swap xy coordinates for bullshit tensorflow draw_bounding_boxes
        xmin = selected_boxes[..., 0:1]
        ymin = selected_boxes[..., 1:2]
        xmax = selected_boxes[..., 2:3]
        ymax = selected_boxes[..., 3:4]

        boxes_yx = tf.concat([ymin, xmin, ymax, xmax], axis=-1)

        # Append batch dim.
        boxes_yx = tf.cast(tf.expand_dims(boxes_yx, 0), dtype=tf.float32)

        return tf.image.draw_bounding_boxes(tf.cast(img, dtype=tf.float32),
                                            boxes_yx, self.colors)

    def _append_classifier(self):
        self.feature_extractor.add(
            # 1x1 convolution.
            tf.keras.layers.Conv2D(filters=(self.boxes * (5 + self.n_classes)),
                                   kernel_size=(1, 1),
                                   strides=(1, 1),
                                   padding="same",
                                   name="classification_head"))

        # Reshape to specific yolov2 output:
        # (bs, grid, grid, anchors, (x,y,w,h,objectivness, n_classes))
        self.feature_extractor.add(
            tf.keras.layers.Reshape(
                (self.grid_h, self.grid_w, self.boxes, 5 + self.n_classes)))

        return self.feature_extractor

    def compile(self, optimizer="adam", lr=1e-4, loss_scaling=False):
        """Defines the optimization part of the learning algorithm to our
        learning model.

        Args:
            optimizer (str, optional): Optimizer. Defaults to "adam".
            lr_gen (Float, optional): Learning rate generator. Defaults to 1e4.
            lr_disc (Float, optional): Learning rate discriminator.
                Defaults to 1e4.
        """
        if optimizer == "adadelta":
            self.optimizer = tf.keras.optimizers.Adadelta(lr)
        elif optimizer == "adagrad":
            self.optimizer = tf.keras.optimizers.Adagrad(lr)
        elif optimizer == "adam":
            self.optimizer = tf.keras.optimizers.Adam(lr)
        elif optimizer == "adamax":
            self.optimizer = tf.keras.optimizers.Adamax(lr)
        elif optimizer == "ftrl":
            self.optimizer = tf.keras.optimizers.Ftrl(lr)
        elif optimizer == "nadam":
            self.optimizer = tf.keras.optimizers.Nadam(lr)
        elif optimizer == "rmsprop":
            self.optimizer = tf.keras.optimizers.RMSprop(lr)
        elif optimizer == "sgd":
            self.optimizer = tf.keras.optimizers.SGD(lr)

        if loss_scaling:
            self.optimizer = tf.keras.mixed_precision.LossScaleOptimizer(
                self.optimizer)

        if self.checkpoint is None:
            self.checkpoint = tf.train.Checkpoint(optimizer=self.optimizer,
                                                  model=self.model)
            self.ckpt_manager = tf.train.CheckpointManager(self.checkpoint,
                                                           self.ckpt_dir,
                                                           max_to_keep=5)

    def fit(self,
            training_data,
            validation_data,
            epochs,
            batch_size,
            len_dataset,
            save_ckpt=5,
            verbose=1,
            max_outputs=2,
            initial_step=0,
            lambda_coord=1.0,
            lambda_obj=5.0,
            lambda_noobj=1.0,
            lambda_class=1.0,
            iou_threshold=0.4,
            class_conf_threshold=0.25,
            mlflow=False):
        """Trains the yolo model for n EPOCHS. Saves ckpts every n EPOCHS.
        The training loop together with the optimization algorithm define the
        learning algorithm.

        Args:
            training_data (tf.dataset): tf.Dataset with
                shape(None, width, height, depth).
            validation_data (tf.dataset): tf.Dataset with
                shape(None, width, height, depth).
            epochs (int): Number of epochs.
            batch_size (int): Batch length.
            save_ckpt (int): Save ckpts every n Epochs.
            verbose (int, optional): Keras Progbar verbose lvl. Defaults to 1.
            max_outputs (int, optional): Number of images shown in TB.
                Defaults to 2.
            initial_step (int, optional): Initial step for tb output.
            lambda_coords(float, optional): Coordinate weight coefficient.
            lambda_obj(float, optional): Object weight coefficient.
            lambda_noobj(float, optional): Noobject weight coefficient.
            lambda_class(float, optional): Class weight coefficient.
            iou_threshold(float, optional): For tb nms output.
            class_conf_threshold(float, optional): For tb nms output.
            mlflow(bool, optional): Tracks validation loss as metric.

        Raises:
            ModelNotCompiledError: Raise if model is not compiled.
        """
        if self.optimizer is None:
            raise ModelNotCompiledError("use compile() first.")
        if mlflow:
            import mlflow  # pylint:disable=import-outside-toplevel

        # Retrace workaround @function signature only tensors.
        step = tf.Variable(initial_step, name="step", dtype=tf.int64)

        num_batches = len_dataset / batch_size

        # Keras Progbar and file writer setup.
        progbar = tf.keras.utils.Progbar(target=num_batches, verbose=verbose)
        file_writer = tf.summary.create_file_writer(self.tensorboard)
        eval_file_writer = tf.summary.create_file_writer(
            os.path.join(self.tensorboard, "eval"))
        file_writer.set_as_default()

        # Iterate over all epochs.
        for epoch in range(epochs):
            step_float = 1
            train_loss_avg = tf.keras.metrics.Mean()
            start = time.time()
            for elements in training_data:
                images = elements[0]
                labels = elements[1]

                # Performs a training step. Inference + BP and GD.
                tb_prediction, tb_label, loss = self.train_step(
                    images, labels, batch_size, step, max_outputs, file_writer,
                    lambda_coord, lambda_obj, lambda_noobj, lambda_class,
                    iou_threshold, class_conf_threshold)

                train_loss_avg.update_state(loss)

                # TODO Workaround. summary image & gpu usage.
                with file_writer.as_default():  #pylint: disable=not-context-manager
                    tf.summary.image("label", tb_label, step=step)
                    tf.summary.image("prediction", tb_prediction, step=step)

                file_writer.flush()
                progbar.update(current=(step_float))
                step_float += 1
                step.assign(step + 1)

            # Save the model every n epochs
            if (epoch + 1) % save_ckpt == 0:
                ckpt_save_path = self.ckpt_manager.save()
                print("\nSaving checkpoint for epoch {} at {}".format(
                    epoch + 1, ckpt_save_path))

            print(" - Epoch: {} - loss {}".format(
                epoch + 1, round(train_loss_avg.result().numpy().item(), 4)))

            print("Start validation loop...")
            self._evaluate(validation_data,
                           iou_threshold=iou_threshold,
                           class_conf_threshold=class_conf_threshold,
                           mlflow=mlflow,
                           tb=True,
                           lambda_coord=lambda_coord,
                           lambda_obj=lambda_obj,
                           lambda_noobj=lambda_noobj,
                           lambda_class=lambda_class,
                           max_outputs=max_outputs,
                           step=step,
                           step_float=step_float,
                           file_writer=eval_file_writer)

    def coco_metric_format(self, tensor, batch_size, class_conf_threshold,
                           iou_threshold, label):
        """[summary]

        Args:
            tensor ([type]): [description]

        Returns:
            [type]: [description]
        """
        bboxs = []
        cat_ids = []
        scores = []
        for img in range(batch_size):
            classes, confidence, boxes = self.decode_yolo_output(
                tf.expand_dims(tensor[img, :, :, :, :], 0),
                self.anchors,
                class_conf_threshold=class_conf_threshold,
                tb=True,
                label=label)

            # Apply multiclass NMS.
            selected_indices = []
            for c in range(self.n_classes):
                # only include boxes of the current class, with > 0 confidence
                class_mask = tf.cast(tf.equal(classes,
                                              tf.cast(c, dtype=tf.float32)),
                                     dtype=tf.float32)
                conf_mask = tf.cast(confidence > 0, dtype=tf.float32)
                mask = class_mask * conf_mask

                # Prunes away boxes that have high intersection-over-union (IOU)
                # overlap with previously selected boxes. Run nms independently
                # for each cl.
                selected_indices_per_class = tf.image.non_max_suppression(
                    boxes, confidence * mask, 1000, iou_threshold, 0.0)

                selected_indices.append(selected_indices_per_class)

            # Flatten nested list.
            selected_indices = tf.concat(selected_indices, axis=-1)
            selected_boxes = tf.gather(boxes, selected_indices)
            selected_classes = tf.gather(classes, selected_indices)
            selected_confidence = tf.gather(confidence, selected_indices)

            bboxs.append(selected_boxes.numpy())
            cat_ids.append(selected_classes.numpy())
            scores.append(selected_confidence.numpy())

        # Flatten nested lists.
        #bboxs = [item for sublist in bboxs for item in sublist]
        #cat_ids = [item for sublist in cat_ids for item in sublist]
        #print(scores)
        #scores = [item for sublist in scores for item in sublist]
        return bboxs, cat_ids, scores

    def restore(self, ckpt_path):
        """Restore model weights from the latest checkpoint.

        Args:
            ckpt_path (str): Relative path to ckpt files.

        Raises:
            ModelNotCompiledError: Raise if model is not compiled.
        """

        restore_path = os.path.dirname(ckpt_path)
        self.logdir = restore_path
        self.tensorboard = os.path.join(self.logdir, "tensorboard")
        self.ckpt_dir = os.path.join(self.logdir, "ckpts")
        if self.ckpt_manager is None:
            raise ModelNotCompiledError("use compile() first.")
        self.ckpt_manager = tf.train.CheckpointManager(self.checkpoint,
                                                       self.ckpt_dir,
                                                       max_to_keep=5)
        # if a checkpoint exists, restore the latest checkpoint.
        if self.ckpt_manager.latest_checkpoint:
            self.checkpoint.restore(self.ckpt_manager.latest_checkpoint)
            print("Latest checkpoint restored!!")
        else:
            print("Can not find ckpt files at {}".format(ckpt_path))

    def export(self, model_format="hdf5"):
        """Exports the trained models in hdf5 or SavedModel format.

        Args:
            model_format (str, optional): SavedModel or HDF5. Defaults to hdf5.
        """
        model_dir = os.path.join(self.logdir, "models")
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

        if model_format == "hdf5":
            self.model.save(os.path.join(model_dir, "yolo.h5"))
        elif model_format == "SavedModel":
            self.model.save(os.path.join(model_dir, "yolo"))

    @tf.function
    def train_step(self, x, y, batch_size, step, max_outputs, file_writer,
                   lambda_coord, lambda_obj, lambda_noobj, lambda_class,
                   iou_threshold, class_confidence):
        """Decorated function (@tf.function) that creates a callable tensorflow
        graph from a python function. Performs an batch inference steps,
        calculates the gradient using BP and updates the trainable params
        using a predefined optimization technique.
        """
        # TODO(Tobi): Trace keras.models graph to visualize in tensorboard.
        with file_writer.as_default():
            with tf.GradientTape() as tape:
                # Predict
                start_time = time.time()
                prediction = self.model(x, training=True)
                end_time = time.time()
                img_per_second = (end_time - start_time) / batch_size
                tf.summary.scalar("inference_time[s]",
                                  img_per_second,
                                  step=step)

                # Bounding box prediction to tensorboard.
                tb_prediction = self._prediction_to_tensorboard(
                    x, prediction, max_outputs, step, iou_threshold,
                    class_confidence)
                # Bounding box label to tensorboard.
                tb_label = self._prediction_to_tensorboard(
                    x,
                    tf.cast(y, dtype=tf.float32),
                    max_outputs,
                    step,
                    iou_threshold,
                    class_confidence,
                    label=True)

                # Loss
                loss = yolo_loss(y,
                                 prediction,
                                 self.anchors,
                                 lambda_coord,
                                 lambda_obj,
                                 lambda_noobj,
                                 lambda_class,
                                 iou_threshold=iou_threshold,
                                 step=step)

            # Calculate gradient.
            gradient = tape.gradient(loss, self.model.trainable_variables)

            # Apply gradient to weights.
            self.optimizer.apply_gradients(
                zip(gradient, self.model.trainable_variables))

            # Piece of shit workaround
            return tb_prediction, tb_label, loss

    def evaluate(self,
                 dataset,
                 iou_threshold=0.4,
                 class_conf_threshold=0.25,
                 lambda_coord=1.0,
                 lambda_obj=5.0,
                 lambda_noobj=1.0,
                 lambda_class=1.0):
        """[summary]

        Args:
            dataset ([type]): [description]
            iou_threshold (float, optional): [description]. Defaults to 0.4.
            class_conf_threshold (float, optional): [description]. Default 0.25.
            lambda_coord (float, optional): [description]. Defaults to 1.0.
            lambda_obj (float, optional): [description]. Defaults to 5.0.
            lambda_noobj (float, optional): [description]. Defaults to 1.0.
            lambda_class (float, optional): [description]. Defaults to 1.0.
        """
        self._evaluate(dataset,
                       iou_threshold=iou_threshold,
                       class_conf_threshold=class_conf_threshold,
                       lambda_coord=lambda_coord,
                       lambda_obj=lambda_obj,
                       lambda_noobj=lambda_noobj,
                       lambda_class=lambda_class)

    def decode_yolo_output(self,
                           predictions,
                           anchors,
                           max_number_bb=100,
                           iou_threshold=0.4,
                           class_conf_threshold=0.25,
                           tb=False,
                           label=False):
        """Performs Yolo post-processing. Extract values from yolo output tensor
        to a readable format & filters predictions by class_conf_threshold &
        filters predictions usind a multi-class non-max suppression.

        Args:
            predictions ([type]): [description]
            anchors ([type]): [description]
            max_number_bb (int, optional): [description]. Defaults to 10.
            iou_threshold (float, optional): [description]. Defaults to 0.4.
            class_confidence (float, optional): [description]. Defaults to 0.6.
            tb (bool, optional): [description]. Defaults to False.
        """

        # TODO wrong order?
        grid_h = tf.cast(tf.shape(predictions)[1], dtype=tf.float32)
        grid_w = tf.cast(tf.shape(predictions)[2], dtype=tf.float32)
        n_boxes = tf.cast(tf.shape(predictions)[3], dtype=tf.float32)
        n_classes = tf.shape(predictions)[4] - 5

        grid_coord = yolo_grid(1, grid_h, grid_w, n_boxes)
        if label:
            p_box_xy, p_box_wh, p_box_conf, p_box_class = extract_label(
                predictions, tb=True)
        else:
            p_box_xy, p_box_wh, p_box_conf, p_box_class = extract_model_output(
                predictions, grid_coord, anchors)

        # Process xywh - coordinates
        # Convert from grid units to IMG coordinates [(0,1), (0,1)].
        # TODO validate next
        p_box_xy = p_box_xy / grid_w
        p_box_wh = p_box_wh / grid_w
        # From center coords (xcenter, ycenter) & width & height to:
        # (xmin,ymin), (x_max,ymax).
        bb_xymin = p_box_xy - p_box_wh / 2.
        bb_xymax = p_box_xy + p_box_wh / 2.

        # Shape (1, grid, grid, anchors, 4).
        boxes = tf.concat([bb_xymin, bb_xymax], axis=-1)

        # Filter predictions with class_conf below obj threshold.
        # class_confidence = box_confidence * class probability
        class_confidence = p_box_conf * tf.nn.softmax(
            tf.cast(p_box_class, dtype=tf.float32))

        if label:
            masked_class_confidence = class_confidence
        else:
            mask = class_confidence > class_conf_threshold
            masked_class_confidence = class_confidence * tf.cast(
                mask, dtype=tf.float32)

        # Get index of class with highest logit
        # p_box_class shape (1, 16, 16, 5, 20)
        # tf.argmax output shape -> (1, 16, 16, 5)
        masked_classes = tf.argmax(masked_class_confidence, axis=-1)
        masked_confidence = tf.reduce_max(masked_class_confidence, axis=-1)

        # flattened tensor length
        shape = grid_h * grid_w * n_boxes
        # For tf non-max suppresion input.
        boxes = tf.reshape(boxes, shape=(shape, 4))

        # Flatten classes
        masked_classes = tf.cast(tf.reshape(masked_classes, shape=[shape]),
                                 dtype=tf.float32)

        # Flatten class_confidence.
        masked_confidence = tf.reshape(masked_confidence, shape=[shape])

        if tb:
            return masked_classes, masked_confidence, boxes
        selected_indices = []

        # apply multiclass NMS
        for c in range(n_classes):
            class_mask = tf.cast(tf.math.equal(masked_classes, c),
                                 dtype=tf.float32)
            score_mask = tf.cast(masked_confidence > 0, dtype=tf.float32)
            mask = class_mask * score_mask
            # Prunes away boxes that have high intersection-over-union (IOU)
            # overlap with previously selected boxes. Run nms independently for
            # each class.
            selected_indices_per_class = tf.image.non_max_suppression(
                boxes, masked_confidence * mask, max_number_bb, iou_threshold,
                0.0)

            selected_indices.append(selected_indices_per_class)

        # Flatten nested list.
        selected_indices = tf.concat(selected_indices, axis=-1)
        selected_boxes = tf.gather(boxes, selected_indices)
        selected_confidence = tf.gather(masked_confidence, selected_indices)
        selected_classes = tf.gather(masked_classes, selected_indices)

        return selected_boxes, selected_confidence, selected_classes

    def _prediction_to_tensorboard(self,
                                   input_img,
                                   prediction,
                                   max_outputs,
                                   step,
                                   iou_threshold,
                                   class_conf_threshold,
                                   label=False):
        del step
        tb_imgs = []
        for img in range(max_outputs):
            classes, confidence, boxes = self.decode_yolo_output(
                tf.expand_dims(prediction[img, :, :, :], 0),
                self.anchors,
                class_conf_threshold=class_conf_threshold,
                tb=True,
                label=label)

            # Apply multiclass NMS.
            selected_indices = []
            for c in range(self.n_classes):
                # only include boxes of the current class, with > 0 confidence
                class_mask = tf.cast(tf.equal(classes,
                                              tf.cast(c, dtype=tf.float32)),
                                     dtype=tf.float32)
                conf_mask = tf.cast(confidence > 0, dtype=tf.float32)
                mask = class_mask * conf_mask

                # Prunes away boxes that have high intersection-over-union (IOU)
                # overlap with previously selected boxes. Run nms independently
                # for each cl.
                selected_indices_per_class = tf.image.non_max_suppression(
                    boxes, confidence * mask, 1000, iou_threshold, 0.0)

                selected_indices.append(selected_indices_per_class)

            # Flatten nested list.
            selected_indices = tf.concat(selected_indices, axis=-1)
            selected_boxes = tf.gather(boxes, selected_indices)
            # TODO draw_boundin_boxes does not support labels right now.
            #selected_classes = tf.gather(classes, selected_indices)
            #selected_confidence = tf.gather(confidence, selected_indices)
            selected_boxes = tf.cast(tf.expand_dims(selected_boxes, 0),
                                     dtype=tf.float32)

            # Swap xy coordinates for bullshit tensorflow draw_bounding_boxes.
            x1 = selected_boxes[..., 0:1]
            y1 = selected_boxes[..., 1:2]
            x2 = selected_boxes[..., 2:3]
            y2 = selected_boxes[..., 3:4]
            boxes_yx = tf.concat([y1, x1, y2, x2], axis=-1)

            tb_img = tf.image.draw_bounding_boxes(
                tf.cast(tf.expand_dims(input_img[img, :, :, :], 0),
                        dtype=tf.float32), boxes_yx, self.colors)
            tb_imgs.append(tb_img)

        tb_output = tf.concat(tb_imgs, axis=0)
        #tf.summary.image("prediction", tb_output, step=step)
        return tb_output

    def _evaluate(self,
                  dataset,
                  iou_threshold=0.4,
                  class_conf_threshold=0.25,
                  mlflow=False,
                  tb=False,
                  lambda_coord=1.0,
                  lambda_obj=5.0,
                  lambda_noobj=1.0,
                  lambda_class=1.0,
                  max_outputs=2,
                  step=None,
                  step_float=None,
                  file_writer=None):  # pylint:disable=too-many-statements
        groundtruth_annotations_list = []
        img_list = []
        detections_list = []
        img_id = 1
        obj_id = 1
        val_loss_avg = tf.keras.metrics.Mean()
        for elements in dataset:
            images = elements[0]
            labels = elements[1]
            img_width = int(
                tf.cast(tf.shape(images)[1], dtype=tf.float32).numpy())
            img_height = int(
                tf.cast(tf.shape(images)[2], dtype=tf.float32).numpy())
            # Set training false, so that BN uses the mean and variance of
            # its moving statistics, learned during training.
            val_logits = self.model(images, training=False)
            loss = yolo_loss(labels,
                             val_logits,
                             self.anchors,
                             lambda_coord=lambda_coord,
                             lambda_obj=lambda_obj,
                             lambda_noobj=lambda_noobj,
                             lambda_class=lambda_class,
                             iou_threshold=iou_threshold,
                             step=step,
                             is_training=False)
            val_loss_avg.update_state(loss)

            if tb:
                # Validation prediction
                # Bounding box prediction to tensorboard.
                tb_prediction_val = self._prediction_to_tensorboard(
                    images, val_logits, max_outputs, step, iou_threshold,
                    class_conf_threshold)
                with file_writer.as_default():
                    tf.summary.image("validation",
                                     tb_prediction_val,
                                     step=step)

            # Coco mAP validation metrics.
            # Effective batch size. Last batch could contain fewer elements.
            eff_bs = tf.cast(tf.shape(images)[0],
                             dtype=tf.int32).numpy().item()
            bboxs, cat_ids, scores = self.coco_metric_format(
                val_logits, eff_bs, class_conf_threshold, iou_threshold, False)
            # Iterate over all detections per image.
            img_id_tmp = img_id
            for bbox_img, cat_id_img, score_img in zip(bboxs, cat_ids, scores):
                # Iterate over all detections in given img.
                for bbox, cat_id, score in zip(bbox_img, cat_id_img,
                                               score_img):
                    # bbox is: [xmin,ymin,xmax,ymax]
                    # bbox : [x,y,w,h]
                    xmin = bbox[0]
                    ymin = bbox[1]
                    xmax = bbox[2]
                    ymax = bbox[3]

                    # Center coordinate.
                    x = 0.5 * (xmin + xmax) * img_width
                    y = 0.5 * (ymin + ymax) * img_height
                    width = (xmax - xmin) * img_width
                    height = (ymax - ymin) * img_height
                    detect_item = {
                        'image_id': img_id_tmp,
                        'category_id': int(cat_id.item()),
                        'bbox': [x, y, width, height],
                        'score': score
                    }
                    detections_list.append(detect_item)

                img_id_tmp += 1

            bboxs, cat_ids, scores = self.coco_metric_format(
                labels, eff_bs, 0, iou_threshold, True)
            # Iterate over all objects in labels.
            img_id_tmp = img_id
            for bbox_img, cat_id_img, score_img in zip(bboxs, cat_ids, scores):
                # Iterate over all detections in given img.
                for bbox, cat_id, score in zip(bbox_img, cat_id_img,
                                               score_img):
                    # bbox is: [xmin,ymin,xmax,ymax]
                    # bbox : [x,y,w,h]
                    xmin = bbox[0]
                    ymin = bbox[1]
                    xmax = bbox[2]
                    ymax = bbox[3]

                    # Center coordinate.
                    x = 0.5 * (xmin + xmax) * img_width
                    y = 0.5 * (ymin + ymax) * img_height
                    width = (xmax - xmin) * img_width
                    height = (ymax - ymin) * img_height
                    grountruth_item = {
                        'id': obj_id,
                        'image_id': img_id_tmp,
                        'category_id': int(cat_id.item()),
                        'bbox': [x, y, width, height],
                        'area': width * height,
                        'iscrowd': 0
                    }
                    obj_id += 1
                    groundtruth_annotations_list.append(grountruth_item)
                img_list.append({"id": img_id_tmp})
                img_id_tmp += 1
            img_id += eff_bs

        groundtruth_dict = {
            'annotations': groundtruth_annotations_list,
            'images': img_list,
            'categories': self.category_list
        }
        #print("dl", detections_list)
        #print("-----------------")
        #print("dl_len", len(detections_list))
        #print("gt_len", len(groundtruth_annotations_list))
        #print("-----------------")
        #print("gt", groundtruth_dict)
        metrics = compute_coco_metrics(groundtruth_dict, detections_list)
        if tb:
            with file_writer.as_default():
                tf.summary.scalar("total_loss",
                                  val_loss_avg.result(),
                                  step=step)
                for key in metrics:
                    tf.summary.scalar(key, metrics[key], step=step)
            file_writer.flush()

        if mlflow:
            # Convert to native python type (db).
            mlflow.log_metric("mAP",
                              metrics["Precision/mAP"].item(),
                              step=step_float)
            mlflow.log_metric("mAP50IOU",
                              metrics["Precision/mAP@.50IOU"].item(),
                              step=step_float)
            mlflow.log_metric("mAP75IOU",
                              metrics["Precision/mAP@.75IOU"].item(),
                              step=step_float)
            mlflow.log_metric("mAPsmall",
                              metrics["Precision/mAP (small)"].item(),
                              step=step_float)
            mlflow.log_metric("mAPmedium",
                              metrics["Precision/mAP (medium)"].item(),
                              step=step_float)
            mlflow.log_metric("mAPlarge",
                              metrics["Precision/mAP (large)"].item(),
                              step=step_float)
            mlflow.log_metric("AR1",
                              metrics["Recall/AR@1"].item(),
                              step=step_float)
            mlflow.log_metric("AR10",
                              metrics["Recall/AR@10"].item(),
                              step=step_float)
            mlflow.log_metric("AR100",
                              metrics["Recall/AR@100"].item(),
                              step=step_float)
            mlflow.log_metric("AR100small",
                              metrics["Recall/AR@100 (small)"].item(),
                              step=step_float)
            mlflow.log_metric("AR100medium",
                              metrics["Recall/AR@100 (medium)"].item(),
                              step=step_float)
            mlflow.log_metric("AR100large",
                              metrics["Recall/AR@100 (large)"].item(),
                              step=step_float)
            mlflow.log_metric("val_loss",
                              val_loss_avg.result().numpy().item(),
                              step=step_float)
        print("...Done - loss {}\n".format(
            round(val_loss_avg.result().numpy().item(), 4)))
