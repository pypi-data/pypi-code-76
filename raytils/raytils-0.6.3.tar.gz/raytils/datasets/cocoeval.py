import copy
import math
import os
import time
from collections import OrderedDict
from typing import Tuple, Optional, List

import matplotlib.pyplot as plt
import numpy as np
from rays_pycocotools.coco import COCO
from rays_pycocotools.cocoeval import COCOeval as __COCOeval
from rays_pycocotools.cocoeval import Params as __Params

__all__ = ["COCOEvalExtended"]


class ParamsExtended(__Params):
    """ Adds the ability to define custom IoU (Intersection of Union) ranges for COCO evaluation (pycocotools.cocoeval)

    Extends the pycocotools.cocoeval.Params object.
    Best used with https://github.com/RaymondKirk/cocoapi/tree/python-api instead of the cocodataset/cocoapi package

    Distribution for setup.py or pip 'pycocotools @ https://github.com/RaymondKirk/cocoapi/archive/python-api.zip'

    Attributes:
        iou_type: 'segm' or 'bbox' determines how the IoU is calculated (mask or bounding box)
        iou_rng: The range of IoU values for evaluation in the form (IoU min, IoU max, IoU step) the default parameters
                 are (0.5, 0.95, 0.05)
        rec_rng: The range of Recall values to calculate precision at for evaluation in the form
                 (recall min, recall max, recall step) the default parameters are (0.0, 1.0, 0.01)
        area_rng: The range of area values to threshold the evaluation at. Default (0->Inf, 0-32^2, 32^2-96^2, 96^2-Inf)
        area_rng_labels: Descriptor of area range. Default ('all', 'small', 'medium', 'large').
    """

    def __init__(self, iou_type: str = 'segm', iou_rng: Tuple[float, float, float] = None,
            rec_rng: Tuple[float, float, float] = None,
            area_rng: Tuple[List[float], List[float], List[float], List[float]] = None,
            area_rng_labels: Tuple[str, str, str, str] = None):
        super().__init__(iou_type)

        # Override iou parameters set by set[Det/Kp]Params function
        if iou_rng is None:
            iou_rng = (0.5, 0.95, 0.05)
        if rec_rng is None:
            rec_rng = (0.0, 1.0, 0.01)
        if area_rng_labels is None:
            area_rng_labels = ('all', 'small', 'medium', 'large')
        if area_rng is None:
            area_rng = ([0 ** 2, float("inf")], [0 ** 2, 32 ** 2], [32 ** 2, 96 ** 2], [96 ** 2, float("inf")])
        if 0 <= len(area_rng) > 4:
            raise ValueError("Invalid area range defined")
        self.iouLow, self.iouHigh, self.iouStep = iou_rng
        self.recLow, self.recHigh, self.recStep = rec_rng
        self.iouThrs = np.linspace(self.iouLow, self.iouHigh,
                                   int(np.round((self.iouHigh - self.iouLow) / self.iouStep)) + 1, endpoint=True)
        self.recThrs = np.linspace(self.recLow, self.recHigh,
                                   int(np.round((self.recHigh - self.recLow) / self.recStep)) + 1, endpoint=True)
        self.areaRng = list(area_rng)
        self.areaRngLbl = list(area_rng_labels)
        print()


