#! /usr/bin/env python

import math
from copy import deepcopy
from visualife.core.styles import ColorRGB, hex_to_rgb, color_by_name, get_color

try:
  from browser import document
except:  document = None


base_color = ColorRGB(*hex_to_rgb("#6AB0DE"))
stroke_color = base_color.create_darker(0.2)
stroke_width = 2
fill_color = base_color.mix(0.8,color_by_name("white"))
highlighted_color = base_color.deepcopy().mix(0.15, color_by_name("red"))

default_node_style = {'stroke_width': '%dpx' % stroke_width,
                      'stroke': stroke_color,
                      'fill': fill_color
                      }

default_text_style = {'stroke_width': '0px',
                      'fill': 'black',
                      'text_anchor': 'middle',
                      'alignment_baseline': 'middle'
                      }

default_segment_length = 30 # in pixels


def repack_node_style_args(node_style_dict, text_style_dict, **attrs):
    """ Repacks drawing style for node and text

    This is a helper function that is used to build a ``**kwargs`` dictionary
    that is then passed to node's draw() method

    :param node_style_dict: (``dict``) a dictionary that provides style for drawing a node
    :param text_style_dict: (``dict``) a dictionary that provides style for text
    :param attrs: dictionary of additional attributes, which may contain
        ``"node_style_dict"`` and ``"text_style_dict"`` keys; all other items of this dictionary are
        considered as node drawing attributes and accordingly packed to ``"node_style"`` dictionary
    :return: a dictionary that holds two entries: ``"node_style"`` and ``"text_style"``
    """

    out = dict()
    out["text_style"] = dict(**text_style_dict)
    if "text_style" in attrs:
        for k, v in attrs["text_style"].items(): out["text_style"][k] = v

    out["node_style"] = dict(**node_style_dict)
    if "node_style" in attrs:
        for k, v in attrs["node_style"].items(): out["node_style"][k] = v

    for k, v in attrs.items():
        if k != "node_style" and k != "text_style":
            out["node_style"][k] = v

    return out


class Point:
    """A simple data structure to hold X,Y coordinates on a screen.

    Diagram nodes, such as RectNode or DotNode are derived from Point to define their location.
    The :class:`Point` class defines also basic arithmetic operations, user can therefore easily
    compute coordinates of a new node based on existing nodes (e.g. coordinates of a point that
    is exactly in the middle of two nodes)
    """

    def __init__(self, x, y):
        """ Creates a point from the given coordinates

        :param x: (``number``) x viewport coordinate
        :param y: (``number``) y viewport coordinate
        """
        self.__x = x
        self.__y = y

    @property
    def x(self): return self.__x

    @x.setter
    def x(self, x): self.__x = x

    @property
    def y(self): return self.__y

    @y.setter
    def y(self, y): self.__y = y

    def __str__(self):
        """ Returns a string representation of this point

        :return: string with coordinates of this point
        """
        return "%.1f %.1f" % (self.x, self.y)

    def __add__(self, rhs):
        """Adds a rhs point and this point

        :param rhs: (:class:`Points`) another point
        :return: a new :class:`Point` object
        """
        return Point(self.x + rhs.x, self.y + rhs.y)

    def __iadd__(self, rhs):
        """Adds a rhs point to this point, returns the self reference

        :param rhs: (:class:`Points`) another point
        :return: ``self``
        """
        self.x += rhs.x
        self.y += rhs.y
        return self

    def __sub__(self, rhs):
        """Subtracts a rhs point from this point, returns a new :class:`Point` object"""
        return Point(self.x - rhs.x, self.y - rhs.y)

    def distance_to(self, another_point):
        """Calculated distance from this :class:`Point` to another one
        
        :param another_point: another :class:`Point`object
        :return: (``float``) a distance in viewport coordinates
        """
        d = another_point.x - self.x
        d2 = d*d
        d = another_point.y - self.y
        d2 += d*d
        return math.sqrt(d2)


def average_point(points):
    """Determines a :class:`Point` that is an average of given :class:`Point` objects.

    The function is e.g. used to find the center of a diagram node

    :param points: (``list[:class:`Point`]``) a list of points
    :return: a :class:`Point` object
    """
    p = Point(0, 0)
    for pi in points:
        p.x += pi.x
        p.y += pi.y
    p.x /= len(points)
    p.y /= len(points)
    return p


