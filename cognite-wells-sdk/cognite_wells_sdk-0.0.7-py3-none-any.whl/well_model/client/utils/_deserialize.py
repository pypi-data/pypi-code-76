import logging
from typing import Dict, List, Optional

from cognite.well_model.model.model_utils import deserialize_model

logger = logging.getLogger("deserializing")


def deserialize_object(dict, cls):
    """
    Deserialize a json into a class object

    @param dict: key-word arguments
    @param cls: class type we want to deserialize
    @return: cls object
    """
    obj: Optional[cls] = None

    try:
        obj = deserialize_model(
            model_data=dict,
            model_class=cls,
            path_to_item=[*dict],
            check_type=False,
            configuration=None,
            spec_property_naming=True,
        )
    except Exception as e:
        obj_id = dict.get("id")
        logger.info(f"object type{cls.__class__.__name__} with the id: {obj_id} could not parse due to: {e}")

    return obj


def deserialize_list(list_of_dict: List[Dict[str, str]], cls) -> List:
    """
    deserialize a json dictionary to a list of class objects

    @param list_of_dict: List of key-word arguments to deserialize
    @param cls: class type we want to deserialize
    @return: List of class objects
    """

    objects: List[cls] = []  # type: ignore
    try:
        for item in list_of_dict:
            obj: Optional[cls] = deserialize_object(item, cls)  # type: ignore
            if obj is not None:
                objects.append(obj)
    except Exception as e:
        logger.info(f"Could not parse {cls.__class__.__name__} items due to: {e}")

    return objects
