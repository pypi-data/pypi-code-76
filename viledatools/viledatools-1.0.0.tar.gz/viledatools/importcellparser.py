# coding=utf-8
"""
(C) FHCS GmbH

Class parsing value from MS Excel cell given, depending on Excel field key provided
"""

import inspect
import types
from datetime import datetime, timedelta
from typing import Any, List, Optional, Tuple, Union

import openpyxl
from openpyxl.cell.cell import Cell

from fatask import FATask
from viledaexceptions import ImportCellParserException
from viledautils import ViledaUtils


# noinspection PyPep8Naming
class ImportCellParser:
    """
    Class parsing value from MS Excel cell given, depending on Excel field key provided
    """
    def __init__(self, fieldkey: Optional[str] = None):
        """
        Gets the Excel field key and provides parse method for that value

        :param fieldkey: case insensitive string field key as specified in the Excel sheet
        """
        # Get class parsers list for field keys, method name have to start with "IQF" same as field key in Excel
        self._parsers_list = [n.upper() for n, v in inspect.getmembers(self, inspect.ismethod)
                              if (isinstance(v, types.MethodType) and n.upper()[:3] == "IQF")]
        if fieldkey is not None:
            if fieldkey not in self._parsers_list:
                raise ImportCellParserException(f"Unknown field key: {fieldkey}")
            self._method = getattr(self, fieldkey)

    def parse(self, cellobject: openpyxl.cell.cell.Cell) -> Any:
        """
        Parse value given cell object with chosen key field

        :param cellobject: openpyxl cell object to parse
        :return: value parsed from the cell
        """
        return self._method(cellobject)

    def getfieldtags(self):
        """
        Returns list of field key tags
        """
        return self._parsers_list

    def _parsenames(self, cellobject: openpyxl.cell.cell.Cell, sep: str) -> Union[List[str], None]:
        """
        Parse list of task owners from cell value, use given separator string

        :param cellobject: openpyxl cell object to parse
        :param sep: string to use as separator for str.split()
        :return: normalized task owners' names in a list() parsed from the cell
        """
        _value = cellobject.value
        # Trim and split by semicolons
        _value_raw_list = _value.strip().split(sep)
        # Normalize each item and filter out empty ones, fill filtered list
        _value_users_list = list()
        for _item in _value_raw_list:
            _trimmed_item = _item.strip()
            if _trimmed_item:
                _value_users_list.append(chr(0x0020).join(ViledaUtils.strnorm(_trimmed_item)))
        return _value_users_list if _value_users_list else None

    def IQF001SITE(self, cellobject: openpyxl.cell.cell.Cell) -> Union[str, None]:
        """
        Parse site name, normalize with ViledaUtils.strnorm()

        :param cellobject: openpyxl cell object to parse
        :return: normalized site name string parsed from the cell
        """
        if not isinstance(cellobject, Cell):
            raise TypeError(f"Provided cell object type {type(cellobject)}, type openpyxl.cell.cell.Cell required")
        if cellobject.value is None:
            return None
        return chr(0x0020).join(ViledaUtils.strnorm(cellobject.value))

    def IQF002FLOOR(self, cellobject: openpyxl.cell.cell.Cell) -> Union[str, None]:
        """
        Parse floor name, normalize with ViledaUtils.strnorm()

        :param cellobject: openpyxl cell object to parse
        :return: normalized floor name parsed from the cell
        """
        if not isinstance(cellobject, Cell):
            raise TypeError(f"Provided cell object type {type(cellobject)}, type openpyxl.cell.cell.Cell required")
        if cellobject.value is None:
            return None
        return chr(0x0020).join(ViledaUtils.strnorm(cellobject.value))

    def IQF003SPACE(self, cellobject: openpyxl.cell.cell.Cell) -> Union[str, None]:
        """
        Parse space name, normalize with ViledaUtils.strnorm()

        :param cellobject: openpyxl cell object to parse
        :return: normalized space name parsed from the cell
        """
        if not isinstance(cellobject, Cell):
            raise TypeError(f"Provided cell object type {type(cellobject)}, type openpyxl.cell.cell.Cell required")
        if cellobject.value is None:
            return None
        return chr(0x0020).join(ViledaUtils.strnorm(cellobject.value))

    def IQF004TASKOWNERS(self, cellobject: openpyxl.cell.cell.Cell) -> Union[List[str], None]:
        """
        Parse list of task owners from cell value, return list of normalized names with ViledaUtils.strnorm(). In the
        MS Excel sheet cell value user names must be separated with ; (semicolon) symbol, empty values between
        separators will be just ignored.

        :param cellobject: openpyxl cell object to parse
        :return: normalized task owners' names in a list() parsed from the cell
        """
        if not isinstance(cellobject, Cell):
            raise TypeError(f"Provided cell object type {type(cellobject)}, type openpyxl.cell.cell.Cell required")
        if cellobject.value is None:
            return None
        if not isinstance(cellobject.value, str):
            raise ImportCellParserException((f"IQF004TASKOWNERS: Cell contents type is {type(cellobject)}, "
                                             f"string type required"))
        return self._parsenames(cellobject, ";")

    def IQF005TASKTIME(self, cellobject: openpyxl.cell.cell.Cell) -> Union[Tuple[timedelta, timedelta], None]:
        """
        Parse task start time and task end time into tuple

        :param cellobject: openpyxl cell object to parse
        :return: tuple (start time, end time) parsed from the cell
        """
        if not isinstance(cellobject, Cell):
            raise TypeError(f"Provided cell object type {type(cellobject)}, type openpyxl.cell.cell.Cell required")
        if cellobject.value is None:
            return None
        _value = cellobject.value
        if not isinstance(_value, str):
            raise ImportCellParserException((f"IQF005TASKTIME: Cell contents type is {type(cellobject)}, "
                                             f"string type required"))
        _value_split = _value.strip().split("-")
        if len(_value_split) != 2:
            raise ImportCellParserException((f"IQF005TASKTIME: Wrong cell contents {_value.strip()}, "
                                             f"must be strictly in format H:M-H:M"))
        _output = []
        for _value_split_item in _value_split:
            _value_split_item_split = _value_split_item.strip().split(":")
            if len(_value_split_item_split) != 2:
                raise ImportCellParserException((f"IQF005TASKTIME: Wrong cell contents {_value.strip()}, "
                                                 f"must be strictly in format H:M-H:M"))
            _value_h = _value_split_item_split[0].strip()
            _value_m = _value_split_item_split[1].strip()
            if _value_h and _value_m:
                try:
                    _value_h_int = int(_value_h)
                    _value_m_int = int(_value_m)
                    if 0 <= _value_h_int <= 23 and 0 <= _value_m_int <= 59:
                        _output.append(timedelta(hours=_value_h_int, minutes=_value_m_int))
                    else:
                        raise Exception
                except Exception:
                    raise ImportCellParserException((f"IQF005TASKTIME: Wrong cell contents {_value.strip()}, "
                                                     f"must be strictly in format H:M-H:M"))
            else:
                raise ImportCellParserException((f"IQF005TASKTIME: Wrong cell contents {_value.strip()}, "
                                                 f"must be strictly in format H:M-H:M"))
        return _output[0], _output[1]

    def IQF006TASKTITLE(self, cellobject: openpyxl.cell.cell.Cell) -> Union[str, None]:
        """
        Parse task title, apply spaces trimming

        :param cellobject: openpyxl cell object to parse
        :return: trimmed task title parsed from the cell
        """
        if not isinstance(cellobject, Cell):
            raise TypeError(f"Provided cell object type {type(cellobject)}, type openpyxl.cell.cell.Cell required")
        if cellobject.value is None:
            return None
        return str(cellobject.value).strip()

    def IQF007TASKDESCR(self, cellobject: openpyxl.cell.cell.Cell) -> Union[str, None]:
        """
        Parse task description, apply spaces trimming

        :param cellobject: openpyxl cell object to parse
        :return: trimmed task description text parsed from the cell
        """
        if not isinstance(cellobject, Cell):
            raise TypeError(f"Provided cell object type {type(cellobject)}, type openpyxl.cell.cell.Cell required")
        if cellobject.value is None:
            return None
        return str(cellobject.value).strip()

    def IQF008STARTDATE(self, cellobject: openpyxl.cell.cell.Cell) -> Union[datetime, None]:
        """
        Parse starting date for task reccurence planning, and if the task is planned as standalone, this is the date
        when this task is to be planned

        :param cellobject: openpyxl cell object to parse
        :return: task start date parsed from the cell
        """
        if not isinstance(cellobject, Cell):
            raise TypeError(f"Provided cell object type {type(cellobject)}, type openpyxl.cell.cell.Cell required")
        if cellobject.value is None:
            return None
        _value = cellobject.value
        if isinstance(_value, datetime):
            # Cell in MS Excel sheet formatted in date / time Excel format,
            # extract year, month, day from it as it is
            return datetime(_value.year, _value.month, _value.day)
        elif isinstance(_value, (int, float)):
            # Cell in MS Excel sheet formatted in numeric format, convert to the datetime
            if _value < 2:
                raise ImportCellParserException((f"IQF008STARTDATE: Start date provided as numeric value: {_value}, "
                                                 f"but the value is out of range, numerical date value must be not "
                                                 f"less than 2"))
            return datetime(1900, 1, 1) + timedelta(days=(_value - 2))
        elif isinstance(_value, str):
            # Cell in MS Excel sheet formatted as string, in this case it have to be formatted as %Y-%m-%d,
            # otherwise wrong result will be returned
            return datetime.strptime(_value, "%Y-%m-%d")

    def IQF009FREQTYPE(self, cellobject: openpyxl.cell.cell.Cell) -> Union[str, None]:
        """
        Parse frequency type for task planning, apply spaces trimming and uppercase

        :param cellobject: openpyxl cell object to parse
        :return: trimmed & uppercased frequency type parsed from the cell
        """
        if not isinstance(cellobject, Cell):
            raise TypeError(f"Provided cell object type {type(cellobject)}, type openpyxl.cell.cell.Cell required")
        if cellobject.value is None:
            return None
        _value_stripped_upper = str(cellobject.value).strip().upper()
        if _value_stripped_upper not in FATask.supportedfreqs():
            raise ImportCellParserException((f"IQF009FREQTYPE: Frequency type not supported by "
                                             f"parser: {_value_stripped_upper}"))
        return _value_stripped_upper

    def IQF010FREQINTVL(self, cellobject: openpyxl.cell.cell.Cell) -> Union[int, None]:
        """
        Parse frequency interval as integer, defines frequency of task planned recurrence

        :param cellobject: openpyxl cell object to parse
        :return: integer recurrence interval parsed from the cell
        """
        if not isinstance(cellobject, Cell):
            raise TypeError(f"Provided cell object type {type(cellobject)}, type openpyxl.cell.cell.Cell required")
        if cellobject.value is None:
            return None
        _value = cellobject.value
        try:
            _value_int = int(_value)
        except Exception:
            raise ImportCellParserException(f"IQF010FREQINTVL: Wrong value in the cell: {_value}, must be integer")
        if _value_int < 1:
            raise ImportCellParserException((f"IQF010FREQINTVL: Value in the cell: {_value} out of range, "
                                             f"frequency interval must be greater than 0"))
        return _value_int

    def IQF011FREQDAYS(self, cellobject: openpyxl.cell.cell.Cell) -> Union[List[str], None]:
        """
        Parse task recurrence days as list of stringified integers, where ["1", "2", "3", "4", "5", "6", '7']
        corresponds to [Mon, Tue, Wed, Thu, Fri, Sat, Sun], list values in the MS Excel sheet must
        be given with ; (semicolon) separator

        :param cellobject: openpyxl cell object to parse
        :return: list of stringified integers parsed from the cell
        """
        if not isinstance(cellobject, Cell):
            raise TypeError(f"Provided cell object type {type(cellobject)}, type openpyxl.cell.cell.Cell required")
        if cellobject.value is None:
            return None
        _value = cellobject.value
        if not isinstance(_value, str):
            raise ImportCellParserException((f"IQF011FREQDAYS: Cell contents type is {type(cellobject)}, "
                                             f"string type required"))
        # Trim and split by semicolons
        _value_raw_list = _value.strip().split(";")
        # Trim each item and filter out empty ones, fill filtered list
        _value_numbers_set = set()
        for _item in _value_raw_list:
            _trimmed_item = _item.strip()
            if _trimmed_item:
                try:
                    _trimmed_item_int = int(_trimmed_item)
                except Exception:
                    raise ImportCellParserException((f"IQF011FREQDAYS: Wrong value in the cell: "
                                                     f"{_trimmed_item}, values in the list must be integers divided by "
                                                     f"semicolons"))
                if _trimmed_item_int in [1, 2, 3, 4, 5, 6, 7]:
                    _value_numbers_set.add(str(_trimmed_item_int))
                else:
                    raise ImportCellParserException((f"IQF011FREQDAYS: Wrong value in the cell: "
                                                     f"{_trimmed_item_int}, integer values in the list must be from "
                                                     f"1 to 7"))
        _value_numbers_list = list(_value_numbers_set)
        _value_numbers_list.sort()
        return _value_numbers_list