class NodeBase(Point):

    def __init__(self, id, x, y):
        """A base class to all nodes.

        A NodeBase is derived from the :class:`Point` class to store coordinates for this node's center.

        Each node (except DotNode) may have a text written on it. The text and the shape of this node itself
        have a distinct IDs; they can be obtained from :meth:`text_id` and  :meth:`shape_id` getters, respectively.
        Each node has also can draw itself on a viewport.

        :param id: (``string``) unique identifier for this node
        :param x: (``number``) X coordinate for this node's center
        :param y: (``number``) Y coordinate for this node's center
        """
        super().__init__(x, y)
        self.__id = id
        if document:
            self.__fill = None
            self.__is_highlighted = False

    @property
    def left(self):
        """Coordinates of the point in the middle of the left side of this node

        Abstract method, raises :class:`NotImplementedError`
        """
        raise NotImplementedError("the *left* property is not implemented")

    @property
    def right(self):
        """Coordinates of the point in the middle of the right side of this node

        Abstract method, raises :class:`NotImplementedError`
        """
        raise NotImplementedError("the *right* property is not implemented")

    @property
    def top(self):
        """Coordinates of the point in the middle of the top side of this node

        Abstract method, raises :class:`NotImplementedError`
        """
        raise NotImplementedError("the *top* property is not implemented")

    @property
    def bottom(self):
        """Coordinates of the point in the middle of the bottom side of this node

        Abstract method, raises :class:`NotImplementedError`
        """
        raise NotImplementedError("the *bottom* property is not implemented")

    @property
    def id(self):
        """Returns ID of this node

        :return: unique ID of this node
        """
        return self.__id

    @property
    def text_id(self):
        """Returns ID of the text element of this node.

        :return: (``string``) ID of the text part of this node
        """
        return self.id + "-text"

    @property
    def shape_id(self):
        """Returns ID of the shape element of this node.

        :return: (``string``) unique ID assigned to the shape element of this node
            (e.g. a <rect> or a <circle>)
        """
        return self.id + "-box"

    @property
    def width(self):
        """The width of this node.

        This property is evaluated as ``self.right.x - self.left.x``, so it relies on :meth:`left` and :meth:`right`
        implementation of a derived class
        :return: width of this node.
        """
        return self.right.x - self.left.x

    @property
    def height(self):
        """The height of this node.

        This property is evaluated as ``self.bottom.y - self.top.y``, so it relies on :meth:`bottom` and :meth:`top`
        implementation of a derived class
        :return: height of this node.
        """
        return self.bottom.y - self.top.y

    def draw(self, viewport, **kwargs):
        """Draw this node on a viewport

        Abstract method, raises :class:`NotImplementedError`

        :param viewport: (:class:`visualife.core.HtmlViewport` or :class:`visualife.core.SvgViewport`) where to draw this node
        :param kwargs: node styling parameters
        """
        raise NotImplementedError("the *bottom* property is not implemented")

    def highlight(self, state=True):
        """Highlights this box or turns it back to normal.

        Highlighting this node will change it's fill color to a reddish tint of its existing (standard) color
        The new color will be visible until :meth:`clear` is called. This method works only when
        :class:`visualife.core.HtmlViewport` is used to render the graphics; otherwise it has no effect.

        :param state: (``boolean``) if ``True``, this node will be highlighted, otherwise any highlight effect
        will be cancelled
        """
        if document:
            if state and not self.__is_highlighted:
                self.__fill = document[self.shape_id].style["fill"]
                hi_col = get_color(self.__fill).mix(0.15, color_by_name("red"))
                document[self.shape_id].style["fill"] = str(hi_col)
                self.__is_highlighted = True
            if not state and self.__is_highlighted:
                document[self.shape_id].style["fill"] = str(self.__fill)
                self.__is_highlighted = False

