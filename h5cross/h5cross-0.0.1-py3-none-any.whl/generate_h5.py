""" Functionalities to generate random nested dictionaries.
    Currently implemented for either 1 or 2 nested levels chosen at random.
"""
'''
    Works currently only for a max of two nested levels!!
    Would need to see what to do for more.
    It is highly probably due to the possible issue of
    base_keys vs variables at some point in the tree.
'''

import sys
import numpy as np

__all__ = ["generate_random_nested_dictionary"]

# variable list of tuples with format  ('name', min_val, max_val)
variables = [('temperature',300.0,1000.0),
                ('pressure',1e5,4e5),
                ('density', 0.08,1.98),
                ('scalar dissipation rate',0.0,2400.0),
                ('mixture fraction',0.0,1.0),
                ('O2 mass fraction',0.0,1.0),
                ('H2 mass fraction',0.0,1.0),
                ('H2O mass fraction',0.0,1.0),
                ('CO mass fraction',0.0,1.0),
                ('N2 mass fraction',0.0,1.0),
                ('CO2 mass fraction',0.0,1.0),
                ('O mass fraction',0.0,1.0),
                ('C mass fraction',0.0,1.0),
                ('total enthalpy',-3e6,3e6),
                ('velocity magnitude',20.0,790.0),
                ('Mach number',0.0,2.0),
                ('viscosity',8e-4,2e-5),
             ]

base_keys = {'Additionals', 'GaseousPhase', 'Special', 'Extras', 'New', 'Magic'}


def check_randomness(num_to_check, array_to_check):
    """ Function that checks if there is a minimal occurance of 1 for each value in given range.
        If it's not the case, one of the max occurences will be replaced by the minumum value.

        Input:
            :num_to_check: integer, the highest num in range to check: range = [0,num_to_check]
            :array_to_check: array of int with values to check
        Output
            :new_array: = array_to_check if each value in range at least one time in array_to_check
                        if above statement not correct, will replace one instance of max occurance
                        by missing one
    """
    new_array = array_to_check
    for item in np.arange(num_to_check):
        if item in new_array:
            continue
        count = np.argmax(np.bincount(new_array))
        index_replace = np.where(new_array == count)[0][0]
        new_array[index_replace] = item
        #print("Replaced value:", count, ' at index ',
        # index_replace, ' by missing value ', item)
    return new_array

def fill_dict_empty_nested(dict_, nested_key_ = None, keys_to_add_ = None):
    """ Function to add nested levels in a dictionary.
        Empty nested dictionaries are added for given keywords to be addded.

        Input:
            dict_: dictionary to which nested levels will be added
            nested_key_: (optional) type string, sets the dictionary level
                         to which to add keys (default = None)
            keys_to_add_ = keyword entries to add to dictionary.
        Output:
            None, modifies input dict_
    """
    if keys_to_add_ is None:
        print("Please specify dictionary entries to add")
        sys.exit()

    if nested_key_ is None:
        for item in keys_to_add_:
            if not dict_ == '':
                dict_[item] = {}
            else:
                dict_ = {item : ""}
    else:
        for item in keys_to_add_:
            if not dict_[nested_key_] == '':
                dict_[nested_key_][item] = {}
            else:
                dict_[nested_key_] = {item : ""}


def fill_dict_with_random_values(dict_, vars_info_, nvals = 20):
    """ Function that will generate the data to be added to the dictionary.

        Input:
            dict_: dictionary where to add the data arrays
            vars_info_: list containing in order
                        1) the dictionary key of where to add the value
                        2) min allowed value of data
                        3) max allowed value of data
        Output:
            None, adds a numpy array of data to the input dictionary
    """
    for item in vars_info_:
        key = item[0]
        var_min = float(item[1])
        var_max = float(item[2])
        #print(key, var_min, var_max)
        values = np.random.uniform(low = var_min, high = var_max, size = nvals)
        dict_[key] = values


def select_elements_from_list_from_value(check_list, select_list, target_value):
    """ Function that selects elements from a list based on a target value.
        Use of numpy where functionality.

        Input:
            check_list: list of values to browse through and evaluate our target value
            select_list: list to select from based on evaluation (could be same as check list)
            target_value: single value to find in check_list
        Output:
            select_elements: list of elements corresponding to target condition

    """
    tmp = np.where(check_list == target_value)[0]
    select_elements = [list(select_list)[index] for index in tmp]
    return select_elements

