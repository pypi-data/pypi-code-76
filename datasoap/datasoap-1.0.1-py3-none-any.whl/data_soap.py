import pandas as pd
import numpy as np
import re
from datasoap.unit_data.conversion import units


class Soap:
    def __init__(self, data, dirty):
        self.data = data
        self.dirty = dirty
        self.clean_copy = self.soap(self.data, self.dirty)

    def __str__(self):
        return f'Instance of Soap class. attr `clean_copy` is a pandas dataframe object with values converted into operable datatypes.'

    def soap(self, data, dirty: list):
        """Pulls trailing and leading character
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError(
                f'TypeError: expected pd.DataFrame object, pd.Series object, or list-like: got {type(data)}')
        # create copy of the dataframe to be cleaned
        clean_data = data.copy()
        for col in dirty:
            clean_data[f'{col}'].replace(clean_data[f'{col}'].values, [pd.to_numeric(self.pull_trailing_character(
                self.pull_leading_character(self.pull_comma(val))), errors='coerce') for val in clean_data[f'{col}']], inplace=True)
        # run pd.DataFrame.replace for all indicated columns on the copy of the df input.
            # applies all formatter functions defined below to the
            # columns replacing the values with the return of those funcitons
            # Takes form: ` df['column to be formatted'].replace(df[column to be formatted].values, [pd.to_numeric(callback_1(callback_2(val))) for val in df['collumn to be formatted']], inplace=True)`
        # return a copy of input of the values properly converted
        return clean_data
        # pass

    @staticmethod
    def show_diff(self):
        """Shows both the original and cleaned dataframes.
        """

        # in order to accomplish this we may need to wrap all the logic in a class with a property for before and after
        # otherwise we may have some issues with being able to retrieve a specific comparison assuming a user needs to clean
        # more than one dataset.

        # show the `.info()` for the original and the cleaned copy
        # show the `.describe` for the original and the cleaned copy
        # accomplised by returning an iterable of print statements for each.
        # e.g. return [(print(f'{origin_info}'), print(f'{cleaned_info}')), (print(f'{origin_describe}'), print(f'{cleaned_describe}'))]
        # pass

    # define methods for pulling commas out of a String
    @staticmethod
    def pull_comma(line: str) -> str:
        """For use on integer||float values represented by strings containing "," characters.
        Does not alter the notation or denomination of the value. ie: "1,000" will not become
        "1k" 
        input <-- str
        output --> str
        """
        if ',' in line:
            line = line.split(',')
            line = ''.join(line)
            return line
        else:
            return line

    # define methods for pulling leading characters

    @staticmethod
    def pull_trailing_character(line):
        """For use on integer||float values represented by strings denoting denomination with the use
        of an alpha-char such as "23k" Does not perform conversion to parts of another denomination.
        ie: "23k" does not become ".023" if you wanted parts of milions. transformation is literal.
        thus "23k" becomes "23000" also works for strings denoting '%' if '%' denoted at end of string

        input<-- str
        output--> str
        """
        # print(line[0:len(line)-1])
        if line[-1].lower() == 'k':
            return (int(float(line[0:len(line)-1])*1000) / 1000000)
        elif line[-1].lower() == 'm':
            return (int(float(line[0:len(line)-1])*1000000) / 1000000)
        elif line[-1].isalpha == False:
            return (line[0:len(line)-1]) or 'NaN'
        else:
            return line

        # current solution assumes that leading chars will always be in the form: `$xx.xx` with no additional whitespaces or chars between
        # the char in question and the numeric string chars we actually want. mvp: keep assumption, note it in Docs. stretch: account for other possibilities
        # current solution takes form ` if type(str[0]) != int: return str[1:]`

    # define methods for pulling trailing characters

    @staticmethod
    def pull_leading_character(line):
        """For use on numeric strings that begin with a currency or denom char.

        """
        return line[0:] if line[0].isdigit() else line[1:len(line)]
        # current solution assumes trailing char only == 'm || M' or 'k || K' and converts 'k || K' to a decimal of 1Million.
        # mvp: keep assumption and note it in Docs. stretch: account for all unit conversion types.
        # current solution takes form ` if str[-1] == 'k': convert to str[:-1]//100^10 else return str[:-1]`

    # identify highest denomination and convert all figures to fraction of that denomination

    @staticmethod
    def convert_unit(line, unit_target):
        # step 1: identify the suffix line -1
        for i in units.keys():
            print(f'i in convert_unit{i} \n units.keys{units.keys()}')
            if i in str(line):
                line = int(float(line[0: line.index(i)])) * \
                    units[i] / units[unit_target]
            else:
                pass
        return str(line)
        # no current logic written for this, previously was handled as part of  pull_trailing logic.
