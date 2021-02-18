import subprocess
import os
import re


def option_dict_to_list(options: dict, reverse: bool):
    options_list = []
    for i_key, i_value in options.items():
        if type(i_value) is str:
            if reverse:
                options_list.extend([str(i_value), "-" + str(i_key)])
            else:
                options_list.extend(["-" + str(i_key), str(i_value)])
        elif type(i_value) is list:
            options_list.append("-" + str(i_key))
            for i_i_value in i_value:
                options_list.append(i_i_value)
        elif type(i_value) is tuple:
            for i_i_value in i_value:
                # print(i_i_value.split(" "))
                temp = ["-" + str(i_key)]
                temp.extend(i_i_value.split(" "))
                options_list.extend(temp)
        elif i_value is None:
            options_list.append("-" + str(i_key))
    return options_list


def add_options_to_command(command, options, reverse=False):
    if options is not None:
        command.extend(option_dict_to_list(options, reverse))
        return command
    else:
        return command


def parse_mrtrix_output(mrtrix_output):
    stderr_message = mrtrix_output.stderr.decode("utf-8")
    print(stderr_message)

    warning_message = re.search("\[WARNING\](.*\n)", stderr_message)
    n_warning_messages = len(warning_message.groups()) if warning_message is not None else 0
    out_warning_messages = []
    if n_warning_messages > 0:
        for i_group_warning_message in range(n_warning_messages):
            out_warning_messages.append(warning_message.groups(i_group_warning_message)[0].strip())

    error_message = re.search("\[ERROR\](.*\n)", stderr_message)
    n_error_messages = len(error_message.groups()) if error_message is not None else 0
    out_error_messages = []
    if n_error_messages > 0:
        for i_group_error_message in range(n_error_messages):
            i_error_message = error_message.groups(i_group_error_message)[0].strip()
            # print("Error: " + i_error_message)


def mrconvert(in_file: str, out_file: str, options: dict = None):
    command = ["mrconvert"]
    command.append(in_file)
    add_options_to_command(command, options)
    command.append(out_file)
    print(command)
    output = subprocess.run(command, capture_output=True)

    parse_mrtrix_output(output)


def mrcat(in_files: list, out_file: str):

    command = ["mrcat"]
    command.extend(in_files)

    command.append(out_file)

    # print(command)
    output = subprocess.run(command, capture_output=True)

    parse_mrtrix_output(output)


def mrinfo(in_file: str, options: dict):
    command = ["mrinfo"]
    command.append(in_file)
    add_options_to_command(command, options)

    # command.append(out_file)

    output = subprocess.run(command, capture_output=True)

    parse_mrtrix_output(output)


def dwi2adc(in_file: str, out_file: str, options: dict):
    command = ["dwi2adc"]
    command.append(in_file)

    add_options_to_command(command, options)

    command.append(out_file)

    output = subprocess.run(command, capture_output=True)

    parse_mrtrix_output(output)


def mrcalc(in_file: str, out_file: str, options: dict):
    command = ["mrcalc"]
    command.append(in_file)

    add_options_to_command(command, options, reverse=True)

    command.append(out_file)

    output = subprocess.run(command, capture_output=True)

    parse_mrtrix_output(output)


def dwishellmath(in_file: str, out_file: str, operation: str):
    command = ["dwishellmath"]
    command.append(in_file)
    command.append(operation)
    command.append(out_file)

    output = subprocess.run(command, capture_output=True)

    parse_mrtrix_output(output)


def mrmath(in_file: str, out_file: str, operation: str, options: dict):
    command = ["mrmath"]
    command.append(in_file)
    command.append(operation)
    add_options_to_command(command, options)
    command.append(out_file)

    output = subprocess.run(command, capture_output=True)

    parse_mrtrix_output(output)


def dwi2tensor(in_file: str, out_file: str, options: dict):
    command = ["dwi2tensor"]
    command.append(in_file)

    add_options_to_command(command, options)

    command.append(out_file)

    output = subprocess.run(command, capture_output=True)

    parse_mrtrix_output(output)


def tensor2metric(in_file: str, options: dict):
    command = ["tensor2metric"]
    command.append(in_file)

    add_options_to_command(command, options)

    output = subprocess.run(command, capture_output=True)

    parse_mrtrix_output(output)


def dwiextract(in_file: str, out_file: str, options: dict):
    command = ["dwiextract"]
    command.append(in_file)

    add_options_to_command(command, options)
    command.append(out_file)

    output = subprocess.run(command, capture_output=True)

    parse_mrtrix_output(output)
