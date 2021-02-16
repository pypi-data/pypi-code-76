# /usr/bin/python3

from . import read_config as rc
import pandas as pd

# returns option dict if exists
def get_options(options, name):
    try:
        opt = options[name]
    except:
        opt = {}
    return opt

# Getting a dictionnary of proprties
def get_prop_dicts(pile, key="set", type=None, name=None):
    com = [key, type, name]
    return get_dict_from_pile(pile, com)

# Dict concaternation
def concatenate_dicts(*args):
    res={}
    for arg in args:
        res.update(arg)
    return res

# Getting a dict from the config represented as a pile
def get_dict_from_pile(pile,com):
    prop_dict={}
    if pile is not None:
        try:
            obj = rc.get_command(pile, com)
            prop_dict = {key: obj.value(key) for key in obj.values()}
        except:
            print("Warning : did not understand properties for %s" %com)
    return prop_dict

# Exports a dataframe to a csv file
def export_analysis(analysis,fname='analysis.csv'):
    if analysis is not None:
        return analysis.to_csv(fname)
    else:
        return None

# iterates over a dict of object to perform analysis
def make_analysis(dict,*args,**kwargs):
    res={}
    for key,item in dict.items():
        res[key]=objects_analysis(item,*args,**kwargs)
    return res


# Iterate over an object set to analyze its objects
# technically could work for iterators ;)
def objects_analysis(objects, analyzer=None, *args,**kwargs):
    datas = None
    keys = None

    try:
        analyzer = analyzer[objects.name]
    except:
        analyzer = None

    # Iteration
    for obj in objects:
        analysis=objects.analyze(obj, *args, analyzer = analyzer , **kwargs)
        if analysis:
            if datas is None:
                keys = analysis.keys()
                datas = pd.DataFrame(columns=keys)

            datas.loc[obj.id] = [analysis[key] for key in keys]

    return datas


# gets a block of lines between two "% frame" comments
def get_frame_block(iterator):
    return get_block(iterator, "% frame")


# gets a block of lines between two _key_ comments
def get_block(iterator,key):
    block = []
    if iterator is not None:
        for line in iterator:
            if line.find(key) < 0:
                block.append(line)
            else:
                break
    return block, len(block) > 0


# from a dictionary of filename dictionaries,
#   returns a dictionary of iterator dictionaries
def make_iter_dict(dict_dict):
    iter_dict = {}
    for name, report_dict in dict_dict.items():
        iters = {}
        for type, report_fname in report_dict.items():
            iters[type] = open(report_fname,'r')
        iter_dict[name] = iters

    return iter_dict


# from a dictionary of iterator dictionaries,
#   returns a dictionary of block dictionaries
def make_block_dict(dict_dict):
    block_dict = {}
    keep=False
    for name, report_dict in dict_dict.items():

        blocks = {}
        for type, report_iter in report_dict.items():
            blocks[type], flag = get_frame_block(report_iter)
            if flag:
                keep=True

        block_dict[name] = blocks

    return block_dict, keep
