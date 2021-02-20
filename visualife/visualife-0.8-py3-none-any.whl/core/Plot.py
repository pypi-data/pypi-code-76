#! /usr/bin/env python

from visualife.core.axes import AxisX, AxisY
from visualife.core.styles import *
from math import sqrt
import math

plot_counter = 0
"""Calculates how many times ``Plot`` constructor was called to provide uniq ids for different plots.
"""

class DataConverter:
  """Converts plot data values to screen coordinates values

  Also stores x and y ranges for class ``Plot`` and has set_nice_range() method which provides automatic 
  nice range for axes
  """
  def __init__(self,plot,x_code,y_code):
    """Creates a DataConverter object 

       :param plot: referance to plot to get axis to convert values
       :type plot: ``Plot``
       :param x_code: letter that defines a AxisX location 
       :type x_code: ``string``
       :param y_code: letter that defines a AxisY location 
       :type y_code: ``string``

    """
    self.__plot = plot
    self.__x_code = x_code
    self.__y_code = y_code
    self.__min_x, self.__min_y = None,None
    self.__max_x, self.__max_y = None,None


  @property
  def plot(self):
    """Returns a reference to a ``Plot`` that this converter belongs to"""
    return self.__plot

  @property
  def max_x(self):
    """Returns maximum of X data in screen coordinates"""
    return self.__max_x

  @property
  def min_x(self):
    """Returns minimum of X data in screen coordinates"""
    return self.__min_x

  @property
  def max_y(self):
    """Returns maximum of Y data in screen coordinates"""
    return self.__max_y

  @property
  def min_y(self):
    """Returns minimum of Y data in screen coordinates"""
    return self.__min_y

  def set_min_and_max_data(self,dataset):
    """Sets min and max for X and Y data of all this converter's series in a ``Plot``
       
       This values is neccesary to set_nice_range() method.
    """

    check=False
    if self.__max_x != None:
      check=True
      old_max_x = self.__max_x
      old_max_y = self.__max_y
      old_min_x = self.__min_x
      old_min_y = self.__min_y
    else:
      self.__max_x = dataset.max_x
      self.__min_x = dataset.min_x
      self.__max_y = dataset.max_y
      self.__min_y = dataset.min_y

    if check:
      self.__max_x = max(dataset.max_x, old_max_x)
      self.__min_x = min(dataset.min_x, old_min_x)
      self.__max_y = max(dataset.max_y, old_max_y)
      self.__min_y = min(dataset.min_y, old_min_y)

  def __set_range(self,miin,maax,tics=5):
    """Finds a nice tics ranges for data between miin and maax and returns it as a list
    """
    range_ = maax-miin
    range_ /= (tics-1)
    cnt = 0
    if range_ == 0:
      lista =  [maax-1,miin+1]
      if lista[-1] < maax:
        lista.append(lista[-1]+1)
      if lista[0] > miin:
        lista=[lista[0]-1]+lista
      return lista
    while range_ > 1.0:
      cnt += 1
      range_ /= 10
    zakres = [0.1,0.20,0.25,0.3,0.4,0.5,0.6,0.7, 0.75, 0.8,0.9,1.0]
    for i in zakres:
      if range_ <= i:
        nice_range = int(i*(10**(cnt))) if int(i*(10**(cnt)))>1 else i*(10**(cnt))
        break

    lista = []
    print("range",nice_range)
    mi = nice_range*math.floor(miin/nice_range)
    print("mi",mi)
    for i in range(tics):
      lista.append(mi+i*nice_range)
    if lista[-1] < maax:
      lista.append(lista[-1]+nice_range)
    if lista[0] > miin:
      lista=[lista[0]-nice_range]+lista
  
    return lista

  def set_nice_range(self,what="xy"):
    """Finds a nice tics ranges for ``Plot`` data

       Uses min and max data stored in ``self``
    """
    if "x" in what:
      tics_x = self.__set_range(self.__min_x,self.__max_x,self.__plot.axes[self.__x_code[0]].n_tics[1])

      formatx = "%d"
      print("X",tics_x)
      for i in tics_x:
        if isinstance(i, float):
          formatx = "%.2f"

      for i in self.__x_code:
        self.__plot.axes[i].set_range(tics_x[0],tics_x[-1])
        self.__plot.axes[i].tics_at_values(tics_x,formatx)

    if "y" in what:

      tics_y = self.__set_range(self.__min_y,self.__max_y,self.__plot.axes[self.__y_code[0]].n_tics[1])

      formaty = "%d"
      print("Y",tics_y)

      for i in tics_y:
        if isinstance(i, float):
          formaty = "%.2f"
          
      for i in self.__y_code:
        self.__plot.axes[i].set_range(tics_y[0],tics_y[-1])
        self.__plot.axes[i].tics_at_values(tics_y,formaty)


  def convert_data(self,x_data,y_data):
    """
    Converts x_data and y_data to screen coordinates

       :param x_data: x_data to convert
       :type x_data: ``list``
       :param y_data: y_data to convert
       :type y_data: ``list``
       :return: ``tuple`` like (x_screen_data,y_screen_data) 
    """
    screen_x_data = []
    screen_y_data = []

    for i in range(len(x_data)):
        ix = self.__plot.axes[self.__x_code[0]].screen_coordinate(x_data[i])
        iy = self.__plot.axes[self.__y_code[0]].screen_coordinate(y_data[i])
        screen_x_data.append(ix)
        screen_y_data.append(iy)
    return screen_x_data,screen_y_data



