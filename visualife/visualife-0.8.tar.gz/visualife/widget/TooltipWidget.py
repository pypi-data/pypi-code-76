from browser import document, html

tooltip_style = {
    'backgroundColor': 'white',
    'color': '#000',
    'textAlign': 'center',
    'padding': '5px 0px',
    'borderRadius': '6px',
    'visibility': 'hidden',
    'position': 'fixed',
    'overflow':'hidden',
    'display': 'none',
    'textDecoration': 'none',
}


class TooltipWidget:

    def __init__(self, id_text,  parent_id, tooltip_text, width, height, **kwargs):
        """Creates a new tooltip

        :param id_text: ID of a html DIV element that will contain this TooltipWidget instance
        :param parent_id: ID of the outer HTML element this tooltip should be inserted
        :param tooltip_text: text that will be displayed by this tooltip (may be set later)
        :param width: width of a tooltip box
        :param height: width of a tooltip box
        :param kwargs: see below

        :Keyword Arguments:
            * *offset_x* (``int``) --
              X value added to the X coordinate of the tooltip so it can be moved to the left/right in respect to the
              position of the hoovered element
            * *offset_y* (``int``) --
              Y value added to the Y coordinate of the tooltip so it can be moved to the up/down in respect to the
              position of the hoovered element
            * *position* (``string``) --
              how the tooltip will be positioned on the screen; the available values are:
                - ``fixed`` : tooltip coordinates must be given in respect to the parent element (defined by its ``parent_id``)
                - ``absolute`` : tooltip coordinates are actual viewport (screen) coordinates
            * *Class*  (``string``) --
              CSS class assigned to this tooltip box
            * *style* (``string``) --
              CSS style definition to be assigned to this tooltip; note, that this may overwrite default settings
        """
        self.__id = id_text
        self.__tooltip_text = tooltip_text
        self.__is_visible = False
        self.__x = 0
        self.__y = 0
        self.__offset_x = kwargs.get("offset_x", 20)
        self.__offset_y = kwargs.get("offset_y", 20)
        style = dict(tooltip_style)
        if "style" in kwargs: style = dict(style, **kwargs["style"])
        style['position'] = kwargs.get("position", "fixed")
        if "Class" in kwargs :
            self.__tooltip = html.DIV(tooltip_text, id=id_text, Class=kwargs["Class"],
                                  style={**style, 'height': height, 'width': width})
        else:
            self.__tooltip = html.DIV(tooltip_text, id=id_text,
                                  style={**style, 'height': height, 'width': width})
        document[parent_id] <= self.__tooltip

    @property
    def tooltip_text(self):
        """Returns tooltip text"""
        return self.__tooltip_text

    @tooltip_text.setter
    def tooltip_text(self, new_tooltip):
        self.__tooltip_text = new_tooltip
        self.__tooltip.innerHTML = new_tooltip

    @property
    def x(self):
        """X coordinate of tooltip div"""
        return self.__x

    @x.setter
    def x(self, x): self.__x = x

    @property
    def y(self):
        """Y coordinate of tooltip div"""

        return self.__y

    @y.setter
    def y(self, y): self.__y = y

    def show(self, x, y):
        """Makes this tooltip visible at given position on the screen.

        :param x: (``int``) x coordinate on the screen
        :param y: (``int``) y coordinate on the screen
        :return: ``None``
        """
        self.__x = x
        self.__y = y
        self.__is_visible = True
        self.__tooltip.style.visibility = "visible"
        self.__tooltip.style.display = "block"
        self.__tooltip.style.top = str(self.__y + self.__offset_y) + 'px'
        self.__tooltip.style.left = str(self.__x + self.__offset_x) + 'px'

    def hide(self, evt=None):
        """ Hides this tooltip
        :param evt: not used but necessary to be able to use this method as an event callback
        :return: ``None``
        """
        self.__is_visible = False
        self.__tooltip.style.visibility = "hidden"
        self.__tooltip.style.display = "none"



