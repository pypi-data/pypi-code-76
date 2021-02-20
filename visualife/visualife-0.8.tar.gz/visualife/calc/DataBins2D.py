#!/usr/bin/env python3
__author__ = "Dominik Gront"
__copyright__ = "University of Warsaw"
__license__ = "Apache License, Version 2.0"

from visualife.calc import Histogram2D
from collections import defaultdict


class DataBins2D(Histogram2D):
    """ DataBins2D class is a kind of a 2D histograms that records all the data that has been inserted into it.

    The object records the full row of data rather than just the two values used to define the 2D bin of this histogram
    """

    def __init__(self, **kwargs):
        """
        Creates the object
        :param kwargs: passed to the base class constructor
        """
        super().__init__(**kwargs)
        self.__data = defaultdict(list)

    def observe(self, *points, **kwargs):
        """Adds observation(s) to this DataBins object

        This method observes a whole row of data in a 2D bin identified by its two columns.
        It decides what should be observed and then calls ``observe_x_y()`` of the base class
        to make the actual observation. Finally it records the data object in the appropriate bin

        :param points: ``tuple(float,float)`` or ``list(tuple(float,float))`` - data to be inserted into this histogram
        :param kwargs: see below
        :return: None

        :Keyword Arguments:
            * *columns* (``tuple(int,int)``) -- which columns of data holds the observations for the histogram
            * *i_column* (``int``) -- which column of data hold observations for the first dimension
            * *j_column* (``int``) -- which column of data hold observations for the second dimension
        """

        if "columns" in kwargs:
            i_column, j_column = kwargs["columns"]
        else:
            i_column = kwargs.get("i_column", 0)
            j_column = kwargs.get("j_column", 1)

        if isinstance(points[0], (int, float)):         # --- user passed just x,y
            ix, iy = super().observe_x_y(points[0], points[1])
            self.__insert(ix, iy, points)
        elif isinstance(points[0], tuple):              # --- user passed a tuple (x,y)
            ix, iy = super().observe_x_y(points[0][i_column], points[0][j_column])
            self.__insert(ix, iy, points[0])
        else:
            for p in points[0]:
                ix, iy = super().observe_x_y(p[i_column], p[j_column])
                self.__insert(ix, iy, p)

    def observe_x_y(self, x, y, *row):
        """Adds an observation to this DataBins object

        This method observes a whole row of data in a 2D bin identified by its two values.

        :param x: value in the first dimension
        :param y: value in the second dimension
        :param row: the row of data to be recorded
        :return: 2D index of the bin where teh given data point was inserted ``(int, int)``
        """

        ix, iy = super().observe_x_y(x, y)
        self.__insert(ix, iy, *row)

    def get_observations(self, bin_coords):
        return self.__data[bin_coords]

    def __insert(self, x_place, y_place, observation):
        key = (x_place, y_place)
        if key not in self.__data:
            self.__data[key] = []
        self.__data[key].append(observation)