class DataSet:
  """Stores data for serie and its min and max values 
  """
  def __init__(self,converter,*args,**kwargs):
    """Creates a DataSet object with X, Y and Z data (if given)

       :param converter: referance to converter for calculating screen coordinates for this DataSet
       :type converter: ``DataConverter``
       :param ``*args``: data to be plotted; can be :
         - two 1D lists with X and Y
         - three 1D lists with X, Y and Z
         - a list of (X,Y) pairs or (X,Y,Z) triplets

       :Keyword Arguments ``(**kwargs)``: check for derived classes

    """
    self.__x_data = []
    self.__y_data = []
    self.__z_data = []
    self.__min_x, self.__min_y, self.__min_z = 0,0,0
    self.__max_x, self.__max_y, self.__max_z = 0,0,0
    self.__converter = converter
    self.__kwargs = kwargs
    self.__marker_size = 5

    self.__marker_style = ""

    self.__title = ""
    self.__colors = ""

    if len(args) >= 2:  # X and Y (and possibly Z) are given as separate arrays
      self.__max_x = max(args[0])
      self.__max_y = max(args[1])
      self.__min_x = min(args[0])
      self.__min_y = min(args[1])
      self.__x_data = args[0]
      self.__y_data = args[1]
      if len(args) > 2:
        self.__min_z = max(args[2])
        self.__max_z = max(args[2])
        self.__z_data = args[2]
    else:
      self.__max_x = args[0][0][0]
      self.__max_y = args[0][0][1]
      self.__min_x = self.__max_x
      self.__min_y = self.__max_y
      found_z = False
      if len(args[0][0]) > 2:
        self.__max_z = args[0][0][2]
        self.__min_z = self.__max_z
        found_z = True

      for i in range(len(args[0])):  # there is only one array given, it holds X and Y values as rows
        self.__max_x = max(self.__max_x, args[0][i][0])
        self.__min_x = min(self.__min_x, args[0][i][0])
        self.__max_y = max(self.__max_y, args[0][i][1])
        self.__min_y = min(self.__min_y, args[0][i][1])
        self.__x_data.append(args[0][i][0])
        self.__y_data.append(args[0][i][1])
        if found_z:
          v = args[0][i][2]
          if v > self.__max_z: self.__max_z = v
          elif v < self.__min_z: self.__min_z = v
          self.__z_data.append(v)

  @property
  def title(self):
    """Returns this DataSet title"""
    return self.__title

  @title.setter
  def title(self,new_title):
    self.__title = new_title

  @property
  def converter(self):
    """Returns this DataSet converter"""
    return self.__converter

  @property
  def kwargs(self):
    """Returns this DataSet kwargs dictionary"""
    return self.__kwargs

  @property
  def colors(self):
    """Returns this DataSet colors"""
    return self.__colors

  @colors.setter
  def colors(self,new_colors):
    self.__colors = new_colors

  @property
  def marker_size(self):
    """Returns this DataSet markersize"""
    return self.__marker_size

  @marker_size.setter
  def marker_size(self,new_size):
    self.__marker_size = new_size

  @property
  def marker_style(self):
    """Returns this DataSet markerstyle"""
    return self.__marker_style

  @marker_style.setter
  def marker_style(self,new_style):
    self.__marker_style = new_style

  @property
  def x_data(self):
    """Returns list with X data in screen coordinates"""
    return self.__x_data

  @property
  def y_data(self):
    """Returns list with Y data in screen coordinates"""
    return self.__y_data

  @property
  def z_data(self):
    """Returns list with Z data as provided to this object

    The returned list may be empty
    """
    return self.__z_data

  @property
  def max_x(self):
    """Returns maximum of X data in screen coordinates"""
    return self.__max_x

  @property
  def min_x(self):
    """Returns minimum of X data in screen coordinates"""
    return self.__min_x

  @property
  def max_y(self):
    """Returns maximum of Y data in screen coordinates"""
    return self.__max_y

  @property
  def min_y(self):
    """Returns minimum of Y data in screen coordinates"""
    return self.__min_y

  @property
  def max_z(self):
    """Returns maximum of Z data"""
    return self.__max_z

  @property
  def min_z(self):
    """Returns minimum of Z data"""
    return self.__min_z

  def draw(self,plot,default_color=0):
    pass


class ScatterDataSet(DataSet):
  """Stores data for scatterplot
  """
  def __init__(self,converter,*args,**kwargs):
    """Creates a ScatterDataSet object with X, Y and Z data (if given)

      :param converter: referance to converter for calculating screen coordinates for this DataSet
      :type converter: ``DataConverter``
      :param ``*args``: data to be plotted; can be :
         - two 1D lists with X and Y
         - three 1D lists with X, Y and Z
         - a list of (X,Y) pairs or (X,Y,Z) triplets
      :Keyword Arguments ``(**kwargs)``:
        * *markersize* (``float``) --
          size of points of this scatterplot
        * *markerstyle* (``char``) --
          point type; available types are:

          * 'o' -- circle
          * 'c' -- circle (same as 'o')
          * 's' -- square
          * 't' -- triangle
          * 'r' -- rhomb

        * *colors* (``list`` [ ``string`` ], ``list`` [ ``float`` ]
          or ``list`` [ :class:`core.styles.ColorBase` ]) -- define fill color for points;
          the colors are cycled over for all points, so if the list contains a single elements, all points will have the same fill color
        * stroke (``float`` or :class:`core.styles.ColorBase` ) - stroke color
        * stroke_width (``float``) - stroke width
        * title (``string``) - title of this data series; if not provided, the word "scatter" will be used
        * *flush* (``bool``) -- if ``True``, the plot will be automatically send to HTML viewport
          have no efefct on SVG viewport; defalit is ``True``
        * converter_type (``string``) - converter type to calculate axis range - may be "primary"
         (bottom and left axis) or "secondary" (upper and rigth axis)
       

    """
    DataSet.__init__(self,converter,*args,**kwargs)

    #overwriting attributes from base class DataSet
    self.marker_size = kwargs.get("markersize",3.0)
    self.marker_style = kwargs.get("markerstyle", 'c')  # circle marker style is the default
    self.title = kwargs.get("title","scatter")
    self.colors = kwargs.get("colors")
    

  def draw(self,viewport,default_color=0):
    """Draws a DataSet on a given viewport
    """

    # Here we convert data X-Y coordinates to data screen coordinates; the points are also repacked to new arrays
    x_data,y_data = self.converter.convert_data(self.x_data,self.y_data)


    if self.marker_style == 'c' or self.marker_style == 'o':  # Circle
      viewport.circles_group(self.title,x_data, y_data, self.colors, self.marker_size, **self.kwargs)
    elif self.marker_style == 's' :  # Square
      viewport.squares_group(self.title,x_data, y_data, self.colors, self.marker_size, **self.kwargs)
    elif self.marker_style == 't':  # Triangle
      viewport.triangle_group(self.title,x_data,y_data, self.colors, self.marker_size, **self.kwargs)
    elif self.marker_style == 'r':  # Rhomb
      viewport.rhomb_group(self.title,x_data,y_data, self.colors, self.marker_size, **self.kwargs)
    else :
      viewport.error_msg("Unknown marker style")

    if viewport.viewport_name() == "HTML" and self.kwargs.get("flush", True):
      viewport.close()


