#! /usr/bin/env python

from visualife.core.AxisX import AxisX
from visualife.core.AxisY import AxisY
from visualife.core.Circle import Circle
from visualife.core.ColorBase import ColorBase
from visualife.core.ColorMap import ColorMap, colormap_by_name
from visualife.core.ColorRGB import ColorRGB, color_by_name
from visualife.core.Plot import Plot

class Feature2dMap(Plot):

  __slots__ = ['__structure','__map']

  def __init__(self,viewport):

    Plot.init(viewport, min_screen_x, max_screen_x, min_screen_y, max_screen_y, min_data_x, max_data_x,
               min_data_y, max_data_y, axes_definition="BL")
    self.__structure = None
    self.__map = None

  @property
  def structure(self):
    return self.__structure

  @structure.setter
  def structure(self,new_structure):
    self.__structure = new_structure

  def add_structure(self,a_structure):
    return self

  def add_contacts(self,a_contact):
    return self

  def plot(self, viewport):
    self.__viewport = viewport
    marker_size = 3.0
    colors = []
    color = "Red"
    colors.append( color_by_name(color) )

    # Here we convert data X-Y coordinates to data screen coordinates; the points are also repacked to new arrays
    x_data = []
    y_data = []
    if len(args) >= 2:  # X and Y are given as separate arrays
      for i in range(len(args[0])):
        x_data.append(self.__axes['B'].screen_coordinate(args[0][i]))
        y_data.append(self.__axes['L'].screen_coordinate(args[1][i]))
    else :
        for i in range(len(args[0])) : # there is only one array given, it holds X and Y values as rows
          x_data.append(self.__axes['B'].screen_coordinate(args[0][i][0])) # bottom axis provides scaling for X
          y_data.append(self.__axes['L'].screen_coordinate(args[0][i][1])) # left axis provides scaling for Y

    elememts = []
    c = Circle()
    for i in range(len(x_data)) :
          c.x = x_data[i]
          c.y = y_data[i]
          c.r = marker_size
          self.__viewport.current_style.set_fill_color(colors[i % len(colors)])
          elements.append(self.__viewport.draw(c))

    else :
      self.__viewport.error_msg("Unknown marker style")
      return elements
