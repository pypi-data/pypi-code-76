""" Module with functionalities related to the visual aspects of h5cross
"""
import subprocess
import sys

from .visit_h5 import get_h5_structure, get_h5_field
from .write_h5 import write_dict_to_yaml
from .tools import add_numpy_statistics, get_desired_field_values, check_environmental_modules

__all__ = ["visual_compare_yaml","compare_h5","visual_h5","compare_scatter_h5"]


def compare_h5(file1, file2, add_stats = False):
    """ Function allowing the comparison of two hdf5 files

        Input:
            :file1: (string), name of first file for comparison
            :file2: (string), name of second file for comparison
            :add_stats: (boolean), option to compute statistics on both input files
        Output:
            :None: interactive comparative view
    """
    module_present = check_environmental_modules(["nobvisual"])
    if module_present[0]:
        dict1 = get_h5_structure(file1)
        dict2 = get_h5_structure(file2)

        # TO DO: write separate functionalities for this??
        if add_stats:
            flow1 = get_h5_field(file1)
            add_numpy_statistics(dict1, flow1)
            del flow1
            flow2 = get_h5_field(file2)
            add_numpy_statistics(dict2, flow2)
            del flow2

        write_dict_to_yaml(dict1, "tmp1", setindent = 2)
        write_dict_to_yaml(dict2, "tmp2", setindent = 2)

        visual_compare_yaml("tmp1.yml","tmp2.yml")

        subprocess.call('rm '+ "tmp1.yml" + ' ' + "tmp2.yml", shell=True)
    else:
        print("Process stopped: nobvisual package not available")
        sys.exit()


def visual_compare_yaml(yaml1,yaml2):
    """ Function calling nobvisual for visual comparison of yaml files

        Input:
            :yaml1: name of first yaml file
            :yaml2: name of second yaml file
        Output:
            :None: interactive view
    """
    module_present = check_environmental_modules(["nobvisual"])
    if module_present[0]:
        subprocess.call('nobvisual cmpfile ' + yaml1 + ' ' + yaml2, shell=True)
    else:
        print("Process stopped: nobvisual package not available")
        sys.exit()

def visual_h5(filename):
    """ Function calling nobvisual for visual view of hdf5 file

        Input:
            :filename: name of hdf5 file
        Output: 
            :None: interactive view
    """
    module_present = check_environmental_modules(["nobvisual"])
    if module_present[0]:
        dict_ = get_h5_structure(filename)
        write_dict_to_yaml(dict_, "tmp", setindent = 2)
        subprocess.call('nobvisual treefile tmp.yml', shell=True)
        subprocess.call('rm '+ "tmp.yml" , shell=True)
    else:
        print("Process stopped: nobvisual package not available")
        sys.exit()


def compare_scatter_h5(file1, file2, variable_list,
                         flag_save = False, save_name = None, flag_show = True, flag_seaborn = True):
    """ Function that controls the generation of scatterplots comparing the same
        variable from two hdf5 files

        Input:
            :file1: (string), name of first file for comparison
            :file2: (string), name of second file for comparison
            :variable_list: list of type string containg keywords of the
                            variables to select for comparison. The same variable
                            will be selected from each file.
            Optional Arguments:
                :flag_save: boolean controlling if the plots get saved (default = False)
                :save_name: (string), base name to be used in saving the plots (default = None)
                :flag_show: boolean setting if the plot gets showed or not (default = True)
                :flag_seaborn: boolean controlling whether seaborn is used or not (default = True)
        Output:
            :None: interactive view. If flag_save = True, a png image of the scatter plots gets saved.
    """
    modules_list = ["matplotlib","seaborn"]
    modules_present = check_environmental_modules(modules_list)
    if modules_present[0] is not False: # matplotlib is a minimum requirement
        flow1 = get_h5_field(file1)
        flow2 = get_h5_field(file2)
        for item in variable_list:
            array1 = get_desired_field_values(flow1, item)
            array2 = get_desired_field_values(flow2,item)
            if (array1 is not None) and (array2 is not None):
                if len(array1) == len(array2):
                    if (modules_present[1] is not False) and (flag_seaborn is True):
                        seaborn_simple_scatter(array1, array2, [item,item],
                                flag_save_ = flag_save, flag_show_ = flag_show, save_name_ = save_name)
                    else:
                        matplotlib_simple_scatter(array1, array2, [item,item],
                                flag_save_ = flag_save, flag_show_ = flag_show, save_name_ = save_name)
                else:
                    print("Warning: data arrays have different length, plotting distribution instead")
                    #if modules_present[1] is not False:
                    #    seaborn_simple_distribution(array1, array2, [item,item],
                    #            flag_save_ = flag_save, flag_show_ = flag_show, save_name_ = save_name)
                    #else:
                    matplotlib_simple_distribution(array1, array2, [item,item],
                                flag_save_ = flag_save, flag_show_ = flag_show, save_name_ = save_name)
    else:
        print("Process stopped: matplotlib module not available")
        sys.exit()

