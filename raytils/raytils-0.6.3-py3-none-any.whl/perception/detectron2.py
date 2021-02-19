#  Raymond Kirk (Tunstill) Copyright (c) 2020
#  Email: ray.tunstill@gmail.com


class _unknown_class:
    def __init__(self):
        pass

    def __getitem__(self, item):
        return "class {}".format(item)


class ModelFromConfig:
    def __init__(self, config_file, model_file=None):
        from detectron2.config import get_cfg
        from detectron2.data import MetadataCatalog, DatasetCatalog
        from detectron2.engine.defaults import DefaultPredictor

        self.cfg = get_cfg()
        self.classes = _unknown_class()

        try:
            from fruit_detection.config import add_fruit_detection_config
            from fruit_detection.datasets import register_data_set
            add_fruit_detection_config(self.cfg)
            self.cfg.merge_from_file(config_file)
            register_data_set(self.cfg.DATASETS.TRAIN[0])
            dataset = DatasetCatalog.get(self.cfg.DATASETS.TRAIN[0])
            metadata = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0])
            self.classes = metadata.get("thing_classes", None)
            if not self.classes:
                self.classes = _unknown_class
        except ImportError:
            self.cfg.merge_from_file(config_file)

        if model_file is not None:
            self.cfg.MODEL.WEIGHTS = model_file
        self.cfg.freeze()

        self.predictor = DefaultPredictor(self.cfg)

    def __call__(self, image):
        return self.predictor(image)

    @property
    def model(self):
        return self.predictor.model
