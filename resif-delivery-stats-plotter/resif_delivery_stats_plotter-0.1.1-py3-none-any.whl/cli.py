#!/usr/bin/env python
# encoding: utf8
import click
import click_log
import logging
import requests_cache
from .errors import NoDataError, ApiError
from .factories.network import NetworkFactory
from .factories.plotter import ServicePlotterFactory
from .factories.report import ReportFactory

# Configure logger
logger = logging.getLogger('resif_delivery_stats_plotter')
click_log.basic_config(logger)

# Configure requests cache (expire after 1h)
requests_cache.install_cache('cache', expire_after=3600)


@click.group()
def cli():
    pass


# REPORT
########################################################################################################################

@cli.command()
@click_log.simple_verbosity_option(logger)
@click.argument('network', type=click.STRING)
@click.argument('year', type=click.INT)
@click.option('--width', type=click.INT)
@click.option('--height', type=click.INT)
@click.option('--format', 'report_format', default='png')
@click.option('--unit', default='GB')
@click.option('--no-plots', 'no_plots', is_flag=True)
def report(network, year, width, height, report_format, unit, no_plots):
    """Generates an annual report of a network"""

    click.echo("Building %i annual report for '%s' network" % (year, network))
    try:
        report = ReportFactory.factory(year, network)
        report.build(output_format=report_format, unit=unit, width=width, height=height, with_plots=(not no_plots))
    except NoDataError:
        click.echo("No data found!")
    except ApiError as e:
        click.echo(e)


# PLOTS
########################################################################################################################

@cli.command()
@click_log.simple_verbosity_option(logger)
@click.argument('network_code', type=click.STRING)
@click.argument('year', type=click.INT)
@click.option('--width', type=click.INT)
@click.option('--height', type=click.INT)
@click.option('--format', 'image_format', default=ServicePlotterFactory.FORMAT_PNG)
def plot_network_availability(network_code, year, width, height, image_format):
    """Plots the annual availability of each station of a network"""

    click.echo("Plotting the %i availability of '%s' network" % (year, network_code))
    try:
        network = NetworkFactory.factory(network_code, channel_year=year)
        service_plotter = ServicePlotterFactory.factory(image_format)
        service_plotter.plot_network_availability(network=network, year=year, width=width, height=height)
    except NoDataError:
        click.echo("No data found!")
    except ApiError as e:
        click.echo(e)


@cli.command()
@click_log.simple_verbosity_option(logger)
@click.argument('network_code', type=click.STRING)
@click.argument('year', type=click.INT)
@click.option('--width', type=click.INT)
@click.option('--height', type=click.INT)
@click.option('--format', 'image_format', default=ServicePlotterFactory.FORMAT_PNG)
@click.option('--unit', default='GB')
def plot_data_send_yearly(network_code, year, width, height, image_format, unit):
    """Plots the amount of data send yearly for a network"""

    click.echo("Plotting the yearly amount data send for '%s' network" % network_code)
    try:
        network = NetworkFactory.factory(network_code)
        service_plotter = ServicePlotterFactory.factory(image_format)
        service_plotter.plot_data_send_yearly(network=network, year=year, width=width, height=height, unit=unit)
    except NoDataError:
        click.echo("No data found!")
    except ApiError as e:
        click.echo(e)


@cli.command()
@click_log.simple_verbosity_option(logger)
@click.argument('network_code', type=click.STRING)
@click.argument('year', type=click.INT)
@click.option('--width', type=click.INT)
@click.option('--height', type=click.INT)
@click.option('--format', 'image_format', default=ServicePlotterFactory.FORMAT_PNG)
@click.option('--unit', default='GB')
def plot_data_send_monthly(network_code, year, width, height, image_format, unit):
    """Plots the amount of data send monthly for a network"""

    click.echo("Plotting the monthly amount data send for '%s' network" % network_code)
    try:
        network = NetworkFactory.factory(network_code)
        service_plotter = ServicePlotterFactory.factory(image_format)
        service_plotter.plot_data_send_monthly(network=network, year=year, width=width, height=height, unit=unit)
    except NoDataError:
        click.echo("No data found!")
    except ApiError as e:
        click.echo(e)