# def check_environmental_modules(module_name_list):
#     """ Function checking if desired modules can be imported

#         Input:
#             module_name_list: list of type string containing names of modules to check
#         Output:
#             module_present: list of type boolean listing if module can be imported
#     """

#     # TO DO : move to tools? -> would make more sense AND move adapt pytests then
#     module_present=[]
#     for item in module_name_list:
#         try:
#             __import__(item)
#             #print("Module exists")
#             module_present.append(True)
#         except ImportError:
#             #print("Module does not exists")
#             module_present.append(False)
#     return module_present

def seaborn_simple_scatter(array1, array2, axes_labels,
                            flag_save_ = False, save_name_ = None, flag_show_ = True):
    """ Function to generate a scatter plot of two data arrays of same length with seaborn

        Input:
            array1: numpy array of first data set
            array2: numpy array of second data set
            axes_labels: list of string of length 2, used to specify the labels of output axis
            Optional Arguments:
                flag_save_: boolean controlling if the plots get saved (default = False)
                save_name_: (string), base name to be used in saving the plots (default = None)
                flag_show_: boolean setting if the plot gets showed or not (default = True)

        Output:
            Default = None, interactive view
            If flag_save = True then outputs a png image
    """
    import seaborn as sns
    import matplotlib.pyplot as plt

    sns.set_theme()

    if check_environmental_modules(["scipy"])[0] is not False:    
        # Get the density map
        zarr = _density_scatter(array1, array2, only_cmap = True)

        # Sort the data for better color map rendering (see link)
        idx = zarr.argsort()
        array1, array2, zarr = array1[idx], array2[idx], zarr[idx]

    data_plot = {"field1": array1, "field2": array2}
    plot = sns.jointplot(data = data_plot, x = "field1", y = "field2", kind = "scatter",
                            marginal_ticks= True,
                            marginal_kws=dict(stat="density") )

    if check_environmental_modules(["scipy"])[0] is not False:                          
        plot.plot_joint(plt.scatter, c=zarr, cmap='viridis')
    plot.set_axis_labels(axes_labels[0] + ' ' + "field 1" ,axes_labels[1] +' ' + "field 2")

    plt.tight_layout()
    if flag_save_:
        if not save_name_:
            base_name = "scatter_"
        else:
            base_name = save_name_
        save_name = base_name + axes_labels[0] + '_' + axes_labels[1]
        plt.savefig(save_name +'.png')
    if flag_show_:
        plt.show()


def seaborn_simple_distribution(array1, array2, axes_labels,
                            flag_save_ = False, save_name_ = None, flag_show_ = True):
    """ Function to generate histograms of two data arrays of different length with seaborn
        NOT YET FUNCTIONAL

        Input:
            array1: numpy array of first data set
            array2: numpy array of second data set
            axes_labels: list of string of length 2, used to specify the labels of output axis
            Optional Arguments:
                flag_save_: boolean controlling if the plots get saved (default = False)
                save_name_: (string), base name to be used in saving the plots (default = None)
                flag_show_: boolean setting if the plot gets showed or not (default = True)

        Output:
            Default = None, interactive view
            If flag_save = True then outputs a png image
    """
    import seaborn as sns
    import matplotlib.pyplot as plt
    #TO DO: create a dictionary for default input items instead of list
    sns.set_theme()
    # Will be deprecated soon, must update data structure
    # https://seaborn.pydata.org/tutorial/data_structure.html
    plot = sns.displot(array1)
    plot.displot(array2)
    plot.set_axis_labels(axes_labels[0], "count")
    plt.tight_layout()
    if flag_save_:
        if not save_name_:
            base_name = "dist_"
        else:
            base_name = save_name_
        save_name = base_name + axes_labels[0] + '_' + axes_labels[1]
        plt.savefig(save_name +'.png')
    if flag_show_:
        plt.show()


