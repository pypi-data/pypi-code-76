# -*- coding: utf-8 -*-
"""create interactive web maps"""
from jinja2 import Environment, PackageLoader
import base64
import codecs
import json
import copy as cp
import textwrap as tw
#
from .utils import *
from .web_classes import *
#
class WebMap:
    """Base interactive map object.
    
    Parameters
    ----------
    scale : bool
            Show a scale (Default: 'True').
    title : str
            String to be displayed on the navigation bar (Default: 'OneWorld').
    **kwargs 
            All other keyword arguments as accepted by the `Map` object in 
            leaflet (see https://leafletjs.com/reference-1.6.0.html#map-option).

    Attributes
    ----------
    options : dict
              Attribute containing the optional kwargs of the Map object.
    scale : bool
            Whether to include a scale on the map or not.
    title : str
            Title of the map.
    layercontrol : object or None
                   If added to the map this will store the Layercontrol object.
    circles : list or None
              List of all the Circle objects added to the map.
    lines : list or None
            List of all the Line objects added to the map.
    styles : dict of dicts
             Dictionary with names of styles as keys and style dictionaries
             as values.
    basemaps : list
               List of Basemap objects added to the map.
    overlays : list
               List of Overlay objects added to the map.
    panel : object or None
            Container for the Panel object, if added to the map.
    box : object or None
          Container for the Box object, if added to the map.
    graph : bool or None
            Will be set to True when a network is added to the map.
    layers : list
             Created when calling the savemap method, this will contain
             the names of all basemaps and overlays in the map.
    logo : object or None
           Container for the Logo object when added to the map.
    geojson : list
              List of Geojson objects added to the map.
    colorbar : list
               List of Colorbar objects added to the map.
    heatmap : object or None
              Container for the Heatmap object, if added to the map.
    """

    def __init__(self, scale = True, title = "OneWorld", **kwargs):
       """Contructor method. Create the world. Well, the map of the world"""
       self.options = kwargs
       self.scale = scale
       self.title = title
       self.layercontrol = None
       self.circles = None
       self.lines = None
       self.styles = {}
       self.basemaps = []
       self.overlays = []
       self.panel = None
       self.box = None
       self.graph = None
       self.layers = []
       self.logo = None
       self.geojson = []
       self.colorbar = []
       self.heatmap = None
#
    def savemap(self, outfile = 'test.html'):
        """Create the file containing the map.
        
        Print a text file that can be opened with an internet connected 
        browser, which will display the map (usually this goes at the end of 
        the script). If no basemap has been added to the map at the time this 
        method is executed, it will add a default basemap.

        Parameters
        ----------
        outfile : str
                  Name of the output file (Default: 'test.html').
        """
        # check if a basemap was added. If not, add a default one
        if not self.basemaps:
            self.add_basemap()
        # network needs this
        self.layers = []
        for i_layer in self.basemaps:
            self.layers.append(i_layer.name)
        for i_layer in self.overlays:
            self.layers.append(i_layer.name)
        #
        env = Environment(loader=PackageLoader('oneworld', 'templates'))
        template = env.get_template('world.html')
        template.stream(pymap = self).dump(outfile)
#
    def add_basemap(self, name = 'StreetMap', tiles = 'OSM', source = '',
                    **kwargs):
        """Add a basemap.
        
        Add a layer to the map object that contains a basemap. A basemap
        consists of tiles, which are the image that will be displayed on the
        background of the web navigator (containing administrative borders,
        physical features, ...). No more than one basemap can be active 
        at any given time.
        
        Parameters
        ----------
        name : str
               Name of the basemap layer. It is also the string that will be
               displayed in a layer control panel in case it is added
               (Default: 'StreetMap').
        tiles : {'OSM', 'OSM_BW', 'Stamen_toner', 'Stamen_terrain', \
                 'Stamen_watercolor', 'ESRI_SAT'}
                Tiles to use on the basemap (Default: 'OSM').
        source : str
                 String to be displayed at the bottom right corner of the
                 window, prefixed by "Source:" (by default, only tile 
                 attributions wiil be displayed).
        **kwargs 
                 All other keyword arguments as accepted by the tileLayer 
                 object in leaflet.
                 (see https://leafletjs.com/reference-1.4.0.html#tilelayer-option)
        
        Warnings
        --------
        If a dataframe is used in any of the other methods, the `name` of the
        basemap cannot coincide with the name of any of the columns of the
        dataframe.
        """
        name_short = clean_string(name)
        self.basemaps.append(Basemap(name_short, name, tiles, source, kwargs))
#    
    def add_overlay(self, name, show_start = True, show_panel = True,
                    alwaysontop = False):
        """Add an overlay layer.

        Add a layer to the map object that contains an overlay. Overlays
        are transparent by default unless they are populated with other
        elements (such as panels, markers, ...) so its only purpose is to serve
        as a container for other element of the map. Overlays stack on top 
        of the active basemap and on top of each other, unless deactivated 
        in the layer control panel (more than one overlay layer can be active
        at a time).

        Parameters
        ----------
        name : str
               Name of the overlay layer. It is also the string that will be
               displayed in a layer control panel in case it is added.
        show_start : bool
                     If True, the overlay will be active on map load
                     (Default: True)
        show_panel : bool
                     If False, its name will never appear in any control layer 
                     panel. This means that it will not be possible to 
                     activate it or deactivate it, it will stay as 
                     show_start defined (Default: True).
        alwaysontop : bool
                      If True, the overlay will always be the top layer, 
                      even when changing active layers through a layer control 
                      (useful for example when mixing markers and choropleths)
                      (Default: False).

        Warnings
        --------
        If a dataframe is used in any of the other methods, the `name` of the
        overlay cannot coincide with the name of any of the columns of the
        dataframe.
        """
        name_short = clean_string(name)
        self.overlays.append(Overlay(name_short, name, show_start, show_panel,
                                     alwaysontop))
