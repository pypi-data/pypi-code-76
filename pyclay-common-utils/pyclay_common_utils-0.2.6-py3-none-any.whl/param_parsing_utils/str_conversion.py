import re
from logger import logger
from ..check_utils import check_type
from ..utils import remove_edge_squarebrackets_from_str, \
    get_str_lists_from_noedge_str

def str2bool(text_str: str) -> bool:
    check_type(item=text_str, valid_type_list=[str])
    if text_str.lower() in ['true', 't', '1']:
        return True
    elif text_str.lower() in ['false', 'f', '0']:
        return False
    else:
        logger.error(f"String cannot be converted to bool: {text_str}")
        raise Exception

def str2int(text_str: str) -> int:
    check_type(item=text_str, valid_type_list=[str])
    return int(text_str)

def str2float(text_str: str) -> float:
    check_type(item=text_str, valid_type_list=[str])
    return float(text_str)

def str2strlistlist(list_str: str) -> list:
    no_edges = remove_edge_squarebrackets_from_str(list_str)
    result = no_edges.replace("'", "")
    result = result.replace(" ", "")
    
    result = re.split('\[|\]', result)
    result = [part for part in result if part not in ['', ',']]
    result = [part.split(',') for part in result]
    return result

def strlist2intlist(strlist: list) -> list:
    list_buffer = []
    for str_text in strlist:
        list_buffer.append(int(str_text))
    return list_buffer

def strlist2floatlist(strlist: list) -> list:
    list_buffer = []
    for str_text in strlist:
        list_buffer.append(float(str_text))
    return list_buffer

def strlist2boollist(strlist: list) -> list:
    list_buffer = []
    for str_text in strlist:
        list_buffer.append(str2bool(str_text))
    return list_buffer

def strlistlist2intlistlist(strlistlist: list) -> list:
    list_buffer = []
    for strlist in strlistlist:
        list_buffer.append(strlist2intlist(strlist))
    return list_buffer

def strlistlist2floatlistlist(strlistlist: list) -> list:
    list_buffer = []
    for strlist in strlistlist:
        list_buffer.append(strlist2floatlist(strlist))
    return list_buffer

def strlistlist2boollistlist(strlistlist: list) -> list:
    list_buffer = []
    for strlist in strlistlist:
        list_buffer.append(strlist2boollist(strlist))
    return list_buffer

def str2intlistlist(text: str) -> list:
    return strlistlist2intlistlist(str2strlistlist(text))

def str2floatlistlist(text: str) -> list:
    return strlistlist2floatlistlist(str2strlistlist(text))

def str2boollistlist(text: str) -> list:
    return strlistlist2boollistlist(str2strlistlist(text))

def str2strlist(list_str: str) -> list:
    temp = list_str.split('[')[1].split(']')[0].replace(' ', '').replace("'", "").split(',')
    return [i for i in temp]

def str2intlist(list_str: str) -> list:
    temp = list_str.split('[')[1].split(']')[0].replace(' ', '').split(',')
    return [int(i) for i in temp]

def str2floatlist(list_str: str) -> list:
    temp = list_str.split('[')[1].split(']')[0].replace(' ', '').split(',')
    return [float(i) for i in temp]