def _density_scatter( xarr , yarr, ax = None, sort = True, bins = 24, only_cmap = False, **kwargs ):
    """
7y        Scatter plot colored by 2d histogram

        Code snippet taken from (adapted naming convention)
        https://stackoverflow.com/questions/20105364/how-can-i-make-a-scatter-plot-colored-by-density-in-matplotlib
        Credits to: Guillaume

        Input:
            arr1: numpy array of first data set
            arr2: numpy array of second data set
            ax: default = None, matplotlib Axes object
            sort: boolean = True, sorting color map values before plotting
            bins: default = 24, integer specifying number of bins in both directions of 2D histogram
            only_cmap: default = False, if True the function only returns the density map 

        Output: 
            ax: matplotlib Axes object
    """
    import matplotlib.pyplot as plt
    from scipy.interpolate import interpn
    import numpy as np
    from matplotlib import cm
    from matplotlib.colors import Normalize 

    data , xedge, yedge = np.histogram2d( xarr, yarr, bins = bins, density = True )
    zarr = interpn( ( 0.5*(xedge[1:] + xedge[:-1]),0.5*(yedge[1:]+yedge[:-1]) ),
                    data ,
                    np.vstack([xarr,yarr]).T ,
                    method = "splinef2d", bounds_error = False)

    # To be sure to plot all data
    zarr[np.where(np.isnan(zarr))] = 0.0

    # If we're only interested in the density color map
    if only_cmap:
        return zarr

    # Sort the points by density, so that the densest points are plotted last
    if sort :
        idx = zarr.argsort()
        xarr, yarr, zarr = xarr[idx], yarr[idx], zarr[idx]

    if ax is None :
        fig , ax = plt.subplots()

    ax.scatter( xarr, yarr, c=zarr, **kwargs )

    norm = Normalize(vmin = np.min(zarr), vmax = np.max(zarr))
    cbar = fig.colorbar(cm.ScalarMappable(norm = norm), ax=ax)
    cbar.ax.set_ylabel('Density')


def matplotlib_simple_scatter(array1, array2, axes_labels,
                                flag_save_ = False, save_name_ = None, flag_show_ = True):
    """ Function to generate a scatter plot of two data arrays of same length with matplotlib.
        If scipy is available a density scatter plot will be generated.

        Input:
            array1: numpy array of first data set
            array2: numpy array of second data set
            axes_labels: list of string of length 2, used to specify the labels of output axis
            Optional Arguments:
                flag_save_: boolean controlling if the plots get saved (default = False)
                save_name_: (string), base name to be used in saving the plots (default = None)
                flag_show_: boolean setting if the plot gets showed or not (default = True)

        Output:
            Default = None, interactive view
            If flag_save = True then outputs a png image
    """
    import matplotlib.pyplot as plt

    if check_environmental_modules(["scipy"])[0] is not False:  
        _density_scatter( array1 , array2,  ax = None)

    else:    
        plt.scatter(array1, array2)
    
    plt.xlabel(axes_labels[0] + ' ' + "field 1" )
    plt.ylabel(axes_labels[1] + ' ' + "field 2")
    plt.tight_layout()
    if flag_save_:
        if not save_name_:
            base_name = "scatter_"
        else:
            base_name = save_name_+"_"
        save_name = base_name + axes_labels[0] + '_' + axes_labels[1]
        plt.savefig(save_name +'.png')
    if flag_show_:
         plt.show()


def matplotlib_simple_distribution(array1, array2, axes_labels,
                                flag_save_ = False, save_name_ = None, flag_show_ = True):
    """ Function to generate an histogram of two data arrays of different length with matplotlib

        Input:
            array1: numpy array of first data set
            array2: numpy array of second data set
            axes_labels: list of string of length 2, used to specify the labels of output axis
            Optional Arguments:
                flag_save_: boolean controlling if the plots get saved (default = False)
                save_name_: (string), base name to be used in saving the plots (default = None)
                flag_show_: boolean setting if the plot gets showed or not (default = True)

        Output:
            Default = None, interactive view
            If flag_save = True then outputs a png image
    """
    import matplotlib.pyplot as plt
    # To Do: look into a "smart" way for bin selection , options include
    #           1) take a fixed nb
    #           2) take longest data array to 'auto' for bin selection
    #           3) take shortest data array to 'auto' for bin selection

    bin_vals, bins, patches = plt.hist(array1, bins='auto',
                                 density=False, facecolor='cornflowerblue', alpha=0.8, label="field 1")
    bin_vals, bins, patches = plt.hist(array2, bins = bins,
                                 density=False, facecolor='lightgreen', alpha=0.6, label="field 2")
    plt.xlabel(axes_labels[0] + ' ')
    plt.ylabel("Count")
    plt.legend()
    plt.tight_layout()
    if flag_save_:
        if not save_name_:
            base_name = "hist_"
        else:
            base_name = save_name_
        save_name = base_name + axes_labels[0]
        plt.savefig(save_name +'.png')
    if flag_show_:
        plt.show()
