import datetime
from abc import abstractmethod, ABC
from typing import List, Union, Optional


class CocoModes:
    """ Enum class to represent the different flavours of CocoFiles"""
    DETECTION = "detection"
    KEYPOINT = "keypoint"
    STUFF = "stuff"
    PANOPTIC = "panoptic"
    CAPTIONING = "captioning"
    modes = [DETECTION, KEYPOINT, STUFF, PANOPTIC, CAPTIONING]

    @staticmethod
    def is_valid(mode: str):
        """Returns true if mode is a valid Coco file format/flavour

        Args:
            mode: One of CocoModes.modes
        """
        return mode in CocoModes.modes


class __CocoField:
    """Abstract base class for a Coco field (a section of the json document)

    See http://cocodataset.org/#format-data
    """

    @property
    @abstractmethod
    def field_name(self):
        """Abstract base property for the name of the Coco field i.e info, licence etc."""
        pass

    def coco_json(self):
        """Returns the dict of class parameters"""
        return self.__dict__

    def __str__(self):
        """Pretty print when str() is called"""
        return self.coco_json().__str__()


class __CocoIterable:
    @abstractmethod
    def get_coco_fields(self):
        """Abstract method to get the coco field objects from the child class

        child.get_coco_fields() should return an array of __CocoField objects i.e CocoImage
        """
        pass

    def coco_json(self):
        """Returns the dictionary representation of all the Coco field classes in the iterable"""
        return [x.coco_json() for x in self.get_coco_fields()]


class __CocoSet(ABC, __CocoIterable, set):
    """Utility iterable for set"""
    pass


class __CocoDict(ABC, __CocoIterable, dict):
    """Utility iterable for dict"""
    pass


class __CocoList(ABC, __CocoIterable, list):
    """Utility iterable for list"""
    pass


class CocoInfo(__CocoField):
    """Represents the info section of the Coco format

    info{
        "year": int,
        "version": str,
        "description": str,
        "contributor": str,
        "url": str,
        "date_created": str,
    }
    """
    field_name = "info"

    def __init__(self, year: int = 0, version: str = "0.0.1", description: str = "", contributor: str = "",
            url: str = "", date_created: str = ""):
        if date_created == "":
            date_created = datetime.datetime.now().strftime("%d-%m-%Y")
        if year == 0:
            date_created = int(datetime.datetime.now().strftime("%Y"))

        self.year = year
        self.version = version
        self.description = description
        self.contributor = contributor
        self.url = url
        self.date_created = date_created


class CocoImage(__CocoField):
    """Represents the image section of the Coco format

    image{
        "id": int,
        "width": int,
        "height": int,
        "file_name": str,
        "license": int,
        "flickr_url": str,
        "coco_url": str,
        "date_captured": str,
    }
    """
    field_name = "image"

    def __init__(self, image_id: int, width: int, height: int, file_name: str, image_license: int, flickr_url: str,
            coco_url: str, date_captured: str, **kwargs):
        """
        Args:
            **kwargs: Extra information to store in the COCO document i.e depth info
        """
        self.id = image_id
        self.width = width
        self.height = height
        self.file_name = file_name
        self.license = image_license
        self.flickr_url = flickr_url
        self.coco_url = coco_url
        self.date_captured = date_captured
        for k, v in kwargs.items():
            setattr(self, k, v)


class CocoLicence(__CocoField):
    """Represents the licence section of the Coco format

    license{
        "id": int,
        "name": str,
        "url": str,
    }
    """
    field_name = "licence"

    def __init__(self, licence_id: int = 0, name: str = "", url: str = ""):
        self.id = licence_id
        self.name = name
        self.url = url


class CocoDetectionAnnotation(__CocoField):
    """Represents the annotation section of the Coco Object Detection format

    annotation{
        "id": int,
        "image_id": int,
        "category_id": int,
        "segmentation": [polygon] or RLE,
        "area": float,
        "bbox": [x,y,width,height],
        "iscrowd": 0 or 1,
    }
    """
    field_name = "annotation"

    def __init__(self, annotation_id: int, image_id: int, category_id: int, segmentation: Union[dict, list],
            area: float, bbox: List[float], iscrowd: int, **kwargs):
        self.id = annotation_id
        self.image_id = image_id
        self.category_id = category_id
        self.segmentation = segmentation
        self.area = area
        self.bbox = bbox
        self.iscrowd = iscrowd
        for k, v in kwargs.items():
            setattr(self, k, v)


class CocoCategory(__CocoField):
    """Represents the category section of the Coco Object Detection format

    category{
        "id": int,
        "name": str,
        "supercategory": str,
    }
    """
    field_name = "category"

    def __init__(self, category_id: int, name: str, supercategory: str):
        self.id = category_id
        self.name = name
        self.supercategory = supercategory


class CocoCategories(__CocoSet):
    """Utility class for generating a CocoList of categories for the Coco categories Object Detection format

    When exported it will automatically calculate category ids and super categories. Inherits from the set object.

    Attributes:
        classes: List of the classes/labels
    """
    field_name = "categories"

    def __init__(self, classes: Optional[List[str]] = None):
        if classes is None:
            classes = []
        super().__init__(classes)

    @property
    def classes_list(self):
        """Return a sorted list of class names (alphabetically a->z)"""
        return sorted(list(self))

    @property
    def classes_to_idx(self):
        """Returns a look up dict to go from class name to class id"""
        return {k: i + 1 for i, k in enumerate(self.classes_list)}

    @property
    def idx_to_classes(self):
        """Returns a look up dict to go from class id to class name"""
        return {i + 1: k for i, k in enumerate(self.classes_list)}

    @property
    def class_to_super_categories(self):
        """Returns the super categories look up dict to go from class name to super category

        Tokenises the class names and tries to find the best matching tokens from other classes, then assigns these as
        the super class
        """
        classes = self.classes_list
        classes_word_splits = {k: k.split(' ') for k in classes}
        super_categories = {k: "" for k in classes_word_splits.keys()}
        for class_name, class_tokens in classes_word_splits.items():
            super_categories_scores = {t: 0 for t in class_tokens}
            for token in class_tokens:
                token_scores = {t: 0 for t in class_tokens}

                for comparison_class in classes:
                    if comparison_class == class_name:
                        continue
                    if token in comparison_class:
                        token_scores[token] += 1

                max_score = max(token_scores.keys(), key=(lambda key: token_scores[key]))
                super_categories_scores[max_score] += token_scores[max_score]

            super_category = max(super_categories_scores.keys(), key=(lambda key: token_scores[key]))
            super_categories[class_name] = super_category

        return super_categories

    @property
    def categories(self):
        """Returns the classes as an array of CocoCategory objects"""
        idx_to_classes = self.idx_to_classes
        super_categories = self.class_to_super_categories
        return [CocoCategory(category_id=class_id, name=class_name, supercategory=super_categories[class_name])
                for class_id, class_name in idx_to_classes.items()]

    def get_coco_fields(self):
        """Returns the list of CocoCategory objects"""
        return self.categories


class CocoList(__CocoList):
    @property
    def field_name(self):
        """Tries to assume what category/field name based on existing entries"""
        if len(self) == 0:
            raise ValueError("Can't get name attribute of CocoList since it's empty")
        return self[0].field_name + "s"

    def get_coco_fields(self):
        """Returns the CocoFields"""
        return self


def combine_coco_objects(coco_objects: List[Union[__CocoField, __CocoIterable]]):
    """Combines the coco_objects array into a single dict for saving using json to coco.json files"""
    return {x.field_name: x.coco_json() for x in coco_objects}