class DotNode(NodeBase):

    def __init__(self, id, x, y, r, **attrs):
        """Creates a node that is dot.

        This node type has no text on it. It may be used as a marker, e.g. to mark a joint between :class:`Connector` lines

        :param id: (``string``) id to be set to the SVG element of the rectangle
        :param x: (``number``) X of the dot's center
        :param y: (``number``) Y of the dot's center
        :param r: (``number``) radius of the dot
        :param attrs: see below

        :Keyword Arguments:
            * *node_style* (``string`` or ``dict``) --
              a style for drawing the dot

       The example below creates a :class:`DotNode` with radius = 50. Four additional small dots mark its
       :meth:`top`, :meth:`left`, :meth:`bottom` and :meth:`right` position.

       .. code-block:: python

              from browser import document
              from visualife.core import HtmlViewport
              from visualife.diagrams import DotNode

              drawing = HtmlViewport(document['svg-dot'],0,0,200,200)
              dot = DotNode("dot-0", 100, 100, 50)
              t = DotNode("dot-1", dot.top.x, dot.top.y, 5)
              l = DotNode("dot-2", dot.left.x, dot.left.y, 5)
              b = DotNode("dot-3", dot.bottom.x, dot.bottom.y, 5)
              r = DotNode("dot-4", dot.right.x, dot.right.y, 5)
              for d in [dot, t, l, b, r]:
                d.draw(drawing)
              drawing.close()

       .. raw:: html

          <div> <svg  id="svg-dot" xmlns="http://www.w3.org/2000/svg" class="right" width="200" height="200"></svg> </div>
          <script type="text/python">
              from browser import document
              from visualife.core import HtmlViewport
              from visualife.diagrams import DotNode

              drawing = HtmlViewport(document['svg-dot'],0,0,200,200)
              dot = DotNode("dot-0", 100, 100, 50)
              t = DotNode("dot-1", dot.top.x, dot.top.y, 5)
              l = DotNode("dot-2", dot.left.x, dot.left.y, 5)
              b = DotNode("dot-3", dot.bottom.x, dot.bottom.y, 5)
              r = DotNode("dot-4", dot.right.x, dot.right.y, 5)
              for d in [dot, t, l, b, r]:
                d.draw(drawing)
              drawing.close()
          </script>
        """
        super().__init__(id, x, y)
        self.__attrs = attrs        # --- copy drawing parameters
        self.__r = r

    def draw(self, viewport, **kwargs):
        """Draw this dot node on a viewport

        :param viewport: (:class:`visualife.core.HtmlViewport` or :class:`visualife.core.SvgViewport`) where to draw this node
        :param kwargs: provide style to draw this dot with *node_style* key
        """
        viewport.circle(self.id, self.x, self.y, r=self.r, **kwargs.get("node_style", default_node_style))

    @property
    def r(self):
        """Radius of this dot

        :return: (``number``) radius of this dot
        """
        return self.__r

    @property
    def left(self):
        """Coordinates of the left-most point of this dot

        :return: (:class:`Point`) the left-most point of this dot
        """
        return Point(self.x - self.r, self.y)

    @property
    def right(self):
        """Coordinates of the right-most point of this dot

        :return: (:class:`Point`) the right-most point of this dot
        """
        return Point(self.x + self.r, self.y)

    @property
    def top(self):
        """Coordinates of the highest point of this dot

        :return: (:class:`Point`) the highest point of this dot
        """
        return Point(self.x, self.y - self.r)

    @property
    def bottom(self):
        """Coordinates of the lowest point of this dot

        :return: (:class:`Point`) the lowest point of this dot
        """
        return Point(self.x, self.y + self.r)


