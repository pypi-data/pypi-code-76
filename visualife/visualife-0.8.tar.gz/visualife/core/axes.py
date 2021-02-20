#! /usr/bin/env python
"""Provides all Axis classes.

These are used by Plot class to draw and plot. There is no need to create them manually. User may however change
properties of an axis as shown below:


.. code-block:: python

  from browser import document
  from core.HtmlViewport import HtmlViewport
  from core.Plot import Plot

  drawing = HtmlViewport(document['svg'],0,0,600,400)
  pl = Plot(drawing,50,550,50,350,0.0,0.5,0.0,0.5, axes_definition="LB")
  left_axis = pl.axes["L"]
  bottom_axis = pl.axes["B"]
  pl.draw_axes()
  drawing.close()
  drawing.finalize()

.. raw:: html

  <div> <svg  id="svg" xmlns="http://www.w3.org/2000/svg" class="right" width="600" height="400"></svg> </div>
  <script type="text/python">
      from browser import document
      from core.HtmlViewport import HtmlViewport
      from core.Plot import Plot

      drawing = HtmlViewport(document['svg'],0,0,600,400)
      pl = Plot(drawing,50,550,50,350,0.0,0.5,0.0,0.5, axes_definition="LB")
      left_axis = pl.axes["L"]
      bottom_axis = pl.axes["B"]
      pl.draw_axes()
      drawing.close()
      drawing.finalize()
  </script>
"""
from math import fabs
from visualife.core.styles import get_color, get_font_size


