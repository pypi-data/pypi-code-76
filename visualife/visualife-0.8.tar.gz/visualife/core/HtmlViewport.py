#! /usr/bin/env python

import re

from visualife.core.SvgViewport import SvgViewport
from browser import console, document, html, window
from visualife.core.styles import *


class HtmlViewport(SvgViewport):
    """
    Draws graphics on a WWW page, in a given ``<svg>`` element of a page

    """

    #__slots__ = ['__svg','__svg_height', '__svg_width','__bind_ids','__bind_events','__bind_funcs']

    def __init__(self, svg_element, x_min, y_min, x_max, y_max, color='transparent',download_button=False,style=default_drawing_style,text_style=default_text_style):
        """
        Defines a drawing area
        """
        super().__init__('', x_min, y_min, x_max, y_max, color,style,text_style)
        self.__svg = svg_element
        self.__svg_width = svg_element.getBoundingClientRect().width
        self.__svg_height = svg_element.getBoundingClientRect().height
        self.__bind_ids = []
        self.__bind_events = []
        self.__bind_funcs = []
        self.__if_download = download_button
        self.__if_download_ready = False
        if "font-awesome" not in document:
            document <= html.LINK(id="font-awesome",
            href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.4.0/css/font-awesome.min.css",
            rel="stylesheet", type="text/css")

        self.__style_tag = html.STYLE(""".default_text_style {%s}
            .default_drawing_style {%s}""" % (self.text_style,self.style))
        self.__svg <= self.__style_tag

    @property
    def svg(self):
        """
        Returns <svg> element of a WWW page
        """
        return self.__svg

    @property
    def width_in_pixels(self):
        """Width of this viewport in pixels.

        Width in pixels may be different from the width defined in the respective SVG element

        :return: viewport width  which is the width of the respective SVG element in the page - in pixels
        """
        return self.__svg_width

    @property
    def height_in_pixels(self):
        """Height of this viewport in pixels

        Height in pixels may be different from the height defined in the respective SVG element

        :return: viewport height which is the height of the respective SVG element in the page - in pixels
        """
        return self.__svg_height

    def scale_x(self):
        """
        Returns a factor used to transform drawing X coordinates to internal SVG coordinates (X axis)

        Factor lower than 1.0 means that X range requested for this object is longer than actual width of the SVG element
        A shape of a given width (say, 50) is multiplied by this factor prior drawing, so if the scale is 1/2
        the drawn shape will be 25 in width
        """
        return self.__svg_width / super().get_width()

    def scale_y(self):
        """
        Returns a factor used to transform drawing Y coordinates to internal SVG coordinates (Y axis)

        Factor lower than 1.0 means that Y range requested for this object is longer than actual width of the SVG element
        A shape of a given height (say, 50) is multiplied by this factor prior drawing, so if the scale is 1/2
        the drawn shape will be 25 in height
        """
        return self.__svg_height / super().get_height()

    def clear(self):
        """
        Clears the viewport by removing all its children elements
        """
        self.__bind_ids = []
        self.__bind_events = []
        self.__bind_funcs = []
        self.__if_download_ready = False
        super().clear()
        

    # def text(self,id_str,x,y,text,**kwargs):
    #     """
    #     First translates "special" characters like < > and then call the method from the base class
    #     """
    #     special_codes = {"<":"&lt;",">":"&gt;"}
    #     text_to_read = text.deepcopy()
    #     for code in text_to_read:
    #         if code in special_codes.keys():
    #             text.replace(code,special_codes[code]) 
    #     print("TEXT",text)
    #     super().text(id_str,x,y,text,**kwargs)

    def error_msg(self,msg):
        """
        Prints error message.

        This polymorphic method prints a given error message to browser's console; SvgViewport will print to std.cerr;
        """
        console.log(msg)

    def viewport_name(self):
        """Returns the name if this viewport, which is always "HTML"

        The method allows dynamic distinction between SVG and HTML viewports
        """
        return "HTML"

    def add_download_button(self):
        """Adds a button to download current image"""

        if self.__if_download_ready: return

        download_id = self.__svg.id + ':' + 'download_plot'
        tooltip = html.A(id=download_id, style={"font-size": "10px", "background": "white",
                    "opacity": "0.8", "text-align": "center"})
        triangle = html.DIV(Class="fa fa-download", style={"font-size": "18px"})
        tooltip <= triangle
        tooltip <= html.DIV("download<br> plot as SVG")
        box = self.__svg.getBoundingClientRect()
        tooltip.style = {'position': 'absolute', 'visibility': "hidden", 'top': str(box.top + 20) + 'px',
                         'left': str(box.right - 30 - box.left) + 'px'}
        tooltip["href_lang"] = 'image/svg+xml'
        tooltip["download"] = "plot.svg"
        self.__svg.parent <= tooltip

        document[self.__svg.id].bind('mouseover',self.__show_dwnld_button)
        document[self.__svg.id].bind('mouseout',self.__hide_dwnld_button)
        document[download_id].bind('mouseover',self.__show_dwnld_button)
        document[download_id].bind('mouseout',self.__hide_dwnld_button)
        svgAsXML = window.XMLSerializer.new().serializeToString(self.__svg)
        document[download_id]["href"] = "data:image/svg+xml;utf8," + window.encodeURIComponent(svgAsXML)
        self.__if_download_ready = True

    def close(self):
        """Closes the SVG tag, adds bindings if any and sets styke for drawing and text"""
        super().close()

        self.__svg.innerHTML = """<style>
            .default_text_style {%s}
            .default_drawing_style {%s}
            </style>\n""" % (self.text_style, self.style) + "\n" + self.innerHTML

        if self.__if_download:
            self.add_download_button()

        for i in range(len(self.__bind_ids)):
            document[self.__bind_ids[i]].bind(self.__bind_events[i], self.__bind_funcs[i])
        
        return self.__svg

    def bind(self, id_str, on_what, func):
        """ Binds a function on given event to the element with given id 
        
        :param id_str: id of element you want to bind event to
        :param on_what: HTML event as `mouseover` or `click`
        :param func: function to bind
        """
        self.__bind_ids.append(id_str)
        self.__bind_events.append(on_what)
        self.__bind_funcs.append(func)

    def text_length(self, text, **kwargs):
        """ Measures the dimensions (in pixels) of a text as it would appear on a page

        :param text: text to be drawn
        :param kwargs: styling parameters as to be sent to ``SvgViewport.text()`` method
        :return: width and height of the text element, in pixels
        """
        backup = self.innerHTML
        self._SvgViewport__innerHTML = ""
        self.text("test-text", 0, 0, text, **kwargs)
        svg_text = self.innerHTML
        document <= html.DIV(id='test-test', style={'visibility': 'hidden'})
        document['test-test'].innerHTML = svg_text
        bb = document['test-text'].getBoundingClientRect()
        w = bb.right - bb.x
        h = bb.bottom - bb.y
        self._SvgViewport__innerHTML = backup

        return w, h


    def __show_dwnld_button(self,evt):
        document[self.__svg.id + ':' + 'download_plot'].style.visibility="visible"

    def __hide_dwnld_button(self,evt):
        document[self.__svg.id + ':' + 'download_plot'].style.visibility="hidden"




