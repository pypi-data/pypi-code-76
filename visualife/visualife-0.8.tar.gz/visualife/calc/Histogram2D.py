#!/usr/bin/env python3
__author__ = "Anna Ożdżeńska, Dominik Gront"
__copyright__ = "University of Warsaw"
__license__ = "Apache License, Version 2.0"

from collections import defaultdict


class Histogram2D:

    __N_BINS = 100
    __WIDTH = 1
    __HIST_RANGE = (-50, 50)

    def __get_width_and_range(self, let: str, by_bins: bool, by_range: bool, by_width: bool):
        if by_bins:
            n_bins: int = self.args[f"n_bins_{let}"]
            if by_range:                                        # by bins and range
                hist_range: tuple = self.args[f"{let}_range"]
                range_len: float = hist_range[1] - hist_range[0]
                width = range_len/n_bins
            elif by_width:                                      # by bins and width
                width = self.args[f"{let}_width"]
                hist_range: tuple = (-width*n_bins/2, width*n_bins/2)
            else:                                               # by bins only
                width = self.__WIDTH
                hist_range: tuple = (-width*n_bins/2, width*n_bins/2)

        elif by_range:
            hist_range: tuple = self.args[f"{let}_range"]
            if by_width:                                        # by range and width
                width = self.args[f"{let}_width"]
            else:                                               # by range only
                width = self.__WIDTH

        elif by_width:                                          # by width only
            width = self.args[f"{let}_width"]
            hist_range: tuple = self.__HIST_RANGE

        else:                                                   # no data was given
            width = self.__WIDTH
            hist_range: tuple = self.__HIST_RANGE

        return width, hist_range

    def __init__(self, **kwargs):
        """Creates a new Histogram2D instance
        :param kwargs: see below
        :return: new Histogram2D instance

        :Keyword Arguments:
            * *n_bins* (``int``) -- number of bins in both dimensions
            * *n_bins_x* (``int``) -- number of bins in X dimension
            * *n_bins_y* (``int``) -- number of bins in Y dimension
            * *range* (``tuple(value,value)``) -- histogram range, same for both dimensions
            * *x_range* (``tuple(float,float)``) -- histogram range in X dimension
            * *y_range* (``tuple(float,float)``) -- histogram range in Y dimension
            * *width* (``float``) -- bin width, same for both dimensions
            * *x_width* (``float``) -- bin width in X dimension
            * *y_width* (``float``) -- bin width in Y dimension
        """
        self.args = kwargs.copy()

        if "n_bins" in kwargs.keys():
            x_by_bins = y_by_bins = True
            self.args["n_bins_x"] = self.args["n_bins_y"] = int(kwargs["n_bins"])
        else:
            x_by_bins = "n_bins_x" in kwargs.keys()
            y_by_bins = "n_bins_y" in kwargs.keys()

        if "range" in kwargs.keys():
            x_by_range = y_by_range = True
            self.args["x_range"] = self.args["y_range"] = kwargs["range"]
        else:
            x_by_range = "x_range" in kwargs.keys()
            y_by_range = "y_range" in kwargs.keys()

        x_by_width = "x_width" in kwargs.keys() or "width" in kwargs.keys()
        y_by_width = "y_width" in kwargs.keys() or "width" in kwargs.keys()
        if "width" in kwargs.keys():
            self.args["x_width"] = kwargs["width"]
            self.args["y_width"] = kwargs["width"]

        self.x_width, self.x_hist_range = self.__get_width_and_range('x', x_by_bins, x_by_range, x_by_width)
        self.y_width, self.y_hist_range = self.__get_width_and_range('y', y_by_bins, y_by_range, y_by_width)
        self.__count_outliers = self.__count_in_hist = 0
        self.__x_hist, self.__y_hist, self.__hist = defaultdict(int), defaultdict(int), defaultdict(int)

    def observe(self, *points, **kwargs):
        """Adds observation(s) to this histogram

        This method decides what should be observed and then calls ``observe_x_y()`` to make the actual observation

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
            self.observe_x_y(points[0],points[1])
        elif isinstance(points[0], tuple):              # --- user passed a tuple (x,y)
            self.observe_x_y(points[0][i_column], points[0][j_column])
        else:
            for p in points[0]:
                self.observe_x_y(p[i_column], p[j_column])

    def observe_x_y(self, x, y):
        """Observes a pair of values: x and y

        :param x: value in the first dimension
        :param y: value in the second dimension
        :return: 2D index of the bin where teh given data point was inserted ``(int, int)``
        """

        x_place = (x // self.x_width) * self.x_width
        y_place = (y // self.y_width) * self.y_width

        if any([
            x_place < self.x_hist_range[0], x_place > self.x_hist_range[1],
            y_place < self.y_hist_range[0], y_place > self.y_hist_range[1],
        ]):
            self.__count_outliers += 1

        else:
            self.__x_hist[x_place] += 1
            self.__y_hist[y_place] += 1
            self.__hist[(x_place, y_place)] += 1
            self.__count_in_hist += 1
        return x_place, y_place

    def outliers(self):
        return self.__count_outliers

    def count(self):
        return self.__count_in_hist

    def histogram_x(self):
        return dict(self.__x_hist)

    def histogram_y(self):
        return dict(self.__y_hist)

    def get_bin_by_point(self, point):
        x, y = point
        x_place = (x // self.x_width) * self.x_width
        y_place = (y // self.y_width) * self.y_width
        return self.get_bin_by_coordinates((x_place, y_place))

    def get_bin_by_coordinates(self, coords):
        return self.__hist[coords]

    def get_bin_coordinates(self, point):
        x, y = point
        x_place = (x // self.x_width) * self.x_width
        y_place = (y // self.y_width) * self.y_width
        return x_place, y_place

    def get_histogram(self):
        return dict(self.__hist)

    def get_xyv(self):
        x, y, val = [], [], []
        for k, v in self.__hist.items():
            x.append(k[0])
            y.append(k[1])
            val.append(v)

        return x, y, val
