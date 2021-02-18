"""Helper functions for validating LFOM.
Created on January 6, 2021

@author: fchapin@aguaclarareach.org
"""

import os
from datetime import datetime
from fpdf import FPDF


class ReportWriter(object):
    """Class to write validation results to a report file"""

    def __init__(self):
        if not os.path.exists("Reports"):
            os.mkdir("Reports")
        now = datetime.now()
        str_now = now.strftime("%Y.%m.%d.%H.%M.%S")
        self.report_name = "Reports/Validation_Report_" + str_now + ".txt"
        self.report_file = open(self.report_name, "x+")
        self.report_file.write("AIDE Validation Report\n")
        self.result = "Valid"

    def set_result(self, msg):
        """Write the given text to the report file

        Args:
            msg: string of text which represents validation result

        Returns:
            none
        """
        self.result = msg

    def get_result(self):
        """Write the given text to the report file

        Args:
            none

        Returns:
            result: string of text which represents validation result
        """
        return self.result

    def write_message(self, msg):
        """Write the given text to the report file

        Args:
            msg: string of text to add to the report file

        Returns:
            none
        """
        self.report_file.write(msg)

    def to_pdf(self, file_name=None, output_path=None):
        """Convert report file to PDF

        Args:
            file_name: path to file to be converted. Defaults to None
                which uses report_name associated with this ReportWriter object

            output_path: path to output file. Defaults to None which replaces .txt
                in report_name associated with this ReportWriter object with .pdf

        Returns:
            none

        """
        if file_name is None:
            file_name = self.report_name

        file = open(file_name, "r")

        if output_path is None:
            output_path = ".".join(self.report_name.split(".")[:-1] + ["pdf"])

        pdf = FPDF()
        # add a page and set font
        pdf.add_page()
        pdf.set_font("Arial", size=15)

        # insert the lines in pdf then save
        for x in file:
            pdf.multi_cell(0, 5, txt=x, align="L")
        pdf.output(output_path)

    def close(self):
        """Closes the report file associated with this ReportWriter

        Args:
            none

        Returns:
            none
        """
        self.report_file.close()