class Axis:
    """Represents an arbitrary axis of a plot.

       The direction of the axis depends on the derived classes (X or Y).
    """

    # __slots__ = ['__dict__','__size','__min_screen_coordinate','__max_screen_coordinate','__small_screen_tics',
    #             '__big_screen_tics','__tics_labels','__tics_width','__are_tics_inside','__axis_location',
    #             '__min_data_value','__max_data_value', '__label','__label_x','__label_y', '__label_shift',
    #             '__grid','__label_font_size','__ticslabel_font_size','__tics_vertical','__show_tics',
    #             __show_tics_labels]

    def __init__(self, min_screen, max_screen, min_data, max_data):
        """Creates an instance of an axis

           :param min_screen:
             starting point to draw this axis in screen coordinates
           :type min_screen: ``float``
           :param max_screen:
             end point to draw this axis in screen coordinates
           :type max_screen: ``float``
           :param min_data:
             minimum value covered by this axis, assigned to ``min_screen``
           :type min_data: ``float``
           :param max_data:
             maximum value covered by this axis, assigned to ``max_screen``
           :type max_data: ``float``
        """

        self.__min_screen_coordinate = min_screen
        self.__max_screen_coordinate = max_screen
        self.__small_screen_tics = []
        self.__big_screen_tics = []
        self.__tics_labels = []
        self.__tics_width = fabs((max_screen - min_screen) / 100)
        self.__are_tics_inside = True
        self.__axis_location = None
        self.__min_data_value = min_data
        self.__max_data_value = max_data
        self.__label = ''
        self.__label_x = 0
        self.__label_y = 0
        self.__label_shift = fabs((max_screen - min_screen) / 15)
        self.__grid = []
        self.__label_font_size = get_font_size((max_screen - min_screen) / 45)
        self.__tics_label_font_size = get_font_size((max_screen - min_screen) / 50)
        self.__tics_vertical = False
        self.__show_tics = True
        self.__show_tics_labels = True
        self.__n_tics = ()

        # ---------properties overwritten from SvgElement class
        self.fill = "Black"
        self.stroke = "Black"
        self.stroke_width = 1

    @property
    def min_screen_coordinate(self):
        """Returns the minimal coordinate of this axis in screen units

            For X axis this will position of the leftmost point, for Y axis - position of the lowest point of this axis
        """
        return self.__min_screen_coordinate

    @property
    def max_screen_coordinate(self):
        """Returns the maximum coordinate of this axis in screen units

            For X axis this will position of the rightmost point, for Y axis - position of the highest point of this axis
        """
        return self.__max_screen_coordinate

    @property
    def small_screen_tics(self):
        """Returns a list of tics positions in screen coordinates"""
        return self.__small_screen_tics

    @property
    def big_screen_tics(self):
        """Returns a list of tics positions in screen coordinates"""
        return self.__big_screen_tics

    @property
    def tics_labels(self):
        """Returns a list of tics labels"""
        return self.__tics_labels

    def add_tics_labels(self, format_string="%.2f"):
        """Sets tics labels using the given format to convert real values into text
        """
        self.__tics_labels = []
        for tx in self.big_screen_tics:
            t = str(format_string % self.axis_coordinate(tx))
            self.__tics_labels.append(t)

        return self.__tics_labels

    @property
    def tics_width(self):
        """the length (vertical for X, horizontal for Y axis) of tics - the same value for all of them

            :getter: returns the current width of tics
            :setter: sets the width of tics
            :type: ``float``
        """
        return self.__tics_width

    @tics_width.setter
    def tics_width(self, tics_width):
        self.__tics_width = tics_width

    @property
    def tics_vertical(self):
        """True if tics are vertical, false if they are horizontal

            :getter: returns the current arrangement of tics
            :setter: sets the arrangement of tics
            :type: ``boolean``
        """
        return self.__tics_vertical

    @tics_vertical.setter
    def tics_vertical(self, are_vertical):
        self.__tics_vertical = are_vertical

    @property
    def min_data_value(self):
        """ the smallest data value fitting into this axis, i.e. the lower range limit of the plotted data

            :getter: returns the left value of the data range
            :setter: sets the left value of the data range
            :type: ``float``
        """
        return self.__min_data_value

    @min_data_value.setter
    def min_data_value(self, min_data_value):
        self.__min_data_value = min_data_value

    @property
    def max_data_value(self):
        """the largest data value fitting into this axis, i.e. the upper range limit of the plotted data

            :getter: returns the right value of the data range
            :setter: sets the right value of the data range
            :type: ``float``
        """
        return self.__max_data_value

    @max_data_value.setter
    def max_data_value(self, max_data_value):
        self.__max_data_value = max_data_value

    @property
    def are_tics_inside(self):
        """defines whether tics point inside the plot

           :getter: returns True if tics are inside
           :setter: sets the value if tics are inside
           :type: ``boolean``

        """
        return self.__are_tics_inside

    @are_tics_inside.setter
    def are_tics_inside(self, if_inside):
        self.__are_tics_inside = if_inside

    @property
    def axis_location(self):
        """a character that defines the location of this axis: either U, B, L or R

            :getter: Returns this axis' location
            :setter: Sets this axis' location
            :type: char

            Allowed values:
             - 'U' or 'u' - upper X axis
             - 'B' or 'B' - bottom X axis
             - 'L' or 'l' - left Y axis
             - 'R' or 'R' - right Y axis
        """
        return self.__axis_location

    @axis_location.setter
    def axis_location(self, locator):
        self.__axis_location = locator

    @property
    def label(self):
        """A label of an axis

           :getter: returns a label of an axis
           :setter: sets new label of an axis
           :type: ``string``
        """
        return self.__label

    @label.setter
    def label(self, new_label):
        self.__label = new_label

    @property
    def label_shift(self):
        """A shift label

           :getter: returns a shift label
           :setter: sets the new shift label
           :type: ``float``
        """
        return self.__label_shift

    @label_shift.setter
    def label_shift(self, new_shift):
        self.__label_shift = new_shift

    @property
    def label_font_size(self):
        """Define font size for the label (title) of this axis

            :getter: returns the font size
            :setter: sets the font size
            :type: ``float``
        """
        return self.__label_font_size

    @property
    def show_tics(self):
        """A flag to show / hide tics of this axis

           Note, that tics labels visibility is separately controlled by ``show_tics_labels`` property

           :getter: returns tics state : tics will be drawn if true is returned
           :setter: sets the new tics visibility state
           :type: ``boolean``
        """
        return self.__show_tics

    @show_tics.setter
    def show_tics(self, flag):
        self.__show_tics = flag

    @property
    def show_tics_labels(self):
        """A flag to show / hide tics labels of this axis

           Note, that tics visibility is separately controlled by ``show_tics`` property
           :getter: returns tics labels state : tics labels will be drawn if true is returned
           :setter: sets the new tics labels visibility state
           :type: ``boolean``
        """
        return self.__show_tics_labels

    @show_tics_labels.setter
    def show_tics_labels(self, flag):
        self.__show_tics_labels = flag

    @label_font_size.setter
    def label_font_size(self, label_font_size):
        self.__label_font_size = label_font_size

    @property
    def tics_label_font_size(self):
        """Define font size for the tics labels of this axis

            :getter: returns the font size
            :setter: sets the font size
            :type: ``float``
        """
        return self.__tics_label_font_size

    @tics_label_font_size.setter
    def tics_label_font_size(self, tics_label_font_size):
        self.__tics_label_font_size = tics_label_font_size

    @property
    def n_tics(self):
        return self.__n_tics
    

    def set_range(self, min_value, max_value):
        """Sets new extreme values for the data range

        :param min_value:
            minimum value covered by this axix
        :type min_value: ``float``
        :param max_value:
            maximum value covered by this axix
        :type max_value: ``float``
        """
        self.__min_data_value = min_value
        self.__max_data_value = max_value

    def axis_coordinate(self, p):
        """Calculates an axis value that would be drawn at a given screen coordinate

        :param p:
            arbitrary point (screen) coordinate
        :type p: ``float``
        :return:
            axis coordinate calculated for the given point
        """
        return (p - self.__min_screen_coordinate) / (self.__max_screen_coordinate - self.__min_screen_coordinate) \
               * (self.__max_data_value - self.__min_data_value) + self.__min_data_value

    def screen_coordinate(self, x):
        """Calculates a screen coordinate for a data point

        :param x:
            arbitrary value to be converted
        :type x: ``float``
        :return:
            screen coordinate value calculated for the given x
        """
        return (x - self.__min_data_value) / (self.__max_data_value - self.__min_data_value) \
               * (self.__max_screen_coordinate - self.__min_screen_coordinate) + self.__min_screen_coordinate

    def tics_at_fraction(self, fraction_values, labels_values):
        """Sets tics for this axis at given fractions of the axis range

        :param fraction_values:
            fractions of this axis range to put tics at
        :type fraction_values: ``float``
        :param labels_values:
            tics labels
        :type labels_values: ``string``
        """
        self.__small_screen_tics.clear()
        self.__big_screen_tics.clear()
        self.__tics_labels.clear()
        if len(fraction_values) == 0:
            for i in range(len(labels_values)):
                fraction_values.append(float(i / (len(labels_values) - 1)))
        for t in fraction_values:
            self.__big_screen_tics.append(
                (self.__max_screen_coordinate - self.__min_screen_coordinate) * t + self.__min_screen_coordinate)
        for lab in labels_values:
            self.__tics_labels.append(lab)

    def tics_at_values(self, values,format_string="%.2f"):
        """Sets tics for this axis at arbitrary axis values

        :param values:
            values to put tics at - in the units of this axis
        :type values: ``float``
        :param labels_values:
            tics labels
        :type labels_values: ``string``
        """
        self.__small_screen_tics.clear()
        self.__big_screen_tics.clear()
        self.__tics_labels.clear()
        for t in values:
            self.__big_screen_tics.append(self.screen_coordinate(t))
        for t in values:
            self.__tics_labels.append(format_string%t)

    def tics(self, n_small_tics, n_big_tics,format_string="%.2f"):
        """Sets a given number of tics for this axis

        the tics are distributed uniformly

        :param n_small_tics:
            the number of small tics to be drawn at this axis
        :type n_small_tics: ``integer``
        :param n_big_tics:
            the number of big tics to be drawn at this axis
        :type n_big_tics: ``integer``
        """
        self.__n_tics = (n_small_tics,n_big_tics)
        self.__small_screen_tics.clear()
        self.__big_screen_tics.clear()
        self.__tics_labels.clear()
        for i in range(n_small_tics):
            self.__small_screen_tics.append((self.__max_screen_coordinate - self.__min_screen_coordinate) * i / float(
                n_small_tics - 1.0) + self.__min_screen_coordinate)
        for i in range(n_big_tics):
            self.__big_screen_tics.append((self.__max_screen_coordinate - self.__min_screen_coordinate) * i / float(
                n_big_tics - 1.0) + self.__min_screen_coordinate)
        self.add_tics_labels(format_string)

    @property
    def tics_factor(self):
        switcher = {"U1": 1, "U0": -1, "B1": -1, "B0": 1, "L1": 1, "L0": -1, "R1": -1, "R0": 1}
        return switcher[self.axis_location + str(int(self.are_tics_inside))]


