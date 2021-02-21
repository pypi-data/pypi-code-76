from pathlib import *
import json
import csv
import matplotlib.pyplot as plt
from abc import ABC

class Exporter(ABC):
    """An **abstract** class that can be used to export simulation results to
    different formats.
    """

    _supported_formats = ["csv", "json", "jpg", "png"]
    """ A list of supported file formats. Used internally to validate a given input format.
    """

    @classmethod
    def export_data(cls, results, file_format, system_elements, rel_path="./results"):
        """Saves the simulation results to the file system.

         rel path: .\\somepath  ./somepath  somepath ../somepath ..\\somepath

        :param results: The result of the simulation
        :type results: dict, see :py:func:`~sysdynpy.simulator.get_simulation_results`
            for more details.
        :param file_format: 'csv' or 'json'
        :type file_format: str
        :param system_elements: Names of the system elements to export data for.
        :type system_elements: list of strings
        :param rel_path: The path where to store the exported file (including the filename).
            Relative to the current working directory. Can include the file format.
            If it is not included it will be appended. Make sure the folder
            already exists, it will not be created. Defaults to "./results".

            Examples:

                |  .\\\\\\\\path\\\\\\\\to\\\\\\\\file.csv
                |  ./path/to/file.json
                |  ..\\\\\\\\path\\\\\\\\to\\\\\\\\file.json
                |  ../path/to/file
        :type rel_path: str
        """
        out_path, results_filtered = None, None
        try:
           out_path, results_filtered = \
                cls._prepare_export(results, file_format, system_elements, rel_path)
        except ValueError as v:
            raise v
        
        if file_format == "csv":
            with open(out_path, "w", encoding="utf-8", newline='') as outfile:
                writer = csv.writer(outfile, delimiter=";")
                writer.writerow(results_filtered.keys())
                writer.writerows(zip(*results_filtered.values()))

        if file_format == "json":
            with open(out_path, "w", encoding="utf-8", newline='') as outfile:
                json.dump(results_filtered, outfile, ensure_ascii=False)
              

        
    @classmethod
    def export_graph(cls, results, file_format, system_elements, \
        range_x, range_y, colors, title="", label_x="", label_y="", line_width=1,
        legend_pos="upper left", rel_path="./results"):
        """Creates a diagram from the simulation results and saves it to the file
        system.

        Many arguments get piped through to `Matplotlib <https://matplotlib.org/>`__.
        See the `Documentation <https://matplotlib.org/api/pyplot_summary.html>`__
        for details. This method serves as a quick way to create a graph, but is
        fairly limited in its options. Use the Matplotlib API directly if you
        need more customization.

        :param results: The result of the simulation
        :type results: dict, see :py:func:`~sysdynpy.simulator.get_simulation_results`
            for more details.
        :param file_format: 'jpg' or 'png'
        :type file_format: str
        :param system_elements: Names of the system elements to export data for.
        :type system_elements: list of strings
        :param range_y: Matplotlib parameter. Defines the range of the y-axis.
            List with two integers. The first is the lower boundary, the second
            is the upper boundary.
        :type range_y: list of integers 
        :param colors: Matplotlib parameter. Colors to use for the trajectories.
            Each color corresponds to the system element at the same index.
        :type colors: list of strings.
        :param title: Matplotlib parameter. Headline of the plot, defaults to ""
        :type title: str
        :param label_x: Matplotlib parameter. Label for the x-axis, defaults to ""
        :type label_x: str
        :param label_y: Matplotlib parameter. Label for the y-axis, defaults to ""
        :type label_y: str
        :param line_width: Matplotlib parameter. Width of the trajectories, defaults to 1
        :type line_width: float
        :param legend_pos: Matplotlib parameter. Position of the legend in the
            canvas, defaults to "upper left"
        :type legend_pos: str
        :param rel_path: The path where to store the exported file (including the filename).
            Relative to the current working directory. Can include the file format.
            If it is not included it will be appended. Make sure the folder
            already exists, it will not be created. Defaults to "./results".

            Examples:

                |  .\\\\\\\\path\\\\\\\\to\\\\\\\\file.csv
                |  ./path/to/file.json
                |  ..\\\\\\\\path\\\\\\\\to\\\\\\\\file.json
                |  ../path/to/file
        :type rel_path: str
        """
        out_path, results_filtered = None, None
        try:
           out_path, results_filtered = \
                cls._prepare_export(results, file_format, system_elements, rel_path)
        except ValueError as v:
            raise v
        
        for key in results_filtered:
            data_x = range(len(results_filtered[key]))
            data_y = results_filtered[key]
            # get position of current key in system_elements so we can set the right color
            idx = system_elements.index(key)
            plt.plot(data_x, data_y, color=colors[idx], \
                linewidth=line_width, label=key)
        
        plt.title(title)
        plt.xlabel(label_x)
        plt.ylabel(label_y)
        plt.xlim(range_x)
        plt.ylim(range_y)
        plt.legend(loc=legend_pos)
        plt.savefig(out_path) # save
        plt.clf() # reset plot

    @classmethod
    def _prepare_export(cls, results, file_format, system_elements, rel_path):
        """Prepares the export. 

        Contains actions that have to be done regardless of export format.
        These actions include:

        * check if file format is supported
        * check if given system elements are in results
        * filter results to only contain given system elements
        * join the given relative path to the location the script is executed from
        
        All these actions are done in separate methods.

        :param file_format: One of the file formats in :py:attr:`~_supported_formats`
        :type file_format: str
        :param results: The result of the simulation
        :type results: dict, see :py:func:`~sysdynpy.simulator.get_simulation_results`
            for more details.
        :param system_elements: Names of the system elements to export data for.
        :type system_elements: list of strings
        :param rel_path: The path where to store the exported file (including the filename).
            Relative to the current working directory. Can include the file format.
            If it is not included it will be appended. Make sure the folder
            already exists, it will not be created. Defaults to "./results".

            Examples:

                |  .\\\\\\\\path\\\\\\\\to\\\\\\\\file.csv
                |  ./path/to/file.json
                |  ..\\\\\\\\path\\\\\\\\to\\\\\\\\file.json
                |  ../path/to/file
        :type rel_path: str
        :return: A tuple with two elements:

            * the joined, absolute output path
            * a filtered version of the result dictionary, including only the
                system elements to export
        :rtype: (str, dict)
        """
        # check if file format is supported
        try:
            cls._check_file_format(file_format)
        except ValueError as v:
            raise v

        # check if all given system elements are in results
        try:
            _check_if_system_elements_in_results(results, system_elements)
        except ValueError as v:
            raise v

         # filter results to only contain given system elements
        results_filtered = _filter_results(results, system_elements)
        
        # create file output path
        out_path = _create_abs_output_path(rel_path, file_format)

        return out_path, results_filtered

    @classmethod
    def _check_file_format(cls, file_format):
        """Checks if the given file format is supported.

        :param file_format: file format to check
        :type file_format: str
        :raises ValueError: If the file format is not supported
        """
        if file_format.lower() not in cls._supported_formats:
            raise ValueError("Given file format '" + file_format
            + "' is not supported. Supported formats are: "
            + cls._supported_formats)

    
