import json
import os
import shutil

import openpyxl
import xlsxwriter

import inforion.helper.api_fields_helper as afh

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
apiDirPath = os.path.join(dir_path,'api-files')
templateFileName = dir_path + "/Mapping_Template.xlsx"

class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

def copyTemplateFile(outputfilename):
    filename = outputfilename
    if not outputfilename.endswith(".xlsx"):
        filename = filename + ".xlsx"
    return shutil.copy(templateFileName, filename)


def checkIfTemplateFileExists():
    return os.path.isfile(templateFileName)


def getTypeCode(type_str):
    if type_str == "string":
        return "A"
    elif type_str == "number":
        return "N"
    elif type_str == "date":
        return "D"


def updateSheetWithFieldsData(filename, fields_list):
    xfile = openpyxl.load_workbook(filename)

    # sheet = xfile.get_sheet_by_name('Mapping Template')
    sheet = xfile["Mapping Template"]

    current_row = 11
    added_fields = []
    for field in fields_list:
        # Serial Number

        if(field[2].upper() in  added_fields):
            continue

        sheet["A" + str(current_row)] = current_row - 10
        sheet["B" + str(current_row)] = field[0]

        sheet["P" + str(current_row)] = field[2]
        sheet["Q" + str(current_row)] = field[0]
        sheet["R" + str(current_row)] = field[1]
        sheet["S" + str(current_row)] = getTypeCode(field[4])
        sheet["V" + str(current_row)] = field[6]
        sheet["W" + str(current_row)] = 1 if field[5] else 0
        sheet["X" + str(current_row)] = field[3]

        added_fields.append(field[2].upper())
        current_row = current_row + 1

    xfile.save(filename)


def generate_api_template_file(program, outputfile):
    
    if not program:
        return "\033[91m" + "Error: Program name is missing" + "\033[0m"

    if not outputfile:
        return "\033[91m" + "Error: Output filename is missing" + "\033[0m"

    api_name = program
    filename = outputfile
    if not outputfile.endswith(".xlsx"):
        filename = filename + ".xlsx"

    fields = afh.get_fields_list_from_db(program)
    if(len(fields)>0):
        copyTemplateFile(filename)
        updateSheetWithFieldsData(filename, fields)
        print(bcolors.OKGREEN + "File generated successfully" + bcolors.ENDC)
        return True
    else:
        print(
            bcolors.FAIL
            + "Error: No fields information found for program '{0}'. Please make sure you have specified correct program name.".format(program)
            + bcolors.ENDC
        )
    return False


def getAPIFileDir():
    return apiDirPath
