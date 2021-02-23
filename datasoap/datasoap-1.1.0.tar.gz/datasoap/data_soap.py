import pandas as pd
import numpy as np
import re


class Soap:
    """[Instances of this class are used to reformat the values in a pandas dataframe column in such a way as to be operable with standard mathematics and plotting. Removing non-digit characters from numeric strings.]
    """
    def __init__(self, data, dirty):
        """[Creates class instance that creates a copy of the original dataframe [Arg: data] and stores a re-formatted copy in the attribute [clean_copy]]

        Args:
            data ([pandas.core.frame.DataFrame]): [any valid pandas dataframe object]
            dirty ([list]): [list of column names that need to be reformatted.]
        
        Other Attributes:
            clean_copy ([pandas.core.frame.DataFrame]): [copy of the original dataframe with the values reformatted. value of self.clean_copy may be operated on with any valid pandas method]

        """
        self.data = data
        self.dirty = dirty
        self.clean_copy = self.soap(self.data, self.dirty)

    def __str__(self):
        return f'Instance of Soap class. attr `clean_copy` is a pandas dataframe object with values converted into operable datatypes.'

    def __repr__(self):
        return f'Instance of {type(self.clean_copy)} with values in columns: {self.dirty}, re-formated into operable datatype; \'float64\' or \'int64\''


    def soap(self, data, dirty:list):
        """[Method used by the Soap class to reformat values in a pandas.dataframe instance to allow correct conversion to correct datatype.]

        Args:
            data ([pandas.DataFrame]): [pandas dataframe instance]
            dirty (list): [list of column names as strings that need reformatting for conversion to operable data types]

        Raises:
            TypeError: [data argument must be a pandas.DataFrame Object]

        Returns:
            [pandas.DataFrame]: [returns copy of the origial dataframe with the specified values converted to the correct dtype]
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError(
                f'TypeError: expected pd.DataFrame object, pd.Series object, or list-like: got {type(data)}')
        
        clean_data = data.copy()
        for col in dirty:
            clean_data[f'{col}'].replace(clean_data[f'{col}'].values, [pd.to_numeric(self.pull_trailing_character(self.pull_leading_character(self.pull_comma(val))), errors='coerce') for val in clean_data[f'{col}']], inplace=True)
        
        return clean_data
     

    
    def show_diff(self):
        """[Calls pd.DataFrame.info method on both the original and the re-formatted dataframes for easy comparison of the data type transformation. for more info on pd.DataFrame.info see [pandas docs](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.info.html?highlight=info)]
        """
        print('Original DataFrame.info: \n')
        self.data.info()
        print('\n Re-Formatted DataFrame.info: \n') 
        self.clean_copy.info() 


    # define methods for pulling commas out of a String
    @staticmethod
    def pull_comma(line: str)-> str:
        """[static method used by Soap class instances to pull commas out of numeric strings]

        Args:
            line (str): [string to be re-formatted e.g. '2,000']

        Returns:
            str: [numeric string e.g. (see Args) --> '2000']
        """
        if ',' in line:
            line = line.split(',')
            line = ''.join(line)
            return line
        else:
            return line

    # define methods for pulling leading characters

    @staticmethod
    def pull_trailing_character(line:str)-> str:
        """[Static method used by Soap class instance to Identify trailing characters and convert values in thousands to values as fractions of a million. also pulls non-alphanumeric trailing characters]

        Args:
            line ([str]): [String to be re-formatted, e.g. '10k' or '1000+' etc]

        Returns:
            [str]: [numeric string converted to correct unit. e.g. (see Args)--> '.01' or '1000']
        """
        # print(line[0:len(line)-1])
        if line[-1].lower() == 'k':
            return (int(float(line[0:len(line)-1])*1000) / 1000000)
        elif line[-1].lower() == 'm':
            return (int(float(line[0:len(line)-1])*1000000) / 1000000)
        elif line[-1].isalpha() == False:
            return line if line[-1].isdigit() else (line[0:len(line)-1]) 
        else:
            return line

        
    # define methods for pulling trailing characters
    @staticmethod
    def pull_leading_character(line:str)-> str:
        """[Static method used by Soap class instance to remove leading non-numeric characters from numeric strings]

        Args:
            line ([str]): [numeric string with leading character, e.g. '$4.99. method assumes no whitespace between char and digits]

        Returns:
            [str]: [re-formatted numeric string with no leading character]
        """
        return line[0:] if line[0].isdigit() else line[1:len(line)]


    @staticmethod
    def convert_unit(line:str, unit_target:str)-> str:
        """[Static method used by Soap class instances to identify units of measure and convert to fractions of specified whole unit. e.g. '10k' to '.01'million]

        Args:
            line ([str]): [numeric string with a trailing unit of measure character]
            unit_target ([str]): [The preferred unit of measure for numeric strings to be converted to e.g. 'M' or 'k']

        Returns:
            [str]: [reformated numeric string as fraction of specified unit_target or numeric string with no trailing non-numeric characters]
        """
        units = {
            'T': 10**12,
            'G': 10**9,
            'M': 10**6,
            'k': 10**3,
            'h': 10**2,
            'da': 10**1,
            'base': 1,
            'd': 10**-1,
            'c': 10**-2,
            'm': 10**-3,
            'µ': 10**-6,
            'n': 10**-9,
            'p': 10**-12
        }

        # step 1: identify the suffix line -1
        for i in units.keys():
            print(f'i in convert_unit{i} \n units.keys{units.keys()}')
            if i in str(line):
                line = int(float(line[0: line.index(i)])) * \
                    units[i] / units[unit_target]
            else:
                pass
        return str(line)
        