# @cli.command()
# @click_log.simple_verbosity_option(logger)
# @click.argument('network_code', type=click.STRING)
# @click.argument('year', type=click.INT)
# @click.option('--width', type=click.INT)
# @click.option('--height', type=click.INT)
# @click.option('--format', 'image_format', default=ServicePlotterFactory.FORMAT_PNG)
# @click.option('--unit', default='GB')
# def plot_data_send_against_other_networks(network_code, year, width, height, image_format, unit):
#     """Plots a pie chart of the amount of data send for a network against other networks"""
#
#     click.echo("Plotting a pie chart of the amount of data send for '%s' network against other networks" % network_code)
#     try:
#         network = NetworkFactory.factory(network_code)
#         service_plotter = ServicePlotterFactory.factory(image_format)
#         service_plotter.plot_data_send_by_other_networks(network=network, year=year, width=width, height=height, unit=unit)
#     except NoDataError:
#         click.echo("No data found!")
#     except ApiError as e:
#         click.echo(e)


@cli.command()
@click_log.simple_verbosity_option(logger)
@click.argument('network_code', type=click.STRING)
@click.argument('year', type=click.INT)
@click.option('--width', type=click.INT)
@click.option('--height', type=click.INT)
@click.option('--format', 'image_format', default=ServicePlotterFactory.FORMAT_PNG)
@click.option('--unit', default='GB')
def plot_data_stored_yearly(network_code, year, width, height, image_format, unit):
    """Plots the amount of data send stored for a network"""

    click.echo("Plotting the monthly amount data stored for '%s' network" % network_code)
    try:
        network = NetworkFactory.factory(network_code)
        service_plotter = ServicePlotterFactory.factory(image_format)
        service_plotter.plot_data_stored_yearly(network=network, year=year, width=width, height=height, unit=unit)
    except NoDataError:
        click.echo("No data found!")
    except ApiError as e:
        click.echo(e)


@cli.command()
@click_log.simple_verbosity_option(logger)
@click.argument('network_code', type=click.STRING)
@click.argument('year', type=click.INT)
@click.option('--width', type=click.INT)
@click.option('--height', type=click.INT)
@click.option('--format', 'image_format', default=ServicePlotterFactory.FORMAT_PNG)
def plot_requests_yearly(network_code, year, width, height, image_format):
    """Plots the number of requests querying yearly a network"""

    click.echo("Plotting the number of requests querying yearly the'%s' network" % network_code)
    try:
        network = NetworkFactory.factory(network_code)
        service_plotter = ServicePlotterFactory.factory(image_format)
        service_plotter.plot_requests_yearly(network=network, year=year, width=width, height=height)
    except NoDataError:
        click.echo("No data found!")
    except ApiError as e:
        click.echo(e)


@cli.command()
@click_log.simple_verbosity_option(logger)
@click.argument('network_code', type=click.STRING)
@click.argument('year', type=click.INT)
@click.option('--width', type=click.INT)
@click.option('--height', type=click.INT)
@click.option('--format', 'image_format', default=ServicePlotterFactory.FORMAT_PNG)
def plot_requests_monthly(network_code, year, width, height, image_format):
    """Plots the number of requests querying yearly a network"""

    click.echo("Plotting the number of requests querying monthly the'%s' network" % network_code)
    try:
        network = NetworkFactory.factory(network_code)
        service_plotter = ServicePlotterFactory.factory(image_format)
        service_plotter.plot_requests_monthly(network=network, year=year, width=width, height=height)
    except NoDataError:
        click.echo("No data found!")
    except ApiError as e:
        click.echo(e)


@cli.command()
@click_log.simple_verbosity_option(logger)
@click.argument('network_code', type=click.STRING)
@click.argument('year', type=click.INT)
@click.option('--width', type=click.INT)
@click.option('--height', type=click.INT)
@click.option('--format', 'image_format', default=ServicePlotterFactory.FORMAT_PNG)
def plot_map_requests_by_country(network_code, year, width, height, image_format):
    """Plots on a world map the number of requests querying a network"""

    click.echo("Plotting on a world map the number of requests querying the'%s' network" % network_code)
    try:
        network = NetworkFactory.factory(network_code)
        service_plotter = ServicePlotterFactory.factory(image_format)
        service_plotter.plot_map_requests_by_country(network=network, year=year, width=width, height=height)
    except NoDataError:
        click.echo("No data found!")
    except ApiError as e:
        click.echo(e)


