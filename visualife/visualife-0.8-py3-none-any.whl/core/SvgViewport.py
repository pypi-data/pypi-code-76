#! /usr/bin/env python 

from visualife.core.styles import create_style
from math import pi, sin, cos


class SvgViewport:
    default_drawing_style = """
    stroke:black;
    """
    """Default style for Svg- and HtmlViewport"""
    default_text_style = """stroke-width:0;
    font-size: 10px;
    font-family:sans-serif;
    font-weight:normal;
    text-anchor:middle;
    color: black;
    """
    """Default text style for Svg- and HtmlViewport"""

    # __slots__ = ['__viewport_width','__viewport_height', '__style', '__y_0', '__x_0',
    #            '__file_handler', '__file_name', '__innerHTML', '__text_style']

    def __init__(self, file_name, x_min, y_min, x_max, y_max, color="transparent", style=default_drawing_style,
                 text_style=default_text_style):
        """
        Defines a viewport that saves a drawing into an SVG file

        :param file_name: (``string``) name of file to write output svg

        """

        self.__file_name = file_name
        self.__file_handler = open(file_name, "w") if len(file_name) > 0 else None
        self.__x_0 = x_min
        self.__y_0 = y_min
        self.__viewport_width = x_max - x_min
        self.__viewport_height = y_max - y_min
        self.__style = style
        self.__text_style = text_style

        self.__set_clean_viewport()

        if color != "transparent":
            self.__innerHTML += """<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" id="bg" style="fill:%s" />\n""" % (
                self.__x_0, self.__y_0, self.__viewport_width, self.__viewport_height, color)

    def __set_clean_viewport(self):

        self.__innerHTML = """<svg viewBox="%.1f %.1f %.1f %.1f" xmlns="http://www.w3.org/2000/svg" version="1.1">\n""" \
                           % (self.__x_0, self.__y_0, self.__viewport_width + self.__x_0,
                              self.__viewport_height + self.__y_0)

        # if it's not called by HtmlViewport print <style> tag
        if self.__file_name != '':
            self.__innerHTML += """<style>
            .default_text_style {%s}
            .default_drawing_style {%s}
            </style>\n""" % (self.__text_style, self.__style)

    def viewport_name(self):
        """Returns the name if this viewport, which is always "SVG"

        The method allows dynamic distinction between SVG and HTML viewports
        """
        return "SVG"

    def set_background(self, color):
        """Sets the background color - specially needed after clear() method"""
        self.__innerHTML += """<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" id="bg" style="fill:%s" />\n""" % ( \
            self.__x_0, self.__y_0, self.__viewport_width, self.__viewport_height, color)

    @property
    def style(self):
        """Defines the default drawing style

          :getter: returns the style
          :type: ``string``
        """
        return self.__style

    @style.setter
    def style(self, new_drawing_css):
        self.__style = new_drawing_css
        if self.__file_name != '':
            self.__innerHTML += """<style> .default_drawing_style {%s} </style>\n""" % self.__style

    @property
    def text_style(self):
        """Defines the default style for drawing text

          :getter: returns the text style
          :type: ``string``
        """
        return self.__text_style

    @text_style.setter
    def text_style(self, new_text_css):
        self.__text_style = new_text_css
        if self.__file_name != '':
            self.__innerHTML += """<style> .default_text_style {%s} </style>\n""" % self.__text_style

    def get_width(self):
        """
        Returns viewport_width
        """
        return self.__viewport_width

    def get_height(self):
        """
        Returns viewport height
        """
        return self.__viewport_height

    @property
    def innerHTML(self):
        """
        Returns innerHTML
        """
        return self.__innerHTML

    def close(self):
        """
        Closes SVG file
        """
        self.__innerHTML += "</svg>"
        if self.__file_name == "":
            return self.__innerHTML
        else:
            self.__file_handler.write(self.__innerHTML)
            self.__file_handler.close()

    def clear(self):
        """
        Clears SVG file
        """
        self.__set_clean_viewport()

    def error_msg(self, msg):
        """
        Prints error message.

        This polymorphic method prints a given error message to sys.stderr;
        HtmlViewport will print to browser's console
        """
        #        print(msg, file=sys.stderr)
        print(msg)

    def scale_x(self):
        """Return 1"""
        return 1

    def scale_y(self):
        """Return 1"""
        return 1

    def text_length(self, text, **kwargs):
        """ Measures the dimensions (in pixels) of a text as it would appear on a page

        :param text: text to be drawn
        :param kwargs: styling parameters as to be sent to ``SvgViewport.text()`` method
        :return: width and height of the text element, in pixels
        """
        n_chars = len(text)
        font_size = kwargs.get("font_size")
        return 0.7 * n_chars * font_size, font_size

    @staticmethod
    def __points_as_string(points):
        str = ""
        for p in points: str += "%.2f,%.2f " % (p[0], p[1])
        return str[:-1]

    def __prepare_attributes(self, **kwargs):
        """Parses attributes that are common for SVG elements

        :param kwargs: see below

        :Keyword Arguments:
            * *translate* (``list(number)`` or ``string``) --
              provides two coordinates for translation
            * *rotate* (``number``) --
              provide angle of rotation
            * *marker_end* (``string``) --
              marker symbol to be attached to the end of a line
            * *marker_start* (``string``) --
              marker symbol to be attached to the beginning of a line
            * *marker_mid*  (``string``) --
              marker symbol to be attached in the middle of a line
            * *Class* (``string``) --
              provide CSS class name for an element (**Note** that it starts with capital 'C' since "class" is a Python keyword)
            * *transform* (``string``) --
              provide a transformation string in SVG notation
        """

        attrs = create_style(**kwargs)
        transform = ""
        if "Class" in kwargs:
            attrs += " class='%s' " % kwargs['Class']
        else:
            attrs += " class=' default_drawing_style ' "
        if "translate" in kwargs:
            val = kwargs["translate"]
            if isinstance(val, list):
                transform = "translate(%.1f %.1f)" % (val[0], val[1])
            elif isinstance(val, str):
                transform = "translate(" + val + ")"
            else:
                self.error_msg("ERROR: unknown translate coordinates: " + str(val))
        if "rotate" in kwargs:
            transform += "rotate(" + kwargs["rotate"] + ")"
        if len(transform) > 0:
            attrs += " transform='" + transform + "'"
        if "marker_start" in kwargs:
            print("mark start")
            attrs += " marker-start='url(#" + kwargs["marker_start"] + ")' "
        if "marker_end" in kwargs:
            print("mark end")
            attrs += " marker-end='url(#" + kwargs["marker_end"] + ")' "
        if "marker_mid" in kwargs:
            attrs += " marker-mid='url(#" + kwargs["marker_mid"] + ")' "
        if "filter" in kwargs:
            attrs += " filter='url(#" + kwargs["filter"] + ")' "

        return attrs

    def radial_gradient(self, id_str, stop1, stop2, **kwargs):
        """Adds radial gradient to an element with a given id

        :param id_str: id of a element you want to add radial gradient
        :param stop1: list or a tuple with first stop in the order [offset,color,opacity]
        :param stop2: list or a tuple with second stop in the order [offset,color,opacity]

        :Keyword Arguments:
            * *cx* (``string``) --
              This attribute defines the x coordinate of the end circle of the radial gradient, default is "50%"
            * *cy* (``number``) --
              This attribute defines the y coordinate of the end circle of the radial gradient, default is "50%"
            * *fx* (``string``) --
              This attribute defines the x coordinate of the start circle of the radial gradient, default is "50%"
            * *fy* (``string``) --
              This attribute defines the y coordinate of the start circle of the radial gradient, default is "50%"
            * *r*  (``string``) --
              This attribute defines the radius of the end circle of the radial gradient.
        """
        cx = kwargs.get("cx", '50%')
        fx = kwargs.get("fx", '50%')
        cy = kwargs.get("cy", '50%')
        fy = kwargs.get("fy", '50%')
        r = kwargs.get("r", '50%')
        self.__innerHTML += """<radialGradient id=\"%s\" cx=\"%s\" cy=\"%s\" r=\"%s\" fx=\"%s\" fy=\"%s\" >\n""" \
                            % (id_str, cx, cy, r, fx, fy)

        self.__innerHTML += """<stop offset=\"%s\" style=\"stop-color:%s;stop-opacity:%s\" />\n""" % (
        stop1[0], stop1[1], stop1[2])
        self.__innerHTML += """<stop offset=\"%s\" style=\"stop-color:%s;stop-opacity:%s\" />\n""" % (
        stop2[0], stop2[1], stop2[2])
        self.__innerHTML += """</radialGradient>\n"""

    def start_clip_path(self, id_str):
        """Start a clipping path

        Anything that will be drawn on this viewport since now, will be recorded as a clipping path
        identified by a given ID string. That content can be used to clip other graphical elements, but itself
        will not be visible on the screen.

        A clipping path restricts the region to which drawing can be applied. Any part of the drawing that lie outside
        of the region bounded by the clipping path will not be drawn.

        Remember to use :meth:`close_clip_path` method to close this clipping path before doing anything else!
        Also note, that in the current implementation of the VL library only a group may be clipped.

        :param id_str: (``string``) a unique string that identifies this clipping path

        .. code-block:: python

            from browser import document
            from visualife.core import HtmlViewport
            from visualife.core.styles import color_by_name

            drawing = HtmlViewport(document['svg-clip'],0,0,200,200)

            drawing.start_clip_path("clip")
            for ix, iy in [(50, 50), (150, 50), (50, 150), (150, 150)]:
              drawing.circle("circ-%d-%d" % (ix, iy), ix, iy, 50)
            drawing.close_clip_path()

            drawing.start_group("g-rect", clip_path="clip")   # Note: VL can clip only a group!
            drawing.rect("rect1", 50, 50, 100, 100, stroke_width=3,
                fill=color_by_name("LightSteelBlue"), stroke=color_by_name("LightSlateGrey"))
            drawing.close_group()
            drawing.close()

        .. raw:: html

          <div> <svg  id="svg-clip" xmlns="http://www.w3.org/2000/svg" class="right" width="200" height="200"></svg> </div>
          <script type="text/python">
              from browser import document
              from visualife.core import HtmlViewport
              from visualife.core.styles import color_by_name

              drawing = HtmlViewport(document['svg-clip'],0,0,200,200)

              drawing.start_clip_path("clip")
              for ix, iy in [(50, 50), (150, 50), (50, 150), (150, 150)]:
                  drawing.circle("circ-%d-%d" % (ix, iy), ix, iy, 50)
              drawing.close_clip_path()

              drawing.start_group("g-rect", clip_path="clip")   # Note: VL can clip only a group!
              drawing.rect("rect1", 50, 50, 100, 100, stroke_width=3,
                    fill=color_by_name("LightSteelBlue"), stroke=color_by_name("LightSlateGrey"))
              drawing.close_group()
              drawing.close()
          </script>
        """
        self.__innerHTML += """<clipPath id="%s">\n""" % (id_str)

    def close_clip_path(self):
        """Closes an open clipping path"""
        self.__innerHTML += """</clipPath>\n"""

    def start_marker(self, id_str, view_box, ref_x, ref_y, width, height, orient="auto"):
        """Start a marker definition

        Anything that will be drawn on this viewport since now, will be recorded as a definition of a new marker.

        Remember to use :meth:`close_marker` method to close this marker definition!

        :param id_str: (``string``) a unique string that identifies this clipping path
        :param view_box: (``string`` or ``list``) defines a viewport for this marker
        :param ref_x: (``number``) defines the X coordinate for the reference point of the marker,
            i.e. the point by which this marker will be attached to its line
        :param ref_y: (``number``) defines the Y coordinate for the reference point of the marker,
            i.e. the point by which this marker will be attached to its line
        :param width: (``number``) width of the marker viewport
        :param height: (``number``) height of the marker viewport
        :param orient: ``"auto"`` or ``"auto-start-reverse"``

        .. code-block:: python

              from browser import document
              from visualife.core import HtmlViewport

              drawing = HtmlViewport(document['svg-marker'],0,0,300,100)

              drawing.start_marker("arrowhead", "0 0 10 10", 5, 5, 5, 5)
              drawing.path("arrowpath", [['M', 0, 0], ['L', 10, 5], ['L', 0, 10], ['z']])
              drawing.close_marker()
              drawing.line("l1", 145, 48, 10, 10, marker_end="arrowhead")
              drawing.line("l1", 149, 50, 10, 90, marker_end="arrowhead")
              drawing.line("l1", 153, 52, 250, 10, marker_end="arrowhead")
              drawing.line("l1", 155, 55, 250, 90, marker_end="arrowhead")
              drawing.close()

        .. raw:: html

          <div> <svg  id="svg-marker" xmlns="http://www.w3.org/2000/svg" class="right" width="300" height="100"></svg> </div>
          <script type="text/python">
              from browser import document
              from visualife.core import HtmlViewport

              drawing = HtmlViewport(document['svg-marker'],0,0,300,100)

              drawing.start_marker("arrowhead", "0 0 10 10", 5, 5, 5, 5)
              drawing.path("arrowpath", [['M', 0, 0], ['L', 10, 5], ['L', 0, 10], ['z']])
              drawing.close_marker()
              drawing.line("l1", 145, 48, 10, 10, marker_end="arrowhead")
              drawing.line("l1", 149, 50, 10, 90, marker_end="arrowhead")
              drawing.line("l1", 153, 52, 250, 10, marker_end="arrowhead")
              drawing.line("l1", 155, 55, 250, 90, marker_end="arrowhead")
              drawing.close()
          </script>
        """

        v = "viewBox="
        if isinstance(view_box, list) and len(view_box) >= 4:
            v += "'%.1f %.1f %.1f %.1f'" % (view_box[0], view_box[1], view_box[2], view_box[3])
        else:
            v += "'" + view_box + "'"
        self.__innerHTML += """<defs><marker id="%s" %s refX="%.1f" refY="%.1f" markerWidth="%.1f" markerHeight="%.1f" orient="%s">\n""" \
                            % (id_str, v, ref_x, ref_y, width, height, orient)

    def close_marker(self):
        """Closes an open marker definition"""
        self.__innerHTML += """</marker></defs>\n"""

    def add_filter(self,id_str,if_black=True):
        """Adds a filter to <defs> section of SVG
        """
        in_offset = "SourceAlpha"
        if if_black==False:
          in_offset = "SourceGraphic"

        self.__innerHTML+="""
        <defs>
          <filter id="shadow" x="0" y="0" width="200%" height="200%">
            <feOffset result="offOut" in="SourceAlpha" dx="8" dy="8" />
            <feGaussianBlur result="blurOut" in="offOut" stdDeviation="5" />
            <feBlend in="SourceGraphic" in2="blurOut" mode="normal" />
          </filter>
        </defs>
        """
        #%(id_str,in_offset)

    def start_group(self, id_str, **kwargs):
        """Start a new group

        Anything that will be drawn on this viewport since now, will be included in a group
        identified by a given ID string. A group may have its own styling parameters or a clipping path;
        they can be passed to this methods with ``**kwargs``. Use :meth:`close_group` method to close this group.

        :param id_str: (``string``) a unique string that identifies this group
        """
        if 'clip_path' in kwargs and kwargs['clip_path'] != "":
            clip_str = """ clip-path="url(#%s)" """ % kwargs['clip_path']
        else:
            clip_str = ""
        self.__innerHTML += """<g id="%s" %s %s>\n""" % (id_str, self.__prepare_attributes(**kwargs), clip_str)

    def close_group(self):
        """Close an open group"""
        self.__innerHTML += "</g>"

    def circles_group(self, gid, x, y, c, r, **kwargs):
        """Group of circles drawn in a single batch.

        This method has been devised to draw circles efficiently. All the circles will be placed in a single group.
        Graphics parameters from ``**kwargs`` fill be assigned to the group element. Therefore this method
        does not allow styling each circle separately except its radius and color.

        :param gid: (``string``) id assigned to the whole group of circles
        :param x: (``list(float)``) list of X coordinates
        :param y: (``list(float)``) list of Y coordinates
        :param c: (``color`` or ``list(color)``) list of colors for circles or a single color - the same for all circles
        :param r:  (``float`` or ``list(float)``) list of radii for circles or a single radii - the same for all circles
        :param kwargs: other graphics parameters assigned to this group rather than separately to each circle

        .. seealso:: :meth:`circle` method, which draws circles separately and allows to style them; to the contrary
          of this example, in the :meth:`circle` figure circles have different transparency and stroke

        .. code-block:: python

              from random import random
              from browser import document
              from visualife.core import HtmlViewport
              from visualife.core.styles import ColorRGB

              drawing = HtmlViewport(document['svg-circles'],0,0,600,150)
              x, y, c, r = [], [], [], []
              n_x, n_y = 20, 5
              for i in range(n_x):
                  for j in range(n_y):
                      x.append(i*30)
                      y.append(j*30)
                      c.append(ColorRGB(255, i*255/n_x, j*255/n_y))
                      r.append(random()*50)
              drawing.circles_group("circles-grp", x, y, c, r)
              drawing.close()

        .. raw:: html

          <div> <svg  id="svg-circles" xmlns="http://www.w3.org/2000/svg" class="right" width="600" height="150"></svg> </div>
          <script type="text/python">
              from random import random
              from browser import document
              from visualife.core.styles import ColorRGB
              from visualife.core import HtmlViewport

              drawing = HtmlViewport(document['svg-circles'],0,0,600,150)
              x, y, c, r = [], [], [], []
              n_x, n_y = 20, 5
              for i in range(n_x):
                  for j in range(n_y):
                      x.append(i*30)
                      y.append(j*30)
                      c.append(ColorRGB(255, i*255/n_x, j*255/n_y))
                      r.append(random()*30)
              drawing.circles_group("circles-grp", x, y, c, r)
              drawing.close()
          </script>
        """
        if not isinstance(r, list):
            r = [r]
        self.__innerHTML += """<g id="%s" %s>\n""" % (gid, self.__prepare_attributes(**kwargs))
        for i in range(len(x)):
            self.__innerHTML += \
                """<circle cx="%.1f" cy="%.1f" r="%.1f" id="%s" fill="%s" />\n""" % (
                    x[i], y[i], r[i % len(r)], gid + ":" + str(i), c[i % len(c)].__str__())
            # self.circle(gid + ":" + str(i), x[i], y[i], r[i % len(r)],
            #             **dict(**kwargs, fill=c[i % len(c)].__str__()))
        self.__innerHTML += "</g>"

    def squares_group(self, gid, x, y, c, a, **kwargs):
        """Group of squares drawn in a single batch.

        This method has been devised to draw squares efficiently. All the squares will be placed in a single group.
        Graphics parameters from ``**kwargs`` fill be assigned to the group element. Therefore this method
        does not allow styling each square separately except its radius and color.

        :param gid: (``string``) id assigned to the whole group of squares
        :param x: (``list(float)``) list of X coordinates
        :param y: (``list(float)``) list of Y coordinates
        :param c: (``color`` or ``list(color)``) list of colors for squares or a single color - the same for all squares
        :param a:  (``float`` or ``list(float)``) list of sides for squares or a single radii - the same for all squares
        :param kwargs: other graphics parameters assigned to this group rather than separately to each one

        """
        self.__innerHTML += """<g id="%s" %s>\n""" % (gid, self.__prepare_attributes(**kwargs))
        cl = "Class='" + kwargs["Class"] + "'" if "Class" in kwargs else ""
        for i in range(len(x)):
            self.__innerHTML += \
                """<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" id="%s" fill="%s" %s />\n""" % (
                    x[i] - a / 2, y[i] - a / 2, a, a, gid + ":" + str(i), c[i % len(c)].__str__(), cl)
        self.__innerHTML += "</g>"

    def lines_group(self, gid, x, y, c, **kwargs):
        """Group of lines drawn in a single batch.

        This method has been devised to draw lines efficiently. All the lines will be placed in a single group.
        Graphics parameters from ``**kwargs`` fill be assigned to the group element. Therefore this method
        does not allow styling each square separately except its radius and color.

        :param gid: (``string``) id assigned to the whole group of lines
        :param x: (``list(float)``) list of X coordinates
        :param y: (``list(float)``) list of Y coordinates
        :param c: (``color`` or ``list(color)``) list of colors for lines or a single color - the same for all lines
        :param kwargs: other graphics parameters assigned to this group rather than separately to each line

        """
        self.__innerHTML += """<g id="%s" %s>\n""" % (gid, self.__prepare_attributes(**kwargs))
        cl = "Class='" + kwargs["Class"] + "'" if "Class" in kwargs else ""
        for i in range(len(x)-1):
            self.__innerHTML += \
                """<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" id="%s" fill="%s" %s />\n""" \
            % (x[i], y[i], x[i+1], y[i+1], gid + ":" + str(i), c[i % len(c)].__str__(), cl)
        self.__innerHTML += "</g>"

    def squares_grid(self, gid, x0, y0, w, h, rows, columns, **kwargs):
        """Draws a grid of  rectangles.

        This method is intended to draws a grid of ``<rect>`` shapes as quickly as possible. Every
        rectangle has the same dimensions. They also have no color, which is to be applied later
        with DOM API. A rectangle of the grid in *i*-th column and *j*-th row (along X and Y axis, respectively)
        is assigned ``gid-i-j`` ID, where ``gid`` is the ID of the whole group.

        :param id_str: (``string``) unique ID string for the group containing rectangles
        :param x0: X coordinate of the top left corner of the rectangle bounding the grid
        :param y0: Y coordinate of the top left corner of the rectangle bounding the grid
        :param w: width of each rectangle
        :param h: height of each rectangle
        :param rows: number of rows of rectangles
        :param columns: number of columns of rectangles
        :param kwargs: see below

        :Keyword Arguments:
            * *margin* (``value``) -- separation between rectangles
            * *xmargin* (``value``) -- separation between rectangles along X axis
            * *ymargin* (``value``) -- separation between rectangles along Y axis
        All other arguments are passed to group construction method of the viewer

        .. code-block:: python

              from math import sin, cos
              from browser import document
              from visualife.core.styles import colormap_by_name
              from visualife.core import HtmlViewport

              drawing = HtmlViewport(document['svg-rect-grid'],0,0,630,150)
              drawing.squares_grid("grid", 2, 2, 4, 4, 126, 32, margin=1, stroke_width=0)
              drawing.close()
              palette = colormap_by_name("pinks", -1, 1)
              for i in range(126):
                  for j in range(32):
                      z = sin(i/20)*cos(j/10)
                      document["grid-"+str(i)+"-"+str(j)].style.fill = str(palette.color(z))

        .. raw:: html

          <div> <svg  id="svg-rect-grid" xmlns="http://www.w3.org/2000/svg" class="right" width="600" height="150"></svg> </div>
          <script type="text/python">
              from math import sin, cos
              from browser import document
              from visualife.core.styles import colormap_by_name
              from visualife.core import HtmlViewport

              drawing = HtmlViewport(document['svg-rect-grid'],0,0,630,150)
              drawing.squares_grid("grid", 2, 2, 4, 4, 126, 32, margin=1, stroke_width=0)
              drawing.close()
              palette = colormap_by_name("pinks", -1, 1)
              for i in range(126):
                  for j in range(32):
                      z = sin(i/20)*cos(j/10)
                      document["grid-"+str(i)+"-"+str(j)].style.fill = str(palette.color(z))
          </script>
        """

        self.__innerHTML += """<g id="%s" %s>\n""" % (gid, self.__prepare_attributes(**kwargs))

        d = kwargs.get("margin", 0)
        dx = w + kwargs.get("xmargin", d)
        dy = h + kwargs.get("ymargin", d)

        x = x0
        if "Class" in kwargs:
            whc = (" width='%.1f' height='%.1f' class='%s' " % (w, h, kwargs["Class"]))
        else:
            whc = (" width='%.1f' height='%.1f'" % (w, h))

        for i in range(rows):
            dxs = "%.1f'" % x
            y = y0
            id = gid + "-" + str(i)
            for j in range(columns):
                self.__innerHTML += "\t<rect x='" + dxs + whc + " y='%.1f' id='%s' />\n" % (y, id + "-" + str(j))
                y += dy
            x += dx

        self.__innerHTML += "</g>"

    def triangle_group(self, gid, x, y, c, r, **kwargs):
        """Group of triangles drawn in a single batch.

        This method has been devised to draw triangles efficiently. All the triangles will be placed in a single group.
        Graphics parameters from ``**kwargs`` fill be assigned to the group element. Therefore this method
        does not allow styling each square separately except its radius and color.

        :param gid: (``string``) id assigned to the whole group of triangles
        :param x: (``list(float)``) list of X coordinates
        :param y: (``list(float)``) list of Y coordinates
        :param c: (``color`` or ``list(color)``) list of colors for triangles or a single color - the same for all triangles
        :param r: (``float`` or ``list(float)``) list of sides for triangles or a single number - the same for all triangles
        :param kwargs: other graphics parameters assigned to this group rather than separately to each triangle

        """

        self.__innerHTML += """<g id="%s" %s>\n""" % (gid, self.__prepare_attributes(**kwargs))
        for i in range(len(x)):
            self.triangle(gid + ":" + str(i), x[i], y[i], r, **dict(**kwargs, fill=c[i % len(c)].__str__()))
        self.__innerHTML += "</g>"

    def rhomb_group(self, gid, x, y, c, r, **kwargs):
        """Group of rhombs drawn in a single batch.

        This method has been devised to draw rhombs efficiently. All the rhombs will be placed in a single group.
        Graphics parameters from ``**kwargs`` fill be assigned to the group element. Therefore this method
        does not allow styling each square separately except its radius and color.

        :param gid: (``string``) id assigned to the whole group of rhombs
        :param x: (``list(float)``) list of X coordinates
        :param y: (``list(float)``) list of Y coordinates
        :param c: (``color`` or ``list(color)``) list of colors for rhombs or a single color - the same for all rhombs
        :param r: (``float`` or ``list(float)``) list of sides for rhombs or a single number - the same for all rhombs
        :param kwargs: other graphics parameters assigned to this group rather than separately to each rhomb

        """
        self.__innerHTML += """<g id="%s" %s>\n""" % (gid, self.__prepare_attributes(**kwargs))
        for i in range(len(x)):
            self.rhomb(gid + ":" + str(i), x[i], y[i], r, **dict(**kwargs, fill=c[i % len(c)].__str__()))
        self.__innerHTML += "</g>"

    def image(self, img_id, x, y, w, h, href, **kwargs):
        """ Draws a raster image in this SVG viewport
        :param img_id: (``string``) element id, assigned to this image
        :param x: (``float``) X
        :param y: (``float``) Y
        :param w: (``float``) width of the image
        :param h: (``float``) height of the image
        :param href: (``string``) file name with path
        :param kwargs:
        :return:
        """
        self.__innerHTML += """<image id="%s" href="%s" x="%.1f" y="%.1f" height="%.1f" width="%.1f" />""" \
                            % (img_id, href, x, y, h, w)

    def rect(self, id_str, x, y, w, h, **kwargs):
        """Creates a <rect> element

        :param id_str: (``string``) to be used as the ID of the element
        :param x: (``number``) x coordinate of the top left corner
        :param y: (``number``) y coordinate of the top left corner
        :param w: (``number``) width of the rectangle
        :param h: (``number``) height of the rectangle
        :param kwargs: see below

        :Keyword Arguments:
            * *rx* (``number``) --
              x radius for rounded corners
            * *ry* (``number``) --
              y radius for rounded corners
            * *angle* (``number``) --
              angle to rotate the rectangle around its center (in degrees!)

        Keyword arguments dictionary is also passed to a :meth:`visualife.core.styles.create_style` method to
        prepare a style for drawing

        .. code-block:: python

            from random import shuffle, random
            from browser import document
            from visualife.core import HtmlViewport
            from visualife.core.styles import ColorRGB

            drawing = HtmlViewport(document['svg-rect'],0,0,600,150)
            n_x, n_y = 20, 5
            points = [(i,j) for i in range(n_x) for j in range(n_y)]
            shuffle(points)
            for i, j in points:
                  drawing.rect("r-%d-%d" % (i, j), i*30, j*30, 25 + random()*10, 25 + random()*10, stroke="darker",
                    fill=str(ColorRGB(255, i*255/n_x, j*255/n_y)), angle=(10-random()*20), fill_opacity=random())
            drawing.close()

        .. raw:: html

          <div> <svg  id="svg-rect" xmlns="http://www.w3.org/2000/svg" class="right" width="600" height="150"></svg> </div>
          <script type="text/python">
            from random import shuffle, random
            from browser import document
            from visualife.core import HtmlViewport
            from visualife.core.styles import ColorRGB

            drawing = HtmlViewport(document['svg-rect'],0,0,600,150)
            n_x, n_y = 20, 5
            points = [(i,j) for i in range(n_x) for j in range(n_y)]
            shuffle(points)
            for i, j in points:
                  drawing.rect("r-%d-%d" % (i, j), i*30, j*30, 25 + random()*10, 25 + random()*10, stroke="darker",
                    fill=str(ColorRGB(255, i*255/n_x, j*255/n_y)), angle=(10-random()*20), fill_opacity=random())
            drawing.close()
          </script>

        """

        s = " "
        if "rx" in kwargs: s += "rx='%.1f' " % kwargs["rx"]
        if "ry" in kwargs: s += "ry='%.1f' " % kwargs["ry"]
        if "angle" in kwargs:
            s += "transform='rotate(%.1f %.1f %.1f)'" % (float(kwargs["angle"]), x + w / 2.0, y + h / 2.0)

        self.__innerHTML += \
            """<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" id="%s" %s %s/>\n""" % ( \
                x, y, w, h, id_str, self.__prepare_attributes(**kwargs), s)

    def square(self, id_str, x, y, a, **kwargs):
        """Creates a square as <rect> element  

        :param id_str: string to be used as the ID of the element
        :param x: (``number``) x coordinate of the center
        :param y: (``number``) y coordinate of the center
        :param a: (``number``) side length
        :param kwargs: see below

        :Keyword Arguments:
            * *rx* (``number``) --
              x radius for rounded corners
            * *ry* (``number``) --
              y radius for rounded corners
            * *angle* (``number``) --
              angle to rotate the rectangle around its center

        Keyword arguments dictionary is also passed to a :meth:`visualife.core.styles.create_style` method to
        prepare a style for drawing
        """
        self.__innerHTML += \
            """<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" id="%s" %s />\n""" % ( \
                x - a / 2, y - a / 2, a, a, id_str, self.__prepare_attributes(**kwargs))

    def circle(self, id_str, x, y, r, **kwargs):
        """Creates a <circle> element  

        :param id_str: string to be used as the ID of the element
        :param x: (``number``) x coordinate of the center
        :param y: (``number``) y coordinate of the center
        :param r: (``number``) radius of this circle
        :param kwargs: parameters to prepare style attributes

        .. seealso:: :meth:`circles_group` method, which draws multiple circles in a single batch. In that example
          however all circles have the same stroke and transparency

        .. code-block:: python

            from random import random
            from browser import document
            from visualife.core import HtmlViewport
            from visualife.core.styles import ColorRGB

            drawing = HtmlViewport(document['svg-circle'],0,0,600,150)
            n_x, n_y = 20, 5
            for i in range(n_x):
              for j in range(n_y):
                  drawing.circle("c-%d-%d" % (i, j), i*30, j*30, random()*50, stroke="darker",
                    fill=str(ColorRGB(255, i*255/n_x, j*255/n_y)), fill_opacity=random())
            drawing.close()

        .. raw:: html

          <div> <svg  id="svg-circle" xmlns="http://www.w3.org/2000/svg" class="right" width="600" height="150"></svg> </div>
          <script type="text/python">
            from random import random
            from browser import document
            from visualife.core.styles import ColorRGB
            from visualife.core import HtmlViewport

            drawing = HtmlViewport(document['svg-circle'],0,0,600,150)
            n_x, n_y = 20, 5
            for i in range(n_x):
              for j in range(n_y):
                  drawing.circle("c-%d-%d" % (i, j), i*30, j*30, random()*50, stroke="darker",
                    fill=str(ColorRGB(255, i*255/n_x, j*255/n_y)), fill_opacity=random())
            drawing.close()
          </script>
        """

        self.__innerHTML += \
            """<circle cx="%.1f" cy="%.1f" r="%.1f" id="%s" %s />\n""" % ( \
                x, y, r, id_str, self.__prepare_attributes(**kwargs))

    def line(self, id_str, xb, yb, xe, ye, **kwargs):
        """Creates a <line> element  

        :param id_str: string to be used as the ID of the element
        :param xb: x coordinate of line begin
        :param yb: y coordinate of line begin
        :param xe: side length of line end
        :param ye: side length of line end
        :param kwargs: parameters to prepare style attributes

        """
        self.__innerHTML += \
            """<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" id="%s" %s />\n""" \
            % (xb, yb, xe, ye, id_str, self.__prepare_attributes(**kwargs))

    def polyline(self, id_str, *points, **kwargs):
        """Creates a <polyline> element

        :param id_str: (``string``) string to be used as the ID of the element
        :param points: (``list((number,number))``) a list of points; each point must be a two-element tuple or list
        :param kwargs: parameters to prepare style attributes

        .. code-block:: python

            from random import random
            from browser import document
            from visualife.core import HtmlViewport

            drawing = HtmlViewport(document['svg-polyline'],0,0,600,150)
            rho = 0.5
            p = [[0,0]]
            for i in range(1, 100):
                p.append([i*6, p[-1][1]*(1-rho) + rho*(1-2*random())])
            for pi in p: pi[1] = pi[1]*50 + 75
            drawing.polyline("polyline", p, fill="none", stroke_width=1)
            drawing.close()

        .. raw:: html

          <div> <svg  id="svg-polyline" xmlns="http://www.w3.org/2000/svg" class="right" width="600" height="150"></svg> </div>
          <script type="text/python">
            from random import random
            from browser import document
            from visualife.core import HtmlViewport

            drawing = HtmlViewport(document['svg-polyline'],0,0,600,150)
            rho = 0.5
            p = [[0,0]]
            for i in range(1, 100):
                p.append([i*6, p[-1][1]*(1-rho) + rho*(1-2*random())])
            for pi in p: pi[1] = pi[1]*50 + 75
            drawing.polyline("polyline", p, fill="none", stroke_width=1)
            drawing.close()
          </script>
        """
        print("kw ",kwargs)
        str = ""
        if len(points) == 1: points = points[0]
        for p in points:
            str += "%.1f,%.1f " % (p[0], p[1])
        self.__innerHTML += """<polyline points="%s" id="%s" %s/>\n""" \
                            % (str, id_str, self.__prepare_attributes(**kwargs))

    def ellipse(self, id_str, x, y, rx, ry, **kwargs):
        """Creates a <ellipse> element  

        :param id_str: string to be used as the ID of the element
        :param x: x coordinate of a center
        :param y: y coordinate of a center
        :param rx: x radius length 
        :param ry: y radius length 
        :param kwargs: parameters to prepare style attributes

        """
        self.__innerHTML += \
            """<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" id="%s" %s />\n""" \
            % (x, y, rx, ry, id_str, self.__prepare_attributes(**kwargs))

    def polygon(self, id_str, points, **kwargs):
        """
        """
        str = SvgViewport.__points_as_string(points)
        self.__innerHTML += \
            """<polygon points="%s" id="%s"  %s />\n""" % (str, id_str, self.__prepare_attributes(**kwargs))

    def triangle(self, id_str, x, y, r, **kwargs):
        """Draws a triangle

        :param id_str: id string of a created element
        :param x: x coordinate for this element
        :param y: y coordinate for this element
        :param r: radius value
        """
        angle = 2 * pi / 3.0
        self.polygon(id_str, [[x + r * sin(0 * angle), y + r * cos(0 * angle)],
                              [x + r * sin(1 * angle), y + r * cos(1 * angle)],
                              [x + r * sin(2 * angle), y + r * cos(2 * angle)]],
                     **kwargs)

    def rhomb(self, id_str, x, y, r, **kwargs):
        """Draws a rhomb

        :param id_str: id string of a created element
        :param x: x coordinate for this element
        :param y: y coordinate for this element
        :param r: radius value
        """
        self.polygon(id_str, [[x, y + r], [x + r, y], [x, y - r], [x - r, y]], **kwargs)

    def path(self, id_str, elements, **kwargs):
        """Draws a path


        :param id_str:
        :param elements:
        :param kwargs:

       .. code-block:: python

              from browser import document
              from visualife.core import HtmlViewport

              drawing = HtmlViewport(document['svg-path'],0,0,300,100)
              path_1 = [["M", 20, 50], ["C", 20,80, 80, 80, 80, 50]]
              path_2 = [["M", 20, 20], ["L", 80, 20], ["L", 20, 50], ["L", 80, 50], ["L", 20, 80], ["L", 80, 80]]
              path_3 = [["M", 20, 50], ["A", 50, 25, 0, 0, 1, 80, 80]]
              path_style = {"fill": "none", "stroke": "#000", "stroke_linecap": "round",
                    "stroke_linejoin": "round", "stroke_width": "5"}
              drawing.rect("r1", 10, 10, 80, 80, stroke='black', stroke_width='1', fill='gainsboro')
              drawing.path("p1", path_1, **path_style)
              drawing.rect("r2", 110, 10, 80, 80, stroke='black', stroke_width='1', fill='gainsboro')
              drawing.path("p2", path_2, **path_style, translate=[100, 0])
              drawing.rect("r3", 210, 10, 80, 80, stroke='black', stroke_width='1', fill='gainsboro')
              drawing.path("p3", path_3, **path_style, translate=[200, 0])
              drawing.close()

       .. raw:: html

          <div> <svg  id="svg-path" xmlns="http://www.w3.org/2000/svg" class="right" width="400" height="200"></svg> </div>
          <script type="text/python">
              from browser import document
              from visualife.core import HtmlViewport

              drawing = HtmlViewport(document['svg-path'],0,0,300,100)
              path_1 = [["M", 20, 50], ["C", 20,80, 80, 80, 80, 50]]
              path_2 = [["M", 20, 20], ["L", 80, 20], ["L", 20, 50], ["L", 80, 50], ["L", 20, 80], ["L", 80, 80]]
              path_3 = [["M", 20, 50], ["A", 50, 25, 0, 0, 1, 80, 80]]
              path_style = {"fill": "none", "stroke": "#000", "stroke_linecap": "round",
                    "stroke_linejoin": "round", "stroke_width": "5"}
              drawing.rect("r1", 10, 0, 80, 80, stroke='black', stroke_width='1', fill='gainsboro')
              drawing.path("p1", path_1, **path_style)
              drawing.rect("r2", 110, 0, 80, 80, stroke='black', stroke_width='1', fill='gainsboro')
              drawing.path("p2", path_2, **path_style, translate=[100, 0])
              drawing.rect("r3", 210, 0, 80, 80, stroke='black', stroke_width='1', fill='gainsboro')
              drawing.path("p3", path_3, **path_style, translate=[200, 0])
              drawing.close()
          </script>
        """
        str = ""
        for e in elements:
            str += " " + e[0]
            if len(e) == 2 and isinstance(e[1], tuple):
                for coord in e[1]:
                    str += " %d" % coord if isinstance(coord, int) else " %.1f" % coord
            else:
                for coord in e[1:]:
                    str += " %d" % coord if isinstance(coord, int) else " %.1f" % coord
        self.__innerHTML += """<path d="%s" id="%s" %s />\n""" % (str, id_str, self.__prepare_attributes(**kwargs))

    def text(self, id_str, x, y, text, **kwargs):
        """Adds text to the viewport

        :param id_str: id string of an element you want to add text to 
        :param x: x coordinate for text
        :param y: y coordinate for text
        :param text: text to write - ``string`` or ``list(string)`` - in this case every list element will be written in a new line

        """

        dy = kwargs.get('dy', "1.0em")
        angle = kwargs.get('angle', 0)

        font_size = kwargs.get('font_size', 10)
        if isinstance(text, list): y -= font_size * (len(text)) / 2.0

        if angle == 0:
            svg_txt = """<text class= 'default_text_style' x="%.1f" y="%.1f" id='%s' %s>""" % (
            x, y, id_str, create_style(**kwargs))
        else:
            svg_txt = """<text class= 'default_text_style' x="%.1f" y="%.1f" id='%s' %s transform="rotate(%.1f %.1f %.1f)"> """ % (
                x, y, id_str, create_style(**kwargs), angle, x, y)

        if isinstance(text, list):
            svg_txt += "\n"
            # x = 0
            for it in text:
                svg_txt += """<tspan dy="%s" x="%.1f">%s</tspan>\n""" % (dy, x, it)
            svg_txt += "</text>\n"
        else:
            svg_txt += str(text) + "</text>\n"

        self.__innerHTML += svg_txt
