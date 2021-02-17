# Copyright 2020 Tobias Höfer
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
"""Python-Wrapper COCO MAP-Evaluierung:
    https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools"""
import copy
from collections import OrderedDict

from pycocotools import coco, cocoeval, mask


def compute_coco_metrics(groundtruth_dict, detections_list):
    """

    Args:
        groundtruth_dict ([type]): [description]
        detection_list ([type]): [description]

    Returns:
        OrderedDict with coco metrics.
    """
    groundtruth = COCOWrapper(groundtruth_dict)
    detections = groundtruth.LoadAnnotations(detections_list)
    evaluator = COCOEvalWrapper(groundtruth, detections, agnostic_mode=False)
    return evaluator.ComputeMetrics()


def _isArrayLike(obj):
    return hasattr(obj, '__iter__') and hasattr(obj, '__len__')


class COCOWrapper(coco.COCO):
    """Wrapper for the pycocotools COCO class."""
    def __init__(self, dataset, detection_type='bbox'):
        """COCOWrapper constructor.
        See http://mscoco.org/dataset/#format for a description of the format.
        By default, the coco.COCO class constructor reads from a JSON file.
        This function duplicates the same behavior but loads from a dictionary,
        allowing us to perform evaluation without writing to external storage.
        Args:
        dataset: a dict holding bounding box annotations in the COCO format.
        detection_type: type of detections being wrapped. Can be one of ['bbox',
            'segmentation']
        Raises:
        ValueError: if detection_type is unsupported.
        """
        supported_detection_types = ['bbox', 'segmentation']
        if detection_type not in supported_detection_types:
            raise ValueError('Unsupported detection type: {}. '
                             'Supported values are: {}'.format(
                                 detection_type, supported_detection_types))
        self._detection_type = detection_type
        coco.COCO.__init__(self)
        self.dataset = dataset
        self.createIndex()

    def LoadAnnotations(self, annotations):
        """Load annotations dictionary into COCO datastructure.
        See http://mscoco.org/dataset/#format for a description of the
        annotations format.  As above, this function replicates the default
        behavior of the API but does not require writing to external storage.
        Args:
        annotations: python list holding object detection results where each
            detection is encoded as a dict with required keys ['image_id',
            'category_id', 'score'] and one of ['bbox', 'segmentation'] based on
            `detection_type`.
        Returns:
        a coco.COCO datastructure holding object detection annotations results
        Raises:
        ValueError: if annotations is not a list
        ValueError: if annotations do not correspond to the images contained
            in self.
        """
        results = coco.COCO()
        results.dataset['images'] = [img for img in self.dataset['images']]

        if not isinstance(annotations, list):
            raise ValueError('annotations is not a list of objects')
        annotation_img_ids = [ann['image_id'] for ann in annotations]
        if (set(annotation_img_ids) != (set(annotation_img_ids)
                                        & set(self.getImgIds()))):
            raise ValueError('Results do not correspond to current coco set')
        results.dataset['categories'] = copy.deepcopy(
            self.dataset['categories'])
        if self._detection_type == 'bbox':
            for idx, ann in enumerate(annotations):
                bb = ann['bbox']
                ann['area'] = bb[2] * bb[3]
                ann['id'] = idx + 1
                ann['iscrowd'] = 0
        elif self._detection_type == 'segmentation':
            for idx, ann in enumerate(annotations):
                ann['area'] = mask.area(ann['segmentation'])
                ann['bbox'] = mask.toBbox(ann['segmentation'])
                ann['id'] = idx + 1
                ann['iscrowd'] = 0

        results.dataset['annotations'] = annotations
        results.createIndex()
        return results