@cli.command()
@click_log.simple_verbosity_option(logger)
@click.argument('network_code', type=click.STRING)
@click.argument('year', type=click.INT)
@click.option('--width', type=click.INT)
@click.option('--height', type=click.INT)
@click.option('--format', 'image_format', default=ServicePlotterFactory.FORMAT_PNG)
def plot_map_clients_by_country(network_code, year, width, height, image_format):
    """Plots on a world map the number of clients querying a network"""

    click.echo("Plotting on a world map the number of clients querying the'%s' network" % network_code)
    try:
        network = NetworkFactory.factory(network_code)
        service_plotter = ServicePlotterFactory.factory(image_format)
        service_plotter.plot_map_clients_by_country(network=network, year=year, width=width, height=height)
    except NoDataError:
        click.echo("No data found!")
    except ApiError as e:
        click.echo(e)


@cli.command()
@click_log.simple_verbosity_option(logger)
@click.argument('network_code', type=click.STRING)
@click.argument('year', type=click.INT)
@click.option('--width', type=click.INT)
@click.option('--height', type=click.INT)
@click.option('--zoom', type=click.INT)
@click.option('--format', 'image_format', default=ServicePlotterFactory.FORMAT_PNG)
def plot_map_network_stations(network_code, year, width, height, zoom, image_format):
    """Plots on a world map the stations a network"""

    click.echo("Plotting on a map locating the stations of the'%s' network" % network_code)
    try:
        network = NetworkFactory.factory(network_code)
        service_plotter = ServicePlotterFactory.factory(image_format)
        service_plotter.plot_map_network_stations(network=network, year=year, width=width, height=height, zoom=zoom)
    except NoDataError:
        click.echo("No data found!")
    except ApiError as e:
        click.echo(e)


# CACHE
########################################################################################################################

@cli.command()
@click_log.simple_verbosity_option(logger)
def clear_requests_cache():
    requests_cache.clear()
    click.echo("Requests cache cleared!")


# DEBUG
########################################################################################################################


@cli.command()
@click_log.simple_verbosity_option(logger)
def list_networks():
    """Lists the networks"""

    click.echo("Listing the networks")
    try:
        networks = NetworkFactory.list()
        for network in networks:
            click.echo(network)
    except NoDataError:
        click.echo("No data found!")
    except ApiError as e:
        click.echo(e)


@cli.command()
@click_log.simple_verbosity_option(logger)
@click.argument('network_code', type=click.STRING)
@click.option('--year', type=click.INT)
def list_stations(network_code, year):
    """Lists the stations of a network"""

    click.echo("Listing the stations of the '%s' network" % network_code)
    try:
        network = NetworkFactory.factory(network_code)
        for station in network.stations:
            click.echo(station)
            if year:
                click.echo(' > Open in %s: %s' % (year, station.is_open(year)))
    except NoDataError:
        click.echo("No data found!")
    except ApiError as e:
        click.echo(e)


@cli.command()
@click_log.simple_verbosity_option(logger)
@click.argument('network_code', type=click.STRING)
@click.argument('station_code', type=click.STRING)
@click.option('--year', type=click.INT)
def list_channels(network_code, station_code, year):
    """Lists the channels of a station of network"""

    click.echo("Listing the channels of the '%s' station from the network" % (station_code, network_code))
    try:
        network = NetworkFactory.factory(network_code)
        station = network.get_station(station_code)
        for channel in station.channels:
            click.echo(channel)
            if year:
                click.echo(' > Open in %s: %s' % (year, channel.is_open(year)))
    except NoDataError:
        click.echo("No data found!")
    except ApiError as e:
        click.echo(e)


if __name__ == '__main__':
    cli()