class RectNode(NodeBase):

    def __init__(self, id, text, xc, yc, w, h, **attrs):
        """Rectangular node of a diagram - a box with a text in it.

        :param id: (``string``) id to be set to the SVG element of the rectangle
        :param text: (``string``) text to be displayed in the box
        :param xc: (``number``) X of the rectangle center
        :param yc: (``number``) Y of the rectangle center
        :param w: (``number``) width of the box
        :param h: (``number``) height of the box
        :param attrs: see below

        :Keyword Arguments:
            * *text_style* (``string`` or ``dict``) --
              a style for text placed at this node
            * *node_style* (``string`` or ``dict``) --
              a style for drawing the rectangle

       The example below creates a :class:`RectNode` . Four additional small dots mark its
       :meth:`top`, :meth:`left`, :meth:`bottom` and :meth:`right` position.

       .. code-block:: python

              from browser import document
              from visualife.core import HtmlViewport
              from visualife.diagrams import RectNode, DotNode

              drawing = HtmlViewport(document['svg-box'],0,0,200,100)
              box = RectNode("box-0", "example box", 100, 40, 100, 50)
              t = DotNode("dot-1", box.top.x, box.top.y, 5)
              l = DotNode("dot-2", box.left.x, box.left.y, 5)
              b = DotNode("dot-3", box.bottom.x, box.bottom.y, 5)
              r = DotNode("dot-4", box.right.x, box.right.y, 5)
              for shape in [box, t, l, b, r]:
                shape.draw(drawing)
              drawing.close()

       .. raw:: html

          <div> <svg  id="svg-box" xmlns="http://www.w3.org/2000/svg" class="right" width="200" height="100"></svg> </div>
          <script type="text/python">
              from browser import document
              from visualife.core import HtmlViewport
              from visualife.diagrams import RectNode, DotNode

              drawing = HtmlViewport(document['svg-box'],0,0,200,100)
              box = RectNode("box-0", "example box", 100, 40, 100, 50)
              t = DotNode("dot-1", box.top.x, box.top.y, 5)
              l = DotNode("dot-2", box.left.x, box.left.y, 5)
              b = DotNode("dot-3", box.bottom.x, box.bottom.y, 5)
              r = DotNode("dot-4", box.right.x, box.right.y, 5)
              for shape in [box, t, l, b, r]:
                shape.draw(drawing)
              drawing.close()
          </script>
        """

        super().__init__(id, xc, yc)
        self.__attrs = attrs        # --- copy drawing parameters
        self.__text = text
        self.__w = w
        self.__h = h

    def draw(self, viewport, **kwargs):
        """Draw this dot node on a viewport.

        :param viewport: (:class:`visualife.core.HtmlViewport` or :class:`visualife.core.SvgViewport`) where to draw this node
        :param kwargs: provide style to draw this dot with *node_style* and *text_style* keys
        """

        params = repack_node_style_args(default_node_style, default_text_style, **self.__attrs)
        params = repack_node_style_args(params["node_style"], params["text_style"], **kwargs)
        params["node_style"]["filter"]="shadow"
        x = self.x - self.w / 2.0
        y = self.y - self.h / 2.0
        viewport.rect(self.shape_id, x, y, self.__w, self.__h, **params["node_style"])
        viewport.text(self.text_id, self.x, self.y, self.__text, **params["text_style"])

    @property
    def w(self):
        """Width of this rectangle

        :return: (``number``) width
        """
        return self.__w

    @property
    def h(self):
        """Height of this rectangle

        :return: (``number``) height
        """
        return self.__h

    @property
    def left(self):
        """Coordinates of the point in the middle of the left side of this rectangle

        :return: (:class:`Point`) middle coordinates of the left side
        """
        return Point(self.x-self.__w/2.0, self.y)

    @property
    def right(self):
        """Coordinates of the point in the middle of the right side of this rectangle

        :return: (:class:`Point`) middle coordinates of the right side
        """
        return Point(self.x + self.__w / 2, self.y)

    @property
    def top(self):
        """Coordinates of the point in the middle of the top side of this rectangle

        :return: (:class:`Point`) middle coordinates of the top side
        """
        return Point(self.x, self.y - self.h / 2)

    @property
    def bottom(self):
        """Coordinates of the point in the middle of the bottom side of this rectangle
        
        :return: (:class:`Point`) middle coordinates of the bottom side
        """
        return Point(self.x, self.y + self.__h / 2)


