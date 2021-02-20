from ..CommonDefine import FigureType
from .Log import Logger
class Figure(object):
    optional_args = ['figure_size', 'save_path', 'title', 'bar_width']
    plot_type_x_y = [FigureType.BAR_PLOT, FigureType.POLYLINE_PLOT, FigureType.SCATTER_PLOT, FigureType.HISTOGRAM_2D_PLOT]
    plot_type_x = [FigureType.HISTOGRAM_PLOT, FigureType.HEATMAP_PLOT]

    @staticmethod
    def check_length_identical(*args):
        length = len(args[0])
        for arg in args:
            if len(arg) != length:
                return False
        return True
    
    def __init__(self, figure_type, Xs, Ys=None, legends=None, styles=None, **kwargs):
        if figure_type in self.plot_type_x_y:
            if Ys is None:
                Logger.get_logger().error("Invalid Ys, Ys cannot be None.")
                raise ValueError('Ys cannot be None when figure type is one of {}'.format(self.plot_type_x_y))
            if not self.check_length_identical(Xs, Ys):
                Logger.get_logger().error("Xs and Ys must have the same dimension.")
        elif figure_type in self.plot_type_x:
            if Ys is not None:
                Logger.get_logger().warning("Ys will be ignored becasue current figure type is one of {}".format(self.plot_type_x))

        self.figure_type = figure_type
        self.legends = legends
        self.Xs = Xs
        self.Ys = Ys
        self.styles = styles if styles is not None else [{} for _ in range(len(Xs))] if figure_type != FigureType.HISTOGRAM_2D_PLOT else {}

        for optional_arg in self.optional_args:
            setattr(self, optional_arg, None)
            if optional_arg in kwargs.keys():
                setattr(self, optional_arg, kwargs[optional_arg])

    