class LineDataSet(DataSet):
  """Stores data for lineplot
  """
  def __init__(self,converter,*args,**kwargs):
    """Creates a LineDataSet object with X, Y and Z data (if given)

       :param converter: referance to converter for calculating screen coordinates for this DataSet
       :type converter: ``DataConverter``
       :param ``*args``: data to be plotted; can be :
         - two 1D lists with X and Y
         - three 1D lists with X, Y and Z
         - a list of (X,Y) pairs or (X,Y,Z) triplets
       :Keyword Arguments ``(**kwargs)``:

        * *colors* (``list`` [ ``string`` ], ``list`` [ ``float`` ]
          or ``list`` [ :class:`core.styles.ColorBase` ]) -- define fill color for points;
          the colors are cycled over for all points, so if the list contains a single elements, all points will have the same fill color
        * stroke (``float`` or :class:`core.styles.ColorBase` ) - stroke color
        * width (``float``) - stroke width
        * title (``string``) - title of this data series; if not provided, the word "line" will be used
        * converter_type (``string``) - converter type to calculate axis range - may be "primary"
         (bottom and left axis) or "secondary" (upper and rigth axis)

    """
    DataSet.__init__(self,converter,*args,**kwargs)
    self.title = kwargs["title"] if "title" in kwargs else "line"
    self.width = kwargs["width"] if "width" in kwargs else 2.0
    self.colors = kwargs.get("colors")

  def draw(self,viewport,default_color=0):
    x_data,y_data = self.converter.convert_data(self.x_data,self.y_data)


    #viewport.start_group("LineGroup",stroke=self.colors[default_color%len(self.colors)].__str__(), stroke_width=self.width)
    #for i in range (len(x_data)-1) :
       # viewport.line(self.title + ":" + str(i),x_data[i],y_data[i],x_data[i+1],y_data[i+1],stroke=self.colors[default_color%len(self.colors)].__str__(), stroke_width=self.width)
    viewport.lines_group(self.title,x_data,y_data,self.colors,stroke=self.colors[default_color%len(self.colors)].__str__(), stroke_width=self.width)
        
    #viewport.close_group()

    if viewport.viewport_name() == "HTML" and self.kwargs.get("flush", True):
        viewport.close()

class BarDataSet(DataSet):
  """Stores data for barplot
  """
  def __init__(self,converter,*args,**kwargs):
    """Creates a BarDataSet object with X, Y and Z data (if given)

       :param converter: referance to converter for calculating screen coordinates for this DataSet
       :type converter: ``DataConverter``
       :param ``*args``: data to be plotted; can be :
         - two 1D lists with X and Y
         - three 1D lists with X, Y and Z
         - a list of (X,Y) pairs or (X,Y,Z) triplets

      :Keyword Arguments ``(**kwargs)``:
        * *markersize* (``float``) --
          a value used to scale radius of each bubbles

        * *colors* (``list`` [ ``string`` ], ``list`` [ ``float`` ]
          or ``list`` [ :class:`core.styles.ColorBase` ]) -- define fill color for bars;
          the colors are cycled over for all points, so if the list contains a single elements, all points will have the same fill color
        * stroke (``float`` or :class:`core.styles.ColorBase` ) - stroke color
        * stroke_width (``float``) - stroke width
        * title (``string``) - title of this data series; if not provided, the word "bars" will be used
        * converter_type (``string``) - converter type to calculate axis range - may be "primary"
         (bottom and left axis) or "secondary" (upper and rigth axis)

    """
    DataSet.__init__(self,converter,*args,**kwargs)
    self.title = kwargs.get("title","bars")
    self.width = kwargs.get("width",3.0)
    self.colors = kwargs.get("colors")
    self.marker_size= kwargs["width"]


  def draw(self,viewport,default_color=0):

    x_data,y_data = self.converter.convert_data(self.x_data,self.y_data)
    x0 , h0 = self.converter.convert_data([0],[0])
    viewport.start_group("BarsGroup", **self.kwargs)
    for i in range(len(x_data)):
      if self.y_data[i]<0:
        viewport.rect(self.title + ":" + str(i), x_data[i], h0[0], self.width,
                         y_data[i]-h0[0], **self.kwargs)
      else:
        viewport.rect(self.title + ":" + str(i), x_data[i],y_data[i], self.width,
                         h0[0]-y_data[i], **self.kwargs)
    viewport.close_group()
    if viewport.viewport_name() == "HTML" and self.kwargs.get("flush", True):
        viewport.close()

class BubblesDataSet(DataSet):
  """Stores data for barplot
  """
  def __init__(self,converter,*args,**kwargs):
    """Creates a BarDataSet object with X, Y and Z data (if given)

      Bubble chart displays three dimensions of data. Radius of each bubble is proportional to the square root
      of Z value of each point

      :param converter: referance to converter for calculating screen coordinates for this DataSet
      :type converter: ``DataConverter``
      :param ``*args``: data to be plotted; see ``DataSet.__init__()`` documentation
  
      :Keyword Arguments ``(**kwargs)``:
        * *markersize* (``float``) --
          a value used to scale radius of each bubbles

        * *colors* (``list`` [ ``string`` ], ``list`` [ ``float`` ]
          or ``list`` [ :class:`core.styles.ColorBase` ]) -- define fill color for points;
          the colors are cycled over for all points, so if the list contains a single elements, all points will have the same fill color
        * stroke (``float`` or :class:`core.styles.ColorBase` ) - stroke color
        * stroke_width (``float``) - stroke width
        * title (``string``) - title of this data series; if not provided, the word "bubble chart" will be used
        * converter_type (``string``) - converter type to calculate axis range - may be "primary"
         (bottom and left axis) or "secondary" (upper and rigth axis)
    """
    DataSet.__init__(self,converter,*args,**kwargs)
    if not "colors" in kwargs: # if no colors provided, use Z values
      kwargs = dict(**kwargs, colors=self.z_data)
    #  --- the array may be smaller that array of points; the modulo operation is used
    self.colors = self.converter.plot.prepare_data_colors(kwargs)

    self.title = kwargs["title"] if "title" in kwargs else "bubble chart"
    # --- Prepare size of each circle based on its Z value
    marker_factor = kwargs.get("markersize", 3.0)
    self.marker_size = []
    for v in self.z_data:
      self.marker_size.append(sqrt(v) * marker_factor)
    

  def draw(self,viewport,default_color=0):

    x_data,y_data = self.converter.convert_data(self.x_data,self.y_data)

    viewport.start_group("Outer" + self.title, **self.kwargs)
    viewport.circles_group(self.title, x_data, y_data, self.colors, self.marker_size, **self.kwargs)
    viewport.close_group()


    if viewport.viewport_name() == "HTML" and self.kwargs.get("flush", True):
        viewport.close()