#
    def add_layer_control(self, position = 'topright', collapsed = True, 
                                autoindex = True, hidesinglebase = True):
        """Add a layer control panel.

           Basemap names will appear by order of creation (top to bottom), 
           and will have radio buttons (only one basemap active at a time). 
           Overlay names will appear by order of creation (top to bottom), 
           with check boxes (multiple overlays active at the same time 
           possible).

           Parameters
           ----------
           position : {'topleft', 'topright', 'bottomleft', 'bottomright'}
                      Position of the panel in the map (Default: 'topright').
           collapsed : bool
                       If True, the panel will be colapsed on map load and 
                       will expand on mouse over (Default: True).
           autoindex : bool
                       If True, displays layers on the panel 
                       by order of creation (top to bottom) (Default: True).
           hidesinglebase : bool   
                            If True, hide the basemap layer from the control 
                            if there is only one single basemap
                            (Default: True).
        """
        self.layercontrol = Layercontrol(position = position, 
                                         collapsed = collapsed,
                                         autoindex = autoindex,
                                         hidesinglebase = hidesinglebase)
#
    def add_panel(self, title = None, lines = None, noinfo = ' ', 
                        position = 'topright', width = None, height = None):
        """Add an information panel.

           The indormation to be displayed will be passed by the different 
           events on the different elements created in the map, if defined
           when adding those elements to the map.

           Parameters
           ----------
           title : str
                   Title on top of the panel. Will always be visible. 
                   Displayed in bold font (Default: None).

           noinfo : str
                    Text to be displayed in case there is no info passed to 
                    the panel (when no event is triggered). (Default: ' ').
           position : {'topleft', 'topright', 'bottomleft', 'bottomright'}
                       Position of the panel in the map (Default: 'topright').
           width : str
                   When set, fixed width of the panel.
                   Must also include units (e.g. '10px', '25%').
                   If not set (i.e. set to None), 
                   panel will dinamically adjust its 
                   dimensions to accomodate text to be displayed
                   (Default: None). 
           height : str
                    When set, fixed height of the panel.
                    Must also include units (e.g. '10px', '25%').
                    If not set (i.e. set to None), 
                    panel will dinamically adjust its
                    dimensions to accomodate text to be displayed
                    (Default: None). 
        """
        self.panel = Panel(title = title, noinfo = noinfo,
                           position = position, width = width, height = height)
#
    def add_box(self, contents = None, position = 'topright'):
        """Add a box that with static content.
           
           Parameters
           ----------
           contents : str
                      contents to be displayed on the box (in html format)
                      (Default: None).
           position : {'topleft', 'topright', 'bottomleft', 'bottomright'}
                       Position of the box in the map (Default: 'topright').
        """
        self.box = Box(contents = contents, position = position)
#
    def add_logo(self, source, position = 'bottomleft', width = None, 
                 embed = True):
        """Add a static image from a file.
        
           Parameters
           ----------
           source : str
                    String containing the full path (including the file name)
                    to the image file.
           position : {'topleft', 'topright', 'bottomleft', 'bottomright'}
                       Position of the image in the map 
                       (Default: 'bottomleft').
           width : int
                   Desired width in pixels of the watermark. 
                   If None, it will be handled
                   automatically by the browser (Defalt: None).
           embed : bool
                    If True, the image will be encoded to base64 and 
                    embedded into the final html file. If not, only the 
                    reference to the file will be included in the html file
                    (Default: True).
        """
        if embedd:
            # open file and convert it to  base64
            with open(source) as fp:
                src_str = base64.b64encode(fp.read())
            src_str = "data:image/png;base64,"+src_str
        else:
            src_str = source
        self.logo = Logo(source = src_str, position = position, width = width)
#
    def add_circles(self, latitude, longitude, size = None, color = '#592a8a',
                    data = None, sizes = None,
                    palette = "Spectral",
                    n_colors = 5,
                    cap_min = False, cap_max = False,
                    layer = "map",
                    style = {'opacity':1.0, 'fillOpacity':0.6},
                    style_mouseover = None,
                    info_mouseover = None,
                    constant_size = False,
                    legend_pos = "bottomright",
                    legend_ndec = 2,
                    _connect_over = None):
   
        if self.circles is None: self.circles = []
        # default sizes
        if sizes is None: 
            if not constant_size:
                sizes = (1000, 10000)
            else:
                sizes = (1, 20)
        if size is None: 
            if not constant_size:
                size = 1000
            else:
                size = 10
        # establish coordinates list
        if data is not None:
            coords = [list(x) for x in zip(data[latitude], data[longitude])]
        elif (isinstance(latitude, (list, tuple)) 
              and isinstance(longitude, (list, tuple))):
            coords = [list(x) for x in zip(latitude, longitude)]
        else:
            coords = [[latitude, longitude]]
        ncircles = len(coords)
        # retrieve input data as lists
        color_l, size_l, layer_l, info_l = self._listomania(color, size, 
                                   layer, info_mouseover, data, ncircles,
                                   palette, n_colors, sizes, cap_min, cap_max,
                                   legend_pos, legend_ndec)      
        if constant_size:
            size_l = [int(x) for x in size_l]
        # loop circles
        indx_l = [x for x in range(ncircles)]
        zipped_lst = zip(coords, color_l, size_l, layer_l, info_l, indx_l)
        for i_coords, i_color, i_size, i_layer, i_info, i_indx in zipped_lst:
            i_style = {'fillColor': i_color, 'color': i_color, 'radius': i_size}
            i_style.update(style)
            style_name = self._get_style_name(i_style)
            events = self._create_events(style_mouseover, i_info, 
                                         _connect_over, i_layer)
            # create and store circle objects
            thiscircle = Circle(coords = i_coords, 
                                style = style_name,
                                layer = i_layer, 
                                events = events,
                                ctant_r = constant_size,
                                nodeindex = i_indx)
            self.circles.append(thiscircle)
