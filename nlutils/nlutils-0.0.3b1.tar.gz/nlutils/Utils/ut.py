from .Figure import Figure
from .Visual import draw_single_figure,draw_multi_figures
from ..CommonDefine import FigureType

import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    # Unit test for compare_visualization_polyline
    Xs = [[1, 2, 3, 4, 5, 6], [1, 2, 6, 8, 9, 11],[1, 2, 6, 8, 9, 11]]
    Xs = np.array(Xs)
    Ys = [[1, 2, 6, 7, 8, 9], [2, 5, 7, 8, 9, 11],[1, 2, 6, 8, 9, 11]]
    Ys = np.array(Ys)
    legends = ['x1', 'x2']
    XHs = [[1,1,1,2,4,5,1,2,3,3,2,1,2,2], [1,1,21,2,3,3,4,5,2,1,2,4,46,33,2,12,4,214,12,42,1,2,2]]
    XHs = np.array(XHs)
    XH2s = [1,1,21,2,3,3,4,5,2,1,2,4,46,33,2,12,4,11,12,42,1,2,2]
    XH2s = np.array(XH2s)
    YH2s = [1,1,21,2,3,3,4,5,2,1,2,4,46,33,2,12,4,11,12,42,1,2,2]
    YH2s = np.array(YH2s)

    harvest = np.array([[0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                    [2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0],
                    [1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0],
                    [0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0],
                    [0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0],
                    [1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1],
                    [0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3]])
    # styles = [{'color':'yellow', 'alpha':0.5, 'edgecolor':'green'}, {'color':'blue', 'alpha':0.3,'edgecolor':'red'}]
    # print(Xs, Ys, type(XHs))
    fig1 = Figure(FigureType.BAR_PLOT, Xs, Ys, legends, title="Bar Plot", figure_size=(5, 10))
    fig2 = Figure(FigureType.POLYLINE_PLOT, Xs, Ys, legends, title="Polyline Plot")
    fig3 = Figure(FigureType.SCATTER_PLOT, Xs, Ys, legends, title="Scatter Plot")
    fig4 = Figure(FigureType.HISTOGRAM_PLOT, XHs, legends=legends, title="His Plot")
    fig5 = Figure(FigureType.HISTOGRAM_2D_PLOT, XH2s, YH2s, styles={'bins':50}, title="Test Case")
    fig6 = Figure(FigureType.HISTOGRAM_PLOT, XHs, legends=legends, title="His Plot")
    fig7 = Figure(FigureType.HISTOGRAM_2D_PLOT, XH2s, YH2s, styles={'bins':50}, title="Test Case")
    # fig6 = Figure(FigureType.HEATMAP_PLOT, Xs, styles={'bins':50}, title="Test Case")
    draw_single_figure([fig1])
    # draw_multi_figures([fig1, fig2, fig3, fig4, fig5, fig6, fig7])