class AxisX(Axis):
    """Represents X axis of a plot.

    """

    # __slots__ = ['__screen_y']

    def __init__(self, screen_y, min_screen, max_screen, min_data, max_data, orientation):
        """Creates an instance of an X axis"""
        Axis.__init__(self, min_screen, max_screen, min_data, max_data)
        self.__screen_y = screen_y
        self.axis_location = orientation

    @property
    def screen_y(self):
        """Screen Y coordinate for this axis

           :getter: returns screen Y coordinate for this axis
           :setter: sets new screen Y coordinate for this axis
           :type: ``float`` 
        """
        return self.__screen_y

    @screen_y.setter
    def screen_y(self, screen_y):
        self.__screen_y = screen_y
        return self

    def draw(self, drawing):
        """Draws axis on a given drawing.

        Draws lines,tics lines, axis labeles and tics labels for this axis.
        """

        # --- draw axis lines and tics
        drawing.line("Xaxis" + self.axis_location, self.min_screen_coordinate, self.screen_y,
                     self.max_screen_coordinate, self.screen_y, stroke=self.stroke, stroke_width=self.stroke_width,
                     fill=self.fill)

        # --- draws axis label
        x = ((self.max_screen_coordinate - self.min_screen_coordinate) / 2.0) + self.min_screen_coordinate
        if self.axis_location == 'U':
            y = self.__screen_y - self.label_shift
        else:
            y = self.__screen_y + self.label_shift + self.label_font_size
        if self.label != "":
            drawing.text("label" + self.axis_location, x, y, self.label, font_size=self.label_font_size)

        # --- draws tics
        if self.show_tics:
            if self.are_tics_inside == True:
                drawing.start_group("XaxisTics" + self.axis_location)
                for x_ti in self.small_screen_tics:
                    drawing.line("small", x_ti, self.screen_y, x_ti, self.screen_y + self.tics_width * self.tics_factor,
                                 stroke=self.stroke, stroke_width=self.stroke_width / 8,
                                 fill=get_color(self.fill).create_darker(0.3))
                for x_ti in self.big_screen_tics:
                    drawing.line("big", x_ti, self.screen_y, x_ti,
                                 self.screen_y + 2 * self.tics_width * self.tics_factor, stroke=self.stroke,
                                 stroke_width=self.stroke_width / 8, fill=get_color(self.fill).create_darker(0.3))
                drawing.close_group()

        # --- draws tics labels
        if self.show_tics_labels:
            drawing.start_group("XaxisTicsLab" + self.axis_location)
            for text, x in zip(self.tics_labels, self.big_screen_tics):
                if self.axis_location == 'U':
                    y = self.__screen_y - 3 * (self.tics_width)
                    angle = -90 if self.tics_vertical else 0
                else:
                    y = self.__screen_y + 4 * (self.tics_width)  # + font_size
                    angle = -90 if self.tics_vertical else 0
                drawing.text("tics_label", x, y, text, font_size=self.tics_label_font_size, angle=angle)
            drawing.close_group()