#
    add_circles.__doc__ = tw.dedent("""\
        Add circles in specific locations.

        Input can be in the form of a pandas dataframe, or in lists or tuples,
        or a combination of both. The color and the size of each circle
        can be associated to the value of a variable (set in the `color`
        and `size` parameters). In the case of color, this variable
        can contain numeric or categorical data. Check out the tutorial.

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
        size : list or tuple or str or int
               Sequence (list or tuple) or name of the column of the
               dataframe in `data` containing 
               the values that will be used to calculate the radius of 
               each circle.  Alternatively, it can be a single
               numerical value, assigning the same radius to all the circles
               (in pixels if `constant_size` is True, in meters otherwise)
               (Default: 1000 for 
               `constant_size` = False, 10 for `constant_size` = True).
        color : list or tuple or str 
                Sequence (list or tuple) or name of the column of the
                dataframe in `data` containing 
                the values that will be used to determine the color of each 
                circle. These values can be numeric (float or int) 
                or categorical (str). Alternatively, `color` can be a
                hex color that will be applied to all the circles 
                (Default: '#592a8a').
        data : pandas DataFrame
               Dataframe containing one or more columns of values to use.
               Each row must contain the data for a circle, with columns
               as the data to be used (Default: None).
        sizes : list or tuple of 2 elements
                Only relevant if `size` is not int. Range of sizes to use 
                as radius for the circles 
                (in pixels if `constant_size` is True, in meters otherwise)
                (Default: (1000, 10000) if `constant_size` = False, (1, 20) 
                otherwise).
        palette : list or tuple or str
                  Only relevant when `color` is not a str corresponding
                  to a hex color. Sequence of hex colors to be used to
                  color the circles according to their value provided 
                  in `color`. Alternatively, `palette` can
                  be a string with the name of a `seaborn` color palette
                  (Default: 'Spectral').
        n_colors : int
                   Number of colors in the specified `seaborn` palette 
                   (Default: 5).
        cap_min : float or int
                  If set, all circles with a numerical value in `color` smaller 
                  than the value set in `cap_min` will be considered as having
                  a value equal to `cap_min` for coloring purposes. The 
                  corresponding entry in the legend will display a '<' sign.
                  (Default: False).
        cap_max : float or int
                  If set, all circles with a numerical value in `color` greater 
                  than the value set in `cap_max` will be considered as having
                  a value equal to `cap_max` for coloring purposes. The 
                  corresponding entry in the legend will display a '>' sign.
                  (Default: False).
        layer : list or tuple or str 
                Sequence (list or tuple) or name of the column of the
                dataframe in `data` containing 
                the name of the layer on which to draw each circle. 
                Alternatively, it can be the name of a single layer on which
                all the circles will be added. If the specified layer has not 
                yet been created, `oneworld` will create an overlay with
                that name using the default  settings (Default: "map", which 
                will add the circles directly to the map object).
        style : dict
                Dictionary containing keywords and values defining common
                style values for all circles. Note that the 'color', 
                'fillColor' and 'radius' keywords defined in `style` 
                will override those  in the `color` and `size` 
                parameters (Default:
                {'opacity':1.0, 'fillOpacity':0.6}).
        style_mouseover : dict
                          If set, style of the circles when the mouse is
                          hovered over a circle (Default: None).
        info_mouseover : list or tuple or str 
                         If set, sequence (list or tuple) or name of the column
                         of the  dataframe in `data` containing
                         the information to be displayed on a pannel when
                         the mouse is hovered over the circle. Accepts
                         html format (Default: None).
        constant_size : bool
                        If True, circles will have the same size regardless 
                        of zoom level (Default: False).
        legend_pos : {'topleft', 'topright', 'bottomleft', 'bottomright', None}
                     Only relevant when `color` is not a str corresponding
                     to a hex color. Position of the color legend, or None
                     for no legend (Default: "bottomright").
        legend_ndec : int
                     Only relevant when `color` is not a str corresponding
                     to a hex color. Number of decimal places to be displayed
                     on the color legend (Default: 2)

        Notes
        -----
        For available color palettes, see
        https://seaborn.pydata.org/tutorial/color_palettes.html

        For a full listing of style options, see 
        https://leafletjs.com/reference-1.6.0.html#path

        Examples
        --------
        To plot the points in the "conferences" dataset using the "Conference"
        column to color each circle, with a constant size for each circle
        of 10 pixels regardless of the zoom level we can proceed as follows:

        >>> import oneworld as ow
        >>> df = ow.load_dataset("conferences")
        >>> mymap = ow.WebMap(center = [39,-96.8], zoom = 4) 
        >>> mymap.add_circles(latitude = 'Lat', longitude = 'Long', data = df,
        ...                   color = "Conference", size = 10, 
        ...                   constant_size = True)

        The resulting map is

        .. raw:: html

            <iframe src="../_static/doc_points1.html" height="345px" width="100%"></iframe>

        """)

#
    def add_lines(self, latitude0, longitude0, latitude1, longitude1,
                    size = 3, color = '#592a8a',
                    data = None, sizes = (3,15),
                    n_colors = 5,
                    palette = "Spectral",
                    cap_min = False, cap_max = False,
                    layer = "map",
                    style = {'opacity':1.0, 'fillOpacity':0.6},
                    style_mouseover = None,
                    info_mouseover = None,
                    legend_pos = "bottomright",
                    legend_ndec = 2,
                    _source = None, _target = None):
        if self.lines is None: self.lines = []
        # establish coordinates list
        if (isinstance(latitude0, (list, tuple)) 
            and isinstance(longitude0, (list, tuple)) 
            and isinstance(latitude1, (list, tuple)) 
            and isinstance(longitude1, (list, tuple))):
            # coords as seqs
            coords0 = [list(x) for x in zip(latitude0, longitude0)]
            coords1 = [list(x) for x in zip(latitude1, longitude1)]
            coords = [list(x) for x in zip(coords0, coords1)]
        elif (data is not None 
            and latitude0 in data.columns 
            and longitude0 in data.columns):
            # coords as dataframe name of columns
            coords0 = [list(x) for x in zip(data[latitude0], data[longitude0])]
            coords1 = [list(x) for x in zip(data[latitude1], data[longitude1])]
            coords = [list(x) for x in zip(coords0, coords1)]
        else:
            # single line
            coords = [[latitude0, longitude0],[latitude1, longitude1]]
        nlines = len(coords)
        # retrieve input data as lists
        color_l, size_l, layer_l, info_l = self._listomania(color, size, 
                                   layer, info_mouseover, data, nlines,
                                   palette, n_colors, sizes, cap_min, cap_max,
                                   legend_pos, legend_ndec)
        # loop lines
        if _source is None: _source = [None] * nlines
        if _target is None: _target = [None] * nlines
        zipped_lst = zip(coords, color_l, size_l, layer_l, info_l, 
                        _source, _target)
        for i_coords, i_colr, i_siz, i_lay, i_inf, i_src, i_trg in zipped_lst:
            i_style = {'color': i_colr, 'weight': i_siz}
            i_style.update(style)
            style_name = self._get_style_name(i_style)
            events = self._create_events(style_mouseover, i_inf, None, None)
            # create and store line object
            thisline = Line(i_coords, style_name, i_lay, events, 
                            i_src, i_trg)
            self.lines.append(thisline)
