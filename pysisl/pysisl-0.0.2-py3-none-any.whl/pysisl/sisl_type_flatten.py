# Copyright PA Knowledge Ltd 2021

class UnsupportedSislType(Exception):
    pass


class SISLTypeFlatten:
    @classmethod
    def flatten(cls, sisl_dict):
        return {key: cls._lookup_type_cast(type_value) for key, type_value in sisl_dict.items()}

    @classmethod
    def _flatten_to_list(cls, sisl_dict):
        return [cls._lookup_type_cast(value) for key, value in sisl_dict.items()]

    @classmethod
    def _lookup_type_cast(cls, type_value):
        return cls._type_cast_mappings().get(type_value["type"], lambda tvp: tvp)(type_value)

    @classmethod
    def _type_cast_mappings(cls):
        return {
            "str": lambda type_value: str(type_value["value"]).replace('\\"', '\"').replace('\\\\', '\\'),
            "obj": lambda type_value: cls.flatten(type_value["value"]),
            "bool": cls._convert_bool,
            "int": lambda type_value: int(type_value["value"]),
            "float": lambda type_value: float(type_value["value"]),
            "list": lambda type_value: cls._flatten_to_list(type_value["value"]),
            "null": lambda type_value: None
        }

    @staticmethod
    def _convert_bool(type_value):
        if type_value["value"] == "true":
            return True
        elif type_value["value"] == "false":
            return False
        else:
            raise UnsupportedSislType(type_value)