class PlotLegend:
  """Stores series data to draw a plot legend
  """
  def __init__(self):
    """Creates an empty PlotLegend object
    """
    self.__series = []

  def add_serie(self,dataset):
    """Adds serie to the list of series

       :param dataset: DataSet object for the added serie
       :type dataset: ``DataSet.__init__()``
       
    """
    self.__series.append(dataset)

  @property
  def series(self):
    """Returns series list
    """
    return self.__series

  def draw(self,viewport,screen_x,screen_y,width,height,font_size):
    """Draws a legend on a plot

       :param screen_x: x coordinate of legend
       :type screen_x: ``float``
       :param screen_y: y coordinate of legend
       :type screen_y: ``float``
       :param width: legend width
       :type width: ``float``
       :param height: legend height
       :type height: ``float``
       :param position: legend position as "RU"(rigth upper)
       :type position: ``string``


    """
    viewport.rect("Legend",screen_x,screen_y,width,height,fill="white")
    for i in range(len(self.series)):
      x_c =screen_x+5+self.series[i].marker_size
      x_t = screen_x+10+2*self.series[i].marker_size
      y_c = screen_y+(i+1)*height/(len(self.series)+1)
      y_t = y_c+self.series[i].marker_size/2
      if self.series[i].marker_style == 'c' or self.series[i].marker_style == 'o':  # Circle
        viewport.circle("lgnd-serie%d-p"%i,x_c,y_c,self.series[i].marker_size,fill=self.series[i].colors[0])
      elif self.series[i].marker_style == 's' :  # Square
        viewport.square("lgnd-serie%d-p"%i,x_c,y_c,self.series[i].marker_size,fill=self.series[i].colors[0])
      elif self.series[i].marker_style == 't':  # Triangle
        viewport.triangle("lgnd-serie%d-p"%i,x_c,y_c,self.series[i].marker_size,fill=self.series[i].colors[0])
      elif self.series[i].marker_style == 'r':  # Rhomb
        viewport.rhomb("lgnd-serie%d-p"%i,x_c,y_c,self.series[i].marker_size,fill=self.series[i].colors[0])
      else :
        viewport.square("lgnd-serie%d-p"%i,x_c,y_c,self.series[i].marker_size,fill=self.series[i].colors[0])
      viewport.text("lgnd-serie%d"%i,x_t,y_t,self.series[i].title,text_anchor="start",font_size=font_size)


