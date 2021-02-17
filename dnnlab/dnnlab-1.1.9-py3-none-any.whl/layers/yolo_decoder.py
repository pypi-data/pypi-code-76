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
# =============================================================================
"""Yolo single spatial resolution output decoder. Gets a yolo output and
transforms it into a readable output for inference. Decoding consists of
class confidence thresholding and non-max suppression.

    Typical usage example:

    CLASSES = "path_to_your/classes.txt"
    MODEL = "path_to_your/yolo.h5"
    CONF = 0.25
    IOU = 0.4
    WIDTH = 416
    HEIGHT = 416
    DEPTH = 3


    model = tf.keras.models.load_model(MODEL)
    decoder = YOLODecoder(ANCHORS, classes, IOU, CONF)

    # Build a functional model.
    inputs = tf.keras.Input(shape=(WIDTH, HEIGHT, DEPTH), name="img")
    net = model(inputs)
    net = decoder(net)
    final = tf.keras.Model(inputs, net)

    # Export final model.
    final.save("yolo_decoded.h5")

    # Import final model.
    test = tf.keras.models.load_model("yolo_decoded.h5",
                                custom_objects={"YOLODecoder": YOLODecoder})
"""
import tensorflow as tf


class YOLODecoder(tf.keras.layers.Layer):
    """Yolo decoding and postprocessing as a custom keras layer.
    """
    def __init__(self, anchors, classes, iou_threshold, class_conf_threshold,
                 **kwargs):
        super().__init__(**kwargs)
        self.anchors = anchors
        self.classes = classes
        self.iou_threshold = iou_threshold
        self.class_conf_threshold = class_conf_threshold

    def build(self, input_shape):
        pass

    def get_config(self):
        config = super().get_config().copy()
        config.update({
            'anchors': self.anchors,
            'classes': self.classes,
            'iou_threshold': self.iou_threshold,
            'class_conf_threshold': self.class_conf_threshold,
        })
        return config

    @tf.function
    def call(self, input):
        grid_h = tf.cast(tf.shape(input)[1], dtype=tf.float32)
        grid_w = tf.cast(tf.shape(input)[2], dtype=tf.float32)
        n_boxes = tf.cast(tf.shape(input)[3], dtype=tf.float32)
        n_classes = tf.shape(input)[4] - 5

        grid_coord = self._yolo_grid(1, grid_h, grid_w, n_boxes)

        p_box_xy, p_box_wh, p_box_conf, p_box_class = self._extract_model_output(
            input, grid_coord, self.anchors)
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
        mask = class_confidence > self.class_conf_threshold
        masked_class_confidence = class_confidence * tf.cast(mask,
                                                             dtype=tf.float32)
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
                                 dtype=tf.int32)

        # Flatten class_confidence.
        masked_confidence = tf.reshape(masked_confidence, shape=[shape])

        #selected_indices = []
        #selected_indices = tf.TensorArray(tf.int32, size=0, dynamic_size=True)

        # apply multiclass NMS
        #for c in range(n_classes):
        #
        #    class_mask = tf.cast(tf.math.equal(masked_classes, c),
        #                         dtype=tf.float32)
        #    score_mask = tf.cast(masked_confidence > 0, dtype=tf.float32)
        #    mask = class_mask * score_mask
        #    # Prunes away boxes that have high intersection-over-union (IOU)
        #    # overlap with previously selected boxes. Run nms independently for
        #    # each class.
        #    selected_indices_per_class = tf.image.non_max_suppression(
        #        boxes, masked_confidence * mask, 100, self.iou_threshold, 0.0)
        # selected_indices.append(selected_indices_per_class)
        #  selected_indices = selected_indices.write(selected_indices.size(),
        # selected_indices_per_class)

        #selected_indices = selected_indices.stack()

        score_mask = tf.cast(masked_confidence > 0, dtype=tf.float32)
        # Prunes away boxes that have high intersection-over-union (IOU)
        # overlap with previously selected boxes.
        selected_indices = tf.image.non_max_suppression(
            boxes, masked_confidence * score_mask, 100, self.iou_threshold,
            0.0)

        # Flatten nested list.
        #selected_indices = tf.concat(selected_indices, axis=-1)
        selected_boxes = tf.gather(boxes, selected_indices)
        selected_confidence = tf.gather(masked_confidence, selected_indices)
        selected_classes = tf.gather(masked_classes, selected_indices)
        #result = tf.TensorArray(tf.int32, size=0, dynamic_size=True)
        #for c in selected_classes:
        #   result =  result.write(result.size(),
        #  self.classes[tf.cast(c, dtype=tf.int32).numpy()])

        return selected_confidence, selected_boxes, selected_classes

    def _yolo_grid(self, batch_size, grid_h, grid_w, boxes):
        """Ouputs yolo grid coordinates to use as cx, cy offsets from top left
        corner.

        Example of batch_size 1 and grid 2x2 and 1 anchors boxes.

            -----------------------
            -          -          -
            -   (0,0)  -   (0,1)  -
            -          -          -
            -----------------------
            -          -          -
            -   (1,0)  -   (1,1)  -
            -          -          -
            -----------------------

        Args:
            batch_size (int): Number of batches.
            grid (int): Grid.
            boxes (int): Number of different anchor boxes.

        Returns:
            [Tensor]: Coordinate grid values.
        """
        # TODO eval
        cell_x = tf.cast(tf.reshape(tf.tile(tf.range(grid_w), [grid_h]),
                                    (1, grid_h, grid_w, 1, 1)),
                         dtype=tf.float32)

        # TODO non symmetrie
        cell_y = tf.transpose(cell_x, (0, 2, 1, 3, 4))
        ## cell_gird.shape = (16, 13, 13, 5, 2)
        ## for any n, k, i, j
        ##    cell_grid[n, i, j, anchor, k] = j when k = 0
        ## for any n, k, i, j
        ##    cell_grid[n, i, j, anchor, k] = i when k = 1
        cell_grid = tf.tile(tf.concat([cell_x, cell_y], -1),
                            [batch_size, 1, 1, boxes, 1])

        return cell_grid

    def _extract_model_output(self, y_pred, grid_coord, anchors):
        """Extract loss specific yolov2 values from model output.

        Args:
            y_pred (Tensor): Yolov2 specific format:
                (BS, GRIDW, GRIDH, BOXES, 5 + CLASSES)
            grid_coord (Tensor): Grid coordinates as cluster centroids.
            anchors (list): List of all anchor widths and heights (Priors).

        Returns:
            box_xy: (tx, ty) -> Center coordinates of object midpoints.
                (BS, GRIDW, GRIDH, BOXES, 2)
            box_wh: (tw, th) -> Anchor box prior offsets.
                (BS, GRIDW, GRIDH, BOXES, 2)
            box_conf: Box confidence values.
                (BS, GRIDW, GRIDH, BOXES, 1)
            box_class: Unprocessed conditional Class probabilities.
                (BS, GRIDW, GRIDH, BOXES, num_classes)
        """
        # Number of anchor boxes.
        boxes = tf.shape(y_pred)[3]

        # Unrestricted xy object midpoints (center coords) (tx, ty).
        box_xy = y_pred[..., 0:2]
        # Direct location prediction!
        # bx = sig(tx) + cx <- Grid cell offset from top left
        # by = sig(ty) + cy <- Grid cell offset from top left
        box_xy = tf.cast(tf.sigmoid(box_xy), dtype=tf.float32) + grid_coord

        # Unrestricted w, h values.
        box_wh = y_pred[..., 2:4]
        # Make w, h strictly positive values. TODO check
        box_wh = tf.cast(tf.exp(box_wh), dtype=tf.float32) * tf.cast(
            tf.reshape(anchors, [1, 1, 1, boxes, 2]), dtype=tf.float32)

        # Restrict box_confidence values to [0, 1].
        # Shape (bs, grid, grid, anchors, 1)

        box_conf = tf.sigmoid(y_pred[..., 4:5])
        # Unrestricted conditional class probabilities: [pC1, pC2....pCn] ->
        # Later input to softmax, so no neccessary processing here.
        box_classes = y_pred[..., 5:]

        return box_xy, box_wh, box_conf, box_classes