#
    add_lines.__doc__ = tw.dedent("""\
        Add lines connecting specific locations.

        Input can be in the form of a pandas dataframe, or in lists or tuples,
        or a combination of both. The color and the width of each line
        can be associated to the value of a variable (set in the `color`
        and `size` parameters). In the case of color, this variable
        can contain numeric or categorical data. Check out the tutorial.

        Parameters
        ----------
        latitude0 : list or tuple or str
                    Sequence (list or tuple) or name of the column of the
                    dataframe in `data` containing 
                    the longitude coordinate for the starting point of each
                    line. 
        longitude0 : list or tuple or str
                     Sequence (list or tuple) or name of the column of the
                     dataframe in `data` containing 
                     the latitude coordinate for the starting point of each
                     line. 
        latitude1 : list or tuple or str
                    Sequence (list or tuple) or name of the column of the
                    dataframe in `data` containing 
                    the longitude coordinate for the ending point of each
                    line. 
        longitude1 : list or tuple or str
                     Sequence (list or tuple) or name of the column of the
                     dataframe in `data` containing 
                     the latitude coordinate for the enfing point of each
                     line. 
        size : list or tuple or str or int
               Sequence (list or tuple) or name of the column of the
               dataframe in `data` containing 
               the values that will be used to calculate the width of 
               each line.  Alternatively, it can be a single
               numerical value, assigning the same width to all lines
               (Default: 3).
        color : list or tuple or str 
                Sequence (list or tuple) or name of the column of the
                dataframe in `data` containing 
                the values that will be used to determine the color of each 
                line. These values can be numeric (float or int) 
                or categorical (str). Alternatively, `color` can be a
                hex color that will be applied to all lines
                (Default: '#592a8a').
        data : pandas DataFrame
               Dataframe containing one or more columns of values to use.
               Each row must contain the data for a line, with columns
               as the data to be used (Default: None).
        sizes : list or tuple of 2 elements
                Only relevant if `size` is not int. Range of widths to use 
                for the lines (Default: (3, 15)).
        palette : list or tuple or str
                  Only relevant when `color` is not a str corresponding
                  to a hex color. Sequence of hex colors to be used to
                  color the lines according to their value provided 
                  in `color`. Alternatively, `palette` can
                  be a string with the name of a `seaborn` color palette
                  (Default: 'Spectral').
        n_colors : int
                   Number of colors in the specified `seaborn` palette 
                   (Default: 5).
        cap_min : float or int
                  If set, all lines with a numerical value in `color` smaller 
                  than the value set in `cap_min` will be considered as having
                  a value equal to `cap_min` for coloring purposes. The 
                  corresponding entry in the legend will display a '<' sign.
                  (Default: False).
        cap_max : float or int
                  If set, all lines with a numerical value in `color` greater 
                  than the value set in `cap_max` will be considered as having
                  a value equal to `cap_max` for coloring purposes. The 
                  corresponding entry in the legend will display a '>' sign.
                  (Default: False).
        layer : list or tuple or str 
                Sequence (list or tuple) or name of the column of the
                dataframe in `data` containing 
                the name of the layer on which to draw each line. 
                Alternatively, it can be the name of a single layer on which
                all lines will be added. If the specified layer has not 
                yet been created, `oneworld` will create an overlay with
                that name using the default  settings (Default: "map", which 
                will add the lines directly to the map object).
        style : dict
                Dictionary containing keywords and values defining common
                style values for all lines. Note that the 'color', 
                'fillColor' and 'radius' keywords defined in `style` 
                will override those  in the `color` and `size` 
                parameters (Default: {'opacity':1.0, 'fillOpacity':0.6}).
        style_mouseover : dict
                          If set, style of a line when the mouse is
                          hovered over it (Default: None).
        info_mouseover : list or tuple or str 
                         If set, sequence (list or tuple) or name of the column
                         of the  dataframe in `data` containing
                         the information to be displayed on a pannel when
                         the mouse is hovered over the line. Accepts
                         html format (Default: None).
        legend_pos : {'topleft', 'topright', 'bottomleft', 'bottomright'}
                     Only relevant when `color` is not a str corresponding
                     to a hex color. Position of the color legend, or None
                     for no legend (Default: "bottomright").
        legend_ndec : int
                     Only relevant when `color` is not a str corresponding
                     to a hex color. Number of decimal places to be displayed
                     on the color legend (Default: 2)
        Notes
        -----
        For available color palettes, see
        https://seaborn.pydata.org/tutorial/color_palettes.html

        For a full listing of style options, see 
        https://leafletjs.com/reference-1.6.0.html#path
        """)
