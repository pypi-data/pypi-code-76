"""
        GNU AFFERO GENERAL PUBLIC LICENSE
           Version 3, 19 November 2007
 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 THIS IS A PART OF MONEY ON CHAIN
 @2020
 by Martin Mulone (martin.mulone@moneyonchain.com)
"""


def array_to_dictionary(data_array, names_array):

    result = {}

    for i in range(0, len(data_array)):
        result[names_array[i]] = data_array[i]

    return result
