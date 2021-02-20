#! /usr/bin/env python

from browser import document
from visualife.core.Plot import Plot

plot_counter = 0

class DraggablePlot(Plot):
  """Represents a draggable plot object
  """


  __slots__ = ['__is_dragged','__drag_x','__drag_y','__shift_x', '__shift_y','__max_drag_x','__max_drag_y','__max_x','__max_y','__min_x','__min_y']

  def __init__(self, viewport, min_screen_x, max_screen_x, min_screen_y, max_screen_y, min_data_x, max_data_x,
               min_data_y, max_data_y, axes_definition="BL"):
    super().__init__(viewport, min_screen_x, max_screen_x, min_screen_y, max_screen_y,
                     min_data_x, max_data_x, min_data_y, max_data_y, axes_definition)

    global plot_counter

    self.__is_dragged = False
    self.__drag_x = 0
    self.__drag_y = 0
    self.__shift_x = 0
    self.__shift_y = 0
    self.__max_drag_x = max_screen_x-min_screen_x
    self.__max_drag_y = max_screen_y-min_screen_y
    self.__max_x = max_data_x
    self.__max_y = max_data_y
    self.__min_x = min_data_x
    self.__min_y = min_data_y
    

    # This creates a clipping mask which is a rectangle covering the inner area of the plot
    plot_counter += 1
    self.clip_path_name = "clip-element-"+str(plot_counter)
    self.clip_path_tics = "clip-axis-"+str(plot_counter)
    viewport.start_clip_path(self.clip_path_name)
    style = """opacity:0;"""
    viewport.rect(self.clip_path_name+"-plot",min_screen_x, min_screen_y, max_screen_x - min_screen_x, max_screen_y - min_screen_y)
    viewport.close_clip_path()
    viewport.start_clip_path(self.clip_path_tics)
    viewport.rect("axisL",0, min_screen_x-10, min_screen_x+20, max_screen_y-min_screen_x+20,style=style)
    viewport.rect("axisB",min_screen_x-10, max_screen_y-10, max_screen_x-min_screen_x+20,min_screen_y,style=style)
    viewport.rect("axisU",max_screen_x-10, min_screen_y-10, min_screen_x+10, max_screen_y - min_screen_y+20,style=style)
    viewport.rect("axisR",min_screen_x-10, min_screen_y-30, max_screen_x-min_screen_x+20,min_screen_y,style=style)
    viewport.close_clip_path()
    #viewport.style={'opacity':1}

    self.axes["B"].tics_at_fraction([0,0.5,1,1.5,2],[0,0.25,0.5,0.75,1.0])

    # If this is HTML viewport, prepare also drag events

    if viewport.viewport_name() == "HTML":
      style="""opacity:0;stroke_width:0;fill:white;"""
      viewport.rect("drag-element",min_screen_x, min_screen_y, max_screen_x - min_screen_x, max_screen_y - min_screen_y,style=style)
      viewport.bind("drag-element","mousedown", self.start_drag)
      viewport.bind("drag-element","mousemove", self.drag)
      viewport.bind("drag-element","mouseup", self.end_drag)
     # viewport.style={'opacity':1}

  def clear(self):

    self.__drag_x = 0
    self.__drag_y = 0
    self.__shift_x = 0
    self.__shift_y = 0
    super(DraggablePlot,self).clear()

  @property
  def is_dragged(self):
    """Returns True if plot is dragged"""
    return self.__is_dragged

  @is_dragged.setter
  def is_dragged(self,new_drag):
    self.__is_dragged=new_drag

  @property
  def max_drag_x(self):
    """Returns max_drag_x value"""
    return self.__max_drag_x

  @max_drag_x.setter
  def max_drag_x(self,new_drag):
    self.__max_drag_x=new_drag

  @property
  def max_drag_y(self):
    """Returns max_drag_y value"""
    return self.__max_drag_y

  @max_drag_y.setter
  def max_drag_y(self,new_drag):
    self.__max_drag_y=new_drag

  @property
  def drag_x(self):
    """Returns drag_x value"""
    return self.__drag_x

  @drag_x.setter
  def drag_x(self,new_drag):
    self.__drag_x=new_drag

  @property
  def drag_y(self):
    """Returns drag_y value"""
    return self.__drag_y

  @drag_y.setter
  def drag_y(self,new_drag):
    self.__drag_y=new_drag

  @property
  def shift_x(self):
    """Returns shift_x value"""
    return self.__shift_x

  @shift_x.setter
  def shift_x(self,new_x):
    self.__drag_y=new_x

  @property
  def shift_y(self):
    """Returns shift_y value"""
    return self.__shift_y

  @shift_y.setter
  def shift_y(self,new_y):
    self.__shift_y=new_y

  def start_drag(self,evt):
    """ Function called when "mousedown" event is recorded; drag is started at that moment

    @param evt: event object passed by a web browser
    """
    self.__drag_x = evt.x
    self.__drag_y = evt.y
    self.__is_dragged = True

  def drag(self,evt):
    """ Performs the actual drag action

    @param evt: event object passed by a web browser; mouse coordinates are extracted from it
    """
    if self.__is_dragged :
      delta_x = evt.x - self.__drag_x + self.__shift_x
      delta_y = evt.y - self.__drag_y + self.__shift_y
      self.set_plot_at_xy(delta_x,delta_y)

  def end_drag(self,evt):
    """ Function called when "mouseup" event is recorded; drag is stopped at that moment

    @param evt: event object passed by a web browser
    """
    self.__is_dragged = False
    self.__shift_x += evt.x - self.__drag_x
    self.__shift_y += evt.y - self.__drag_y
    if self.__shift_x > 0 : self.__shift_x = 0
    if self.__shift_y < 0 : self.__shift_y = 0
    if self.__shift_x < -self.__max_drag_x : self.__shift_x = -self.__max_drag_x
    if self.__shift_y > self.__max_drag_y : self.__shift_y = self.__max_drag_y

  def set_plot_at_xy(self,x,y):
    """Sets the middle of plot in (x,y) point. x and y are the screen coordinates"""
    if self.viewport.viewport_name() == "HTML":
      if x > 0 : x = 0
      if y < 0 : y = 0
      if x < -self.__max_drag_x : x = -self.__max_drag_x
      if y > self.__max_drag_y : y = self.__max_drag_y
      for did in self.data_ids :
        document[did].attrs["transform"] = "translate(%.1f %.1f)" % (x,y)
      document["YaxisTicsLabR"].attrs["transform"] = "translate(%.1f %.1f)" % (0,y)
      document["YaxisTicsLabL"].attrs["transform"] = "translate(%.1f %.1f)" % (0,y)
      document["XaxisTicsLabU"].attrs["transform"] = "translate(%.1f %.1f)" % (x,0)
      document["XaxisTicsLabB"].attrs["transform"] = "translate(%.1f %.1f)" % (x,0)

  def set_axes(self):


    fractions=[]
    values=[]
    self.max_drag_x=self.axes["B"].screen_coordinate(self.converter.max_x)-self.axes["B"].screen_coordinate(self.__max_x)
    self.max_drag_y=-self.axes["L"].screen_coordinate(self.converter.max_y)+self.axes["L"].screen_coordinate(self.__max_y)
    frac = (self.__max_x-self.__min_x)/4.0
    N = int(self.converter.max_x/frac+1)
    for i in range(N+1):
      fractions.append(i/4)
      values.append(i*frac)
    self.axes["B"].tics_at_fraction(fractions,values)
    self.axes["U"].tics_at_fraction(fractions,values)
    fractions.clear()
    values.clear()
    frac = (self.__max_y-self.__min_y)/4.0
    N = int(self.converter.max_y/frac+1)
    for i in range(N+1):
      fractions.append(i/4)
      values.append(i*frac)
    self.axes["L"].tics_at_fraction(fractions,values)
    self.axes["R"].tics_at_fraction(fractions,values)

  def scatter(self,*args,**kwargs):
    super().scatter(*args,**kwargs)
    self.set_axes()
