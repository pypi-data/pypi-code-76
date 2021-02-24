
import json
import re
import random


def get_random_string(length=10):
    random_box = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    random_box_length = len(random_box)
    result = ""
    for _ in range(length):
        result += random_box[int(random.random()*random_box_length)]

    return result

def set_var(target, dictionary: dict):
    temp = ""
    if isinstance(target, dict):
        temp = json.dumps(target, ensure_ascii=False, default=str)
    elif isinstance(target, str):
        temp = target
    else:
        raise ValueError(f"invalid target type {type(target)}")

    for key in dictionary:
        value = dictionary[key]
        temp = temp.replace("{{"+key+"}}", value)

    if isinstance(target, dict):
        temp = json.loads(temp)

    return temp

def get_var(target):
    temp = ""
    if isinstance(target, dict):
        temp = json.dumps(target, ensure_ascii=False, default=str)
    elif isinstance(target, str):
        temp = target
    else:
        raise ValueError(f"invalid target type {type(target)}")

    return re.findall(r"{{.+?}}", temp)

def is_unchanged_var_exists(target):
    if isinstance(target, dict):
        temp = json.dumps(target, ensure_ascii=False, default=str)
    elif isinstance(target, str):
        temp = target
    else:
        raise ValueError(f"invalid target type {type(target)}")

    return len(re.findall(r"{{.+?}}", temp)) != 0

