from bokeh.plotting import figure

from xbokeh.figure.base import BaseFigure


class DateGapFigure(BaseFigure):
    def __init__(self, date_list, title, width, height, tick_num=4, **kwargs):
        fig = figure(
            title=title,
            plot_width=width,
            plot_height=height,
            x_axis_label="Date",
            y_axis_label="Value",
            toolbar_location="above",
            **kwargs,
        )
        fig.xaxis.minor_tick_line_alpha = 0.0
        fig.yaxis.minor_tick_line_alpha = 0.3
        # fig.xgrid[0].ticker.desired_num_ticks = tick_num

        super().__init__(fig)

        self._label_mapper = None
        self.refresh_date_list(date_list)

    def _init_data(self) -> dict:
        return dict(x=[], y=[], x_desc=[])

    def refresh_date_list(self, date_list):
        label_mapper = dict()
        for index, date in enumerate(date_list):
            date = str(date)
            label_mapper[index] = "%s/%s/%s" % (date[2:4], date[4:6], date[6:])

        self._figure.xaxis.major_label_overrides = label_mapper
        self._figure.xaxis.bounds = (0, len(date_list))

        self._label_mapper = label_mapper

    # def set_source(self, group, name, **kwargs):
    #     x_range = kwargs.get("x")
    #     if x_range is None:
    #         raise ValueError("x is not defined")

    #     kwargs["x_desc"] = [self._label_mapper[i] for i in x_range]
    #     super().set_source(group, name, **kwargs)