def select_next_nested_dict_level(dict_):
    """ Function accessing the next nested level of a dictionary.
        Reference to the original input dictionary is kept, i.e. no deepcopy returned.

        Input:
            dict_: nested dictionary from which to select next nested level
        Output:
            new_dict: dictionary starting at the next nested level of the input dict
    """
    new_dict = dict()
    for index, key in enumerate(list(dict_.keys())):
        if index == 0:
            #print(key)
            new_dict = dict_[key]
        else:
            new_dict[key] = dict_[key]
    return new_dict


def get_random_nested_dict(num_nested_levels_,
                            base_keys_, base_reshuffle_,
                            var_keys_, var_reshuffle_,
                            array_length_ = 20):
    """ Function generating a random nested dictionary with data points.

        Input:
            num_nested_levels_: int, sets the number of nested levels
                                (must be either 1 or 2 in current implementation)
            base_keys_: list of type string, contains the dictionary entries for
                        the different levels
            base_reshuffle_: list of type int, random assignment of base_keys_ to the
                            different levels
            var_keys_: list of type tuples, the variables for which to generate data
                        and add to the dictionary
            var_reshuffle_: list of type int, random assignment of var_keys_ to the
                            different levels
            array_length_: (optional), type int, controls the length of the generated
                            data for each entry of var_keys_
        Output:
            mydict: random nested dictionary

    """
    mydict = dict()
    tmp_dict = dict()
    for ii in np.arange(num_nested_levels_):
        # Select our base keys to add to the dict
        select_keys = select_elements_from_list_from_value(base_reshuffle_, base_keys_, ii)
        num_keys = len(select_keys)

        # Select the variables to add to the dict
        select_vars = select_elements_from_list_from_value(var_reshuffle_, var_keys_, ii)

        # Distribute our variables over the number of base keys through a random shuffle
        local_shuffle = np.random.randint(num_keys, size = len(select_vars))
        local_shuffle = check_randomness(num_keys, local_shuffle)

        if ii == 0:
            fill_dict_empty_nested(mydict, None, select_keys)
            for jj in range(len(select_keys)):
                vars_to_add = select_elements_from_list_from_value(local_shuffle, select_vars, jj)

                fill_dict_empty_nested(mydict, select_keys[jj], np.array(vars_to_add)[:,0])
                fill_dict_with_random_values(mydict[select_keys[jj]],
                                                np.array(vars_to_add),
                                                nvals = array_length_)
                tmp_dict = mydict
        else:
            # We need to distribute the next nested level (base keys) on the existing
            # last nested level base keys branches
            next_base_shuffle = np.random.randint(len(tmp_dict.keys()), size = len(select_keys))
            next_base_shuffle = check_randomness(len(tmp_dict.keys()), next_base_shuffle)
            for kk in range(len(tmp_dict.keys())):
                base_to_add = select_elements_from_list_from_value(next_base_shuffle,
                                                                     select_keys, kk)
                nested_level = list(tmp_dict.keys())[kk]
                fill_dict_empty_nested(tmp_dict[nested_level], None, base_to_add)

            for jj in range(len(select_keys)):
                vars_to_add = select_elements_from_list_from_value(local_shuffle, select_vars, jj)
                #print(vars_to_add)
                nested_level = list(tmp_dict.keys())[next_base_shuffle[jj]]

                fill_dict_empty_nested(tmp_dict[nested_level],
                                        select_keys[jj],
                                        np.array(vars_to_add)[:,0])
                fill_dict_with_random_values(tmp_dict[nested_level][select_keys[jj]],
                                                        np.array(vars_to_add),
                                                        nvals= array_length_)

            tmp_dict = select_next_nested_dict_level(tmp_dict)

    return mydict



def generate_random_nested_dictionary(array_length = 20):
    """ Function controlling the generation of a random nested dictionary.
        The randomness will generate a dictionary with either 1 or 2 nested levels.

        Input:
            array_length: (optional), sets the length of the data that is generated
        Output:
            mydict: nested dictionary
    """
    # TO DO: add exception if num_nested_levels = 0 -> then would need to just generate a
    # list of all values instead and do not consider the base keys then
    #       ->perhaps generare a list of vars instead in a seperate function

    num_nested_levels = np.random.randint(1,3,size=1)

    var_reshuffle = np.random.randint(num_nested_levels, size = len(variables))
    var_reshuffle = check_randomness(num_nested_levels, var_reshuffle)

    base_reshuffle = np.random.randint(num_nested_levels, size = len(base_keys))
    base_reshuffle = check_randomness(num_nested_levels, base_reshuffle)

    # TO DO: add Parameters with some random fill, at level 0 : like nnode and min vol and other
    # -->  lik a standard to add

    mydict = get_random_nested_dict(num_nested_levels, base_keys,
                                    base_reshuffle, variables,
                                    var_reshuffle, array_length_= array_length)

    return mydict
