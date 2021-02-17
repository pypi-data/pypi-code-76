"""  Module with tools for h5cross
"""

import numpy as np

__all__ = ["add_numpy_statistics","check_environmental_modules","indentify_next_nested_level"]

# def delete_dict_entries(dict_, keys_to_remove_):
#     """
#         Remove iteratively the desired entries at level 0 if they exist
#         Input:
#             dict_ : dictionary to iterate through
#             keys_to_remove_ : list of type string with entries to be removed

#         Output: None, modifies the input dictionary
#         TO DO: could add option to remove keys at a given level
#             --> need to work on this, or iterative way but careful as might
#                 delete undesired entries perhaps?
#             --> more easily: create another function that calls this function
#                 with dict of certain level! --> YES BETTER, cfr get_desired_field_values
#     """
#     for key in dict_:
#         for ii in keys_to_remove_:
#             if ii in dict_[key]:
#                 del dict_[key][ii]

# def delete_dict_entries_at_level(dict_, keys_to_remove_, level_):
#     Should input either level in a number or a key which will set the level?


def check_environmental_modules(module_name_list):
    """ Function checking if desired modules can be imported

        Input:
            module_name_list: list of type string containing names of modules to check
        Output:
            module_present: list of type boolean listing if module can be imported
    """

    # TO DO : move to tools? -> would make more sense
    module_present=[]
    for item in module_name_list:
        try:
            __import__(item)
            #print("Module exists")
            module_present.append(True)
        except ImportError:
            #print("Module does not exists")
            module_present.append(False)
    return module_present


# def add_numpy_statistics_previous(dict_, flow_, stat_list_= None, skip_list_ = None):
#     """
#         Adds desired (based on numpy library) statistics to a dictionary tree structure

#         Input:
#             :dict_: dictionary to which statistics will be added
#             :flow_: flow field dictionary containing the data to calculate the statistics
#             :stat_list_: list of type string containing statistics to be computed.
#                         Must be keywords known by numpy.
#             :skip_list_: list of type string with dict_ keywords  for which statistics
#                         will not be computed.

#         Output:
#             None, modifies the dict_ entry
#     """
#     if stat_list_ is None:
#         stat_list_ = ["min", "max", "mean", "median", "std"]

#     for key in dict_:
#         if (skip_list_ is None) or (not key in skip_list_):
#             print(key)
#             for keys in dict_[key]:
#                 print("  ", keys)
#                 for item in stat_list_:
#                     try:
#                         dict_[key][keys][item] = str(eval("np."+item)(flow_[key][keys]))
#                     except ValueError:
#                         print("Statistics keyword \"", item, \
#                                 "\" not recognised by numpy for given key:", keys)
#                         #pass
#         else:
#             print("Skip key:", key)




def indentify_next_nested_level(dict_):
    """ Function indentifying if nested object is of type dictionary.
        Loops through the input dictionary keys.

        Input:
            dict_: the dictionary to study
        Output:
            local_dict_: a dictionary with keywords "False" or "True",
                        implying whether for a given key, the nested object
                        is a dictionary or not.
    """
    local_dict_ = {}
    for keys in dict_:
        local_dict_[keys] = False
        if isinstance(dict_[keys], dict):
            local_dict_[keys] = True
    return local_dict_


def compute_numpy_statistics(dict_, array_, stat_list_):
    """ Perform the computation of existing numpy statistics

        Input:
            dict_: dictionary to which statistics will be added
            array_: data array to be used to compute the stats
            stat_list_: list of type string containing statistics to be computed.
                        Must be keywords known by numpy.
        Output: adds stat keys to the input dictionary
    """
    accepted_types = ["float32","float64","int32","int64"]
    # if (dict_["dtype"] in accepted_types) and ("array" in dict_["value"]):
    if (dict_["dtype"] in accepted_types) and isinstance(dict_["value"],str):
        for item in stat_list_:
            try:
                dict_[item] = str(eval("np."+item)(array_))
            except NameError: # could be AttributError instead
                print("Statistics keyword \"", item, "\" not recognised by numpy")


def findkeys(node, kv):
    """
        Function allowing to find instances of a key in a nested dictionary.
        
        Code snippet taken from
        https://stackoverflow.com/questions/9807634/find-all-occurrences-of-a-key-in-nested-dictionaries-and-lists
        Credit to arainchi

        Input:
            node: dictionary to iterate through
            kv: keyword to find
        Output:
            generator with result of the search
    """
    if isinstance(node, list):
        for ii in node:
            for item in findkeys(ii, kv):
                yield item
    elif isinstance(node, dict):
        if kv in node:
            yield node[kv]
        for jj in node.values():
            # we skip current level and go to next level
            for item in findkeys(jj, kv):
                yield item


def get_desired_field_values(field_, fieldname_):
    """ Function will give the list of values back from the desired field name if it exists

        Input:
            field_:  dictionary of hdf5 object including the field data
            fieldname_: type string, key to find in the field_ dictionary
        Output:
            numpy array of desired field data if it exists
    """
    vals = list(findkeys(field_, fieldname_))
    # assume only one instance in vals -> perhaps need to add option of multiple
    if not vals:
        print("Field \"", fieldname_, "\" does not exist")
        return None
    if len(vals) > 1:
        print("Multiple instances of the desired variable \"", fieldname_, \
                            "\": selected first encounter")
    return vals[0]


def add_numpy_statistics(dict_, flow_, stat_list_= None, skip_list_ = None):
    """
        Adds desired (based on numpy library) statistics to a dictionary tree structure.
        Default stats are "min", "max", "mean", "median" and "std".

        Input:
            :dict_: dictionary to which statistics will be added
            :flow_: flow field dictionary containing the data to calculate the statistics
            :stat_list_: list of type string containing statistics to be computed.
                        Must be keywords known by numpy. (default = None)
            :skip_list_: list of type string with dict_ keywords  for which statistics
                        will not be computed. (default = None)

        Output:
            :None: modifies the dict_ entry
    """
    # define default statistics to compute if no user input
    if stat_list_ is None:
        stat_list_ = ["min", "max", "mean", "median", "std"]

    for key in dict_:
        if (skip_list_ is None) or (not key in skip_list_):
            dict_type_ = indentify_next_nested_level(dict_[key])
            tmp_key = list(dict_type_.keys())[0]
            if not dict_type_[tmp_key]:
                compute_numpy_statistics(dict_[key], flow_[key], stat_list_)
            else:
                add_numpy_statistics(dict_[key], flow_[key], stat_list_, skip_list_)



# def replace_string_in_dict(dict_, key_, string_original_, string_replace_, skip_list_ = None):
#     #TO DO: rethink this, should be level based, so perhaps 2functions cfr delete_dict_entries
#           -> perhaps function that calls given to argument at given level
#     # What if multilevel? could be annoying then eh ...
#     """
#        Replace encounters of a string inside a dictionary.
#     """
#     for key in dict_:
#         if (skip_list_ is None) or (not key in skip_list_):
#             print(key)
#             for keys in dict_[key]:
#                 if key_ in dict_[key][keys]:
#                     if isinstance(dict_[key][keys][key_], str) and \
#                         (string_original_ in dict_[key][keys][key_]):
#                         dict_[key][keys][key_] =  \
#                                  dict_[key][keys][key_].replace(string_original_,string_replace_)
#         else:
#             print("Skip key:", key)