#
    def add_network(self, latitude, longitude, source = None, target = None, 
                    group_connect = None,
                    node_data = None, edge_data = None,
                    connect_mouseover = None,
                    node_kwargs = {}, edge_kwargs = {}):
        self.graph = True
        # layer cannot be "map"
        if "layer" not in node_kwargs:
            node_kwargs["layer"] = "network"
        if "layer" not in edge_kwargs:
            edge_kwargs["layer"] = "network"
        # get connectivity
        if group_connect is not None:
            node_kwargs["color"] = group_connect
            edge_kwargs["legend_pos"] = None
            # group_connect
            source = []
            target = []
            if node_data is not None:
                # node dataframe provided
                for thiscat in node_data[group_connect].unique():
                    nodes = node_data.index[node_data[group_connect] == thiscat]
                    nodes = nodes.tolist()
                    nodes2 = cp.deepcopy(nodes)
                    for i_node1 in nodes:
                        nodes2.remove(i_node1)
                        for i_node2 in nodes2:
                            source.append(i_node1)
                            target.append(i_node2)
            else:
                # node is seq
                for thiscat in set(group_connect):
                    nodes = []
                    for i_node, nodecat in enumerate(group_connect):
                        if nodecat == thiscat:
                            nodes.append(i_node)
                    nodes2 = cp.deepcopy(nodes)
                    for i_node1 in nodes:
                        nodes2.remove(i_node1)
                        for i_node2 in nodes2:
                            source.append(i_node1)
                            target.append(i_node2)
            # copy node_kwargs to edge_kwargs if not defined
            for i_kwarg in ("color", "size", "layer"):
                if i_kwarg not in edge_kwargs and i_kwarg in node_kwargs:
                    kwarg_l = self._update_edge_d(node_data, node_kwargs, 
                                                  i_kwarg, source) 
                    edge_kwargs[i_kwarg] = kwarg_l
        # build zipped connectivity list
        nodeindx_z = []
        if edge_data is not None and group_connect is None: 
            source = edge_data[source].tolist()
            target = edge_data[target].tolist()
        nodeindx_z = zip(source, target)
        # make sure layers of edges coincide with layers of nodes
        if 'layer' not in edge_kwargs and 'layer' in node_kwargs:
            kwarg_l = self._update_edge_d(node_data, node_kwargs, 
                                          'layer', source) 
            edge_kwargs['layer'] = kwarg_l
        # get corresponding coordinates
        lat0 = []
        lon0 = []
        lat1 = []
        lon1 = []
        if (node_data is not None 
            and latitude in node_data.columns 
            and longitude in node_data.columns):
            # node dataframe
            for node0, node1 in nodeindx_z:
                lat0.append(node_data[latitude][node0])
                lon0.append(node_data[longitude][node0])
                lat1.append(node_data[latitude][node1])
                lon1.append(node_data[longitude][node1])
        else:
            # node list
            for node0, node1 in nodeindx_z:
                lat0.append(latitude[node0])
                lon0.append(longitude[node0])
                lat1.append(latitude[node1])
                lon1.append(longitude[node1])
        self.add_circles(latitude, longitude, data = node_data, 
                         _connect_over = connect_mouseover, **node_kwargs)
        self.add_lines(lat0, lon0, lat1, lon1, data = edge_data, 
                       _source = source, _target = target, **edge_kwargs)
#
    add_network.__doc__ = tw.dedent("""\
        Add nodes connected by edges.

        Nodes will be depicted as circles, connected by lines (edges).
        For the nodes, input can be in the form of a pandas dataframe, 
        or in lists or tuples, or a combination of both. Connectivity
        between nodes can be specified either by the `source` and
        `target` parameters, or using the `group_connect` parameter.
        In the latter case, `oneworld` will fully connect all
        nodes that have the same value in the `group_connect` parameter.

        Parameters
        ----------
        latitude : list or tuple or str
                   Sequence (list or tuple) or name of the column of the
                   dataframe in `node_data` containing 
                   the longitude coordinate for the center of a node.
        longitude : list or tuple or str
                    Sequence (list or tuple) or name of the column of the
                    dataframe in `node_data` containing 
                    the latitude coordinate for the center of a node. 
        source : list or tuple or str
                 Sequence (list or tuple) or name of the column of the
                 dataframe in `edge_data` where each element contains the index
                 of the source node of one edge (Default: None).
        target : list or tuple or str
                 Sequence (list or tuple) or name of the column of the
                 dataframe in `edge_data` where each element contains the index
                 of the target node of one edge (Default: None).
        group_connect : list or tuple or str
                        Sequence (list or tuple) or name of the column of the
                        dataframe in `node_data` containing the values that
                        will be used to group the nodes in fully connected
                        components in the network (Default: None)    
        node_data : pandas DataFrame
                    Dataframe containing one or more columns of values to use.
                    Each row must contain the data for a node, with columns
                    as the data to be used (Default: None).
        edge_data : pandas DataFrame
                    Dataframe containing one or more columns of values to use.
                    Each row must contain the data for a node, with columns
                    as the data to be used (Default: None).
        connect_mouseover : list or tuple of two dicts
                            If set, the first dict specifies the style of
                            the neighboring nodes when a given node is
                            hovered by the mouse. The second dict defines
                            the styles of the edges connecting the hovered
                            node with its neighbors (Default: None).
        node_kwargs : dict
                      Dictionary containing extra parameters to pass to the
                      `add_circles` method. If `node_data` is provided,
                      it will be passed automatically as the `data` parameter
                      to the `add_circles` method (Default: {}).
                      
        edge_kwargs : dict
                      Dictionary containing extra parameters to pass to the
                      `add_lines` method. If `edge_data` is provided,
                      it will be passed automatically as the `data` parameter
                      to the `add_lines` method (Default: {}).

        See Also
        --------
        add_circles, add_lines

        Notes
        -----
        For available color palettes, see
        https://seaborn.pydata.org/tutorial/color_palettes.html

        For a full listing of style options, see 
        https://leafletjs.com/reference-1.6.0.html#path

        Examples
        --------
        For a dataframe `df` containing the latitudes and longitudes of
        nodes in columns 'Lat' and 'Long' respectively, to connect nodes
        2 and 3, nodes 2 and 5 and nodes 5 and 8 we would
     
        >>> import oneworld as ow
        >>> df = ow.load_dataset("conferences")
        >>> mymap = ow.WebMap(center = [39,-96.8], zoom = 4) 
        >>> mymap.add_network(latitude = 'Lat', longitude = 'Long', 
        ...                   node_data = df,
        ...                   source = [2, 2, 5], target = [3, 5, 8])

        .. raw:: html

            <iframe src="../_static/doc_net1.html" height="345px" width="100%"></iframe>

        If instead we want to connect all the nodes that have the same value on
        column 'Conference' of the dataframe and color nodes and edges
        accordingly we can write:
        
        >>> mymap.add_network(latitude = 'Lat', longitude = 'Long', 
        ...                   node_data = df, group_connect = 'Conference')

        .. raw:: html

            <iframe src="../_static/doc_net2.html" height="345px" width="100%"></iframe>

        """)
