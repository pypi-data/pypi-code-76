# # encoding: utf8
# import logging
# import os
# import datetime
# import folium
# import statistics
# import plotly.express as px
# import plotly.graph_objects as go
# from iso3166 import countries
# from io import StringIO
# from resif_delivery_stats_plotter.services.clients.availabilty import ServiceClientAvailability as service_availability
# from . import ServicePlotterAbstract
#
# logger = logging.getLogger(__name__)
#
#
# class ServicePlotterHTML(ServicePlotterAbstract):
#     """
#     Dynamic JS plotter
#     """
#
#     FORMAT_FULL_HTML = 'full_html'
#     FORMAT_DIV = 'div'
#
#     @classmethod
#     def plot_network_availability(cls, network, year=None, width=None, height=None, output_format=FORMAT_FULL_HTML):
#         """
#         Plots the annual availability of each station of a network
#         :param network: The network object
#         :param year: The year
#         :param width: The width of the output image
#         :param height: The height of the output image
#         :param output_format: The output format (default='full_html' | 'div')
#         :return: The plot output file path or the div content
#         :rtype: str
#         """
#         logger.debug("ServicePlotterHTML.plot_network_availability(%s, %s, %s, %s, %s)" % (network, year, width, height, output_format))
#         year = year or datetime.datetime.now().year
#         logger.info("Plotting availability of network %s in %i" % (network.code, year))
#
#         # Initialize colors and labels
#         qualities = {}
#         qualities_colors_map = {
#             'Valid': 'blue',
#             'Raw': 'orange',
#         }
#         for quality in (service_availability.QUALITY_Q_CONTROLLED, service_availability.QUALITY_M_MODIFIED):
#             qualities[quality] = 'Valid'
#         for quality in (service_availability.QUALITY_R_RAW, service_availability.QUALITY_D_INDETERMINATE):
#             qualities[quality] = 'Raw'
#
#         # Build plot data
#         plot_data = []
#         for station in network.stations:
#             for channel in station.representative_channels(year):
#                 channel_qualities = service_availability.channel(channel.code, channel.location, station.code, network.code, year)
#                 if channel_qualities:
#                     for quality, timespans in channel_qualities.items():
#                         for timespan in timespans:
#                             plot_data.append(
#                                 dict(Station="%s.%s.%s" % (network.code, station.code, channel.location_code),
#                                      Start=timespan[0], Finish=timespan[1], Quality=qualities.get(quality))
#                                 )
#
#         # Save
#         figure = px.timeline(plot_data, x_start="Start", x_end="Finish", y="Station", color="Quality",
#                              color_discrete_map=qualities_colors_map)
#
#         if output_format == cls.FORMAT_DIV:
#             with StringIO() as buffer:
#                 figure.write_html(
#                     include_plotlyjs=False,
#                     full_html=False,
#                     file=buffer
#                 )
#                 output = buffer.getvalue()
#
#             logger.info("Plot build as a <div>")
#             return output
#
#         else:
#             output_filename = 'plot_data_availability_network.html'
#             output_filepath = os.path.join(cls.output_dir(network, year), output_filename)
#             figure.write_html(
#                 include_plotlyjs='cdn',
#                 full_html=True,
#                 file=output_filepath
#             )
#             logger.info("Plot saved as %s" % output_filepath)
#             return output_filename
#
#     @classmethod
#     def plot_data_send_yearly(cls, network, year=None, width=None, height=None, output_format=FORMAT_FULL_HTML, start_year=None, unit=None):
#         """
#         Plots the amount of data send yearly for a network
#         :param network: The network object
#         :param year: The year
#         :param width: The width of the output image
#         :param height: The height of the output image
#         :param output_format: The output format (default='full_html' | 'div')
#         :param start_year: The starting year
#         :param unit: The unit in which the values are converted
#         :return: The plot output file path or the div content
#         :rtype: str
#         """
#         logger.debug("ServicePlotterHTML.plot_data_send_yearly(%s, %s, %s, %s, %s, %s, %s)" % (network, year, width, height, output_format, start_year, unit))
#         year = year or datetime.datetime.now().year
#         logger.info("Plotting data send yearly by network %s until %i" % (network.code, year))
#
#         #Build plot data
#         plot_data_years = []
#         plot_data_dataselect = []
#         plot_data_seedlink = []
#
#         # Calculate starting year
#         if start_year:
#             start_year = max(start_year, start_year)
#         else:
#             start_year = network.year_start
#         logger.debug('Starting year: %s' % start_year)
#
#         # Plot data
#         has_data = False
#         for y in range(start_year, year+1):
#             send_dataselect = network.data_send_dataselect(year=y, unit=unit)
#             send_seedlink = network.data_send_seedlink(year=y, unit=unit)
#             if has_data or send_dataselect or send_seedlink:
#                 has_data = True
#                 plot_data_years.append(y)
#                 plot_data_dataselect.append(send_dataselect or 0)
#                 plot_data_seedlink.append(send_seedlink or 0)
#
#         # Save
#         figure = go.Figure(data=[
#             go.Bar(name='Seedlink (%s)' % (unit or 'Bytes'), x=plot_data_years, y=plot_data_seedlink),
#             go.Bar(name='Dataselect (%s)' % (unit or 'Bytes'), x=plot_data_years, y=plot_data_dataselect)
#         ])
#         figure.update_layout(barmode='stack')
#
#         if output_format == cls.FORMAT_DIV:
#             with StringIO() as buffer:
#                 figure.write_html(
#                     include_plotlyjs=False,
#                     full_html=False,
#                     file=buffer
#                 )
#                 output = buffer.getvalue()
#
#             logger.info("Plot build as a <div>")
#             return output
#
#         else:
#             output_filename = 'plot_data_send_yearly.html'
#             output_filepath = os.path.join(cls.output_dir(network, year), output_filename)
#             figure.write_html(
#                 include_plotlyjs='cdn',
#                 full_html=True,
#                 file=output_filepath
#             )
#             logger.info("Plot saved as %s" % output_filepath)
#             return output_filename
#
#     @classmethod
#     def plot_data_send_monthly(cls, network, year=None, width=None, height=None, output_format=FORMAT_FULL_HTML, unit=None):
#         """
#         Plots the amount of data send monthly for a network
#         :param network: The network object
#         :param year: The year
#         :param width: The width of the output image
#         :param height: The height of the output image
#         :param output_format: The output format (default='full_html' | 'div')
#         :param unit: The unit in which the values are converted
#         :return: The plot output file path or the div content
#         :rtype: str
#         """
#         logger.debug("ServicePlotterHTML.plot_data_send_monthly(%s, %s, %s, %s, %s, %s)" % (network, year, width, height, output_format, unit))
#         year = year or datetime.datetime.now().year
#         logger.info("Plotting data send monthly by network %s in %i" % (network.code, year))
#
#         # Build plot data
#         plot_data_months = []
#         plot_data_dataselect = []
#         plot_data_seedlink = []
#
#         for month in range(1, 13):
#             send_dataselect = network.data_send_dataselect(year=year, month=month, unit=unit) or 0
#             send_seedlink = network.data_send_seedlink(year=year, month=month, unit=unit) or 0
#
#             plot_data_dataselect.append(send_dataselect)
#             plot_data_seedlink.append(send_seedlink)
#             plot_data_months.append(month)
#
#         # Build HTML output
#         figure = go.Figure(data=[
#             go.Bar(name='Seedlink (%s)' % (unit or 'Bytes'), x=plot_data_months, y=plot_data_seedlink),
#             go.Bar(name='Dataselect (%s)' % (unit or 'Bytes'), x=plot_data_months, y=plot_data_dataselect)
#         ])
#         figure.update_layout(barmode='stack')
#
#         if output_format == cls.FORMAT_DIV:
#             with StringIO() as buffer:
#                 figure.write_html(
#                     include_plotlyjs=False,
#                     full_html=False,
#                     file=buffer
#                 )
#                 output = buffer.getvalue()
#
#             logger.info("Plot build as a <div>")
#             return output
#
#         else:
#             output_filename = 'plot_data_send_monthly.html'
#             output_filepath = os.path.join(cls.output_dir(network, year), output_filename)
#             figure.write_html(
#                 include_plotlyjs='cdn',
#                 full_html=True,
#                 file=output_filepath
#             )
#             logger.info("Plot saved as %s" % output_filepath)
#             return output_filename
#
#     @classmethod
#     def plot_data_send_by_other_networks(cls, network, year=None, width=None, height=None, output_format=FORMAT_FULL_HTML, unit=None):
#         """
#         Plots a pie chart with the amount of data send yearly for a network against the other networks
#         :param network: The network object
#         :param year: The year
#         :param width: The width of the output image
#         :param height: The height of the output image
#         :param output_format: The output format (default='full_html' | 'div')
#         :param unit: The unit in which the values are converted
#         :return: The plot output file path or the div content
#         :rtype: str
#         """
#         logger.debug("ServicePlotterHTML.plot_data_send_by_other_networks(%s, %s, %s, %s, %s, %s)" % (network, year, width, height, output_format, unit))
#         year = year or datetime.datetime.now().year
#         logger.info("Plotting ratio of data send for network %s against all networks in %i" % (network.code, year))
#         # TODO
#         pass
#
#     @classmethod
#     def plot_data_stored_yearly(cls, network, year=None, width=None, height=None, output_format=FORMAT_FULL_HTML, start_year=None, unit=None):
#         """
#         Plots the amount of data stored yearly for a network
#         :param network: The network object
#         :param year: The year
#         :param width: The width of the output image
#         :param height: The height of the output image
#         :param output_format: The output format (default='full_html' | 'div')
#         :param start_year: The starting year
#         :param unit: The unit in which the values are converted
#         :return: The plot output file path or the div content
#         :rtype: str
#         """
#         logger.debug("ServicePlotterHTML.plot_data_stored_yearly(%s, %s, %s, %s, %s, %s, %s)" % (network, year, width, height, output_format, start_year, unit))
#         year = year or datetime.datetime.now().year
#         logger.info("Plotting data stored yearly by network %s until %i" % (network.code, year))
#         # TODO
#         pass
#
#     @classmethod
#     def plot_map_requests_by_country(cls, network, year=None, width=None, height=None, output_format=FORMAT_FULL_HTML):
#         """
#         Plots a world map colored by number of requests querying a network
#         :param network: The network object
#         :param year: The year
#         :param width: The width of the output image
#         :param height: The height of the output image
#         :param output_format: The output format (default='full_html' | 'div')
#         :return: The plot output file path or the div content
#         :rtype: str
#         """
#         logger.debug("ServicePlotterHTML.plot_map_requests_by_country(%s, %s, %s, %s, %s)" % (network, year, width, height, output_format))
#         year = year or datetime.datetime.now().year
#         logger.info("Plotting map of requests by country for network %s in %i" % (network.code, year))
#
#         # Build plot data
#         plot_data_locations = []
#         plot_data_values = []
#
#         for country_code, country_requests in network.requests_by_country(year=year).items():
#             try:
#                 country = countries.get(country_code)
#                 plot_data_locations.append(country.alpha3)
#                 plot_data_values.append(int(country_requests))
#             except KeyError:
#                 logger.debug("Unable to resolve country code '%s'" % country_code)
#                 continue
#
#         # Output
#         figure = go.Figure(data=go.Choropleth(locations=plot_data_locations, z=plot_data_values, colorbar_title='Requests', colorscale='Reds'))
#
#         if output_format == cls.FORMAT_DIV:
#             with StringIO() as buffer:
#                 figure.write_html(
#                     include_plotlyjs=False,
#                     full_html=False,
#                     file=buffer
#                 )
#                 output = buffer.getvalue()
#
#             logger.info("Plot build as a <div>")
#             return output
#
#         else:
#             output_filename = 'plot_map_requests_by_country.html'
#             output_filepath = os.path.join(cls.output_dir(network, year), output_filename)
#             figure.write_html(
#                 include_plotlyjs='cdn',
#                 full_html=True,
#                 file=output_filepath
#             )
#             logger.info("Plot saved as %s" % output_filepath)
#             return output_filename
#
#     @classmethod
#     def plot_map_clients_by_country(cls, network, year=None, width=None, height=None, output_format=FORMAT_FULL_HTML):
#         """
#         Plots a world map colored by number of clients querying a network
#         :param network: The network object
#         :param year: The year
#         :param width: The width of the output image
#         :param height: The height of the output image
#         :param output_format: The output format (default='full_html' | 'div')
#         :return: The plot output file path or the div content
#         :rtype: str
#         """
#         logger.debug("ServicePlotterHTML.plot_map_clients_by_country(%s, %s, %s, %s, %s)" % (network, year, width, height, output_format))
#         year = year or datetime.datetime.now().year
#         logger.info("Plotting map of clients by country for network %s in %i" % (network.code, year))
#
#         # Build plot data
#         plot_data_locations = []
#         plot_data_values = []
#
#         for country_code, country_requests in network.clients_by_country(year=year).items():
#             try:
#                 country = countries.get(country_code)
#                 plot_data_locations.append(country.alpha3)
#                 plot_data_values.append(int(country_requests))
#             except KeyError:
#                 logger.debug("Unable to resolve country code '%s'" % country_code)
#                 continue
#
#         # Output
#         figure = go.Figure(data=go.Choropleth(locations=plot_data_locations, z=plot_data_values, colorbar_title='Requests', colorscale='Reds'))
#
#         if output_format == cls.FORMAT_DIV:
#             with StringIO() as buffer:
#                 figure.write_html(
#                     include_plotlyjs=False,
#                     full_html=False,
#                     file=buffer
#                 )
#                 output = buffer.getvalue()
#
#             logger.info("Plot build as a <div>")
#             return output
#
#         else:
#             output_filename = 'plot_map_clients_by_country.html'
#             output_filepath = os.path.join(cls.output_dir(network, year), output_filename)
#             figure.write_html(
#                 include_plotlyjs='cdn',
#                 full_html=True,
#                 file=output_filepath
#             )
#             logger.info("Plot saved as %s" % output_filepath)
#             return output_filename
#
#     @classmethod
#     def plot_map_network_stations(cls, network, year=None, width=None, height=None, output_format=FORMAT_FULL_HTML, zoom=None):
#         """
#         Plots a world map locating the stations of a network
#         :param network: The network object
#         :param year: The year
#         :param width: The width of the output image
#         :param height: The height of the output image
#         :param output_format: The output format (default='full_html' | 'div')
#         :param zoom: The map zoom
#         :return: The plot output file path or the div content
#         :rtype: str
#         """
#         logger.debug("ServicePlotterHTML.plot_map_network_stations(%s, %s, %s, %s, %s, %s)" % (network, year, width, height, output_format, zoom))
#         year = year or datetime.datetime.now().year
#         logger.info("Plotting map of stations for network %s in %i" % (network.code, year))
#
#         folium_markers = []
#         latitudes = []
#         longitudes = []
#
#         for station in network.stations:
#             latitudes.append(station.latitude)
#             longitudes.append(station.longitude)
#             folium_markers.append(
#                 folium.Marker(
#                     location=[station.latitude, station.longitude],
#                     popup=station.code,
#                 )
#             )
#
#         folium_map = folium.Map(
#             location=[statistics.mean(latitudes), statistics.mean(longitudes)],
#             zoom_start=5
#         )
#
#         for folium_marker in folium_markers:
#             folium_marker.add_to(folium_map)
#
#         # Output
#         if output_format == cls.FORMAT_DIV:
#             logger.info("Plot build as a <div>")
#             return folium_map._repr_html_()
#
#         else:
#             output_filename = 'plot_map_network_stations.html'
#             output_filepath = os.path.join(cls.output_dir(network, year), output_filename)
#             folium_map.save(output_filepath)
#             logger.info("Plot saved as %s" % output_filepath)
#             return output_filename