class COCOEvalExtended(__COCOeval):
    """Extends the COCOeval object in pycocotools.cocoeval

    COCOEval computes the precision and recall over the dependant variable Iou Thresh
    Provides additional functionality such as the abilty to generate error analysis graphs.

    The analysis function is in the style of http://dhoiem.cs.illinois.edu/publications/eccv2012_detanalysis_derek.pdf

    Attributes:    #  cocoGt=..., cocoDt=...       # load dataset and results
        coco_gt: COCO json dataset ground truth file (gt=ground truth)
        coco_dt: COCO json dataset predictions file (dt=detections)
        iou_type: 'segm' or 'bbox' determines how the IoU is calculated (mask or bounding box)
        iou_rng: The range of IoU values for evacuation in the form (IoU min, IoU max, IoU step) the default parameters
                 are (0.5, 0.95, 0.05)
        rec_rng: The range of Recall values to calculate precision at for evaluation in the form
                 (recall min, recall max, recall step) the default parameters are (0.0, 1.0, 0.01)
        area_rng: The range of area values to threshold the evaluation at. Default (0->Inf, 0-32^2, 32^2-96^2, 96^2-Inf)
        area_rng_labels: Descriptor of area range. Default ('all', 'small', 'medium', 'large').
    """

    def __init__(self, coco_gt: COCO = None, coco_dt: COCO = None, iou_type: str = 'segm',
            iou_rng: Optional[Tuple[float, float, float]] = None,
            rec_rng: Tuple[float, float, float] = None,
            area_rng: Tuple[List[float], List[float], List[float], List[float]] = None,
            area_rng_labels: Tuple[str, str, str, str] = None):
        super().__init__(coco_gt, coco_dt, iou_type)
        self.analyze_figures = {}  # for analyse function to store plots
        self.params = ParamsExtended(iou_type, iou_rng, rec_rng, area_rng, area_rng_labels)
        if coco_gt is not None:
            self.params.imgIds = sorted(coco_gt.getImgIds())
            self.params.catIds = sorted(coco_gt.getCatIds())
        self.eval_cm = {}
        self.eval_images_cm = {}
        self.ious_cm = {}

    @staticmethod
    def from_file(coco_gt_json, coco_dt_json, *args, **kwargs):
        """Utility function to get COCOEvaluator object from two file paths instead of COCO objects

        Args:
            coco_gt_json: File path to the *.json coco ground truth file
            coco_dt_json: File path to the *.json coco predictions file
            *args: Passed to the constructed COCOEvalExtended object
            **kwargs: Passed to the constructed COCOEvalExtended object

        Returns:
            COCOEvalExtended object
        """
        coco_gt = COCO(coco_gt_json)
        coco_dt = coco_gt.loadRes(coco_dt_json)
        return COCOEvalExtended(coco_gt, coco_dt, *args, **kwargs)

    def summarise_extended(self):
        """Replaces functionality of COCOEval.summarize with added evaluation metrics

            Adds clarity to an otherwise unreadable function.
        """

        def __summarise(metric, iou_threshold=None, area_range_str='all', max_detections=100):
            p = self.params
            i_str = ' {:<18} {} @[ IoU={:<9} | area={:>6s} | maxDets={:>3d} ] = {:0.3f}'
            title_str = {'af1': 'Average F1', 'ap': 'Average Precision', 'ar': 'Averge Recall'}[metric]
            type_str = {'af1': '(AF1)', 'ap': '(AP) ', 'ar': '(AR) '}[metric]

            if iou_threshold is None:
                iou_str = '{:0.2f}:{:0.2f}'.format(p.iouThrs[0], p.iouThrs[-1])
                iou_threshold_params_index = slice(None)  # All the iou thresholds
            else:
                iou_str = '{:0.2f}'.format(iou_threshold)
                iou_threshold_params_index = np.where(iou_threshold == p.iouThrs)[0]

            area_index = [i for i, area_range_lbl in enumerate(p.areaRngLbl) if area_range_lbl == area_range_str]
            max_dets_index = [i for i, max_dets in enumerate(p.maxDets) if max_dets == max_detections]

            # [TxRxKxAxM] T=p.iou_threshes, R=p.recall_threshes, K=classes, A=p.areas, M=p.max dets
            if metric == 'ap':
                # Dimension of precision: [T x R x K x A x M] (see above notation)
                s_value = self.eval['precision'][iou_threshold_params_index][:, :, :, area_index, max_dets_index]
            elif metric == 'ar':
                # Dimension of recall: [T x K x A x M] (see above notation)
                s_value = self.eval['recall'][iou_threshold_params_index][:, :, area_index, max_dets_index]
            elif metric == "af1":
                precision = self.eval['precision'][iou_threshold_params_index]
                recall = self.eval['recall'][iou_threshold_params_index]
                precision = precision.mean(axis=1)  # Mean on the recall threshold axis R
                f1 = 2 * (precision * recall) / (precision + recall + np.finfo(float).eps)
                s_value = f1[:, :, area_index, max_dets_index]
            else:
                raise ValueError(f"Metric '{metric}' isn't supported in COCOEvalExtended")

            # Check all values are > -1 (-1 used for invalid/NaN)
            if len(s_value[s_value > -1]) == 0:
                metric_value = -1
            else:
                metric_value = np.mean(s_value[s_value > -1])

            print(i_str.format(title_str, type_str, iou_str, area_range_str, max_detections, metric_value))
            return metric_value

        def __summarise_detections():
            stats = np.zeros((18,))
            stats[0] = __summarise("ap")
            stats[1] = __summarise("ap", iou_threshold=.5, max_detections=self.params.maxDets[2])
            stats[2] = __summarise("ap", iou_threshold=.75, max_detections=self.params.maxDets[2])
            stats[3] = __summarise("ap", area_range_str='small', max_detections=self.params.maxDets[2])
            stats[4] = __summarise("ap", area_range_str='medium', max_detections=self.params.maxDets[2])
            stats[5] = __summarise("ap", area_range_str='large', max_detections=self.params.maxDets[2])
            stats[6] = __summarise("ar", max_detections=self.params.maxDets[0])
            stats[7] = __summarise("ar", max_detections=self.params.maxDets[1])
            stats[8] = __summarise("ar", max_detections=self.params.maxDets[2])
            stats[9] = __summarise("ar", area_range_str='small', max_detections=self.params.maxDets[2])
            stats[10] = __summarise("ar", area_range_str='medium', max_detections=self.params.maxDets[2])
            stats[11] = __summarise("ar", area_range_str='large', max_detections=self.params.maxDets[2])

            stats[12] = __summarise("af1")
            stats[13] = __summarise("af1", iou_threshold=.5, max_detections=self.params.maxDets[2])
            stats[14] = __summarise("af1", iou_threshold=.75, max_detections=self.params.maxDets[2])
            stats[15] = __summarise("af1", area_range_str='small', max_detections=self.params.maxDets[2])
            stats[16] = __summarise("af1", area_range_str='medium', max_detections=self.params.maxDets[2])
            stats[17] = __summarise("af1", area_range_str='large', max_detections=self.params.maxDets[2])

            return stats

        def __summarise_keypoints():
            stats = np.zeros((10,))
            stats[0] = __summarise(1, max_detections=20)
            stats[1] = __summarise(1, max_detections=20, iou_threshold=.5)
            stats[2] = __summarise(1, max_detections=20, iou_threshold=.75)
            stats[3] = __summarise(1, max_detections=20, area_range_str='medium')
            stats[4] = __summarise(1, max_detections=20, area_range_str='large')
            stats[5] = __summarise(0, max_detections=20)
            stats[6] = __summarise(0, max_detections=20, iou_threshold=.5)
            stats[7] = __summarise(0, max_detections=20, iou_threshold=.75)
            stats[8] = __summarise(0, max_detections=20, area_range_str='medium')
            stats[9] = __summarise(0, max_detections=20, area_range_str='large')
            return stats

        def __summarise_detections_confusion_matrix():
            iou_ind = area_ind = 0
            max_det_ind = len(self.params.maxDets) - 1
            cm = self.eval_cm["confusion_matrix"][iou_ind, area_ind, max_det_ind]
            class_names = ["None"] + [c["name"] for c in self.cocoGt.cats.values()]
            cm_printer = ConfusionMatrix(cm, class_names=class_names)

            i_str = ' {:<18} @[ IoU={:<9} | area={:>6s} | maxDets={:>3d} ]'
            iou_str = '{:0.2f}'.format(self.params.iouThrs[iou_ind])
            area_str = self.params.areaRngLbl[area_ind]
            print(i_str.format("\nConfusion matrix", iou_str, area_str, self.params.maxDets[max_det_ind]))
            cm_printer.tabulate()
            cm_printer.summarise()
            # print(i_str.format("\nBinary Confusion matrix", iou_str, area_str, self.params.maxDets[max_det_ind]))
            # bcm = self.eval_cm["binary_confusion_matrix"][iou_ind, area_ind, max_det_ind]
            # bcm_class_names = ["None"] + ['+'.join([c["name"] for c in self.cocoGt.cats.values()])]
            # bcm_printer = ConfusionMatrix(bcm, class_names=bcm_class_names)
            # bcm_printer.tabulate()
            # bcm_printer.summarise()

        if not self.eval:
            raise Exception('Please run accumulate() first')

        iou_type = self.params.iouType
        if iou_type == 'segm' or iou_type == 'bbox':
            if self.eval_cm:
                __summarise_detections_confusion_matrix()
            summarise = __summarise_detections
        elif iou_type == 'keypoints':
            summarise = __summarise_keypoints
        else:
            raise ValueError(f"IoU type '{iou_type}' not supported in COCOEvalExtended")

        self.stats = summarise()

    def __str__(self):
        self.summarise_extended()

    def accumulate(self, p=None, cm=True):
        """Wrapper for COCOEval.accumulate to also run extra metrics"""
        super().accumulate(p)
        if cm:
            self.__accumulate_class_wise_confusion_matrix()

    def evaluate(self, cm=True):
        """Wrapper for COCOEval.evaluate to ensure extra metrics are computed (confusion matrix)

            Summary of internal cocoapi metrics computation here:
            https://blog.zenggyu.com/en/post/2018-12-16/an-introduction-to-evaluation-metrics-for-object-detection/
        Args:
            cm: Confusion matrix if true in self.eval_cm if true
        """
        super().evaluate()

        if cm:
            p = self.params
            if p.iouType == 'segm' or p.iouType == 'bbox':
                print('Running per image evaluation for confusion matrix...')
                tic = time.time()

                # loop through images, area range, max detection number
                category_ids = p.catIds if p.useCats else [-1]
                compute_iou = self.computeIoU
                max_det = p.maxDets[-1]
                temp_use_cats = self.params.useCats
                self.params.useCats = False
                self.ious_cm = {(imgId, catId): compute_iou(imgId, catId) for imgId in p.imgIds for catId in
                                category_ids}
                evaluate_image_confusion_matrix = self.__evaluate_image_confusion_matrix
                self.eval_images_cm = [evaluate_image_confusion_matrix(imgId, areaRng, max_det)
                                       for areaRng in p.areaRng
                                       for imgId in p.imgIds]
                self.params.useCats = temp_use_cats
                toc = time.time()
                print('DONE (t={:0.2f}s).'.format(toc - tic))
            else:
                print("Warning: Only 'segm' and 'bbox' is currently supported for 'p.iouType' confusion matrix")

    def __evaluate_image_confusion_matrix(self, img_id, a_rng, max_det):
        """Perform confusion matrix evaluation for single image. Gather all actual and predicted values.

            1. Generates a y_true array with the classes of ground truth annotations, skipping annotations
                outside the range of the threshold parameters
            2. Matches detections to the ground truth annotations and generates a y_pred array of detection classes
            3. For all unmatched detections update y_true with 0 and y_pred with the class ID
            4. Return y_true and y_pred

        """
        params = self.params
        ground_truth = [_ for cId in params.catIds for _ in self._gts[img_id, cId]]
        detections = [_ for cId in params.catIds for _ in self._dts[img_id, cId]]
        if len(ground_truth) == 0 and len(detections) == 0:
            return None

        for gt_data in ground_truth:
            gt_data['_ignore'] = gt_data['ignore'] or (gt_data['area'] < a_rng[0] or gt_data['area'] > a_rng[1])

        # Sort detections with the highest score first and ground truth with ignore flag last
        gt_sorted_indexes = np.argsort([g['_ignore'] for g in ground_truth], kind='mergesort')
        ground_truth = [ground_truth[i] for i in gt_sorted_indexes]
        dt_sorted_indexes = np.argsort([-d['score'] for d in detections], kind='mergesort')
        detections = [detections[i] for i in dt_sorted_indexes[0:max_det]]
        gt_iscrowd = [int(o['iscrowd']) for o in ground_truth]

        # load computed ious
        ious = self.ious_cm[img_id, params.catIds[0]][:, gt_sorted_indexes] \
            if len(self.ious_cm[img_id, params.catIds[0]]) > 0 else self.ious_cm[img_id, params.catIds[0]]

        iou_thresh_count = len(params.iouThrs)

        ground_truth_matches = np.zeros((iou_thresh_count, len(ground_truth)))
        ground_truth_ignore = np.array([g['_ignore'] for g in ground_truth])
        eps = np.finfo(float).eps

        y_true = np.asarray(
            [gt["category_id"] for i, gt in enumerate(ground_truth) if not ground_truth_ignore[i]]
        ).reshape(1, -1).repeat(iou_thresh_count, 0).tolist()
        y_pred = np.zeros_like(y_true).tolist()

        if not len(ious) == 0:
            for iou_thresh_ind, iou_thresh in enumerate(params.iouThrs):
                unmatched_y_pred = []
                for detection_ind, d in enumerate(detections):
                    # Skip if invalid area range
                    if d['area'] < a_rng[0] or d['area'] > a_rng[1]:
                        continue

                    # Information about best match so far (m=-1 -> unmatched)
                    iou = min([iou_thresh, 1 - eps])
                    gt_match_index = -1

                    for gt_index in range(len(ground_truth)):
                        # If this ground truth detection already matched and not a crowd then continue
                        if ground_truth_matches[iou_thresh_ind, gt_index] > 0 and not gt_iscrowd[gt_index]:
                            continue
                        # If dt matched to reg gt, and on ignore gt, stop
                        if gt_match_index > -1 and ground_truth_ignore[gt_match_index] == 0 and ground_truth_ignore[
                            gt_index] == 1:
                            break
                        # Continue to next gt unless better match made
                        if ious[detection_ind, gt_index] < iou:
                            continue
                        # If match successful and best so far, store appropriately
                        iou = ious[detection_ind, gt_index]
                        gt_match_index = gt_index

                    # If no match then continue else store id of match for both dt and gt
                    if gt_match_index == -1:
                        unmatched_y_pred.append(d["category_id"])
                        continue

                    if not ground_truth_ignore[gt_match_index]:
                        y_pred[iou_thresh_ind][gt_match_index] = d["category_id"]
                    ground_truth_matches[iou_thresh_ind, gt_match_index] = d['id']

                y_true[iou_thresh_ind].extend([0] * len(unmatched_y_pred))
                y_pred[iou_thresh_ind].extend(unmatched_y_pred)

        # Store results for given image
        return {
            'image_id': img_id,
            'aRng': a_rng,
            'maxDet': max_det,
            'y_true': y_true,
            'y_pred': y_pred,
        }

    def __accumulate_class_wise_confusion_matrix(self, p=None):
        '''Accumulate per image evaluation results for confusion matrix and store the result in self.eval

        :param p: input params for evaluation
        :return: None
        '''
        print('Accumulating evaluation results for confusion matrix...')
        tic = time.time()

        if not self.eval_images_cm:
            print('Please run evaluate() first')

        # allows input customized parameters
        if p is None:
            p = self.params

        p.catIds = p.catIds if p.useCats == 1 else [-1]
        iou_len = len(p.iouThrs)
        class_len = len(p.catIds) if p.useCats else 1
        area_len = len(p.areaRng)
        mdets_len = len(p.maxDets)

        # [TxKxAxMxCxC] (C=N Classes)
        n_classes = class_len + 1
        class_wise_confusion_matrix = -np.ones((iou_len, area_len, mdets_len, n_classes, n_classes))
        binary_confusion_matrix = -np.ones((iou_len, area_len, mdets_len, 2, 2))

        # Create dictionaries for future indexing
        _pe = self._paramsEval
        catIds = _pe.catIds if _pe.useCats else [-1]
        setK = set(catIds)
        setA = set(map(tuple, _pe.areaRng))
        setM = set(_pe.maxDets)
        setI = set(_pe.imgIds)

        # Get index lists of parameters to evaluate
        if 0 in setK:
            raise ValueError("Please start category ids from 1! Cannot assign 0 for No Object class")
        class_ind_list = [0] + [int(k) for n, k in enumerate(p.catIds) if k in setK]
        m_list = [m for n, m in enumerate(p.maxDets) if m in setM]
        area_ind_list = [n for n, a in enumerate(map(lambda x: tuple(x), p.areaRng)) if a in setA]
        image_ind_list = [n for n, i in enumerate(p.imgIds) if i in setI]
        image_list_count = len(_pe.imgIds)

        # Retrieve evaluation image at each area range and max number of detections
        for area_ind in area_ind_list:
            Na = area_ind * image_list_count
            for max_det_ind, max_det in enumerate(m_list):
                # Get all evaluation images for the current parameter combination
                evaluation_images = [self.eval_images_cm[Na + i] for i in image_ind_list]
                evaluation_images = [e for e in evaluation_images if e is not None]
                if len(evaluation_images) == 0:
                    continue

                y_true = [[] for _ in range(iou_len)]
                y_pred = [[] for _ in range(iou_len)]

                for img in evaluation_images:
                    for iou_thresh in range(iou_len):
                        y_true[iou_thresh].extend(img["y_true"][iou_thresh][0:max_det])
                        y_pred[iou_thresh].extend(img["y_pred"][iou_thresh][0:max_det])

                class_wise_confusion_matrix[:, area_ind, max_det_ind, :, :] = [
                    ConfusionMatrix.get_matrix(gt, dt, labels=class_ind_list) for gt, dt in zip(y_true, y_pred)
                ]

                binary_confusion_matrix[:, area_ind, max_det_ind, :, :] = [
                    ConfusionMatrix.get_matrix(
                        [0 if g == 0 else 1 for g in gt],
                        [0 if d == 0 else 1 for d in dt], labels=[0, 1]) for gt, dt in zip(y_true, y_pred)
                ]

        self.eval_cm = {'params': p, 'confusion_matrix': class_wise_confusion_matrix,
                        "binary_confusion_matrix": binary_confusion_matrix}

        toc = time.time()
        print('DONE (t={:0.2f}s).'.format(toc - tic))

    def plot_class_pr(self, fig=None, save_to_dir=None, show=False, save_ext=".pdf"):
        """Display the precision/recall curve of the COCOeval evaluation

        This function shows a basic PR curve for the COCOeval evaluation

        Usage:
        .. code-block:: python

            coco_evaluator = COCOEvalExtended.from_file(ground_truth_file_path, predictions_file_path)
            coco_evaluator.plot_class_pr(class_names=coco_evaluator.cocoGt.cats, save_to_dir=None, show=True)

        Args:
            fig: A figure object to plot the pr curve on, if None it will create one
            class_names: The list of class names from the evaluated predictions
            save_to_dir: The directory to save the plots to i.e 'figures', if None the figures are not saved
            show: Opens the plots in a matplotlib window if True
            save_ext: matplotlib figure save extension (.pdf|.png|.jpg etc.)

        Returns:
            The figure object of the rendered plot
        """

        def __plot_pr_curve(iou_threshold=None, area_range_str='all', max_detections=100, fig=None, save_dir=None,
                show=False):

            # If iou_threshold == None get all the iou_thresholds
            iou_threshold_index = slice(None) if iou_threshold is None else \
                np.where(iou_threshold == self.params.iouThrs)[0]

            # Get the area index in the params that corresponds to the area string
            area_index = self.params.areaRngLbl.index(area_range_str)
            max_det_index = self.params.maxDets.index(max_detections)

            # Get precision values for recall thresholds of self.params.recThrs
            # T=p.iou_threshes, R=p.recall_threshes, K=classes, A=p.areas, M=p.max dets
            recall_thresholds = self.params.recThrs

            precision = self.eval['precision']  # [T x R x K x A x M]
            recall = self.eval['recall']  # [T x K x A x M]

            # Calculate PR for classes
            class_id_to_index = {v: i for i, v in enumerate(self.eval["params"].catIds)}
            classes = {lbl_index: self.cocoGt.cats[lbl_id]["name"] for lbl_id, lbl_index in class_id_to_index.items()}

            fig = plt.figure(figsize=(9, 7))
            colours = plt.rcParams['axes.prop_cycle'].by_key()['color']

            for class_index, class_name in classes.items():
                # Get precision values for filters and class K=class_index (remove invalid values -1)
                precision_values = precision[iou_threshold_index, :, class_index, area_index, max_det_index]
                precision_values = precision_values[precision_values > -1]

                # Get recall value for filters and class K=class_index (remove invalid values -1)
                recall_value = recall[iou_threshold_index, class_index, area_index, max_det_index]
                recall_value = recall_value[recall_value > -1]

                # Get F1 Score from mean of precision and recall
                recall_mean, precision_mean = recall_value.mean(), precision_values.mean()
                f1_value = 2 * (precision_mean * recall_mean) / (precision_mean + recall_mean + np.finfo(float).eps)

                # Plot F1 chart of precision calculated at recall values
                cls_colour = colours[class_index]
                plt.step(recall_thresholds, precision_values, color=cls_colour, alpha=1.0, where='pre',
                         label=class_name)
                plt.fill_between(recall_thresholds, precision_values, alpha=0.2, color=cls_colour, step='pre')
                plt.xlabel('Recall')
                plt.ylabel('Precision')
                plt.ylim([0.0, 1.0])
                plt.xlim([0.0, 1.0])
                # Fancy F1 display (solution lines)
                for f_score in np.linspace(0.2, 0.8, num=4):
                    x = np.linspace(0.01, 1)
                    y = f_score * x / (2 * x - f_score)
                    plt.plot(x[y >= 0], y[y >= 0], color='gray', alpha=0.2)
                    plt.annotate(r'$F_1$' + '= {0:0.1f}'.format(f_score), xy=(0.89, y[45] + 0.02), color='gray')
                # Plot actual F1 score (get from array to pixel perfect plot, actual value has greater resolution)
                f1_plotted_line = 2 * ((recall_thresholds * precision_values) /
                                       (precision_values + recall_thresholds + np.spacing(1)))
                f1_idx = f1_plotted_line.argmax()
                plt.scatter(recall_thresholds[f1_idx], precision_values[f1_idx], marker='s', color=cls_colour)
                plt.annotate(r'$F_1$' + "= {:0.3f}".format(f1_value),
                             xy=(recall_thresholds[f1_idx], precision_values[f1_idx]))
                # Plot F1 solution space of F1 score
                f1_possible_x = np.linspace(0.01, 1, 100)
                f1_possible_y = f1_plotted_line[f1_idx] * f1_possible_x / (2 * f1_possible_x - f1_plotted_line[f1_idx])
                plt.plot(f1_possible_x[f1_possible_y >= 0], f1_possible_y[f1_possible_y >= 0], color=cls_colour,
                         alpha=0.5)

            iou_str = '{:0.2f}:{:0.2f}'.format(self.params.iouThrs[0], self.params.iouThrs[-1]) \
                if iou_threshold is None else '{:0.2f}'.format(iou_threshold)
            plot_name = "AllClasses_IOU={}_Area={}_MaxDets={}".format(iou_str, area_range_str, max_detections)
            plt.legend(loc='lower left')
            plt.title(plot_name.replace("_", " "))
            plt.tight_layout()

            if show:
                plt.show()

            # if save_dir is set, figure will be saved to save_dir
            if save_dir is not None:
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)

                save_file = f"{save_dir}/{plot_name.replace(' ', '_')}{save_ext}"
                print('save figure to %s' % save_file)
                fig.savefig(save_file)
            plt.close()

            return fig

        def _plotDets(fig=None, save_to_dir=None, show=False):
            return __plot_pr_curve(iou_threshold=self.params.iouLow, max_detections=self.params.maxDets[-1], fig=fig,
                                   save_dir=save_to_dir, show=show)

        if not self.eval:
            raise Exception('Please run accumulate() first')

        if self.params.iouType == 'segm' or self.params.iouType == 'bbox':
            plot_fn = _plotDets
        else:
            raise ValueError("Only iouType segm or bbox supported")

        return plot_fn(fig=fig, save_to_dir=save_to_dir, show=show)

    def __makeplot(self, recThrs, precisions, recalls, name, save_dir=None, show=False, iou_labels=None,
            font_size=None, save_ext=".pdf"):
        def strip_tfloat(f, p):  # Strips leading 0 and displays to p sig fig
            return ("{:." + str(p) + "f}").format(f)[1:]

        if iou_labels is None:
            iou_labels = ['C75', 'C50', 'LOC']
        if save_dir is not None and not os.path.exists(save_dir):
            os.makedirs(save_dir)
        # precisions  7x101x4x1]
        assert precisions.shape[2] == 4
        assert recalls.shape[1] == 4
        areaNms = ['All Areas', 'Small Area <32x32px', 'Medium Area [<96x96px]', 'Large Area [>96x96px]']
        areaNms = [
            f"{self.params.areaRngLbl[i]} area {self.params.areaRng[i][0] ** 0.5}< a < {self.params.areaRng[i][1] ** 0.5}"
            for i in range(len(self.params.areaRng))]
        figures_np = {}

        if font_size is not None:
            plt.rcParams.update({'font.size': 20})

        for aidx in range(precisions.shape[2]):
            plotname = '%s - %s' % (name, areaNms[aidx])
            # ps shape 7x101
            ps = precisions[:, :, aidx, 0].squeeze()
            rs = recalls[:, aidx, 0].squeeze()
            ap = np.mean(ps, axis=1)

            # TODO: Enable functionality to calculate f1 from recallThrs or actual recall
            # f1_value = 2 * (precision_mean * recall_mean) / (precision_mean + recall_mean + np.finfo(float).eps)
            f1_values = 2 * (ap * rs) / (ap + rs + np.finfo(float).eps)

            ds = np.concatenate((np.expand_dims(ps[0], axis=0), np.diff(ps, axis=0)))
            colors = [[.13, .54, .68], [0.5, 0.5, 0.5], [.05, .13, .29], [.75, .31, .30], [.36, .90, .38],
                      [.50, .39, .64], [1.0, .6, 0.0]]
            # Calculate each lines F1 score

            # format legend str
            ln = [iou_labels[0], iou_labels[1], iou_labels[2], 'SIM', 'CLS', 'BGR', 'FIN']
            ls = copy.copy(ln)
            for i in range(precisions.shape[0]):
                if ap[i] == 1.0:
                    ls[i] = r'AP=1.00 $F_1$=1.00 ' + ls[i]
                else:
                    ls[i] = "AP={} $F_1$={} {}".format(strip_tfloat(ap[i], 3), strip_tfloat(f1_values[i], 3), ls[i])

            fig = plt.figure(figsize=(9, 7))
            plt.stackplot(recThrs, ds, labels=ls, colors=colors, alpha=0.5)

            for f_score in np.linspace(0.2, 0.8, num=4):
                x = np.linspace(0.01, 1)
                y = f_score * x / (2 * x - f_score)
                plt.plot(x[y >= 0], y[y >= 0], color='gray', alpha=0.3)
                plt.annotate(r'$F_1$' + '= {0:0.1f}'.format(f_score), xy=(.875, y[45] + 0.02), color='gray')

            # Calculate F1 for Arrays
            plt_f1_for = [0, 1]
            for j in plt_f1_for:
                f1_plotted_line = 2 * ((recThrs * ds[j]) /
                                       (ds[j] + recThrs + np.spacing(1)))
                f1_idx = f1_plotted_line.argmax()
                plt.scatter(recThrs[f1_idx], ds[j][f1_idx], marker='s', color=colors[j])
                plt.annotate(r'$F_1$' + "= {:0.3f}".format(f1_values[j]),
                             xy=(recThrs[f1_idx], recThrs[f1_idx]))
                # Plot F1 solution space of F1 score
                f1_possible_x = np.linspace(0.01, 1, 100)
                f1_possible_y = f1_plotted_line[f1_idx] * f1_possible_x / (2 * f1_possible_x - f1_plotted_line[f1_idx])
                plt.plot(f1_possible_x[f1_possible_y >= 0], f1_possible_y[f1_possible_y >= 0], color=colors[j],
                         alpha=0.5)

            plt.axis([0.0, 1.0, 0.0, 1.0])
            plt.legend(loc='lower left')
            plt.xlabel('Recall')
            plt.ylabel('Precision')
            plt.title(plotname)
            plt.tight_layout()

            # if save_dir is set, figure will be saved to save_dir
            if save_dir is not None:
                save_file = f"{save_dir}/{plotname.replace(' ', '_')}{save_ext}"
                print('save figure to %s' % save_file)
                fig.savefig(save_file)

            fig.canvas.draw()
            data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
            data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
            figures_np[plotname] = (data, fig)

            if show:
                plt.show()

            plt.close()

        return figures_np

    def analyze(self, save_to_dir=None, show=False, iou_threshes=None, iou_labels=None, font_size=None,
            save_ext=".pdf"):
        """Derek Hoiem et al., inspired breakdown of false positives in COCO predictions

        Usage:
        .. code-block:: python

            iou_rng = (0.5, 0.95, 0.05)  # Standard COCO evaluation metrics
            coco_eval = COCOEvalExtended(coco_true, coco_pred, iouType='bbox', iouRng=iou_rng)
            # Standard coco eval summary
            coco_eval.params.imgIds = image_ids
            coco_eval.evaluate()
            coco_eval.accumulate()
            coco_eval.summarize()
            stats = coco_eval.stats.copy()

            # Analysis plots
            coco_eval.plot_class_pr(class_names=dataset.labels, save_to_dir='{}figures'.format(name), show=True)
            iou_labels = ["C75", "C50", "LOC"]  # Standard scales for the localisation error analysis
            iou_threshes = [0.75, 0.5, 0.1]
            _ = coco_eval.analyze('{}figures'.format(name), show=True, iou_threshes=iou_threshes,
                                  iou_labels=iou_labels)


        Custom implementation for F1 support etc, originally from Matlab code for http://cocodataset.org/#detection-eval
        The categories of evaluation summarised in this plot are listed below, each step is more permissive allowing a
        clean visualisation of the errors in object detection by stacking the PR curves

        .. code-block::

            C75: PR at IoU=.75 (AP at strict IoU), area under curve corresponds to APIoU=.75 metric.
            C50: PR at IoU=.50 (AP at PASCAL IoU), area under curve corresponds to APIoU=.50 metric.
            Loc: PR at IoU=.10 (localization errors ignored, but not duplicate detections). All remaining settings use IoU=.1.
            Sim: PR after supercategory false positives (fps) are removed. Specifically, any matches to objects with a different class label but that belong to the same supercategory don't count as either a fp (or tp). Sim is computed by setting all objects in the same supercategory to have the same class label as the class in question and setting their ignore flag to 1. Note that person is a singleton supercategory so its Sim result is identical to Loc.
            Oth: PR after all class confusions are removed. Similar to Sim, except now if a detection matches any other object it is no longer a fp (or tp). Oth is computed by setting all other objects to have the same class label as the class in question and setting their ignore flag to 1.
            BG: PR after all background (and class confusion) fps are removed. For a single category, BG is a step function that is 1 until max recall is reached then drops to 0 (the curve is smoother after averaging across categories).
            FN: PR after all remaining errors are removed (trivially AP=1).


        Args:
            save_to_dir: The directory to save the plots to i.e 'figures', if None the figures are not saved
            show: Opens the plots in a matplotlib window if True
            iou_threshes: Tuple of IoU threshes to analyse (default is (0.75, 0.5 and 0.1) as per the COCO format
            iou_labels: Corresponding labels for the iou_threshes (default is ('C75', 'C50', 'LOC'))
            font_size: Display font size
            save_ext: matplotlib figure save extension (.pdf|.png|.jpg etc.)

        Returns:
            The rendered figure objects
        """
        if iou_labels is None:
            iou_labels = ['C75', 'C50', 'LOC']
        if iou_threshes is None:
            iou_threshes = [0.75, 0.5, 0.1]
        self.params.outDir = save_to_dir
        prm = copy.deepcopy(self.params)
        self.params.maxDets = [100]
        cat_ids = sorted(self.cocoGt.getCatIds())
        self.params.catIds = cat_ids
        self.params.iouThrs = np.array(iou_threshes)
        self.evaluate(cm=False)
        self.accumulate(cm=False)

        # PS storage = 0:C75, 1:C50, 2:C10/LOC, 3:SIM, 4:CLS, 5:BGR, 6:FIN
        ps = self.eval['precision']
        rc = self.eval['recall']
        ps = np.concatenate((ps, np.zeros([4] + list(ps.shape[1:]))))
        rc = np.concatenate((rc, np.zeros([4] + list(rc.shape[1:]))))

        self.params.iouThrs = np.array([0.1])
        self.params.useCats = 0

        gt = self.cocoGt
        self.analyze_figures = {}
        for k, catId in enumerate(cat_ids):
            nm = self.cocoGt.loadCats(catId)[0]
            nm = nm['name'] if 'supercategory' not in nm else nm['supercategory'] + '-' + nm['name']

            print('Analyzing %s (%d):' % (nm, k))
            start_time = time.time()

            # select detections for single category only
            self.params.keepDtCatIds = [catId]

            # compute precision but ignore superclass confusion
            cur_cat = gt.loadCats(catId)[0]
            if 'supercategory' in cur_cat:
                similar_cat_ids = gt.getCatIds(supNms=cur_cat['supercategory'])
                self.params.keepGtCatIds = similar_cat_ids
                self.params.targetCatId = catId

                # computeIoU need real catIds, we need to recover it
                self.params.catIds = cat_ids
                self.evaluate(cm=False)
                self.accumulate(cm=False)
                ps[3, :, k, :, :] = self.eval['precision'][0, :, 0, :, :]
                rc[3, k, :, :] = self.eval['recall'][0, 0, :, :]
            else:
                # skip  superclass confusion evaluation
                ps[3, :, k, :, :] = ps[2, :, k, :, :]
                rc[3, k, :, :] = rc[2, k, :, :]

            # compute precision but ignore any class confusion
            self.params.targetCatId = catId
            self.params.keepGtCatIds = cat_ids
            self.params.catIds = cat_ids
            self.evaluate(cm=False)
            self.accumulate(cm=False)
            ps[4, :, k, :, :] = self.eval['precision'][0, :, 0, :, :]
            rc[4, k, :, :] = self.eval['recall'][0, 0, :, :]

            # fill in background and false negative errors and plot
            ps[ps == -1] = 0
            ps[5, :, k, :] = (ps[4, :, k, :] > 0).astype(np.float32)
            ps[6, :, k, :] = 1
            rc[rc == -1] = 0
            rc[5, k, :] = (rc[4, k, :] > 0).astype(np.float32)
            rc[6, k, :] = 1
            end_time = time.time()

            figures = self.__makeplot(self.params.recThrs, ps[:, :, k, :, :], rc[:, k, :, :], nm,
                                      save_dir=self.params.outDir,
                                      show=show, iou_labels=iou_labels, font_size=font_size, save_ext=save_ext)
            self.analyze_figures.update(figures)
            print('Analyzing DONE (t=%0.2fs).' % (end_time - start_time))

        # reset Dt and Gt, params
        self.params = prm
        figures = self.__makeplot(self.params.recThrs, np.mean(ps, axis=2), np.mean(rc, axis=1), 'All Classes',
                                  save_dir=self.params.outDir,
                                  show=show, iou_labels=iou_labels, font_size=font_size, save_ext=save_ext)
        self.analyze_figures.update(figures)
        if 'supercategory' in list(self.cocoGt.cats.values())[0]:
            sup = [cat['supercategory'] for cat in self.cocoGt.loadCats(cat_ids)]
            print('all sup cats: %s' % (set(sup)))
            for k in set(sup):
                ps1 = np.mean(ps[:, :, np.array(sup) == k, :, :], axis=2)
                rc1 = np.mean(rc[:, np.array(sup) == k, :, :], axis=1)
                figures = self.__makeplot(self.params.recThrs, ps1, rc1, 'Overall - %s' % k,
                                          save_dir=self.params.outDir,
                                          show=show, iou_labels=iou_labels, font_size=font_size, save_ext=save_ext)
                self.analyze_figures.update(figures)
        return self.analyze_figures


