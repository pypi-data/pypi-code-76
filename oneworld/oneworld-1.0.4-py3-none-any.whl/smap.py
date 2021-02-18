# Create a map, plot, points, ...
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.img_tiles import StamenTerrain, GoogleTiles, OSM
import cartopy.io.shapereader as shpreader
from matplotlib.transforms import offset_copy

from .utils import *
#
#
class StaticMap:
    """Base static map object.
    
    Parameters
    ----------
    position : tuple or None
               Position of the map inside the `figure` object, in figure
               relative coordinates (left, bottom, width, height), or None
               for full window map (Default: None).
    view : list or str
           Window span in coordinates 
           (longitude 1, longitude 2, latitude 1, latitude 2), or string
           indicating a predefined span (available predefined spans:
           "NC", "USA", "World") (Default: "USA").
    create_fig : bool
                 Create a new empty figure object when creating the map 
                 (Default: 'True').
    size : tuple
           Size of the figure in hundreds of pixels in (width, height) format
           (Default: (12, 9)).
    projection : str
                 Name of the projection to use. Standard `cartopy` projections
                 are supported (see
                 https://scitools.org.uk/cartopy/docs/latest/crs/projections.html)
                 plus the 'MercatorGoogle', 'MercatorStamen' and 
                 'OSM' tiles set (Default: 'PlateCarree').
    tiles_zoom : int
                 Level of tile zoom in case a projection with tiles is
                 selected (Default: 10).
    nation_borders : list or tuple or None
                     Sequence of strings of 3 characters, each string
                     representing the ISO 3166 country code for which
                     to plot the national borders, or None for no
                     national borders (Default: None).
    inner_borders : list or tuple or None
                    Sequence of strings of 3 characters, each string
                    representing the ISO 3166 country code for which
                    to plot the inner (regional) borders, or None for no
                    national borders (Default: None).
    pop_areas : list or tuple or None
                Sequence of strings of 3 characters, each string
                representing the ISO 3166 country code for which
                to plot the most populated areas (capitals, major cities
                and towns), or None for no
                national borders (Default: None).
    physical : str or None
               Add physical features to map. Currently supported features
               are: 'rivers' for river centerlines, 'lakes' to display
               lake areas, and 'rivers_na' and 'lakes_na' to display
               supplementary data for rivers and lakes in North America
               (Default: None).
    resolution : {'10m', '50m', '110m'}
                Resolution of nation and inner borders, populated areas
                and physical features when requested (Default: '110m').
    **kwargs
             Extra keyword arguments for the projection (see
             https://scitools.org.uk/cartopy/docs/latest/crs/projections.html)

    Attributes
    ----------
    position : tuple or None
               Position of the map inside the `figure` object, in figure
               relative coordinates (left, bottom, width, height), or None
               for full window map.
    view : list or str
           Window span in coordinates 
           (longitude 1, longitude 2, latitude 1, latitude 2), or string
           indicating a predefined span.
    create_fig : bool
                 Create a new empty figure object when creating the map.
    size : tuple
           Size of the figure in inches in (width, height) format.
    projection : str
                 Name of the projection used.
    tiles_zoom : int
                 Level of tile zoom in case a projection with tiles is
                 selected.
    nation_borders : list or tuple or None
                     Sequence of strings of 3 characters, each string
                     representing the ISO 3166 country code for which
                     to plot the national borders, or None for no
                     national borders.
    inner_borders : list or tuple or None
                    Sequence of strings of 3 characters, each string
                    representing the ISO 3166 country code for which
                    to plot the inner (regional) borders, or None for no
                    national borders.
    pop_areas : list or tuple or None
                Sequence of strings of 3 characters, each string
                representing the ISO 3166 country code for which
                to plot the most populated areas (capitals, major cities
                and towns), or None for no
                national borders.
    physical : str or None
               Add physical features to map.
    resolution : {'10m', '50m', '110m'}
                Resolution of nation and inner borders, populated areas
                and physical features when requested.
    fig : object
          Matplotlib figure object containing the map.
    ax : object
         Matplotlib axes object containing the map.
    data : object
           Pandas dataframe containing the last input data used in the map.
    lat_col : str
             Name of the column in `data` containing the latitude coordinates.
    lon_col : str
             Name of the column in `data` containing the longitude coordinates.
    text_col : str
               Name of the column in `data` containing the text to be 
               displayed.
    col_col : str
              Name of the column in `data` containing the values to be used
              to determine the color.
    siz_col : str
              Name of the column in `data` containing the values to be used
              to determine the size.
    col_def : bool
              Whether all the elements will have the same color property value.
    siz_def : bool
              Whether all the elements will have the same size property value.
    col_lst : list
              List containing the colors of the last input elements.
    col_leg : list
              List containing the entries of the color legend. Each entry
              consists of two elements: the label and the color in hex code.
    siz_lst : list
              List containing the sizes of the last input elements.
    siz_leg : list
              List containing the entries of the sizes legend. Each entry
              consists of two elements: the label and the corresponding size.
    sm : object
         Matplotlib Scalar Mappable object used for the last input data.
    """
    #
    def __init__(self, position = None, view = "USA", 
                 create_fig = True, size = (12,9),
                 projection = "PlateCarree", tiles_zoom = 10,
                 nation_borders = None, inner_borders = None, 
                 pop_areas = None, physical = None, resolution = '110m', 
                 **kwargs):
        """Constructor""" 
        self.position = position
        self.resolution = resolution
        self.view = view
        self.projection = projection
        self.nation_borders = nation_borders
        self.tiles_zoom = tiles_zoom
        self.inner_borders = inner_borders
        self.pop_areas = pop_areas
        self.physical = physical
        self.create_fig = create_fig, 
        self.size = size
        #
        # Create a figure object
        if create_fig:
            self.fig = plt.figure(figsize = self.size)
        # or get figure already created
        else:
            self.fig = plt.gcf()
        #
        # select projection
        if self.projection == "MercatorStamen":
            tiler = StamenTerrain(**kwargs)
            this_proj = tiler.crs
        #
        # Google kwargs: style='street','satellite', 'terrain' or 'only_streets'
        elif self.projection == "MercatorGoogle":
            tiler = GoogleTiles(**kwargs)
            this_proj = tiler.crs
        #
        # Open Street Map
        elif self.projection == "OSM":
            tiler = OSM(**kwargs)
            this_proj = tiler.crs
        #
        # Standard cartopy projections:
        else:
            this_proj = self.get_projection(self.projection, **kwargs)
        #
        # create world's self.axes in desired position inside fig if specified
        if self.position is not None:
            self.ax = plt.axes(position, projection = this_proj)
        else:
            self.ax = plt.axes(projection = this_proj)
        #
        # don't plot frame
        self.ax.outline_patch.set_visible(False)
        #
        # the view window
        coords_d = {"EC": [-80, -75, 33.5, 36.55],
                    "NC":[-85, -75, 33.5, 37],
                    "USA":[-125, -66.5, 20, 50],
                    "ESP":[-9, 4.2, 35, 45],
                    "World":[-179.99,179.99,-89.1,89.1]
                   }
        if isinstance(view, str):
            coords_lst = coords_d.get(view,[-179.99,179.99,-89.1,89.1])
        else:
            coords_lst = view
        self.ax.set_extent(coords_lst)#, crs = ccrs.PlateCarree()) # default is geodetic
        #
        # physical tiles if desired
        if projection in ["MercatorPhysic", "MercatorGoogle", "OSM"]:
            self.ax.add_image(tiler, self.tiles_zoom, 
                              interpolation = 'bicubic') #or 'spline36'
        #
        # Extra features to be added to the map
        if self.nation_borders is not None: self.plot_outter()
        if self.inner_borders is not None: self.plot_inner()
        if self.pop_areas is not None: self.plot_pop()
        if self.physical is not None: self.plot_physics()
    #
    def get_projection(self, proj, **kwargs):
        """Get the map projection.

        Given the name of the projection, return an instance of that
        projection.
  
        Parameters
        ----------
        proj : str
               Name of the projection (see
               https://scitools.org.uk/cartopy/docs/latest/crs/projections.html
               )
        **kwargs
                 Extra arguments for the projection.

        Returns
        -------
        object
               The projection object
        """
        proj_d = {"PlateCarree": ccrs.PlateCarree,
                  "AlbersEqualArea": ccrs.AlbersEqualArea,
                  "Mercator":ccrs.Mercator,
                  "AzimuthalEquidistant": ccrs.AzimuthalEquidistant,
                  "LambertConformal": ccrs.LambertConformal,
                  "LambertCylindrical": ccrs.LambertCylindrical,
                  "Miller": ccrs.Miller,
                  "Mollweide": ccrs.Mollweide,
                  "Orthographic": ccrs.Orthographic,
                  "Robinson": ccrs.Robinson,
                  "Sinusoidal": ccrs.Sinusoidal,
                  "Stereographic": ccrs.Stereographic,
                  "TransverseMercator": ccrs.TransverseMercator,
                  "InterruptedGoodeHomolosine": ccrs.InterruptedGoodeHomolosine,
                  "RotatedPole": ccrs.RotatedPole,
                  "Geostationary": ccrs.Geostationary,
                  "NearsidePerspective": ccrs.NearsidePerspective,
                  "Gnomonic": ccrs.Gnomonic,
                  "NorthPolarStereo": ccrs.NorthPolarStereo,
                  "SouthPolarStereo": ccrs.SouthPolarStereo,
                  "LambertAzimuthalEqualArea": ccrs.LambertAzimuthalEqualArea,
                  "Geodetic": ccrs.Geodetic
                  }
        #instantiate (don't fortget the parenthesis
        this_proj = proj_d[proj](**kwargs) 
        return this_proj
    #
    def plot_outter(self):
        """Plot the outter border for given countries.
        
        This method reads the elements in the attribute `nation_borders`
        and plots the national borders for each element on that list.
        Data for the borders is retrieved from the `natural earth`
        dataset http://www.naturalearthdata.com/.
        """
        # read shape file
        shpfilename = shpreader.natural_earth(resolution=self.resolution,
                                              category='cultural',
                                              name='admin_0_countries_lakes')
        reader = shpreader.Reader(shpfilename)
        countries = reader.records()
        # look for specified countries, add their geometries
        count_2plot = []
        for country in countries:
            if country.attributes['ADM0_A3'] in self.nation_borders:
                count_2plot.append(country.geometry)
        self.ax.add_geometries(count_2plot, ccrs.PlateCarree(),
                                      facecolor = cfeature.COLORS['land'],
                                      edgecolor = 'black')
        return
    #
    def plot_inner(self):
        """Plot the inner borders for given countries.
        
        This method reads the elements in the attribute `inner_borders`
        and plots the internal regional borders for each element on that list.
        Data for the borders is retrieved from the `natural earth`
        dataset http://www.naturalearthdata.com/.
        """
        # read shape file
        shpfilename = shpreader.natural_earth(resolution = self.resolution,
                                              category='cultural',
                                              name='admin_1_states_provinces_lakes')
        reader = shpreader.Reader(shpfilename)
        countries = reader.records()
        # look for specified countries, add their geometries
        count_2plot = []
        for country in countries:
            if country.attributes['adm0_a3'] in self.inner_borders:
                count_2plot.append(country.geometry)
        self.ax.add_geometries(count_2plot, ccrs.PlateCarree(),
                                      facecolor = cfeature.COLORS['land'],
                                      edgecolor = 'black')
        return
    #
    def plot_physics(self):
        """Add physical features to the map.

        Add each requested physical feature as defined in the attribute
        `physical`. Current supported features are: 'rivers' for river 
        centerlines, 'lakes' to display lake areas, and 'rivers_na' 
        and 'lakes_na' to display supplementary data for rivers and 
        lakes in North America. Features are retrieved from the
        `natural earth` dataset http://www.naturalearthdata.com/.
        """
        # available options
        xtras_d = {'rivers_na':      {'resolution':self.precision, 
                                      'name':'rivers_north_america',
                                      'edge_c':cfeature.COLORS['water'],
                                      'face_c':'none'},
                   'lakes_na' :      {'resolution':self.precision,
                                      'name':'lakes_north_america',
                                      'edge_c':'face',
                                      'face_c':cfeature.COLORS['water']},
                   'rivers':         {'resolution': self.precision,
                                      'name':'rivers_lakes_centerlines',
                                      'edge_c':cfeature.COLORS['water'],
                                      'face_c':'none'},
                   'lakes' :         {'resolution':self.precision, 
                                      'name':'lakes',
                                      'edge_c':'face',
                                      'face_c':cfeature.COLORS['water']}
                   }
        # get characteristics and read desired record
        for this_feat in self.physical:
            args_d = xtras_d[this_feat]
            shpfilename = shpreader.natural_earth(resolution=args_d['resolution'],
                                                  category='physical',
                                                  name=args_d['name'])
            reader = shpreader.Reader(shpfilename)
            countries = reader.records()
            count_2plot = []
            for country in countries:
                count_2plot.append(country.geometry)
            self.ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                                          facecolor = args_d['face_c'],
                                          edgecolor = args_d['edge_c'])
        return
    #
    def plot_pop(self):
        """Plot populated areas for given countries.

        Plot populated areas (capitals, major cities and towns) of the
        countries defined in the `pop_areas` attribute. 
        Data is retrieved from the
        `natural earth` dataset http://www.naturalearthdata.com/.
        """
        # read shapes
        pop_areas = shpreader.natural_earth(category='cultural',
                    name="populated_places", resolution = self.resolution)
        reader = shpreader.Reader(pop_areas)
        countries = reader.records()
        # look for desired countries
        for country in countries:
            if country.attributes['ADM0_A3'] in self.pop_areas:
                longi = country.attributes['LONGITUDE']
                latit = country.attributes['LATITUDE']
                self.ax.plot(longi, latit, marker='o', color='black', markersize=2,
                        alpha=1.0, transform=ccrs.Geodetic())
                # put text 10 or 5 pixels above and to the left of city mark
                geodetic_transform = ccrs.Geodetic()._as_mpl_transform(self.ax)
                text_transform = offset_copy(geodetic_transform, units='dots',
                                             y=10, x=-5)
                decoded_name = country.attributes['name_en'].decode("utf-8")
                self.ax.text(longi, latit, decoded_name,
                         verticalalignment='center',
                         horizontalalignment='right',
                         transform=text_transform)
        return
    #
    def add_txt(self, latitude, longitude, text, data = None, 
                x_offset = 10, y_offset = 10,
                crs = "Geodetic", box_kwargs = None,
                **kwargs):
        """Add text to the map.

        Given a set of coordinates and text, put said text in the map at
        a small offset of the coordinates. The reason behind the offset is
        that you can supply the coordinates of a named place, and plot
        text regarding that point in the map without the point covering
        the point itself. That offset can be nullified if desired.

        Parameters
        ----------
        latitude : list or tuple or str
                   Sequence (list or tuple) or name of the column of the
                   dataframe in `data` containing 
                   the longitude coordinate for the center of each circle. 
        longitude : list or tuple or str
                    Sequence (list or tuple) or name of the column of the
                    dataframe in `data` containing 
                    the latitude coordinate for the center of each circle.
        text : list or tuple or str
               Sequence (list or tuple) or name of the column of the
               dataframe in `data` containing 
               the text to be displayed.
        data : pandas DataFrame
               Dataframe containing one or more columns of values to use.
               Each row must contain the data for a circle, with columns
               as the data to be used (Default: None).
        x_offset : int
                    Offset of the text with regard to the longitude value
                    provided in the `longitude` parameter, in pixels
                    (Default: 10).
        y_offset : int
                    Offset of the text with regard to the latitude value
                    provided in the `latitude` parameter, in pixels
                    (Default: 10).
        crs : str
              Coordinate reference system on which `latitude` and 
              `longitude` are specified. See 
              https://scitools.org.uk/cartopy/docs/latest/crs/index.html for 
              a full list of supported crs (Default: 'Geodetic')
        box_kwargs : dict or None
                     Extra keyword arguments for the text box. See
                     https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.patches.FancyBboxPatch.html
                     for a list of supported arguments (Default: None)
        **kwargs : 
                   Extra arguments for the text plotting function. See
                   https://matplotlib.org/3.2.1/api/text_api.html#matplotlib.text.Text
                   for a list of supported arguments.
        """
        # if no dataframe is supplied, build it
        if data is None:
                self.data = pd.DataFrame(list(zip(latitude, longitude, text)),
                                    columns = ("Latitude", "Longitude", "Text"))
                self.lat_col = "Latitude"
                self.lon_col = "Longitude"
                self.text_col = "Text"
        else:
                self.data = data
                self.lat_col = latitude
                self.lon_col = longitude
                self.text_col = text
        # Etablish default parameters and replace them as demanded
        txt_kwargs = {'horizontalalignment':'left',
                            'verticalalignment':'center',
                            'fontsize':10, 'fontweight':'normal'},
        txt_kwargs.update(kwargs)
        # put text some pixels above and to the right of coordinates
        proj = get_projection(crs)
        geodetic_transform = proj._as_mpl_transform(self.ax)
        text_transform = offset_copy(geodetic_transform, units = 'dots',
                                         y = y_offset, x = x_offset)
        # Do it
        for (longi,latit), label in zip(self.data[self.lon_col],self.data[self.lat_col],self.data[self.text_col]):
            t = self.ax.text(longi, latit, label, transform=text_transform, **txt_kwargs)
            if box_kwargs is not None:
                t.set_bbox(**box_kwargs)
        return
    #
    def add_markers(self, latitude, longitude, size = 10, color = '#592a8a',
                    data = None, sizes = (5, 15),
                    n_colors = 5,
                    palette = "Spectral",
                    legend_pos = 'lower center', marker = 'o',
                    legend_labels = 4, legend_ndec = 2, crs = "Geodetic",
                    cap_min = False, cap_max = False,
                    legend_show = True,
                    legend_kwargs = {}, plt_kwargs = {}):
        """Add markers to the map.

        Location of markers can be specified via a sequence or a dataframe.
        Colors and sizes of markers can be specified in the same way, or
        using a single color and/or size which will be common to all markers.

        Parameters
        ----------
        latitude : list or tuple or str
                   Sequence (list or tuple) or name of the column of the
                   dataframe in `data` containing 
                   the longitude coordinate for each marker. 
        longitude : list or tuple or str
                    Sequence (list or tuple) or name of the column of the
                    dataframe in `data` containing 
                    the latitude coordinate for each marker. 
        size : list or tuple or str or int
               Sequence (list or tuple) or name of the column of the
               dataframe in `data` containing 
               the values that will be used to calculate the size of 
               each marker.  Alternatively, it can be a single
               numerical value, assigning the same size (in pixels)
               to all markers  (Default: 10).
        color : list or tuple or str 
                Sequence (list or tuple) or name of the column of the
                dataframe in `data` containing 
                the values that will be used to determine the color of each 
                marker. These values can be numeric (float or int) 
                or categorical (str). Alternatively, `color` can be a
                hex color that will be applied to all the markers
                (Default: '#592a8a').
        data : pandas DataFrame
               Dataframe containing one or more columns of values to use.
               Each row must contain the data for a marker, with columns
               as the data to be used (Default: None).
        sizes : list or tuple of 2 elements
                Only relevant if `size` is not int. Range of sizes (in pixels)
                to use for the markers (Default: (5, 15)). 
        palette : list or tuple or str
                  Only relevant when `color` is not a str corresponding
                  to a hex color. Sequence of hex colors to be used to
                  color the circles according to their value provided 
                  in `color`. Alternatively, `palette` can
                  be a string with the name of a `seaborn` color palette
                  https://seaborn.pydata.org/tutorial/color_palettes.html
                  (Default: 'Spectral').
        n_colors : int
                   Number of colors in the specified `seaborn` palette 
                   (Default: 5).
        marker : str
                 Shape of marker to use. See
                 https://matplotlib.org/3.2.1/api/markers_api.html
                 (Default: 'o').
        cap_min : float or int
                  If set, all numerical values less than this value will 
                  have the same characteristics (color, size, ...).
                  Ignored for categorical data (Default: False).
        cap_max : float or int
                  If set, all numerical values greater than this value will 
                  have the same characteristics (color, size, ...).
                  Ignored for categorical data (Default: False).
        legend_show : bool
                      If True, display a color and/or size legend
                      (Default: True).
        legend_labels : int or list or tuple
                        If int, number of points in the sizes legend 
                        (will be plotted as evenly separated values as 
                        possible), or seq containg the values to be displayed 
                        on the sizes legend. The color of the points on the 
                        legend will be that defined in color (Default: 4).
        legend_pos : {'best', 'upper right', 'upper left', 'lower left', \
                      'lower right', 'right', 'center left', 'center right', \
                      'lower center', 'upper center', 'center'}
                     Only relevant when `legend_show` is True.
                     Position of the legend (Default: 'lower center').
        legend_ndec : int
                      Only relevant when `legend_show` is True.
                      Number of decimal places to be displayed
                      on the legend (Default: 2).
        crs : str
              Coordinate reference system on which `latitude` and 
              `longitude` are specified. See 
              https://scitools.org.uk/cartopy/docs/latest/crs/index.html for 
              a full list of supported crs (Default: 'Geodetic').
        plt_kwargs : dict 
                     Dict with extra args to pass to the plot function
                     (Default: {}).
        leg_kwargs: dict
                    Dict with extra args to pass to the legend function
                    (Default: {}).
        """
        # set legend title to nothing
        legend_title = ''
        #
        # DATAFRAME
        # if no dataframe is provided, build it and store it as map attribute
        if data is None:
            # Global settings for no dataframe
            self.data = pd.DataFrame(list(zip(latitude, longitude)), 
                     columns = ("Latitude", "Longitude"))
            self.lat_col = "Latitude"
            self.lon_col = "Longitude"
            self.col_col = "Color"
            self.siz_col = "Size"
            # check data consistency
            if len(latitude) != len(longitude):
                raise ValueError("Latitude and longitude sizes do not match")
            else:
                ncoords = len(latitude)
            # check if color seq is given, or we use the default
            if isinstance(color, (list, tuple)):
                self.data[self.col_col] = color
                self.col_def = False
            else:
                self.data[self.col_col] = [color] * ncoords
                self.col_def = True
            # check if size seq is given, or we use the default
            if isinstance(size, (list, tuple)):
                self.data[self.siz_col] = size
                self.siz_def = False
            else:
                self.data[self.siz_col] = [size] * ncoords
                self.siz_def = True
        # dataframe provided
        else:
            # check data consistency
            if len(data[latitude]) != len(data[longitude]):
                raise ValueError("Latitude and longitude sizes do not match")
                return
            else:
                ncoords = len(data[latitude])
            # store as map attribute
            self.data = data
            self.lat_col = latitude
            self.lon_col = longitude
            # check if color column is given, or we use the default
            if color in self.data.columns:
                self.col_col = color
                self.col_def = False
            else:
                self.col_col = "Color"
                self.data[self.col_col] = [color] * ncoords
                self.col_def = True
            # check if size column is given, or we use the default
            if size in self.data.columns:
                self.siz_col = size
                self.siz_def = False
            else:
                self.siz_col = "Size"
                self.data[self.siz_col] = [size] * ncoords
                self.siz_def = True
        #
        # COLORS & SIZES
        if self.col_def:
            self.col_lst = self.data[self.col_col]
            self.col_leg = None
        else:
            self.col_lst, self.col_leg, self.col_cat, self.sm = get_hexes(self.data[self.col_col], palette, n_colors, cap_min, cap_max, legend_ndec)
        if self.siz_def:
             self.siz_lst = self.data[self.siz_col]
             self.siz_leg = None
        else:
            self.siz_lst, self.siz_leg = get_sizes(self.data[self.siz_col], sizes, legend_labels, cap_min, cap_max, legend_ndec)
        #
        # LEGEND(S)
        if self.siz_def and self.col_def : legend_show = False
        if legend_show:
            self.add_legend(marker, legend_pos, plt_kwargs, legend_kwargs)
        #
        # PLOT
        # prepare the zipped list
        zipped = zip(self.data[self.lon_col], self.data[self.lat_col], 
                     self.col_lst, self.siz_lst)
        # get coord ref system
        proj = self.get_projection(crs)
        # loop through coordinates and plot each point
        for longi, latit, this_color, this_size in zipped:
            self.ax.plot(longi, latit, 
                         color = this_color, 
                         markersize = this_size,
                         transform = proj,  marker = marker, **plt_kwargs)
        #
        return
    #
    def add_legend(self, marker, legend_pos, plt_kwargs, legend_kwargs):
        """Add a legend to the map.

        The added legend will contain information regarding the last data
        input. This method is called automatically when the `legend_show`
        parameter is set to True.

        Parameters
        ----------
        marker : str
                 Shape of marker to use. See
                 https://matplotlib.org/3.2.1/api/markers_api.html
        legend_pos : {'best', 'upper right', 'upper left', 'lower left', \
                      'lower right', 'right', 'center left', 'center right', \
                      'lower center', 'upper center', 'center'}
                     Only relevant when `legend_show` is True.
                     Position of the legend (Default: 'lower center').
        plt_kwargs : dict 
                     Dict with extra args to pass to the plot function
                     (Default: {}).
        leg_kwargs: dict
                    Dict with extra args to pass to the legend function
                    (Default: {}).       
        
        See also
        --------
        add_colorbar
        """
        title = ''
        markers = []
        labels = []
        # Establish position outside of map WARNING! Varies with tight_layout
        posdict = {"upper": 1.1, "lower": -0.2, "center": 0.5, "left": -0.2,
                   "right": 1.01}
        words = legend_pos.split()
        bbox = [posdict[words[1]], posdict[words[0]]]
        # set orientation
        if words[1] != "center":
            orient = "vertical"
        else:
            orient = "horizontal"
        # set default size and color
        size = 10
        if not self.col_def and not self.siz_def:
            color = 'black'
        else:
            color = self.col_lst[0]
        #
        # Colors legend
        if not self.col_def:
            # if we also have sizes legend and legend in vertical porition
            if not self.siz_def and orient == "vertical":
                # put column name on top of color legend 
                li, = plt.plot([],[], '-', color = 'none')
                markers.append(li)
                labels.append(r"$\bf{"+"\ ".join(self.col_col.strip().split())+"}$")
            # set color part of legend
            for this_label, this_color in self.col_leg:
                li, = plt.plot([],[], marker, 
                           markersize = size, color = this_color, **plt_kwargs)
                markers.append(li)
                labels.append(this_label)
            # set title
            title = self.col_col
        #
        # Sizes legend
        if not self.siz_def:
            # if we also have color legend and legend in vertical portion
            if not self.col_def and orient == "vertical":
                # add column name as title for size part
                li, = plt.plot([],[], '-', color = 'none')
                markers.append(li)
                labels.append(r"$\bf{"+"\ ".join(self.siz_col.strip().split())+"}$")
            # set size part of the legend
            for this_label, this_size in self.siz_leg:
                li, = plt.plot([],[], marker, markersize = this_size,
                               color = color, **plt_kwargs)
                markers.append(li)
                labels.append(this_label)
            # set title
            title = self.siz_col
        # no global legend title if both legends are plotted
        if not self.siz_def and not self.col_def: title = ''
        if orient == "vertical":
            ncol = 1
        else:
            ncol = len(labels)
        #
        # Set Default settings, update them accordingly with user demands
        kwargs = {"ncol": ncol, 'bbox_to_anchor': bbox, "loc": legend_pos,
                  "frameon": False, "scatterpoints": 1, "fontsize": 12,
                  "title": title}
        kwargs.update(legend_kwargs)
        # Plot
        leg = self.ax.legend(markers, labels, **kwargs)
        # Legend title with same fontsize as legend entries
        plt.setp(leg.get_title(), fontsize = kwargs["fontsize"])
        # Add the legend artist separately in case there are multiple legends
        self.ax.add_artist(leg)
        #
        return
    #
    def add_choropleth(self,shp_file, geoid, color, data = None, 
                       shp_key = "GEOID",
                       crs = "PlateCarree", palette = "YlOrRd", 
                       n_colors = 10, cap_max = False, 
                       cap_min = False, legend_show = True,
                       legend_pos = "lower center", legend_orient = 'vertical',
                       legend_ndec = 2, 
                       **kwargs):
        """Add a choropleth to the map.

        Polygons representing areas must be supplied via a shapefile.
        Colors of polygons can be specified using a sequence containing
        the values to be used to determine color or a dataframe.
        For each value
        in `color` there should be a value in `geoid`, which will be used
        to identidfy the corresponding polygon in the shapefile. The
        algorithm will look for such values in the `shp_key` attribute
        of the shapefile.

        Parameters
        ----------
        shp_file : str
                    Full path name of the shapefile.
        geoid : list or tuple or str
                Sequence (list or tuple) or name of the column of the
                dataframe in `data` containing
                the `string` that will be used to identify each polygon
                on the `shp_file`.
        color : list or tuple or str 
                Sequence (list or tuple) or name of the column of the
                dataframe in `data` containing 
                the values that will be used to determine the color of each 
                polygon. These values can be numeric (float or int) 
                or categorical (str). 
        data : pandas DataFrame
               Dataframe containing one or more columns of values to use.
               Each row must contain the data for a polygon, with columns
               as the data to be used (Default: None).
        shp_key : str
                   Name of the attribute
                   that will be used to identify each polygon (Default: 
                   "GEOID").
        palette : list or tuple or str
                  Sequence of hex colors to be used to
                  color the polygons according to their value provided 
                  in `color`. Alternatively, `palette` can
                  be a string with the name of a `seaborn` color palette
                  https://seaborn.pydata.org/tutorial/color_palettes.html
                  (Default: 'Spectral').
        n_colors : int
                   Number of colors in the specified `seaborn` palette 
                   (Default: 5).
        cap_min : float or int
                  If set, all numerical values less than this value will 
                  have the same color.
                  Ignored for categorical data (Default: False).
        cap_max : float or int
                  If set, all numerical values greater than this value will 
                  have the same color.
                  Ignored for categorical data (Default: False).
        legend_show : bool
                      If True, display a color legend
                      (Default: True).
        legend_pos : {'best', 'upper right', 'upper left', 'lower left', \
                      'lower right', 'right', 'center left', 'center right', \
                      'lower center', 'upper center', 'center'} or
                      list or tuple
                     Position of the colorbar. Can be one of the predefined
                     positions, or a list or tuple of figure relative
                     coordinates (x, y, width, height) 
                     Only relevant when `legend_show` is True.
                     (Default: 'lower center').
        legend_orient : {'horizontal', 'vertical'}
                        Only relevant when `legend_pos` is a list or tuple
                        containing coordinates and dimensions of the colorbar.
                        Orientation of the colorbar (Default: 'vertical')
        legend_ndec : int
                      Only relevant when `legend_show` is True.
                      Number of decimal places to be displayed
                      on the legend (Default: 2).
        crs : str
              Coordinate reference system on which polygon geometries
              are specified. See 
              https://scitools.org.uk/cartopy/docs/latest/crs/index.html for 
              a full list of supported crs (Default: 'PlateCarree').
        **kwargs : 
                   Extra arguments for the plotting function.

        See also
        --------
        add_shp
        """
        # if no dataframe is supplied, build it
        if data is None:
            self.data = pd.DataFrame(list(zip(geoid, color)), 
                                     columns = ("Geoids", "Color"))
            geoid = "Geoids"
            self.col_col = "Color"
        else:
            self.data = data
            self.col_col = color
        # color cannot be default color
        self.col_def = False
        # get list of colors
        self.col_lst, self.col_leg, self.col_cat, self.sm = get_hexes(self.data[self.col_col], palette, n_colors, cap_min, cap_max, legend_ndec)
        # add values to dataframe
        self.data["hue"] = self.col_lst
        # load shape file
        reader = shpreader.Reader(shp_file)
        # get full list (Note: convert to list so we can iterate multiple times)
        shapes = list(reader.records())
        # get projection
        proj = self.get_projection(crs)
        # Get geoids of each color
        for this_label, this_color in self.col_leg:
            geoids_lst = list(self.data.loc[self.data["hue"] == this_color, geoid])
            # get shapes geometry
            shps_lst = []
            for this_shp in shapes:
                if this_shp.attributes[shp_key] in geoids_lst:
                    shps_lst.append(this_shp.geometry)
            self.ax.add_geometries(shps_lst, proj, facecolor = this_color,
                              **kwargs)
        #
        # The dreaded Colorbar
        if legend_show:
            self.add_colorbar(legend_pos, cap_min, cap_max, legend_orient)
        # enough
        return
    #
    def add_colorbar(self, legend_pos = 'lower center',
                     cap_min = False, cap_max = False, cb_orient = 'vertical'):
        """Add a colorbar to the map.

        The added colorbar will contain information regarding the last data
        input. This method is called automatically when the `legend_show`
        parameter is set to True.

        Parameters
        ----------
        legend_pos : {'best', 'upper right', 'upper left', 'lower left', \
                      'lower right', 'right', 'center left', 'center right', \
                      'lower center', 'upper center', 'center'} or
                      list or tuple
                     Position of the colorbar. Can be one of the predefined
                     positions, or a list or tuple of figure relative
                     coordinates (x, y, width, height) 
                     Only relevant when `legend_show` is True.
                     (Default: 'lower center').
        cb_orient : {'horizontal', 'vertical'}
                    Only relevant when `legend_pos` is a list or tuple
                    containing coordinates and dimensions of the colorbar.
                    Orientation of the colorbar (Default: 'vertical')
        cap_min : float or int
                  If set, all numerical values less than this value will 
                  have the same color.
                  Ignored for categorical data (Default: False).
        cap_max : float or int
                  If set, all numerical values greater than this value will 
                  have the same color.
                  Ignored for categorical data (Default: False).

        See also
        --------
        add_legend
        """
        self.sm._A = []
        # Determine legend placement
        if isinstance(legend_pos, str):
            posdict = {"upper": 0.4, 
                       "lower": 0.05, 
                       "center": 0.25, 
                       "left": 0.05,
                        "right": 0.90}
            words = legend_pos.split()
            # determine horizontal or vertical
            if words[1] != "center":
                width = 0.05
                height = 0.5
                cborient = "vertical"
            else:
                width = 0.5
                height = 0.05
                cborient = "horizontal"
            # Determine axes that contain legend:[x0,y0,width,height] rel to fig
            cbrect = [posdict[words[1]], posdict[words[0]], width, height]
        else:
            cbrect = legend_pos
            cborient = cb_orient
        # Create axes for colorbar legend at desired position (rel to fig)
        cbaxes = self.fig.add_axes(cbrect)
        #
        # Create the colorbar
        cbar = plt.colorbar(self.sm, cax = cbaxes, orientation = cborient)
        #
        # Tick marks (and labels)
        if not self.col_cat:
            # numerical data: ticks at end of interval
            barticks = [x.split(" - ")[1] for x,y in self.col_leg]
            # add first tick and get num values
            barticks.insert(0, self.col_leg[0][0].split(" - ")[0])
            barticks_nocomma = [x.replace(",", "") for x in barticks]
            barticksvalue = [float(x) for x in barticks_nocomma]
            # set first and last tick val = to sm limits (avoid round err)
            barticksvalue[0] = self.sm.get_clim()[0]
            barticksvalue[-1] = self.sm.get_clim()[-1]
            bartickslabel = barticks
            # change the tick labels so they display the '<=' and ">=" signs
            if cap_min != False:
                bartickslabel[0] = r'$\leq$'+bartickslabel[0]
            if cap_max != False:
                bartickslabel[-1] = r'$\geq$'+bartickslabel[-1]
        else:
            # categorical data
            barticksvalue = []
            ncat = len(self.col_leg)
            # ticks at half the inerval
            for i in range(ncat):
                this_tick = i*1.0/ncat+1.0/(2.0*ncat)
                barticksvalue.append(this_tick)
            bartickslabel = [x for x,y in self.col_leg]
        # set tick and ticklabels
        cbar.set_ticks(barticksvalue)
        cbar.set_ticklabels(bartickslabel)
        cbar.update_ticks()
        # colorbar title
        cbaxes.set_title(self.col_col)
        # set the plot (not colorbar) axes as current axes 
        plt.sca(self.ax)
        #
        return
    #
    def add_shp(self, shp_file, subset = None, subset_key = "GEOID",
                color = cfeature.COLORS['land'],
                crs = "PlateCarree", **kwargs):
        """Add polygons from a shapefile.

        All polygons on the shapefile will have the same characteristics.
        Alternatively, a subset of polygons matching a certain criteria
        can be selected for plotting, leaving the rest unplotted. If set,
        only those polygons which `subset_key` attribute value
        matches that specified in `subset` will be added to the map.

        Parameters
        ----------
        shp_file : str
                    Full path name of the shapefile.
        subset : str or None
                 If set,
                 only those polygons which `subset_key` attribute value
                 matches that specified in `subset` will be added to the map
                 (Default: None).
        subset_key : str
                     Attribute that will be used to identify which polygons
                     to plot, in case `subset` is defined (Default: "GEOID").
        color : str
                Color of the area of the polygons (Default: '#efefdb').
        crs : str
              Coordinate reference system on which polygon geometries
              are specified. See 
              https://scitools.org.uk/cartopy/docs/latest/crs/index.html for 
              a full list of supported crs (Default: 'PlateCarree').
        kwargs :
                 Extra arguments for the plotting funtcion.

        See also
        --------
        add_choropleth
        """
        # load shape file
        reader = shpreader.Reader(shp_file)
        shapes = reader.records()
        # Gather all geometries
        if subset is None:
            shapes_lst = [shp.geometry for shp in shapes]
        # or only a subset of the geometries
        else:
            shapes_lst = []
            for this_shp in shapes:
                if this_shp.attributes[subset_key] == subset:
                    shapes_lst.append(this_shp.geometry)
        # get coord ref system
        proj = self.get_projection(crs)
        # plot each and all shapes from shapefile
        self.ax.add_geometries(shapes_lst, proj, facecolor = color, **kwargs)
        #
        return
    #
    def savemap(self, filename, tight = True):
        """Save the map to a file.

        Parameters
        ----------
        filename : str
                   Name of the file (including extension) where the map
                   will be saved.
        tight : bool
                Request a tight layout or not (Default: True).
        """
        if tight:
            self.fig.canvas.draw()
            plt.tight_layout()
        plt.savefig(filename)