def _create_abs_output_path(rel_path, file_format):
    """Joins the current working directory with the relative path.

    :param rel_path: The path to join.
    
        Examples:

                |  .\\\\\\\\path\\\\\\\\to\\\\\\\\file.csv
                |  ./path/to/file.json
                |  ..\\\\\\\\path\\\\\\\\to\\\\\\\\file.json
                |  ../path/to/file
    :type rel_path: str
    :param file_format: The file format to append to the path.
    :type file_format: str
    :return: The joined, absolute path
    :rtype: str
    """
    current_dir = Path.cwd()
    if file_format not in rel_path:
        rel_path += "." + file_format.lower()
    return (current_dir / rel_path).resolve()


def _check_if_system_elements_in_results(results, system_elements):
    """Checks if the given system elements are included in the result dictionary.

    :param results: The dictionary with simulation results.
    :type results: dict
    :param system_elements: List of system element names
    :type system_elements: list of strings
    :raises ValueError: If any of the system element names in not in the
        simulation results.
    """
    for element in system_elements:
        if element not in results.keys():
            raise ValueError("Given system element "
                + element + " is not in simulation results")


def _filter_results(results, system_elements):
    """Filters the simulation results to only include certain system elements.

    :param results: The simulation results
    :type results: dict
    :param system_elements: List of system element names to keep
    :type system_elements: list of strings
    :return: The filtered results
    :rtype: dict
    """
    results_filtered = {}
    for key in results.keys():
        if key in system_elements:
            results_filtered[key] = results[key]
    return results_filtered