#
    def add_geojson(self, json_file, subset = None, subset_key = "GEOID",
                    layer = "map", 
                    style = {'opacity':1.0, 'fillOpacity':0.6,
                             'color': '#fee391', 'fillColor': '#fee391'}, 
                    style_mouseover = None,
                    info_mouseover = None):
        layer = self._check_layer(layer)
        # make sure to avoid non-ascii characters & create json object
        with codecs.open(json_file, encoding='utf-8', errors='replace') as jfil:
            json_raw = jfil.read()
        json_raw = json_raw.replace('\n','')
        json_obj = json.loads(json_raw)
        # subset if desired
        if subset is not None:
            json_sub = {}
            for key, val in json_obj.items():
                if key != "features": json_sub[key] = val
            json_sub["features"] = []
            for feature in json_obj["features"]:
                if feature["properties"][subset_key] == subset:
                    json_sub["features"].append(feature)
        else:
            json_sub = json_obj
        # add init style & info to json
        style_name = self._get_style_name(style)
        for feature in json_sub["features"]:
            feature["properties"]["init_style"] = style_name
            feature['properties']['info_over'] = info_mouseover
        # create info & style change 
        events = self._create_json_ev(style_mouseover, info_mouseover)
        # return json object to a unicode string
        json_data = json.dumps(json_sub)
        # create the object (it's alist, in case there is more than 1)
        self.geojson.append(Geojson(json_data, events, layer))
#
    add_geojson.__doc__ = tw.dedent("""\
        Add a GeoJSON file to the map.

        You can add all the features in the GeoJSON file, or only a subset
        of those using the `subset` and `subset_key` parameters. If you do so,
        only those features whose `subset_key` value under the feature's
        properties matches the value specified in `subset` will be added to the
        map.
  
        Parameters
        ----------
        json_file : str
                    Full path name of the GeoJSON file.
        subset : str
                 If defined, only the `features` of the file whose value of 
                 `subset_key` matches the value in `subset` will be added to 
                 the map (Default: None, i.e., add all features on the file).
        subset_key : str
                     Only relevant if `subset` is defined. Name of the property
                     (under `properties` of each feature) that will be used to
                     determine if a feature is added to the map (Default: 
                     "GEOID").
        layer : str
                Name of the layer on which the selected features will be added. 
                If the specified layer has not yet been created, `oneworld` 
                will create an overlay with that name using the default 
                settings (Default: "map", which  will add the lines directly to 
                the map object).
        style : dict
                Dictionary containing keywords and values defining common
                style values for all features in the GeoJSON file. 
                (Default: {'opacity':1.0, 'fillOpacity':0.6, 
                'color': '#fee391', 'fillColor': '#fee391'}). 
        style_mouseover : dict
                          If set, style of a `feature` when the mouse is
                          hovered over it (Default: None).
        info_mouseover : str 
                         If set, information to be displayed on a pannel when
                         the mouse is hovered over any `feature`. Accepts
                         html format (Default: None).

        See Also
        --------
        add_choropleth

        Notes
        -----
        For a full listing of style options, see 
        https://leafletjs.com/reference-1.6.0.html#path
        """)
#
    def add_choropleth(
                       self, json_file, geoid, color,
                       data = None, 
                       json_key = "GEOID",
                       palette = "Spectral",
                       n_colors = 5,
                       cap_min = False, cap_max = False,
                       layer = "map",
                       style = {'opacity':1.0, 'fillOpacity':0.6},
                       style_mouseover = None,
                       info_mouseover = None,
                       legend_pos = "bottomright",
                       legend_ndec = 2):
        if data is not None:
            geoid_l = [str(x) for x in data[geoid]]
        else:
            geoid_l = [str(x) for x in geoid]
        ngeoms = len(geoid_l)
        # retrieve desired attributes
        color_l, size_l, layer_l, info_l = self._listomania(color, None, 
                                   layer, info_mouseover, data, ngeoms,
                                   palette, n_colors, None, cap_min, cap_max,
                                   legend_pos, legend_ndec)
        zipped_lst = zip(geoid_l, color_l, info_l)
        # make sure to avoid non-ascii characters & create json object
        with codecs.open(json_file, encoding='utf-8', errors='replace') as jfil:
            json_raw = jfil.read()
        json_raw = json_raw.replace('\n','')
        json_obj = json.loads(json_raw)
        json_chr = {}
        for key, val in json_obj.items():
            if key != "features": json_chr[key] = val
        json_chr["features"] = []
        # get features corresponding to each geoid and assign attributes
        for i_geoid, i_color, i_info in zipped_lst:
            i_style = {'fillColor': i_color, 'color': i_color}
            i_style.update(style)
            style_name = self._get_style_name(i_style)
            # retrieve feature and assign attrb
            for feature in json_obj["features"]:
                if feature["properties"][json_key] == i_geoid:
                    feature["properties"]["init_style"] = style_name
                    feature['properties']['info_over'] = i_info
                    json_chr["features"].append(feature)
        # return json object to a unicode string
        json_data = json.dumps(json_chr)
        # events dict
        events = self._create_json_ev(style_mouseover, info_mouseover)
        # create the object and store it
        layer = self._check_layer(layer)
        self.geojson.append(Geojson(json_data, events, layer))