class ConfusionMatrix(object):
    """Utility class for manipulating/visualising confusion matrices

        Metrics based on https://stackoverflow.com/a/48030708.
    """
    # TODO: Implement to binary confusion matrix function
    __metrics = {
        "statistics": {
            "accuracy": lambda tp, tn, fp, fn: (tp + tn) / (tp + tn + fp + fn) if (tp + tn) > 0 else 0.0,
            "f1score": lambda tp, tn, fp, fn: (2 * tp) / ((2 * tp) + (fp + fn)) if tp > 0 else 0.0,
            "sensitivity": lambda tp, tn, fp, fn: tp / (tp + fn) if tp > 0 else 0.0,
            "specificity": lambda tp, tn, fp, fn: tn / (tn + fp) if tn > 0 else 0.0,
            "precision": lambda tp, tn, fp, fn: tp / (tp + fp) if tp > 0 else 0.0,
            "recall": lambda tp, tn, fp, fn: tp / (tp + fn) if tp > 0 else 0.0,
            "tpr": lambda tp, tn, fp, fn: tp / (tp + fn) if tp > 0 else 0.0,
            "tnr": lambda tp, tn, fp, fn: tn / (tn + fp) if tn > 0 else 0.0,
            "fpr": lambda tp, tn, fp, fn: fp / (fp + tn) if fp > 0 else 0.0,
            "fnr": lambda tp, tn, fp, fn: fn / (fn + tp) if fn > 0 else 0.0,
            "ppv": lambda tp, tn, fp, fn: tp / (tp + fp) if tp > 0 else 0.0,
            "npv": lambda tp, tn, fp, fn: tn / (tn + fn) if tn > 0 else 0.0,
            "mcc": lambda tp, tn, fp, fn: ((tp * tn) - (fp * fn)) / math.sqrt(
                (tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)) if (tp * tn * fn * fp) > 0 else 0.0,
            "j-statistic": lambda tp, tn, fp, fn: (tp / (tp + fn)) + (tn / (tn + fp)) - 1 if (tp > 0 or (
                    tp + fn) > 0) or (tn > 0 or (tn + fp) > 0) else -1.0
        },
        "counts": {
            "tp": lambda tp, tn, fp, fn: tp,
            "tn": lambda tp, tn, fp, fn: tn,
            "fp": lambda tp, tn, fp, fn: fp,
            "fn": lambda tp, tn, fp, fn: fn,
            "pos": lambda tp, tn, fp, fn: tp + fn,
            "neg": lambda tp, tn, fp, fn: tn + fp,
            "prop": lambda tp, tn, fp, fn: (tp + fn) / (tp + tn + fp + fn)
        }
    }

    def __init__(self, confusion_matrix, classes=None, class_names=None):
        self.matrix = confusion_matrix
        if classes is None:
            classes = [i for i in range(confusion_matrix.shape[0])]
        if class_names is None:
            class_names = [str(i) for i in classes]
        self.classes = classes
        self.class_names = class_names
        self.class2index = {key: i for i, key in enumerate(self.classes)}
        self.index2class = {i: key for i, key in enumerate(self.classes)}
        self.metrics = self.__metrics

        self.matrix_sum = sum([sum(row) for row in self.matrix])
        self.normalised_matrix = [row for row in
                                  map(lambda i: list(map(lambda j: j / self.matrix_sum, i)), self.matrix)]
        self.results = None
        self.__compute_stats()

    @staticmethod
    def get_matrix(actual, predicted, labels=None):
        if labels is None:
            labels = actual
        classes = sorted(set(labels))
        matrix = np.zeros((len(classes), len(classes)))
        class2index = {key: i for i, key in enumerate(classes)}
        index2class = {i: key for i, key in enumerate(classes)}
        for pv, av in zip(predicted, actual):
            matrix[class2index[pv]][class2index[av]] += 1
        return matrix

    def __get_class_balance(self):
        return {
            self.index2class[i]: self.results[self.index2class[i]]["counts"]["pos"] for i, _ in enumerate(self.classes)
        }

    def __get_cohen_kappa(self, weight=None):
        """Based on scikit-learn metrics.cohen_kappa"""
        n_classes = self.matrix.shape[0]
        sum0 = np.sum(self.matrix, axis=0)
        sum1 = np.sum(self.matrix, axis=1)
        expected = np.outer(sum0, sum1) / np.sum(sum0)

        weights = None
        if weights is None:
            w_mat = np.ones([n_classes, n_classes], dtype=np.int)
            w_mat.flat[:: n_classes + 1] = 0
        elif weights == "linear" or weights == "quadratic":
            w_mat = np.zeros([n_classes, n_classes], dtype=np.int)
            w_mat += np.arange(n_classes)
            if weights == "linear":
                w_mat = np.abs(w_mat - w_mat.T)
            else:
                w_mat = (w_mat - w_mat.T) ** 2
        else:
            raise ValueError("Unknown kappa weighting type.")

        k = np.sum(w_mat * self.matrix) / np.sum(w_mat * expected)
        return 1 - k

    def __compute_stats(self):
        self.results = OrderedDict(((c, {
            "counts": OrderedDict(),
            "stats": OrderedDict()
        }) for c in self.classes))
        for i in range(len(self.classes)):
            row = sum(self.matrix[i][:])
            col = sum([row[i] for row in self.matrix])
            tp = self.matrix[i][i]
            fp = row - tp
            fn = col - tp
            tn = self.matrix_sum - row - col + tp
            for count, func in self.metrics["counts"].items():
                self.results[self.index2class[i]]["counts"][count] = self.metrics["counts"][count](tp, tn, fp, fn)
            for stat, func in self.metrics["statistics"].items():
                self.results[self.index2class[i]]["stats"][stat] = self.metrics["statistics"][stat](tp, tn, fp, fn)

    def summarise(self):
        first_column_width = max(7, max([len(s) for s in self.class_names]))
        count_metrics_len = len(self.metrics["counts"].keys())
        count_type_max_len = max([len(s) + 1 for s in self.metrics["counts"].keys()])
        counts_fmt = f" {{:<{first_column_width}}}  " + ' '.join([f"{{:<{count_type_max_len}}}"] * count_metrics_len)
        counts_title = counts_fmt.format(*(["Counts"] + list(self.metrics["counts"].keys())))
        stat_metrics_len = len(self.metrics["statistics"].keys())
        stat_type_max_len = max([len(s) + 1 for s in self.metrics["statistics"].keys()])
        stats_fmt = f" {{:<{first_column_width}}}  " + ' '.join([f"{{:<{stat_type_max_len}}}"] * stat_metrics_len)
        stats_title = stats_fmt.format(*(["Stats"] + list(self.metrics["statistics"].keys())))

        print(counts_title)
        for class_idx, class_name in enumerate(self.class_names):
            row_fmt = f" {{:<{first_column_width}}}  " + ' '.join([f"{{:<{count_type_max_len}}}"] * count_metrics_len)
            count_values = list(self.results[self.index2class[class_idx]]["counts"].values())
            row_str = row_fmt.format(*([class_name] + [
                ("{:d}" if r.is_integer() else "{:0.2f}%").format(
                    int(r) if r.is_integer() else r * 100) for r in count_values]))
            print(row_str)

        print()
        print(stats_title)
        for class_idx, class_name in enumerate(self.class_names):
            row_fmt = f" {{:<{first_column_width}}}  " + ' '.join([f"{{:<{stat_type_max_len}}}"] * stat_metrics_len)
            stat_values = list(self.results[self.index2class[class_idx]]["stats"].values())
            row_str = row_fmt.format(*([class_name] + [
                ("{:d}" if r.is_integer() else "{:0.2f}%").format(
                    int(r) if r.is_integer() else r * 100) for r in stat_values]))
            print(row_str)

        print((f"\n {{:<{first_column_width}}}  ").format("Cohen Kappa") + (f"{{:<{stat_type_max_len}}}\n").format(
            "{:0.2f}".format(self.__get_cohen_kappa())
        ))

    def tabulate(self, normalised=False):
        first_column_width = max(9, max([len(s) for s in self.class_names]) + 1)
        count_width = max([len(str(c)) for c, n in self.__get_class_balance().items()])
        column_widths = max(first_column_width, count_width)
        title_fmt = f" {{:<{first_column_width}}} " + ' '.join([f"{{:<{column_widths}}}"] * len(self.class_names))
        title = title_fmt.format(*(["Actual"] + [c + "ᴬ" for c in self.class_names]))
        print(title)
        print((f" {{:<{first_column_width}}} ").format("Predicted"))
        matrix = self.normalised_matrix if normalised else self.matrix

        for class_name, row in zip(self.class_names, matrix):
            row_fmt = f" {{:<{first_column_width}}} " + ' '.join([f"{{:<{column_widths}}}"] * len(self.class_names))
            row_str = row_fmt.format(*([class_name + "ᴾ"] + [
                ("{:d}" if r.is_integer() else "{:0.2f}%").format(
                    int(r) if r.is_integer() else r * 100) for r in row
            ]))
            print(row_str)

        print()
