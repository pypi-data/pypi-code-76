""" Command line module of h5cross"""

import click
import h5cross

# not to bu used aside of the CLI
__all__ = []

@click.group()
def main_cli():
    """---------------    H5CROSS  --------------------

You are now using the Command line interface of h5cross
a Python3 helper to explore and compare hdf5 files, created at CERFACS (https://cerfacs.fr).


This is a python package currently installed in your python environement.
"""


@click.command()
@click.argument("filename", nargs=1)
def tree(filename):
    """Print the content of an hdf5 file in terminal.

    """
    h5cross.print_h5_structure(filename)

main_cli.add_command(tree)


# NOTE: QUICK COMMANDS: e.g. @click.option('--out-name', '-n', 
# -n will be shortcut for --out-name
# -i  for out-indent 


@click.command()
@click.argument("filename", nargs=1)
@click.option('--out-name', required=False, default=None, type=str,
    help='default = None , if specified used as YAML output name. \
                            If not specified output name = filename.yml')
@click.option('--out-indent', required=False, default=2, type=int,
    help ='default = 2, sets the indentation level in ouput YAML file')
def dump(filename, out_name, out_indent):
    """Write the content of an hdf5 file into a YAML file.

    """
    mydict = h5cross.get_h5_structure(filename)

    if out_name is not None:
        writename = out_name
    else:
        writename = filename.split('.')[0]

    configure_yaml_output(mydict,writename, out_indent)

main_cli.add_command(dump)


@click.command()
@click.argument("filename", nargs=1)
def view(filename):
    """Show the content of an hdf5 file interactively with nobvisual.

    """
    h5cross.visual_h5(filename)

main_cli.add_command(view)


@click.command()
@click.argument("filename", nargs=1)
@click.option('--print-to-console', required=False, default=True, type=bool,
    help='default = True')
@click.option('--pretty-table', required=False, default=True, type=bool,
    help='default = True, controls if pretty table output is selected')
@click.option('--pretty-full-path', required=False, default=True, type=bool,
    help='default = True, controls if full paths in nested dictionary are output in pretty table')          
@click.option('--save-as-yaml', required=False, default=False, type=bool,
    help='default = False , if True: default output name is set to input file name')
@click.option('--out-name-yaml', required=False, default=None, type=str,
    help= 'default = None, if specified used as output name of YAML file')
@click.option('--out-indent', required=False, default=2, type=int,
    help ='default = 2, sets the indentation level in ouput YAML file')
# @click.option('--save-as-h5', required=False, default=False, type=bool,
#                     help='To be implemented')
# @click.option('--out-name-h5', required=False, default=None, type=str,
#                     help='To be implemented')
def stats(filename, print_to_console, pretty_table, pretty_full_path, save_as_yaml, out_name_yaml, out_indent):
#            save_as_h5, out_name_h5):
    """Compute statistics of arrays from hdf5 file.

    """
    mydict = h5cross.get_h5_structure(filename)
    myfield_dict = h5cross.get_h5_field(filename)

    h5cross.add_numpy_statistics(mydict, myfield_dict)
    if print_to_console:
        if pretty_table:
            h5cross.pretty_table_h5_stats(mydict, full_path = pretty_full_path)
        else:
            h5cross.print_h5_structure(mydict)

    if save_as_yaml:
        if out_name_yaml is not None:
            writename = out_name_yaml
        else:
            writename = filename.split('.')[0]

        configure_yaml_output(mydict, writename, out_indent)

    
    # TO DO: rethink the save_as-> should be in the flow file, so not logic in struct
    #if save_as_h5:
    #    print("Currently not implemented")
    #     if out_name_h5 is not None:
    #         writename = out_name_h5
    #     else:
    #         writename = filename.split('.')[0] + "_stats"

    #     h5cross.write_h5(mydict,save_name = writename)

main_cli.add_command(stats)


@click.command()
@click.argument("file_left", nargs=1)
@click.argument("file_right", nargs=1)
@click.option('--add-stats', required=False, default=False, type=bool,
     help='default = False, if True will compute statistics for each file before comparing')
def diff(file_left, file_right, add_stats):
    """Compare the content of two hdf5 files and view interactively with nobvisual.

    """
    h5cross.compare_h5(file_left, file_right, add_stats)

main_cli.add_command(diff)

@click.command()
@click.argument("file_left", nargs=1)
@click.argument("file_right", nargs=1)
@click.option('--select-vars', required=True, default=None, type=str,
    help='default = None, select variables to plot. Requires a comma separated string with \
            variables to select, e.g. \"temperature,pressure\" ')
@click.option('--save-output', required=False, default=False, type=bool,
    help='default = False, if True will save the outputs of the plot(s)')
@click.option('--save-name', required=False, default=None, type=str,
    help='default = None, string specifying desired output base name for each plot')
@click.option('--show-output', required=False, default=True, type=bool,
    help='default = True, controls whether plot(s) are shown or not')
@click.option('--use-seaborn', required=False, default=True, type=bool,
    help='default = True, controls the use of seaborn. If False, matplotlib.pyplot is used.')

def scatter(file_left, file_right, select_vars, save_output, save_name, show_output, use_seaborn):
    """ Scatter plot comparison of two hdf5 files.
        Seaborn is used to generate the plots but can
        be deactivated in which case matplotlib.pyplot is used.

        Note: The matplotlib package is a minimal requirement for this functionality.

    """
    #print(select_vars)
    var_list = select_vars.split(",")
    #select_vars #["temperature","pressure"]
    h5cross.compare_scatter_h5(file_left, file_right, var_list,
                flag_save=save_output, save_name=save_name,
                flag_show=show_output, flag_seaborn= use_seaborn)

main_cli.add_command(scatter)


@click.command()
@click.option('--array-length', required=False, default=None, type=int,
    help='default = None, controls the length of the data arrays')
@click.option('--out-name-h5', required=False, default=None, type=str,
    help='Optional output name for hdf5 file, default = dump.h5')
@click.option('--out-location-h5', required=False, default=None, type=str,
    help='Optional path where to save the hdf5 file, default = current dir')

def generate(array_length, out_name_h5, out_location_h5):
    """ Generates an hdf5 file from a random nested dictionary (also generated).
        It allows an easy input to test the other functionalities.
    """
    if array_length:
        tmp_dict = h5cross.generate_random_nested_dictionary(array_length=array_length)
    else:
        tmp_dict = h5cross.generate_random_nested_dictionary()

    if out_name_h5 is not None:
        if out_location_h5 is not None:
            h5cross.write_h5(tmp_dict, save_name_ = out_name_h5, save_path_= out_location_h5)
        else:
            h5cross.write_h5(tmp_dict, save_name_ = out_name_h5)
    else:
        if out_location_h5 is not None:
            h5cross.write_h5(tmp_dict, save_path_= out_location_h5)
        else:
            h5cross.write_h5(tmp_dict)


main_cli.add_command(generate)


#----------------------extra functionalities------------------------#
def configure_yaml_output(dict_, out_name_, indent_):
    """ Function to set output options and write the yaml output

        Input:
            :dict_: dictionary to write out as a yaml file
            :out_name_: dtype = string, name of output yaml file
            :indent_: dtype = int, indentation level for output
        Output:
            writes a yaml file in current directory
    """
    if indent_ is None:
        indent_ = 2
    h5cross.write_dict_to_yaml(dict_, out_name_, setindent=indent_)