class COCOEvalWrapper(cocoeval.COCOeval):
    """Wrapper for the pycocotools COCOeval class.
        To evaluate, create two objects (groundtruth_dict and detections_list)
        using the conventions listed at http://mscoco.org/dataset/#format.
        Then call evaluation as follows:
            groundtruth = coco_tools.COCOWrapper(groundtruth_dict)
            detections = groundtruth.LoadAnnotations(detections_list)
            evaluator = coco_tools.COCOEvalWrapper(groundtruth, detections,
                                                agnostic_mode=False)
            metrics = evaluator.ComputeMetrics()
    """
    def __init__(self,
                 groundtruth=None,
                 detections=None,
                 agnostic_mode=False,
                 iou_type='bbox'):
        """COCOEvalWrapper constructor.
        Note that for the area-based metrics to be meaningful, detection and
        groundtruth boxes must be in image coordinates measured in pixels.
        Args:
            groundtruth: a coco.COCO (or coco_tools.COCOWrapper) object holding
            groundtruth annotations
            detections: a coco.COCO (or coco_tools.COCOWrapper) object holding
            detections
            agnostic_mode: boolean (default: False). If True, evaluation ignores
            class labels, treating all detections as proposals.
            iou_type: IOU type to use for evaluation. Supports `bbox` or `segm`.
        """
        cocoeval.COCOeval.__init__(self,
                                   groundtruth,
                                   detections,
                                   iouType=iou_type)
        if agnostic_mode:
            self.params.useCats = 0

    def GetCategory(self, category_id):
        """Fetches dictionary holding category information given category id.
        Args:
        category_id: integer id
        Returns:
        dictionary holding 'id', 'name'.
        """
        return self.cocoGt.cats[category_id]

    def GetAgnosticMode(self):
        """Returns true if COCO Eval is configured to evaluate in agnostic mode.
        """
        return self.params.useCats == 0

    def GetCategoryIdList(self):
        """Returns list of valid category ids."""
        return self.params.catIds

    def ComputeMetrics(self):
        """Computes detection metrics.
        Args:
        include_metrics_per_category: If True,will include metrics per category.
        all_metrics_per_category: If true, include all the summery metrics for
            each category in per_category_ap. Be careful with setting it to true
            if you have more than handful of categories, because it will pollute
            your mldash.
        Returns:
        1. summary_metrics: a dictionary holding:
            'Precision/mAP': mean average precision over classes averaged over
                IOU.
            thresholds ranging from .5 to .95 with .05 increments
            'Precision/mAP@.50IOU': mean average precision at 50% IOU
            'Precision/mAP@.75IOU': mean average precision at 75% IOU
            'Precision/mAP (small)': mean average precision for small objects
                            (area < 32^2 pixels)
            'Precision/mAP (medium)': mean average precision for medium sized
                            objects (32^2 pixels < area < 96^2 pixels)
            'Precision/mAP (large)': mean average precision for large objects
                            (96^2 pixels < area < 10000^2 pixels)
            'Recall/AR@1': average recall with 1 detection
            'Recall/AR@10': average recall with 10 detections
            'Recall/AR@100': average recall with 100 detections
            'Recall/AR@100 (small)': average recall for small objects with 100
            detections
            'Recall/AR@100 (medium)': average recall for medium objects with 100
            detections
            'Recall/AR@100 (large)': average recall for large objects with 100
            detections
        2. per_category_ap: a dictionary holding category specific results with
            keys of the form: 'Precision mAP ByCategory/category'
            (without the supercategory part if no supercategories exist).
            For backward compatibility 'PerformanceByCategory'is included in the
            output regardless of all_metrics_per_category.
            If evaluating class-agnostic mode, per_category_ap is an empty
            dictionary.
        Raises:
        ValueError: If category_stats does not exist.
        """
        self.evaluate()
        self.accumulate()
        self.summarize()

        summary_metrics = OrderedDict([
            ('Precision/mAP', self.stats[0]),
            ('Precision/mAP@.50IOU', self.stats[1]),
            ('Precision/mAP@.75IOU', self.stats[2]),
            ('Precision/mAP (small)', self.stats[3]),
            ('Precision/mAP (medium)', self.stats[4]),
            ('Precision/mAP (large)', self.stats[5]),
            ('Recall/AR@1', self.stats[6]), ('Recall/AR@10', self.stats[7]),
            ('Recall/AR@100', self.stats[8]),
            ('Recall/AR@100 (small)', self.stats[9]),
            ('Recall/AR@100 (medium)', self.stats[10]),
            ('Recall/AR@100 (large)', self.stats[11])
        ])

        return summary_metrics