class DiamondNode(RectNode):

    def __init__(self, id, text, xc, yc, w, **attrs):
        """Draws a diamond node.

        This shape can be used to represent a conditional statement in block algorithms. Diamond node
        is derived from a RectNode; in fact its just a square rotated by 45 degrees

        :param id: (``string``) id to be set to the SVG element of the rectangle
        :param text: (``string``) text to be displayed in the box
        :param xc: (``number``) X of the bottom left corner
        :param yc: (``number``) Y of the bottom left corner
        :param w: (``number``) width of the box
        :param attrs: see below

        :Keyword Arguments:
            * *text_style* (``string``) --
              a dictionary holding style settings for text
            * *node_style* (``string``) --
              a style for drawing

       The example below creates a :class:`DiamondNode` . Four additional small dots mark its
       :meth:`top`, :meth:`left`, :meth:`bottom` and :meth:`right` position.

       .. code-block:: python

              from browser import document
              from visualife.core import HtmlViewport
              from visualife.diagrams import DiamondNode, DotNode

              drawing = HtmlViewport(document['svg-dia'],0,0,200,100)
              box = DiamondNode("dia-1", "example box", 100, 80, 50)
              t = DotNode("dot-1a", box.top.x, box.top.y, 5)
              l = DotNode("dot-2a", box.left.x, box.left.y, 5)
              b = DotNode("dot-3a", box.bottom.x, box.bottom.y, 5)
              r = DotNode("dot-4a", box.right.x, box.right.y, 5)
              for shape in [box, t, l, b, r]:
                  shape.draw(drawing)
              drawing.close()

       .. raw:: html

          <div> <svg  id="svg-dia" xmlns="http://www.w3.org/2000/svg" class="right" width="200" height="100"></svg> </div>
          <script type="text/python">
              from browser import document
              from visualife.core import HtmlViewport
              from visualife.diagrams import DiamondNode, DotNode

              drawing = HtmlViewport(document['svg-dia'],0,0,200,100)
              box = DiamondNode("dia-1", "example box", 100, 80, 50)
              t = DotNode("dot-1a", box.top.x, box.top.y, 5)
              l = DotNode("dot-2a", box.left.x, box.left.y, 5)
              b = DotNode("dot-3a", box.bottom.x, box.bottom.y, 5)
              r = DotNode("dot-4a", box.right.x, box.right.y, 5)
              for shape in [box, t, l, b, r]:
                  shape.draw(drawing)
              drawing.close()
          </script>
        """
        super().__init__(id, text, xc-w/2.0, yc-w/2.0, w, w)
        self.__attrs = attrs        # --- copy drawing parameters

    def draw(self, viewport, **kwargs):
        """Draw this dot node on a viewport.

        :param viewport: (:class:`visualife.core.HtmlViewport` or :class:`visualife.core.SvgViewport`) where to draw this node
        :param kwargs: provide style to draw this dot with *node_style* and *text_style* keys
        """

        super(DiamondNode, self).draw(viewport, **kwargs, angle=45)

    @property
    def left(self):
        """Coordinates of the left vertex of this node

        :return: (:class:`Point`) coordinates of the left vertex
        """
        return Point(self.x - self.w * math.sqrt(2) / 2.0, self.y)

    @property
    def right(self):
        """Coordinates of the right vertex of this node

        :return: (:class:`Point`) coordinates of the left vertex
        """
        return Point(self.x + self.w * math.sqrt(2) / 2.0, self.y)

    @property
    def top(self):
        """Coordinates of the top vertex of this node

        :return: (:class:`Point`) coordinates of the left vertex
        """
        return Point(self.x, self.y - self.w * math.sqrt(2)/2.0)

    @property
    def bottom(self):
        """Coordinates of the bottom vertex of this node

        :return: (:class:`Point`) coordinates of the left vertex
        """
        return Point(self.x, self.y + self.w * math.sqrt(2) / 2.0)


class Connector(NodeBase):

    def __init__(self, id, *points, **attrs):
        """Connector is a line path that connects two nodes of a diagram.

        It's also derived from NodeBase so it's possible to compute its center and assign a location

        :param viewport: (:class:`visualife.core.HtmlViewport` or :class:`visualife.core.SvgViewport`) where to draw this node
        :param id: (``string``) unique ID of this line
        :param points: (``list[Point]``) of points to connect with a line
        """
        super().__init__(id, average_point(points).x, average_point(points).y)
        self.points = points
        self.__attrs = attrs        # --- copy drawing parameters

    def draw(self, viewport, **kwargs):
        """Draw this dot node on a viewport.

        :param viewport: (:class:`visualife.core.HtmlViewport` or :class:`visualife.core.SvgViewport`) where to draw this node
        :param kwargs: provide style to draw this connecting line, see below (also accepts parameters to style the line: color, width etc.):

        :Keyword Arguments:
            * *mark* (``string``) --
              add a UML marker to this connector line; marker name must be one of the following:
                - ``"inheritance"`` to mark inheritance
                - ``"composition"`` to mark composition
                - ``"aggregation"`` to mark aggregation

            * *reverse_connector* (``boolean``) --
              draw arrows / markers in an opposite direction
        """

        params = repack_node_style_args(default_node_style, default_text_style, **self.__attrs)
        params = repack_node_style_args(params["node_style"], params["text_style"], **kwargs)

        ptx = [(p.x, p.y) for p in self.points]
        marker = None
        if "mark" in params["node_style"]:
            if params["node_style"]["mark"] == "inheritance":  marker = "inheritance_marker"
            elif params["node_style"]["mark"] == "composition": marker = "composition_marker"
            elif params["node_style"]["mark"] == "aggregation": marker = "aggregation_marker"

            if marker:
                if "reverse_connector" in params["node_style"]:
                    params["node_style"]["marker_start"] = marker+"_reversed"
                    print("params ",params)

                else:
                    params["node_style"]["marker_end"] = marker
        params["node_style"]["fill"] = "none"
        viewport.polyline(self.id, *ptx, **params["node_style"])