class AxisY(Axis):
    """
    Represents Y axis of a plot.

    """

    # __slots__ = ['__screen_x']

    def __init__(self, screen_x, min_screen, max_screen, min_data, max_data, orientation):
        """Creates an instance of an Y axis"""
        Axis.__init__(self, min_screen, max_screen, min_data, max_data)
        self.__screen_x = screen_x
        self.axis_location = orientation

    @property
    def screen_x(self):
        """Screen X coordinate for this axis

           :getter: returns screen X coordinate for this axis
           :setter: sets new screen X coordinate for this axis
           :type: ``float``
        """
        return self.__screen_x

    @screen_x.setter
    def screen_x(self, screen_x):
        self.__screen_x = screen_x
        return self

    def draw(self, drawing):
        """Draws axis on a given drawing.

          Draws lines,tics lines, axis labeles and tics labels for this axis.
          """

        # --- drawing Axis line
        drawing.line("Yaxis" + self.axis_location, self.screen_x, self.min_screen_coordinate, self.screen_x,
                     self.max_screen_coordinate, stroke=self.stroke, stroke_width=self.stroke_width, fill=self.fill)

        # --- drawing tics lines
        lab_width, lab_height = 0, 0        # --- define them to avoid problems in the future
        if self.show_tics:
            if self.are_tics_inside:
                drawing.start_group("YaxisTics" + self.axis_location)
                for y_ti in self.small_screen_tics:
                    drawing.line("small", self.screen_x, y_ti, self.screen_x + self.tics_width * self.tics_factor, y_ti)
                for y_ti in self.big_screen_tics:
                    drawing.line("big", self.screen_x, y_ti, self.screen_x + 2 * self.tics_width * self.tics_factor,
                                 y_ti)
                drawing.close_group()

            # --- drawing tisc labels
        lab_width = 0
        if self.show_tics_labels:
            if drawing.viewport_name() == "SVG":
                n_char = len(self.tics_labels[0])
                # loop just to get an index of the longest label
                cnt = 0
                for i in range(len(self.tics_labels)):
                    n = len(self.tics_labels[i])
                    if n > n_char :
                        cnt = i
                lab_width, lab_height = drawing.text_length(self.tics_labels[cnt], font_size=self.tics_label_font_size)
            else:           # --- for HTMLViewport this is slower but more precise
                lab_width, lab_height = drawing.text_length(self.tics_labels[0])
                for lab in self.tics_labels[1:]:
                    w, h = drawing.text_length(lab)
                    if w > lab_width :lab_width = w

            drawing.start_group("YaxisTicsLab" + self.axis_location)
            for text, y in zip(self.tics_labels, self.big_screen_tics):
                if self.axis_location == 'L':
                    x = self.screen_x - 15
                    angle = -90 if self.tics_vertical else 0
                    anchor = "end"
                else:
                    x = self.screen_x + 15
                    angle = 90 if self.tics_vertical else 0
                    anchor = "start"
                drawing.text("tics_label", x, y, text, font_size=self.tics_label_font_size, angle=angle,text_anchor=anchor)
            drawing.close_group()

        # --- drawing axis label
        lab_shift = lab_width if not self.tics_vertical else lab_height

        if self.axis_location == 'L':
            x = self.__screen_x - 30 - lab_shift 
            angle = -90
        else:
            x = self.__screen_x + 30 + lab_shift
            angle = 90
        y = ((self.min_screen_coordinate - self.max_screen_coordinate) / 2.0) + self.max_screen_coordinate
        drawing.text("LabelY", x, y, self.label, font_size=self.label_font_size, angle=angle)