class Plot:
  """Represents a plot object
  """

  __slots__ = ['__viewport','__axes', '__plot_label', '__default_style_index', '__mask_element', '__label_text_style',
               '__data_ids', '__clip_path_name','__clip_path_tics','__axes_svg', '__plot_label_font_size', '__extra_labels',
               '__axes_definition','__legend','__primary_converter','__secondary_converter',
               '__data_sets','__plot_id']


  def __init__(self, viewport, min_screen_x, max_screen_x, min_screen_y, max_screen_y, min_data_x=0, max_data_x=1,
               min_data_y=0, max_data_y=1, axes_definition="BL"):
    """Creates a plot object with axes

       :param viewport: selected viewport object to draw a plot
       :type viewport: :class:`core.HtmlViewport` or :class:`core.SvgViewport`
       :param min_screen_x: starting x value to draw a plot in screen coordinates
       :type min_screen_x: ``float``
       :param max_screen_x:
         ending point x value to draw a plot in screen coordinate
       :type max_screen_x: ``float``
       :param min_screen_y:
         starting point x value to draw a plot in screen coordinate
       :type min_screen_y: ``float``
       :param max_screen_y:
         ending point x value to draw a plot in screen coordinate
       :type max_screen_y: ``float``
       :param min_data_x:
         minimum x data value
       :type min_data_x: ``float``
       :param max_data_x:
         maximum x data value
       :type max_data_x: ``float``
       :param min_data_y:
         minimum y data value
       :type min_data_y: ``float``
       :param max_data_y:
         maximum y data value
       :type max_data_y: ``float``
       :param axes_definition:
         string containg letters represents axis to create in a plot <B - bottom, U - upper, R - right, L - left> ("BL" set by default)
       :type axes_definition: ``string``

       The example below creates a plot in a SVG viewport:

       .. code-block:: python

           drawing = SvgViewport("scatterplot.svg", 0, 0, 800, 400)
           plot = Plot(drawing,50,750,50,350,0.0,0.5,0.0,0.5, axes_definition="UBLR")

       Viewport is 800x400, the plot takes 700x300 of it (from 50 to 750 and from 50 to 350 along X and Y asis, respectively)
       All four axis will be shown because of "UBLR" argument. Output plot will be stored in ``scatterplot.svg`` file (SVG format).
       If you want to make a plot on a web-page, use :class:`core.HtmlViewport`:

       .. code-block:: python

              from random import random
              from browser import document
              from visualife.core import HtmlViewport
              from visualife.core.Plot import Plot

              xy_data = [ (random(), random()) for i in range(500)]
              drawing = HtmlViewport(document['svg'],0,0,600,400)
              pl = Plot(drawing,50,550,50,350,0.0,1.0,0.0,1.0, axes_definition="UBLR")
              pl.scatter(xy_data)
              pl.draw(grid=True)
              drawing.close()

       .. raw:: html

          <div> <svg  id="svg" xmlns="http://www.w3.org/2000/svg" class="right" width="600" height="400"></svg> </div>
          <script type="text/python">
              from random import random
              from browser import document
              from visualife.core.HtmlViewport import HtmlViewport
              from visualife.core.Plot import Plot

              xy_data = [ (random(), random()) for i in range(500)]
              drawing = HtmlViewport(document['svg'],0,0,600,400)
              pl = Plot(drawing,50,550,50,350,0.0,1.0,0.0,1.0, axes_definition="UBLR")
              pl.scatter(xy_data)
              pl.draw(grid=True)
              drawing.close()
          </script>
    """

    global plot_counter

    plot_counter+=1
    self.__viewport = viewport
    self.__axes = {}
    self.__plot_label = ''
    self.__extra_labels = []
    self.__default_style_index = 0 # We start plotting with the very first default style and increment them by one
    self.__plot_label_font_size = get_font_size((max_screen_x-min_screen_x)/40)
    self.__data_ids = []
    self.__axes_svg = {}
    self.__clip_path_name = ''
    self.__clip_path_tics = ''
    self.__axes_definition = axes_definition
    self.__legend = PlotLegend()
    self.__primary_converter = DataConverter(self,"BU","LR")
    self.__secondary_converter = DataConverter(self,"U","R")
    self.__data_sets = []
    self.__plot_id = "plot-%d"%plot_counter


    if axes_definition.find("B") != -1:
      x_bottom_axis = AxisX(max_screen_y, min_screen_x, max_screen_x, min_data_x, max_data_x, 'B')
      if x_bottom_axis.label == "" : x_bottom_axis.label = " "
      x_bottom_axis.tics(13,5)
      self.__axes["B"] = x_bottom_axis

    if axes_definition.find("U") != -1:
      x_top_axis = AxisX(min_screen_y, min_screen_x, max_screen_x, min_data_x, max_data_x, 'U')
      if x_top_axis.label == "" : x_top_axis.label = " "
      x_top_axis.tics(13,5)
      self.__axes["U"] = x_top_axis

    if axes_definition.find("L") != -1:
      y_left_axis = AxisY(min_screen_x, max_screen_y, min_screen_y, min_data_y, max_data_y, 'L')
      if y_left_axis.label == "" : y_left_axis.label = " "
      y_left_axis.tics(13,5)
      self.__axes["L"] = y_left_axis

    if axes_definition.find("R") != -1:
      y_right_axis = AxisY(max_screen_x, max_screen_y, min_screen_y, min_data_y, max_data_y, 'R')
      y_right_axis.tics(13,5)
      if y_right_axis.label == "": y_right_axis.label = " "
      self.__axes["R"] = y_right_axis


  @property
  def converter(self):
    return self.__primary_converter
  

  def clear(self):
    for name,group in self.__axes_svg.items() :
      group.parent.removeChild(group)
    self.__axes_svg.clear()

  def axes_svg_x(self):
    """Returns axes elements as an svg object"""
    return self.__axes_svg["axis"].children[1].children

  def axes_svg_y(self):
    """Returns axes elements as an svg object"""
    return self.__axes_svg["axis"].children[5].children

  @property
  def extra_labels(self):
    """Provides access to the list of extra labels of this plot

    :return: a list of labels, each label as a tuple ``(x, y, "text", dict)``. The ``dict`` holds kwargs with plotting style
    """
    return self.__extra_labels

  def add_extra_label(self, label_text, data_x, data_y, **kwargs):
    """Adds a new label that will be drawn in the plot.

    Besides tics labels, axis labels, etc a plot may also have extra labels, placed in arbitrary locations given
    in data coordinates. Plot object will convert these X,Y coordinates do screen coordinates using main X and Y axes

    :param label_text: text to be written in this plot
    :param data_x: - data X coordinate of a label
    :param data_y: - data y coordinate of a label
    :param kwargs: - style parameters
    :return: None
    """
    if len(kwargs) > 0:
      self.__extra_labels.append((data_x, data_y, label_text, kwargs))
    else:
      self.__extra_labels.append((data_x, data_y, label_text))

  def scale(self,scale):
    """ Scales plot
      :param scale: provides a scale
      :type scale: ``float``
    """
    self.__viewport.svg.attrs["transform"]="scale(%.1f)"%(scale)

  @property
  def data_ids(self):
    """Returns data_ids
    """
    return self.__data_ids

  @property
  def viewport(self):
    """Returns viewport
    """
    return self.__viewport

  @property
  def axes_svg(self):
    """Returns axes
        """
    return self.__axes_svg


  @property
  def plot_label(self):
    """Defines title (label) of this plot

      :getter: returns the label as text
      :setter: sets the new label text
      :type: ``string``
    """
    return self.__plot_label

  @plot_label.setter
  def plot_label(self,new_label):
    self.__plot_label = str(new_label)

  @property
  def plot_label_font_size(self):
    """Defines the font size used to draw title (label) of this plot

      :getter: returns the label font size
      :setter: sets the new label font size
      :type: ``float``
    """
    return self.__plot_label_font_size

  @plot_label_font_size.setter
  def plot_label_font_size(self, new_font_size):
    self.__plot_label_font_size = new_font_size

  @property
  def clip_path_name(self):
    """Defines clip_path_name of this plot

      :getter: returns the clip path name
      :setter: sets the new clip path name
      :type: ``string``
    """
    return self.__clip_path_name

  @clip_path_name.setter
  def clip_path_name(self,name):
    self.__clip_path_name = name

  @property
  def clip_path_tics(self):
    """Defines clip_path_name of this plot

      :getter: returns the clip path name
      :setter: sets the new clip path name
      :type: ``string``
    """
    return self.__clip_path_tics

  @clip_path_tics.setter
  def clip_path_tics(self,name):
    self.__clip_path_tics = name

  def draw_plot_label(self):
    """Draws a plot label - its title and all extra labels that has been added to this plot
    """ 
    y = self.__axes["U"].screen_y-(self.__axes["U"].max_screen_coordinate-self.__axes["U"].min_screen_coordinate)/10
    x = (self.__axes["U"].max_screen_coordinate - self.__axes["U"].min_screen_coordinate)/2 + self.__axes["U"].min_screen_coordinate
    self.__viewport.text("PlotLabel", x, y, self.__plot_label, fill=self.__axes["U"].stroke,font_size=self.plot_label_font_size)
    i = 0
    for xyl in self.__extra_labels:
      x = self.axes["B"].screen_coordinate(xyl[0])
      y = self.axes["L"].screen_coordinate(xyl[1])
      if len(xyl) == 4:
        self.__viewport.text("extra-"+str(i), x, y, xyl[2], **xyl[3])
      else:
        self.__viewport.text("extra-" + str(i), x, y, xyl[2])

  @property
  def axes(self):
    """Dictionary of axes in a plot - key is a letter defines axis (U,B,R,L) and Axis object is a value

       :getter: returns a dictionary holding axes objects; dictionary keys are ``B``, ``U``, ``R`` and ``L``
          for **b**\ ottom, **t**\ op, **r**\ ight and **l**\ eft axis, respectively
       :type: ``dictionary(Axis)``
    """
    return self.__axes

  def draw_axes(self):
    """Draws axes as an <svg> element
    """
    if self.__clip_path_tics == "":
      self.__viewport.start_group("Outer-Axis")
    else:  
      self.__viewport.start_group("Outer-Axis",clip_path=self.__clip_path_tics)
    self.__viewport.start_group("Axis")
    for ax_key in self.__axes:
      self.__axes[ax_key].draw(self.__viewport)
    self.__viewport.close_group()
    self.__viewport.close_group()

  def draw_grid(self):
    """Draws grid as an <svg> element
    """

    def draw_horizontal_grid_lines(x_from, x_to, y, style):
      for yi in y: self.__viewport.line("gr", x_from, yi, x_to, yi, **style)

    def draw_vertical_grid_lines(x, y_from, y_to, style):
      for xi in x: self.__viewport.line("gr", xi, y_from, xi, y_to, **style)

    self.__viewport.start_group("Grid")

    style = {'stroke_dasharray':4,'stroke': self.__axes['B'].stroke, 'stroke_width': self.__axes['B'].stroke_width / 3.0}
    draw_vertical_grid_lines(self.__axes['B'].big_screen_tics[1:-1], self.__axes['L'].min_screen_coordinate,
                             self.__axes['L'].max_screen_coordinate,style)
    draw_horizontal_grid_lines(self.__axes['B'].min_screen_coordinate, self.__axes['B'].max_screen_coordinate,
                               self.__axes['L'].big_screen_tics[1:-1],style)
    self.__viewport.close_group()

  def draw_legend(self,position="RU"):
    """Calculates legend position and size and draws it
    """

    n_rows = len(self.__legend.series)
    height = n_rows*30
    width = (self.axes["U"].max_screen_coordinate - self.axes["U"].min_screen_coordinate)/5
    if position[0]=="R" or position[0]=="L":
      if position[0] == "R" :  x = self.axes["R"].screen_x + 15
      elif position[0] == "L" : x = self.axes["L"].screen_x - 15 - width
      #if len(position)==1 then default is set to center
      y = (self.axes["B"].screen_y - self.axes["U"].screen_y)/2 + self.axes["U"].screen_y - width/2
      if len(position)>1:
        if position[1] == "U" :
          y = self.axes["U"].screen_y + 15
        elif position[1] == "C" :
          y = (self.axes["B"].screen_y - self.axes["U"].screen_y)/2 + self.axes["U"].screen_y - width/2
        elif position[1] == "B" :
          y = self.axes["B"].screen_y - 15 - height
    if position[0]=="U" or position[0]=="B":
      if position[0] == "U" :  y = self.axes["U"].screen_y - 15 - height
      elif position[0] == "B" : y = self.axes["B"].screen_y + 15 + height
      x = (self.axes["R"].screen_x - self.axes["L"].screen_x)/2 + self.axes["L"].screen_x - width/2
      if len(position)>1:
        if position[1] == "L" :
          x = self.axes["L"].screen_x + 15
        elif position[1] == "C" :
          x = (self.axes["R"].screen_x - self.axes["L"].screen_x)/2 + self.axes["L"].screen_x - width/2
        elif position[1] == "R" :
          x = self.axes["R"].screen_x - 15 - width

    self.__legend.draw(self.__viewport,x,y,width,height,self.axes["B"].label_font_size)

  def prepare_data_colors(self, kwargs_dict):
    """Returns list of colors used to draw points

    This method makes the following choice:

      - if ``kwargs_dict`` does not contain ``"colors"`` key, a single color will be returned to plot all points
        the returned color will be selected from the current palette assigned to differentiate between data series
      - if ``"colors"`` provides a ``string`` that is a valid color palette name (i.e. registered in ``styles.known_color_scales``)
        the requested pallete is returned
      - if ``"colors"`` provides a ``int``, the number is interpreted as an index of a color in the data series palette;
        a single color is returned
      - if ``"colors"`` provides a ``list`` of values, a color is evaluated separately for every value using a color map
        If ``kwargs_dict`` provides ``"cmap"`` key, the requested color map is used for that purpose; otherwise
        a default ``"blues"`` map is used. In addition, when ``"cmap_reversed"`` key is set to ``True``,
        the cmap will be reversed, e.g. ``"red_blue"`` color map will become ``"blue_red"``

    The colors are defined based on what user requested by kwargs parameters passed to plotting methods
    as``bubbles()``, ``scatter()`` or ``line()``
    """
    colors = []
    if "colors" in kwargs_dict:
      color = kwargs_dict["colors"]                                   # --- get color of points from kwargs
      if isinstance(color, str) and color in known_color_scales:      # --- if this is a name of a known color palette,
        return known_color_scales[color]                              # ... just return its colors
      if isinstance(color, str): colors.append(color_by_name(color))  # --- it's color by name (e.g. "Red")
      elif isinstance(color, int) :                                   # --- it's the index of the default plotting color
        colors.append( get_color(default_plotting_colors[color % len(default_plotting_colors)]) )
      elif isinstance(color, ColorBase): colors.append(color)         # --- it's color object
      elif isinstance(color, list):                                   # --- it's Z-coordinate do get colors from color map
        min_z = min(color)
        max_z = max(color)
        cmap = kwargs_dict["cmap"] if "cmap" in kwargs_dict else "blues"    # --- get cmap to convert Z-values into colors
        if isinstance(cmap, str) :                                    # --- if cmap is a string, it must be a palette name
          cmap1 = colormap_by_name(cmap, min_z, max_z, if_reversed=("cmap_reversed" in kwargs_dict))
        else:
          cmap1 = cmap                                                # It's no a string -> assume it's a pallete by itselfs
        for z in color: colors.append(cmap1.color(z))
    else :
      colors.append( get_color(default_plotting_colors[self.__default_style_index]) )
      self.__default_style_index += 1

    return colors

  def draw(self,**kwargs):
    """Draws this plot on its viewport

    Its necessary to call this method at the end of plotting; only then this plot will be actually drawn.
    Also, any adjustments (e.g. extra labels, axis, etc.) added after this call will not be included in
    this plot.

    :Keyword Arguments ``(**kwargs)``:
        * *axes* (``bool``) --
          draws axes if ``True`` (as default)
        * *grid* (``bool``) --
          draws grid if ``True`` (default is ``False``)
        * *plot_label* (``bool`` ) --
          draws plot_label if ``True`` (as default)
        * *legend* (``string``or ``bool``) -- 
          legend position; default is ``False``; if ``True`` then default location is set (see ``PlotLegend.__init__()``)

    """

    self.__viewport.start_group(self.__plot_id) 
    if_grid = kwargs.get("grid",False)
    if_plot_label = kwargs.get("plot_label",True)
    if_axes = kwargs.get("axes",True)
    if_legend = kwargs.get("legend",False)

    if if_axes: self.draw_axes()
    if if_grid: self.draw_grid()
    if if_plot_label: self.draw_plot_label()
    if if_legend: 
      if isinstance(if_legend,str):
        self.draw_legend(if_legend)
      else: self.draw_legend()

    for d_set in self.__data_sets:
      self.__viewport.start_group("Outer"+d_set.title,clip_path=self.clip_path_name,**d_set.kwargs) # self.__clip_path_name is the name of a path used to clip points in this plot
      d_set.draw(self.viewport,self.__default_style_index)
      self.__viewport.close_group()
    
    self.__viewport.close_group()

    if self.__viewport.viewport_name() == "HTML" and kwargs.get("flush", True):
      self.__viewport.close()

  def scatter(self, *args, **kwargs):
    """Creates a scatterplot

    :Keyword Arguments ``(**kwargs)``:
        * *markersize* (``float``) --
          size of points of this scatterplot
        * *markerstyle* (``char``) --
          point type; available types are:

          * 'o' -- circle
          * 'c' -- circle (same as 'o')
          * 's' -- square
          * 't' -- triangle
          * 'r' -- rhomb

        * *colors* (``list`` [ ``string`` ], ``list`` [ ``float`` ]
          or ``list`` [ :class:`core.styles.ColorBase` ]) -- define fill color for points;
          the colors are cycled over for all points, so if the list contains a single elements, all points will have the same fill color
        * stroke (``float`` or :class:`core.styles.ColorBase` ) - stroke color
        * stroke_width (``float``) - stroke width
        * title (``string``) - title of this data series; if not provided, the word "scatter" will be used
        * *flush* (``bool``) -- if ``True``, the plot will be automatically send to HTML viewport
          have no efefct on SVG viewport; defalit is ``True``
        * converter_type (``string``) - converter type to calculate axis range - may be "primary"
         (bottom and left axis) or "secondary" (upper and rigth axis)
        * adjust_range - False if you want to keep values from Plot constructor and True (default) if you want to have automatically adjust scale
         
    """


    converter = kwargs.get("converter_type","primary")
    colors = self.prepare_data_colors(kwargs)
    kwargs["colors"] = colors
    string_format=kwargs.get("tics_label_format","%.2f")

    if converter == "primary":
      scatter_set = ScatterDataSet(self.__primary_converter, *args, **kwargs)
      self.__primary_converter.set_min_and_max_data(scatter_set)

      if kwargs.get("adjust_range",True)==True:
        self.__primary_converter.set_nice_range(string_format)
    else:
      scatter_set = ScatterDataSet(self.__secondary_converter, *args, **kwargs)
      self.__secondary_converter.set_min_and_max_data(scatter_set)

      if kwargs.get("adjust_range",True)==True:
        self.__secondary_converter.set_nice_range(string_format)
    self.__data_ids.append(scatter_set.title)
    self.__data_sets.append(scatter_set)
    self.__legend.add_serie(scatter_set)


  def bubbles(self, *args, **kwargs):
    """Creates a bubble chart

    Bubble chart displays three dimensions of data. Radius of each bubble is proportional to the square root
    of Z value of each point

    :param ``*args``: data to be plotted; see ``DataSet.__init__()`` documentation

    :Keyword Arguments ``(**kwargs)``:
        * *markersize* (``float``) --
          a value used to scale radius of each bubbles

        * *colors* (``list`` [ ``string`` ], ``list`` [ ``float`` ]
          or ``list`` [ :class:`core.styles.ColorBase` ]) -- define fill color for points;
          the colors are cycled over for all points, so if the list contains a single elements, all points will have the same fill color
        * stroke (``float`` or :class:`core.styles.ColorBase` ) - stroke color
        * stroke_width (``float``) - stroke width
        * title (``string``) - title of this data series; if not provided, the word "bubble chart" will be used
        * converter_type (``string``) - converter type to calculate axis range - may be "primary"
         (bottom and left axis) or "secondary" (upper and rigth axis
        * adjust_range - False if you want to keep values from Plot constructor and True (default) if you want to have automatically adjust scale
             """

    #  --- 'colors' array defines color of every bubble;
    converter = kwargs.get("converter_type","primary")
    

    if converter == "primary":
      data_set = BubblesDataSet(self.__primary_converter, *args, **kwargs)
      self.__primary_converter.set_min_and_max_data(data_set)

      if kwargs.get("adjust_range",True)==True:
        self.__primary_converter.set_nice_range()
    else:
      data_set = BubblesDataSet(self.__secondary_converter, *args, **kwargs)
      self.__secondary_converter.set_min_and_max_data(data_set)

      if kwargs.get("adjust_range",True)==True:
        self.__secondary_converter.set_nice_range()
    self.__data_ids.append(data_set.title)
    self.__data_sets.append(data_set)
    self.__legend.add_serie(data_set)

  def line(self, *args, **kwargs):
    """Creates a line plot

    Line plot displays data conected with lines. 

    :Keyword Arguments ``(**kwargs)``:

        * *colors* (``list`` [ ``string`` ], ``list`` [ ``float`` ]
          or ``list`` [ :class:`core.styles.ColorBase` ]) -- define fill color for points;
          the colors are cycled over for all points, so if the list contains a single elements, all points will have the same fill color
        * stroke (``float`` or :class:`core.styles.ColorBase` ) - stroke color
        * width (``float``) - stroke width
        * title (``string``) - title of this data series; if not provided, the word "line" will be used
        * converter_type (``string``) - converter type to calculate axis range - may be "primary"
         (bottom and left axis) or "secondary" (upper and rigth axis)
        * adjust_range - False if you want to keep values from Plot constructor and True (default) if you want to have automatically adjust scale

    """

    # --- colors to draw a line
    converter = kwargs.get("converter_type","primary")

    colors = self.prepare_data_colors(kwargs)
    kwargs["colors"] = colors


    if converter == "primary":
      data_set = LineDataSet(self.__primary_converter, *args, **kwargs)
      self.__primary_converter.set_min_and_max_data(data_set)

      if kwargs.get("adjust_range",True)==True:
        self.__primary_converter.set_nice_range()
    else:
      data_set = LineDataSet(self.__secondary_converter, *args, **kwargs)
      self.__secondary_converter.set_min_and_max_data(data_set)

      if kwargs.get("adjust_range",True)==True:
        self.__secondary_converter.set_nice_range()
    self.__data_ids.append(data_set.title)
    self.__data_sets.append(data_set)
    self.__legend.add_serie(data_set)


  def bars(self, *args, **kwargs):
    """Creates a bar plot

    :Keyword Arguments ``(**kwargs)``:

        * *colors* (``list`` [ ``string`` ], ``list`` [ ``float`` ]
          or ``list`` [ :class:`core.styles.ColorBase` ]) -- define fill color for points;
          the colors are cycled over for all points, so if the list contains a single elements, all points will have the same fill color
        * stroke (``float`` or :class:`core.styles.ColorBase` ) - stroke color
        * width (``float``) - width of each  bar (in data units!)
        * title (``string``) - title of this data series; if not provided, the word "bars" will be used
        * converter_type (``string``) - converter type to calculate axis range - may be "primary"
         (bottom and left axis) or "secondary" (upper and rigth axis)
        * adjust_range - False if you want to keep values from Plot constructor and True (default) if you want to have automatically adjust scale
    """

    # --- colors to draw a line
    converter = kwargs.get("converter_type","primary")
    colors = self.prepare_data_colors(kwargs)
    kwargs["colors"]=colors
    default_width = (self.axes['B'].max_data_value-self.axes['B'].min_data_value) / 100.0
    width = kwargs.get("width",default_width)
        
    kwargs["width"] = self.axes['B'].screen_coordinate(width) - self.axes['B'].screen_coordinate(0)
    # --- backup drawing style parameters
    kwargs['fill'] = kwargs.get("color",colors[self.__default_style_index % len(colors)])

    if converter == "primary":
      data_set = BarDataSet(self.__primary_converter, *args, **kwargs)
      self.__primary_converter.set_min_and_max_data(data_set)

      if kwargs.get("adjust_range","xy")!=False:
        self.__primary_converter.set_nice_range(kwargs.get("adjust_range","xy"))
    else:
      data_set = BarDataSet(self.__secondary_converter, *args, **kwargs)
      self.__secondary_converter.set_min_and_max_data(data_set)

      if kwargs.get("adjust_range","xy")!=False:
        self.__secondary_converter.set_nice_range(kwargs.get("adjust_range","xy"))
    self.__data_ids.append(data_set.title)
    self.__data_sets.append(data_set)
    self.__legend.add_serie(data_set)
    

  def boxes(self, *args, **kwargs):

    # --- colors to draw a line
    colors = self.prepare_data_colors(kwargs)
    title = kwargs["title"] if "title" in kwargs else "boxes"
    kwargs['width'] = kwargs["width"] if "width" in kwargs else 15.0
    # --- backup drawing style parameters
    kwargs['fill'] = kwargs.get("color","white")
    kwargs['stroke_width'] = kwargs.get("stroke_width", 1)
    kwargs['stroke'] = kwargs.get("stroke","black")

    if len(args) == 1 :
      data = args[0] # the passed data is a 2D array, each dimension having (x), min, q1, q2, q3, max; x is optional
    else :
      data = args   # the passed data is a bunch of 1D arrays, having (x), min, q1, q2, q3, max; x is optional
    width = kwargs.get("box_width", 10)
    self.__viewport.start_group("BoxesGroup",**kwargs)
    median_style = """stroke-width:%s; stroke:%s;""" % (kwargs['stroke_width'] * 3.0, kwargs['stroke'])
    circle_style = """stroke-width:0; fill:%s;""" % kwargs['stroke']
    for i_box in range (len(data)) :
      if len(data[i_box]) < 6 : data[i_box].insert(0, i_box + 1)
      x = self.axes['B'].screen_coordinate(data[i_box][0])
      q1 = self.axes['L'].screen_coordinate(data[i_box][2])
      q2 = self.axes['L'].screen_coordinate(data[i_box][3])
      q3 = self.axes['L'].screen_coordinate(data[i_box][4])
      ymin = self.axes['L'].screen_coordinate(data[i_box][1])
      ymax = self.axes['L'].screen_coordinate(data[i_box][5])
      # --- box
      self.viewport.rect(title + "-b-" + str(i_box), x - width * 0.5, q3, width, (q1 - q3))
      # --- median line
      self.viewport.line(title + "-l-" + str(i_box), x - width * 0.5, q2,  x + width * 0.5, q2, style=median_style)
      # --- middle circle
      self.viewport.circle(title + "-c-" + str(i_box), x,  q2, width * 0.1, style=circle_style)
      # --- top whisker
      self.viewport.line(title + "-t-" + str(i_box), x, ymax,  x, q3)
      self.viewport.line(title + "-t-" + str(i_box), x - width * 0.5, ymax,  x + width * 0.5, ymax)
      # --- down whisker
      self.viewport.line(title + "-d-" + str(i_box), x - width * 0.5, ymin,  x + width * 0.5, ymin)
      self.viewport.line(title + "-d-" + str(i_box), x, ymin,  x, q1)

    self.__viewport.close_group()

    if self.__viewport.viewport_name() == "HTML" and kwargs.get("flush", True):
        self.__viewport.close()
