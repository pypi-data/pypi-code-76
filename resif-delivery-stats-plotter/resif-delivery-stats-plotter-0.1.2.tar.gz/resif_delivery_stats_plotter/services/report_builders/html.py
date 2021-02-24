# encoding: utf8
import logging
import os
import pathlib
import shutil
import datetime
from jinja2 import Environment, PackageLoader
from . import ServiceReportBuilderAbstract
from resif_delivery_stats_plotter import __version__

logger = logging.getLogger(__name__)


class ServiceReportBuilderHtml(ServiceReportBuilderAbstract):
    """
    HTML report builder
    """

    FORMAT_PNG = 'png'
    FORMAT_HTML = 'html'

    @classmethod
    def build(cls, report, output_format=FORMAT_PNG, unit=None, width=None, height=None, use_local_assets=True, with_plots=True):
        """
        Builds an HTML report
        :param report: The report object
        :param output_format: The plot format (default='png')
        :param unit: The unit in which the amount of data are converted
        :param width: The width of generated images
        :param height: The height of generated images
        :param use_local_assets: Enables the usage of local assets instead of on-line assets
        :param with_plots: Include plots
        :return: The output file path
        :rtype: str
        """
        logger.debug("ServiceReportBuilderHtml.build(%s, %s, %s, %s, %s, %s, %s)" % (report, output_format, unit, width, height, use_local_assets, with_plots))

        jinja_env = Environment(loader=PackageLoader('resif_delivery_stats_plotter'),
                                lstrip_blocks=True)  # , trim_blocks=True)

        # Get output directory path
        output_dirpath = cls.output_dir(report, True)

        # Copy assets if needed
        if use_local_assets:
            cls.copy_assets(output_dirpath, (output_format == cls.FORMAT_HTML))

        # Render the page content and get the output filename
        output_filename = None
        if output_format == cls.FORMAT_PNG:
            output = cls.render_png(report, jinja_env, unit, width, height, use_local_assets, with_plots)
            output_filename = 'report_png.html'
        elif output_format == cls.FORMAT_HTML:
            output = cls.render_html(report, jinja_env, unit, width, height, use_local_assets, with_plots)
            output_filename = 'report.html'
        else:
            raise Exception("Format '%s' is not supported by any renderer" % output_format)

        # Write the output content to output file
        output_filepath = os.path.join(output_dirpath, output_filename)
        with open(output_filepath, 'w') as output_file:
            output_file.write(output)

        logger.info("Report saved as %s" % output_filepath)
        return output_filename

    @staticmethod
    def render_png(report, jinja_env, unit, width, height, use_local_assets, with_plots):
        """
        Render an HTML report using static PNG plots
        :param report: The report object
        :param jinja_env: The Jinja2 environment
        :param unit: The unit in which the amount of data are converted
        :param width: The width of generated images
        :param height: The height of generated images
        :param use_local_assets: Enables the usage of local assets instead of on-line assets
        :param with_plots: Include plots
        :return: The HTML report content
        :rtype: str
        """
        logger.debug("ServiceReportBuilderHtml.render_png(%s, %s)" % (report, jinja_env))

        params = {
            'report': report,
            'unit': unit,
            'use_local_assets': use_local_assets,
            'use_plotly': False,
            'version': __version__,
            'today': datetime.datetime.utcnow().strftime("%Y-%m-%d at %Hh%M UTC"),
        }
        if with_plots:
            from resif_delivery_stats_plotter.services.plotters.png import ServicePlotterPNG as service_plotter
            params.update({
                'plot_availability_network': service_plotter.plot_network_availability(report.network, report.year, width, height),
                'plot_data_send_yearly': service_plotter.plot_data_send_yearly(report.network, report.year, width, height, unit=unit),
                'plot_data_send_monthly': service_plotter.plot_data_send_monthly(report.network, report.year, width, height, unit=unit),
                'plot_data_stored_yearly': service_plotter.plot_data_stored_yearly(report.network, report.year, width, height, unit=unit),
                'plot_requests_yearly': service_plotter.plot_requests_yearly(report.network, report.year, width, height),
                'plot_requests_monthly': service_plotter.plot_requests_monthly(report.network, report.year, width, height),
                'map_requests_by_country': service_plotter.plot_map_requests_by_country(report.network, report.year, width, height),
                'map_clients_by_country': service_plotter.plot_map_clients_by_country(report.network, report.year, width, height),
                'map_stations': service_plotter.plot_map_network_stations(report.network, report.year, width, height), #FIXME
            })

        jinja_tpl = jinja_env.get_template('report_html_png.jinja2')
        jinja_out = jinja_tpl.render(**params)
        return jinja_out

    @staticmethod
    def render_html(report, jinja_env, unit, width, height, use_local_assets, with_plots):
        """
        Render an HTML report using dynamic JS plots
        :param report: The report object
        :param jinja_env: The Jinja2 environment
        :param unit: The unit in which the amount of data are converted
        :param width: The width of generated images
        :param height: The height of generated images
        :param use_local_assets: Enables the usage of local assets instead of on-line assets
        :param with_plots: Include plots
        :return: The HTML report content
        :rtype: str
        """
        logger.debug("ServiceReportBuilderHtml.render_html(%s, %s)" % (report, jinja_env))

        params = {
            'report': report,
            'unit': unit,
            'use_local_assets': use_local_assets,
            'use_plotly': True,
            'version': __version__
        }
        if with_plots:
            from resif_delivery_stats_plotter.services.plotters.html import ServicePlotterHTML as service_plotter
            params.update({
                'plot_availability_network': service_plotter.plot_network_availability(report.network, report.year, width, height, output_format=service_plotter.FORMAT_DIV),
                'plot_data_send_yearly': service_plotter.plot_data_send_yearly(report.network, report.year, width, height, output_format=service_plotter.FORMAT_DIV, unit=unit),
                'plot_data_send_monthly': service_plotter.plot_data_send_monthly(report.network, report.year, width, height, output_format=service_plotter.FORMAT_DIV, unit=unit),
                'map_requests_by_country': service_plotter.plot_map_requests_by_country(report.network, report.year, width, height, output_format=service_plotter.FORMAT_DIV),
                'map_clients_by_country': service_plotter.plot_map_clients_by_country(report.network, report.year, width, height, output_format=service_plotter.FORMAT_DIV),
                'map_stations': service_plotter.plot_map_network_stations(report.network, report.year, width, height, output_format=service_plotter.FORMAT_DIV),
            })

        jinja_tpl = jinja_env.get_template('report_html.jinja2')
        jinja_out = jinja_tpl.render(**params)
        return jinja_out

    @staticmethod
    def copy_assets(output_dir, use_plotly=False):
        """
        Copy assets to output directory

        :param output_dir: The output directory path
        """
        logger.debug("ServiceReportBuilderHtml.copy_assets(%s, %s)" % (output_dir, use_plotly))

        # List the assets to copy
        assets = [
            'resif_logo.png',
            'bootstrap.min.css',
            'bootstrap.bundle.min.js',
            'jquery-3.5.1.slim.min.js',
            'jquery.dataTables.min.css',
            'jquery.dataTables.min.js',
        ]
        if use_plotly:
            assets.append('plotly-latest.min.js')

        # Get the assets source directory path
        root_dir = pathlib.Path(__file__).resolve().parent.parent.parent

        # Copy each asset to output directory
        for asset in assets:
            shutil.copyfile(os.path.join(root_dir, 'assets', asset), os.path.join(output_dir, asset))