#
    add_choropleth.__doc__ = tw.dedent("""\
        Add a choropleth.

        Given a GeoJSON file, color each of its `features` according
        to some value provided in the `color` parameter. For each value
        in `color` there should be a value in `geoid`, which will be used
        to identidfy the corresponding `feature` in the file using the
        `json_key` parameter, which should be under the `properties`
        key of the `feature`.

        Parameters
        ----------
        json_file : str
                    Full path name of the GeoJSON file.
        geoid : list or tuple or str
                Sequence (list or tuple) or name of the column of the
                dataframe in `data` containing
                the `string` that will be used to identify each `feature`
                on the `json_file`.
        color : list or tuple or str 
                Sequence (list or tuple) or name of the column of the
                dataframe in `data` containing 
                the values that will be used to determine the color of each 
                `feature`. These values can be numeric (float or int) 
                or categorical (str). Alternatively, `color` can be a
                hex color that will be applied to all `features`.
        data : pandas DataFrame
               Dataframe containing one or more columns of values to use.
               Each row must contain the data for a `feature`, with columns
               as the data to be used (Default: None).
        json_key : str
                   Name of the property (under `properties` of each feature) 
                   that will be used to identify each `feature` (Default: 
                   "GEOID").
        palette : list or tuple or str
                  Sequence of hex colors to be used to
                  color the `features` according to their value provided 
                  in `color`. Alternatively, `palette` can
                  be a string with the name of a `seaborn` color palette
                  (Default: 'Spectral').
        n_colors : int
                   Number of colors in the specified `seaborn` palette 
                   (Default: 5).
        cap_min : float or int
                  If set, all `features` with a numerical value in `color` 
                  smaller than the value set in `cap_min` will be considered 
                  as having a value equal to `cap_min` for coloring purposes. 
                  The corresponding entry in the legend will display a '<' 
                  sign (Default: False).
        cap_max : float or int
                  If set, all `features` with a numerical value in `color` 
                  greater than the value set in `cap_max` will be considered 
                  as having a value equal to `cap_max` for coloring purposes. 
                  The corresponding entry in the legend will display a '>' 
                  sign (Default: False).
        layer : str 
                Name of the layer on which
                all `features` will be added. If the specified layer has not 
                yet been created, `oneworld` will create an overlay with
                that name using the default  settings (Default: "map", which 
                will add the choropleth directly to the map object).
        style : dict
                Dictionary containing keywords and values defining common
                style values for all `features`. Note that the 'color' and
                'fillColor' keywords defined in `style` 
                will override those  in the `color` parameters (Default: 
                {'opacity':1.0, 'fillOpacity':0.6}).
        style_mouseover : dict
                          If set, style of the `feature` when the mouse is
                          hovered over it (Default: None).
        info_mouseover : list or tuple or str 
                         If set, sequence (list or tuple) or name of the column
                         of the  dataframe in `data` containing
                         the information to be displayed on a pannel when
                         the mouse is hovered over the `feature`. Accepts
                         html format (Default: None).
        legend_pos : {'topleft', 'topright', 'bottomleft', 'bottomright'}
                     Position of the color legend, or None for no legend
                     (Default: "bottomright").
        legend_ndec : int
                      Number of decimal places to be displayed
                      on the color legend (Default: 2).

        See Also
        --------
        add_gejson

        Notes
        -----
        For available color palettes, see
        https://seaborn.pydata.org/tutorial/color_palettes.html

        For a full listing of style options, see 
        https://leafletjs.com/reference-1.6.0.html#path

        Examples
        --------
        A minimal example of how to plot a choropleth using the GeoJSON file
        "us_states.json" and the "farms" dataframe is:
      
        >>> import oneworld as ow
        >>> df = ow.load_dataset("farms")
        >>> mymap = ow.WebMap(center = [39,-96.8], zoom = 4)
        >>> mymap.add_choropleth(json_file = "us_states.json",
        ...                      geoid = "FIPS", color = "Region",
        ...                      data = df, json_key = "GEOID")

        In this example, each `feature` on the file is matched with the row
        in the dataframe that has the same `json_key` value of the `feature`
        in the `geoid` column of the dataframe (e.g. the `feature` with a
        "GEOID" `property` of "34" will be associated to the row in `df`
        with a value of "34" in the column "FIPS"). Then that `feature` 
        is colored according to the value of `color` in that row.

        .. raw:: html

            <iframe src="../_static/doc_chor.html" height="345px" width="100%"></iframe>

        Note that in this case it was not necessary to define the `json_key` 
        parameter as it uses the same value as its default value 
        value in `add_choropleth` ("GEOID"),
        but is included in the example for clarity.

        """)
#
    def add_heatmap(self, latitude, longitude, intensity, data = None, 
                    layer = "map", **kwargs):
        """Add a heatmap to the map. Note that this method is experimental.
        
        Parameters
        ----------
        latitude : list or tuple or str
                   Sequence (list or tuple) or name of the column of the
                   dataframe in `data` containing 
                   the longitude coordinate for the center of each area. 
        longitude : list or tuple or str
                    Sequence (list or tuple) or name of the column of the
                    dataframe in `data` containing 
                    the latitude coordinate for the center of each area. 
        intensity : list or tuple or str
                    Sequence (list or tuple) or name of the column of the
                    dataframe in `data` containing 
                    the numeric value of each area.
        data : pandas DataFrame
               Dataframe containing one or more columns of values to use.
               Each row must contain the data for an area, with columns
               as the data to be used (Default: None).
        layer : str 
                Name of the layer on which the heatmap will be added. 
                (Default: "map", which 
                will add the choropleth directly to the map object).
        kwargs : dict
                 Extra keyword arguments to pass to the Leaflet.heat plugin.

        Notes
        -----
        Experimental. This method uses the Leaflet.heat plugin (you don't
        need to download it). Documentation can be found in:
        https://github.com/Leaflet/Leaflet.heat
        """
        if (isinstance(latitude, (list, tuple)) and 
            isinstance(longitude, (list, tuple))):
            lat_l = latitude
            lon_l = longitude
        elif (data is not None 
              and latitude in data.columns 
              and longitude in data.columns):
            lat_l = data[latitude].tolist()
            lon_l = data[longitude].tolist()
        else:
            raise ValueError("You must provide valid latitude and longitude")
            return
        if isinstance(intensity, (list, tuple)):
            int_l = intensity
        elif data is not None and intensity in data.columns:
            int_l = data[intensity].tolist()
        # rescale intensities so they are between 0 and 1
        max_int = max(int_l)
        min_int = min(int_l)
        int_rescal = rescale(min_int, max_int, 0.0, 1.0, int_l)
        # zip list
        points = [list(x) for x in zip(lat_l, lon_l, int_rescal)]
        # create object and store it
        self.heatmap = Heatmap(points, kwargs, layer)
