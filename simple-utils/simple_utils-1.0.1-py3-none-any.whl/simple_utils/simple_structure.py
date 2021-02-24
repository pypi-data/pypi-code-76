import hashlib
import jsonschema
import re
import os

class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def make_dict_a_hash(*args):
    h = hashlib.sha256()

    for piece in args:
        h.update(str(piece).encode())

    return h.hexdigest()


def set_type(type_name, value):
    if type_name == "int":
        return int(value)
    elif type_name == "float":
        return float(value)
    elif type_name == "string":
        return str(value)
    elif type_name == "bool":
        if value == "true":
            return True
        elif value == "false":
            return False
        else:
            raise ValueError(f"invalid bool value. value is [{value}]")
    else:
        raise ValueError("invalid set type name %s" % (type_name))



def get_validated_obj(obj, schema_item):

    schema = schema_item.get("schema", {})
    properties = schema_item.get("properties", {})

    for name in properties:
        prop = properties[name]

        for key in prop:
            if key == "default":
                default = prop[key]
                if name not in obj:
                    obj[name] = default

        for key in prop:
            value = obj[name]
            if key == "change_type":
                type_name = prop[key]
                obj[name] = set_type(type_name, value)
    try:
        jsonschema.validate(obj, schema)
    except Exception as e:
        raise ValueError(f"validate failed. {e}")

    return obj

def is_match_obj(obj: object, matcher: object):

    for fk in matcher:
        fv = matcher[fk]

        if fk not in obj:
            raise ValueError(
                "matcher key is not in obj. obj -> %s, matcher -> %s" % (str(obj), str(matcher)))

        ov = obj[fk]
        if ov != fv:
            return False

    return True
    
def get_match_objs(objs: list, matcher: object):
    result = []
    for obj in objs:
        try:
            if is_match_obj(obj, matcher):
                result.append(obj)
        except ValueError:
            continue

    return result



def find_all_by_name(start_dir, regex):
    finded_files = []
    compiled_regex = re.compile(regex)

    for root, _, files in os.walk(start_dir):
        for filename in files:
            if compiled_regex.findall(filename):
                finded_files.append(os.path.join(
                    root, filename).replace("\\", "/"))

    return finded_files

def is_obj_looking_for(obj: dict, user_obj: dict):
    o = obj.copy()
    uo = user_obj.copy()

    o.update(uo)

    if o == obj:
        return True

    return False

def is_array_looking_for(array: list, user_array: list):
    a = array.copy()
    ua = user_array.copy()

    a += ua

    if set(a) == set(array):
        return True

    return False

