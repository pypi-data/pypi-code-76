"""Classes for the WebMap"""
class Basemap:
    """Basemap class with its name and the tiles name"""

    def __init__(self, name, full_name, tiles, source, options):
        self.name = name
        self.full_name = full_name
        self.tiles = tiles
        self.source = source
        self.options = options

class Overlay:
    """OverLay class with its name, if it is shown on start and if it
       appears on the layer control panel"""

    def __init__(self, name, full_name, show_start, show_panel, alwaysontop):
        self.name = name
        self.full_name = full_name
        self.show_start = show_start
        self.show_panel = show_panel
        self.alwaysontop = alwaysontop

class Panel:
    """A panel to display info. Title is highlighted"""

    def __init__(self, title, noinfo, position, width, height):
        self.title = title
        self.noinfo = noinfo
        self.position = position
        self.width = width
        self.height = height

class Box:
    """A box to display static information"""

    def __init__(self, contents, position):
        self.contents = contents
        self.position = position

class Layercontrol:
    """A Llayer control object"""

    def __init__(self, position, collapsed, autoindex, hidesinglebase):
        self.position = position
        self.collapsed = collapsed
        self.autoindex = autoindex
        self.hidesinglebase = hidesinglebase

class Circle:
    """Circle class, contains all needed variables to represent in template"""
    def __init__(self, coords, style, layer, events, ctant_r, nodeindex):
        self.coords = coords
        self.layer = layer
        self.style = style
        self.events = events
        self.ctant_r = ctant_r
        self.nodeindex = nodeindex

class Line:
    """A line class containing all needed elements"""
    def __init__(self, coords, style, layer, events, source, target):
        self.coords = coords
        self.layer = layer
        self.style = style
        self.events = events
        self.source = source
        self.target = target

class Logo:
    """a logo. A simple image"""
    def __init__(self, source, position, width):
        self.source = source
        self.position = position
        if not width:
            self.width = 'auto'
        else:
            self.width = str(width)+'px'

class Geojson:
    """An object containing all the geo json options"""
    def __init__(self, data, events, layer):
        self.data = data
        self.events = events
        self.layer = layer

class Colorbar:
    """Data for the colorbar: the colors and the labels"""
    def __init__(self, pairs, position, title, basemap):
        self.pairs = pairs
        self.position = position
        self.title = title
        self.basemap = basemap
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class Heatmap:
    """a heatmap"""
    def __init__(self, points, options, layer):
        self.points = points
        self.options = options
        self.layer = layer