#
    def _check_layer(self, layer):
        """Remove non alphanumeric characters from a layer name. Also, check 
           if it exists. If not, create an 
           overlay with that name. Return layer clean name"""
        layer_short = clean_string(layer)
        if (layer_short != "map" 
            and layer_short not in [iover.name for iover in self.overlays] 
            and layer_short not in [ibasem.name for ibasem in self.basemaps]):
           self.add_overlay(name = layer_short)
        return layer_short
#
    def _get_style_name(self, new_style):
        """get the name of the style defined in the args or assign new num"""
        # check if it already exists
        for this_name, this_style in self.styles.items():
            if new_style == this_style:
                style_name = this_name
                break
        # if not, add it to styles list
        else:
            style_number = len(self.styles.keys())
            style_name = 'style_{}'.format(style_number)
            self.styles[style_name] = cp.deepcopy(new_style)
        return style_name
#
    def _listomania(self, color, size, layer, info_mouseover, data, ndim,
                    palette, n_colors, sizes, cap_min, cap_max,
                    legend_pos, legend_ndec):
        """Create lists from inputs"""
        need_cb = False
        # colors
        if isinstance(color, (list, tuple)):
            col_lst, leg_pairs, quant, sm = get_hexes(color, palette, n_colors, 
                                                 cap_min, cap_max, legend_ndec)
            # we need a colorbar
            need_cb = True
        elif data is not None and color in data.columns:
            col_lst, leg_pairs, quant, sm = get_hexes(data[color], palette, 
                                                      n_colors, cap_min, 
                                                      cap_max, legend_ndec)
            # we need a colorbar
            need_cb = True
        else:
            col_lst = [color] * ndim
        # sizes
        legend_labels = 0 #unimplemented (to do)
        if isinstance(size, (list, tuple)):
            siz_lst, siz_leg = get_sizes(size, sizes, legend_labels, 
                                         cap_min, cap_max, legend_ndec)
        elif data is not None and size in data.columns:
            siz_lst, siz_leg = get_sizes(data[size], sizes, legend_labels, 
                                         cap_min, cap_max, legend_ndec)   
        else:
            siz_lst = [size] * ndim
        # layers
        if isinstance(layer, (list, tuple)):
            lay_lst = [self._check_layer(x) for x in layer]
            if self.layercontrol is None:
                self.add_layer_control()
        elif data is not None and layer in data.columns:
            lay_lst = [self._check_layer(x) for x in data[layer]]
            if self.layercontrol is None:
                self.add_layer_control()
        else:
            lay_lst = [self._check_layer(layer)] * ndim
        # add now the colorbar if needed to each requested layer
        if need_cb and legend_pos is not None:
            for this_lay in lay_lst:
                short_name = clean_string(this_lay)
                for this_basemap in self.basemaps:
                    if short_name in this_basemap.name:
                        cb_base = short_name
                        break
                else:
                    cb_base = None
                if not isinstance(color, (list, tuple)):
                    cb_title = color
                else:
                    cb_title = ''
                this_cb = Colorbar(leg_pairs, legend_pos, cb_title, cb_base)
                for other_cb in self.colorbar:
                    if this_cb.__eq__(other_cb):
                        break
                else:
                    self.colorbar.append(this_cb)
        # info panel
        if isinstance(info_mouseover, (list, tuple)):
            inf_lst = info_mouseover
            if self.panel is None:
                self.add_panel()
        elif data is not None and info_mouseover in data.columns:
            inf_lst = data[info_mouseover]
            if self.panel is None:
                self.add_panel(title = info_mouseover)
        else:
            inf_lst = [None] * ndim
        #
        return col_lst, siz_lst, lay_lst, inf_lst
#
    def _create_events(self, style_over, info_over, connect_over, layer):
        """Create the events dict"""
        # check events
        events = {}
        if (style_over is not None 
            or info_over is not None 
            or connect_over is not None):
            # In any case
            events['mouseover'] = []
            events['mouseout'] = []
            if style_over is not None:
                style_name = self._get_style_name(style_over)
                overstr = 'makeOver(this, '+style_name+');'
                events['mouseover'].append(overstr)
                events['mouseout'].append('makeInit(this);')
            if info_over is not None:
                infostr = 'var circle_info = "'+info_over+'";'
                events['mouseover'].append(infostr)
                events['mouseover'].append('panel.update(circle_info);')
                events['mouseout'].append('panel.update();')
                if self.panel is None:
                    self.add_panel()
            if connect_over is not None:
                n_stylnam = self._get_style_name(connect_over[0]) 
                e_stylnam = self._get_style_name(connect_over[1])
                connstr = 'connectedNodes(this, "'+layer+'", '+n_stylnam \
                           +', '+e_stylnam+');'
                events['mouseover'].append(connstr)
                resconnstr = 'resConnectedNodes(this, "'+layer+'");'
                events['mouseout'].append(resconnstr)
        return events
#
    def _create_json_ev(self, style_over, info_over):
        """Create avents dict for geojson objec. Update it with info"""
        events = {}
        if style_over is not None or info_over is not None:
            events['mouseover'] = []
            events['mouseout'] = []
        if style_over is not None:
            style_name = self._get_style_name(style_over)
            pref_str = 'layer.setStyle('
            events['mouseover'].append(pref_str+style_name+');')
            out_str = pref_str+'eval(feature.properties.init_style));'
            events['mouseout'].append(out_str)
        if info_over is not None:
            pref_str = 'panel.update('
            info_str = pref_str+'layer.feature.properties.info_over);'
            events['mouseover'].append(info_str)
            events['mouseout'].append(pref_str+');')
            if self.panel is None:
                self.add_panel()
        return events
#
    def _update_edge_d(self, node_data, node_kwargs, key, indxs_l): 
        """Update the edge data dict"""
        edge_attrs = []
        if node_data is not None and node_kwargs[key] in node_data.columns:
            for i_node in indxs_l:
                kwarg_val = node_data.loc[node_data.index[i_node],  
                                          node_kwargs[key]]
                edge_attrs.append(kwarg_val)
        elif isinstance(node_kwargs[key], (list, tuple)):
            for i_node in indxs_l:
                kwarg_val = node_kwargs[key][i_node]
                edge_attrs.append(kwarg_val)
        else:
            edge_attrs = node_kwargs[key]
        return edge_attrs
