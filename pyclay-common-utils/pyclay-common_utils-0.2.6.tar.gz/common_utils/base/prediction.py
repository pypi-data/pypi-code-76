from __future__ import annotations
from typing import TypeVar, List
from .basic import BasicLoadableObject, BasicLoadableHandler, BasicHandler

T = TypeVar('T')
H = TypeVar('H')

print(f'Warning: common_utils.base.prediction is still under testing.')

class PredictionDatum(BasicLoadableObject[T]):
    def __init__(self, frame: str=None, test_name: str=None, model_name: str=None):
        """Base class representing the data of a single prediction.
        This structure is used often for creating dump data by running inference using a trained
        model on test data.

        Args:
            frame (str, optional):
                The name of the frame. Usually an image filename.
                When working with images loaded from a video, the frame number can be used instead.
                When working with a live stream of images, such as a webcamera stream, a timestamp
                can be used here instead. This value is meant strictly for identification purposes.
                Defaults to None.
            test_name (str, optional):
                The name of the test data used to generate this prediction data.
                This can be the name of an image set the name of a video file, or some kind of description
                of what makes the test data unique.
                Defaults to None.
            model_name (str, optional):
                The name of the trained model that was used when inferring the test data to get this
                prediction data. This is usually a string that contains the name of the network,
                important hyperparameters used during training, and/or a timestamp indicating when the
                model was trained.
                Defaults to None.
        """
        super().__init__()
        self.frame = frame
        self.model_name = model_name
        self.test_name = test_name
    
class PredictionData(
    BasicLoadableHandler[H, T],
    BasicHandler[H, T]
):
    """TODO: Write docstring"""
    def __init__(self, obj_type: type, obj_list: List[T]=None):
        super().__init__(obj_type=obj_type, obj_list=obj_list)
    
    @property
    def frames(self) -> List[str]:
        frames = list(set([datum.frame for datum in self]))
        frames.sort()
        return frames

    @property
    def test_names(self) -> List[str]:
        test_names = list(set([datum.test_name for datum in self]))
        test_names.sort()
        return test_names

    @property
    def model_names(self) -> List[str]:
        model_names = list(set([datum.model_name for datum in self]))
        model_names.sort()
        return model_names

class GTDatum(BasicLoadableObject[T]):
    def __init__(self, test_name: str=None, frame: str=None):
        """Base class representing the data of a single GT.

        Args:
            frame (str, optional):
                The name of the frame. Usually an image filename.
                When working with images loaded from a video, the frame number can be used instead.
                When working with a live stream of images, such as a webcamera stream, a timestamp
                can be used here instead. This value is meant strictly for identification purposes.
                Defaults to None.
            test_name (str, optional):
                The name of the test data used to generate this prediction data.
                This can be the name of an image set the name of a video file, or some kind of description
                of what makes the test data unique.
                Defaults to None.
        """
        super().__init__()
        self.frame = frame
        self.test_name = test_name

class GTData(
    BasicLoadableHandler[H, T],
    BasicHandler[H, T]
):
    """TODO: Write docstring"""
    def __init__(self, obj_type: type, obj_list: List[T]=None):
        super().__init__(obj_type=obj_type, obj_list=obj_list)
    
    @property
    def frames(self) -> List[str]:
        frames = list(set([datum.frame for datum in self]))
        frames.sort()
        return frames

    @property
    def test_names(self) -> List[str]:
        test_names = list(set([datum.test_name for datum in self]))
        test_names.sort()
        return test_names

# class PairDatum(BasicLoadableObject[T]):
#     def __init__(self, dt: PredictionDatum, gt: GTDatum):
#         super().__init__()
#         assert dt.test_name == gt.test_name
#         assert dt.frame == gt.frame
#         if not isinstance(dt, PredictionDatum):
#             raise TypeError
#         if not isinstance(gt, GTDatum):
#             raise TypeError
#         self.dt = dt
#         self.gt = gt

class HybridDatum(BasicLoadableObject[T]):
    """TODO: Write docstring"""
    def __init__(self, frame: str=None, test_name: str=None, model_name: str=None):
        super().__init__()
        self.frame = frame
        self.test_name = test_name
        self.model_name = model_name

    @classmethod
    def from_gtdt(cls, gt: GTDatum, dt: PredictionDatum, **kwargs) -> T:
        raise NotImplementedError

class HybridData(
    BasicLoadableHandler[H, T],
    BasicHandler[H, T]
):
    """TODO: Write docstring"""
    def __init__(self, obj_type: type, obj_list: List[T]=None):
        super().__init__(obj_type=obj_type, obj_list=obj_list)
    
    @property
    def frames(self) -> List[str]:
        frames = list(set([datum.frame for datum in self]))
        frames.sort()
        return frames

    @property
    def test_names(self) -> List[str]:
        test_names = list(set([datum.test_name for datum in self]))
        test_names.sort()
        return test_names

    @property
    def model_names(self) -> List[str]:
        model_names = list(set([datum.model_name for datum in self]))
        model_names.sort()
        return model_names

    @classmethod
    def from_gtdt(cls, gt: GTData, dt: PredictionData, obj_type: type, **kwargs) -> H:
        assert hasattr(obj_type, 'from_gtdt')
        result = cls()
        assert isinstance(gt, GTData)
        assert isinstance(dt, PredictionData)
        model_names = dt.model_names
        for test_name in gt.test_names:
            gt_test, dt_test = gt.get(test_name=test_name), dt.get(test_name=test_name)
            for frame in gt_test.frames:
                gt_frame, dt_frame = gt_test.get(frame=frame), dt_test.get(frame=frame)
                assert len(gt_frame) == 1
                gt_datum = gt_frame[0]
                for model_name in model_names:
                    dt_model = dt_frame.get(model_name=model_name)
                    if len(dt_model) > 0:
                        assert len(dt_model) == 1, f'len(dt_model): {len(dt_model)}, test_name: {test_name}, frame: {frame}, model_name: {model_name}'
                        dt_datum = dt_model[0]
                        result_datum = obj_type.from_gtdt(gt=gt_datum, dt=dt_datum, **kwargs)
                        result.append(result_datum)
                    else:
                        result_datum = obj_type.from_gtdt(gt=gt_datum, dt=None, fallback_model_name=model_name, **kwargs)
                        result.append(result_datum)
        return result