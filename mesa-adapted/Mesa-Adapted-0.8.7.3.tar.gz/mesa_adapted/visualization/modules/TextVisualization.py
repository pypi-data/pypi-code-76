"""
Text Module
============

Module for drawing live-updating text.

"""
from mesa_adapted.visualization.ModularVisualization import VisualizationElement


class TextElement(VisualizationElement):
    package_includes = ["TextModule.js"]
    js_code = "elements.push(new TextModule());"