class Diagram:
    __composition_marker = [['M', 0, 0], ['L', 10, 5], ['L', 20, 0], ['L', 10, -5], ['z']]
    __inherit_marker = [['M', 0, -5], ['L', 10, 0], ['L', 0, 5], ['z']]

    def __init__(self, viewport, id, **kwargs):
        """Diagrams made out of rectangular shapes, possibly connected with lines.

        This class is intended to draw algorithm, UML or flow diagrams. Its methods allow easy placement of a few kinds
        of nodes: :class:`RectNode`, :class:`DotNode` and :class:`DiamondNode`

        The nodes may be connected by the following connector types:

            * *directly*
            * *X-Y* --
              connecting line goes first along X axis and then along Y axis to reach the end point
            * *Y-X* --
              connecting line goes first along Y axis and then along X axis to reach the end point

        :param viewport: (:class:`visualife.core.HtmlViewport` or :class:`visualife.core.SvgViewport`) where to draw this diagram
        :param id: (``string``) unique ID of this diagram
        :param kwargs: see below

        :Keyword arguments:
            * *autoconnect* (``boolean``) --
              if true (which is the default), nodes will be automatically connected with lines. Say ``False``
              to globally switch *autoconnect* for this diagram. Connection to a particular node may be also cancelled
              by passing ``autoconnect=False`` keyword argument to :meth:`add_node` method
        """
        self.__viewport = viewport
        self.__nodes = {}
        self.__id = id
        self.__node_style_defaults = default_node_style
        self.__text_style_defaults = default_text_style
        self.__last_id = 0
        self.__autoconnect = kwargs.get("autoconnect", True)

        self.__marker_size = 10
        viewport.start_marker("inheritance_marker", "-10 -10 20 20", 10, 0, self.__marker_size, self.__marker_size)
        viewport.path("inherit_arrow_path", Diagram.__inherit_marker, fill="white",
                              stroke=default_node_style["stroke"], stroke_width=default_node_style["stroke_width"])
        viewport.close_marker()

        viewport.start_marker("composition_marker", "-10 -10 30 30", 20, 0, self.__marker_size, self.__marker_size)
        viewport.path("composition_marker_path", Diagram.__composition_marker, fill=default_node_style["stroke"],
                              stroke=default_node_style["stroke"], stroke_width=default_node_style["stroke_width"])
        viewport.close_marker()

        viewport.start_marker("aggregation_marker", "-10 -10 30 30", 20, 0, self.__marker_size, self.__marker_size)
        viewport.path("aggregation_marker_path", Diagram.__composition_marker, fill="white",
                              stroke=default_node_style["stroke"], stroke_width=default_node_style["stroke_width"])
        viewport.close_marker()

        viewport.start_marker("inheritance_marker_reversed", "-10 -10 20 20", 10, 0, self.__marker_size, self.__marker_size,"auto-start-reverse")
        viewport.path("inherit_arrow_path_r", Diagram.__inherit_marker, fill="white",
                              stroke=default_node_style["stroke"], stroke_width=default_node_style["stroke_width"])
        viewport.close_marker()

        viewport.start_marker("composition_marker_reversed", "-10 -10 30 30", 20, 0, self.__marker_size, self.__marker_size,"auto-start-reverse")
        viewport.path("composition_marker_path_r", Diagram.__composition_marker, fill=default_node_style["stroke"],
                              stroke=default_node_style["stroke"], stroke_width=default_node_style["stroke_width"])
        viewport.close_marker()

        viewport.start_marker("aggregation_marker_reversed", "-10 -10 30 30", 20, 0, self.__marker_size, self.__marker_size,"auto-start-reverse")
        viewport.path("aggregation_marker_path_r", Diagram.__composition_marker, fill="white",
                              stroke=default_node_style["stroke"], stroke_width=default_node_style["stroke_width"])
        viewport.close_marker()
        viewport.add_filter("shadow")

    def __getitem__(self, node_id):
        """ Returns a node of this diagram

        :param node_id: (``string``) node ID, assigned to a node constructor
        :return: a node of this diagram
        """
        return self.__nodes[node_id]

    def add_node(self, node, **kwargs):
        """Adds a node to this diagram.

        This method can also connect the newly added node to the reference node

        :param node: (:class:`NodeBase`) a node to be added to this diagram
        :param kwargs: see below
        :return: a :class:`Connector` object if the added node is connected to another node, ``None`` otherwise

        :Keyword arguments:
            * *center_at* (:class:`Point`) --
              where to place the center of the node (x, y coordinates)
            * *below* (:class:`Point`) --
              place the node argument below the given node, e.g. another :class:`RectNode` or a :class:`Point`.
              The placed node will be centered in respect to the reference node
            * *right_below* (:class:`NodeBase`) --
              place the node argument below the given node, e.g. a :class:`RectNode`
              The placed node will be right-justified in respect to the reference node
            * *left_below* (:class:`NodeBase`) --
              place the node argument below the given node, e.g. a :class:`RectNode`
              The placed node will be left-justified in respect to the reference node
            * *above* (:class:`Point`) --
              place the newly created box above the given node, e.g. another :class:`RectNode` or a :class:`Point`.
              The placed node will be centered in respect to the reference node
            * *left_of* (:class:`Point`) --
              place the argument node on the left of the given node, e.g. another :class:`RectNode` or a :class:`Point`
            * *right_of* (:class:`Point`) --
              place the argument node on the right of the given node, e.g. another :class:`RectNode` or a :class:`Point`
            * *dx* (``number``) --
              a horizontal space left between two nodes when a relative placement is used;
              also the length of a linker for horizontal connections (``right_of=``, ``left_of=``)
            * *dy* (``number``) --
              a vertical space left between two nodes when a relative placement is used;
              length of a linker for vertical connections such as (``below=``, ``above=``)
            * *autoconnect* (``bool``) --
              if ``True`` (and this is the default), this method also create a connecting line
              i.e. creates an appropriate :class:`Connector` instance. *autoconnect* works only if the new node is placed
              *below*, *right_of* or *left_of* another node. Say ``autoconnect=False`` to switch it off for
              one this behavior.
            * *connect_xy* (:class:`Point`) --
              connect this box with a given :class:`Point` in the X-Y manner
            * *connect_yx* (:class:`Point`) --
              connect this box with a given :class:`Point` in the Y-X manner
            * *shift_by* (:class:`Point`) --
              a translation vector to be added to

        """
        self.__only_add(node)
        to_connect = []
        if "center_at" in kwargs:
            b = kwargs["center_at"]
            node.y = b.y
            node.x = b.x
            return None
        elif "below" in kwargs:
            b = kwargs["below"].bottom
            dy = kwargs.get("dy", default_segment_length)
            node.y = b.y + float(dy) + node.height / 2.0
            node.x = b.x
            to_connect = [b,node.top]
        elif "right_below" in kwargs:
            b = kwargs["right_below"].right
            dy = kwargs.get("dy", default_segment_length)
            node.y = b.y + float(dy) + node.height / 2.0
            node.x = b.x - node.width / 2.0
            to_connect = [b, node.top]
        elif "left_below" in kwargs:
            b = kwargs["left_below"].left
            dy = kwargs.get("dy", default_segment_length)
            node.y = b.y + float(dy) + node.height / 2.0
            node.x = b.x + node.width/2.0
            to_connect = [b, node.top]
        elif "above" in kwargs:
            b = kwargs["above"].top
            dy = kwargs.get("dy", default_segment_length)
            node.y = b.y - float(dy) - node.height / 2.0
            node.x = b.x
            to_connect = [b, node.bottom]
        elif "right_of" in kwargs:
            dx = kwargs.get("dx", default_segment_length)
            b = kwargs["right_of"].right
            node.x = b.x + float(dx) + node.width / 2.0
            node.y = b.y
            to_connect = [b, node.left]
        elif "left_of" in kwargs:
            dx = kwargs.get("dx", default_segment_length)
            b = kwargs["left_of"].left
            node.x = b.x - float(dx) - node.width / 2.0
            node.y = b.y
            to_connect = [b, node.right]

        if "shift_by" in kwargs:
            node += kwargs["shift_by"]

        if len(to_connect) > 0 and kwargs.get("autoconnect", self.__autoconnect):
            id = self.__id + ":" + str(self.__last_id)
            self.__last_id += 1
            c = Connector(id, *to_connect, **dict(**default_node_style, **kwargs))
            self.__only_add(c)
            return c

    def draw(self, viewport, **kwargs):
        """Draws all nodes of this diagram
        :param viewport: a viewport to draw nodes of this diagram
        :param kwargs: keyword arguments passed to :meth:`visualife.diagrams.NodeBase.draw` method to style the drawing
        """
        for n in self.__nodes.values():
            n.draw(viewport, **kwargs)

    @property
    def node_style(self):
        """Default style to draw nodes.

        A change to this dictionary will affect any nodes drawn after this call unless a node style has been
        overridden with ``**kwargs`` styling parameters

        :return: ``dict``
        """
        return self.__node_style_defaults

    @property
    def text_style(self):
        """Default style to draw node text.

        A change to this dictionary will affect any nodes drawn after this call unless a node style has been
        overridden with ``**kwargs`` styling parameters

        :return: ``dict``
        """
        return self.__text_style_defaults

    @property
    def id(self):
        """ID string of this diagram.

        This string is used e.g. to create unique IDs for this diagram's connectors
        :return: ``string``
        """
        return self.__id

    def highlight(self, state=True):
        """Removes or set highlight effect on all nodes of this diagram.

        :param state: (``boolean``) if ``True``, this node will be highlighted, otherwise any highlight effect
        will be cancelled
        """
        for n in self.__nodes.values(): n.highlight(state)

    def connect(self, *what, **kwargs):
        """Creates a :class:`Connector` node that connects the given points.

        :param what: (``list(:class:`Point`)``) list of points to connect
        :param kwargs: see below
        :return: a :class:`Connector` instance

        :Keyword Arguments:
            * *mark* (``string``) --
              a marker type; allowed parameter values are:
                - ``inheritance`` -- an arrow that marks class inheritance
        """
        id = self.__id + ":" + str(self.__last_id)
        self.__last_id += 1

        if len(what) < 2: return None       # --- nothing to connect
        if len(what) > 2:
            c = Connector(id, *what, **dict(**default_node_style, **kwargs))
            self.__only_add(c)
            return c
        else:
            p_from = what[0]
            p_to = what[1]

        if "connect_xy" in kwargs:          # --- from left / right to top
            if p_from.left.distance_to(p_to.top) < p_from.right.distance_to(p_to.top):
                connector = self.connect_xy(p_from.left, p_to.top)
            else:
                connector = self.connect_xy(p_from.right, p_to.top)
        elif "connect_yx" in kwargs:        # --- from bottom to left / right
            if p_to.left.distance_to(p_from.bottom) < p_to.right.distance_to(p_from.bottom):
                connector = self.connect_yx(p_from.bottom, p_to.left)
            else:
                connector = self.connect_yx(p_from.bottom, p_to.right)
        else:
            c = Connector(id, *what, **dict(**default_node_style, **kwargs))
            self.__only_add(c)
            return c

        return connector

    def connect_xy(self, start, stop,**kwargs):
        """Adds an X-Y connector between the two given nodes.

        This method connects ``start`` and ``stop`` nodes with an X-Y connector

        :param start: (:class:`Point`) start point of the connector
        :param stop: (:class:`Point`) end point of the connector
        :return: (:class:`Connector`) a connector instance
        """
        id = self.__id + ":" + str(self.__last_id)
        self.__last_id += 1
        coords = [start, Point(stop.x, start.y), stop]
        self.__only_add(Connector(id, *coords, **dict(**default_node_style, **kwargs)))
        return self.__nodes[id]

    def connect_yx(self, start, stop,**kwargs):
        """Adds an Y-X connector between the two given nodes.

        This method connects ``start`` and ``stop`` nodes with an Y-X connector

        :param start: (:class:`Point`) start point of the connector
        :param stop: (:class:`Point`) end point of the connector
        :return: (:class:`Connector`) a connector instance
        """

        id = self.__id + ":" + str(self.__last_id)
        self.__last_id += 1
        coords = [start, Point(start.x, stop.y), stop]
        self.__only_add(Connector(id, *coords, **dict(**default_node_style, **kwargs)))
        return self.__nodes[id]

    def max_x(self):
        """Returns maximum X coordinate of all elements of this diagram

        :return: maximum X  coordinate of any element of this diagram
        """

        max_x = self.__nodes[0].bottom.x
        for n in self.__nodes[1:]: max_x = max(max_x, n.bottom.x)

    def max_y(self):
        """Returns maximum Y coordinate of all elements of this diagram

        :return: maximum Y  coordinate of any element of this diagram
        """
        max_y = self.__nodes[0].bottom.y
        for n in self.__nodes[1:]:
            max_y = max(max_y, n.bottom.y)
        return max_y

    def __only_add(self, node):
        self.__nodes[node.id] = node

