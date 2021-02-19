# beepbeep.ss: spreadsheet functions
from typing import Union, IO, Any
import csv
from xlrd import open_workbook


def convert_local_excel_file_sheet_to_dict(
                        local_excel_file_path: str, 
                        sheet_name: str, 
                        start_row: int=0, 
                        start_col: int=0, 
                        on_demand: bool=True) -> Union[list, None]:
    """
     Converting information from Local Excel files to a list of dict.


    Parameters:
        local_excel_file_path (str) : Local excel file path
        sheet_name (str) : The name of the sheet
        start_row (int) : Start row number. (Default= 0)
        start_col (int) : Start col number. (Default= 0)
        on_demand (bool) Set to True: Allows saving memory and time by loading only those sheets that the caller is interested in.

    Returns:
        If successful:
            Return a list of dict with the output generated.
        Otherwise:
            Return None
    """    

    try:
        workbook = open_workbook(local_excel_file_path) 
        sheet_names = workbook.sheet_names()

        sheet = workbook.sheet_by_name(sheet_name)
        sheet_headers = dict( (i, sheet.cell_value(start_col, i) ) for i in range(sheet.ncols) ) 
        output_generator = (dict( (sheet_headers[j], sheet.cell_value(i, j)) for j in sheet_headers ) for i in range(start_row + 1, sheet.nrows) )

        output_dict: Union[list, None]
        output_dict = [row for row in output_generator]

    except Exception as e:
        print(e)
        output_dict = None

    return output_dict


def write_list_of_dicts_to_csv(input_dict_list: dict, output_filename: str) -> Union[IO[Any], None]:
    """
     Converting list of dicts to a CSV file.


    Parameters:
        input_dict_list (dict) : List of Dicts will be converted into a CSV file.
        output_filename (str) : The output filename to write the content in a CSV Format.

    Returns:
        If successful:
            Return a csv file with the data of type bytes.
        Otherwise:
            Return None
    """    
    csv_columns = input_dict_list[0].keys()
    csvfile_data: Union[IO[Any], None] = None

    try:
        with open(output_filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile,delimiter=',', fieldnames=csv_columns)
            writer.writeheader()
            for data in input_dict_list:
                writer.writerow(data)
        csvfile_data = csvfile
    
    except Exception as e:
        print(e)
        csvfile_data = None
    
    return csvfile_data