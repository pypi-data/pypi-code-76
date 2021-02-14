import numpy as np
import matplotlib.pyplot as plt

from numerical_analysis.dependencies import GeometricalPlace
from numerical_analysis.splines import Bezier


class CompositeQuadraticBezier(GeometricalPlace):

    def __init__(self, control_points: np.array, datatype=np.float):
        super().__init__()
        self.datatype = datatype
        self.cp = control_points
        self.cp_enriched = control_points
        self.enrich_control_points()
        self.sectors = [Bezier(np.array([self.cp_enriched[2*i], self.cp_enriched[2*i + 1], self.cp_enriched[2*i + 2]]))
                        for i in range((len(self.cp_enriched)-1)//2)]

    def enrich_control_points(self):

        def mid_cp(cp0, cp1):
            return np.array([0.5 * (cp0[0] + cp1[0]), 0.5 * (cp0[1] + cp1[1])])

        self.cp_enriched = self.cp

        i = 1
        for j in range(len(self.cp) - 3):
            self.cp_enriched = np.insert(self.cp_enriched, i + 1,
                                         mid_cp(self.cp_enriched[i], self.cp_enriched[i + 1]), 0)
            i += 2

    def translate_t(self, t):
        if t != 1:
            i = int(t * len(self.sectors))
            u = t * len(self.sectors) - i
        else:
            i = len(self.sectors) - 1
            u = 1.
        return i, u

    def y_x(self, x):
        def detect_sector():
            i = 0
            while True:
                if self.sectors[i].x_t(1.) >= x:
                    return i
                i += 1
        return self.sectors[detect_sector()].y_x(x)

    def x_t(self, t):
        i, u = self.translate_t(t)
        return self.sectors[i].x_t(u)

    def y_t(self, t):
        i, u = self.translate_t(t)
        return self.sectors[i].y_t(u)

    def dx_dt(self, t):
        i, u = self.translate_t(t)
        return self.sectors[i].dx_dt(u)

    def dy_dt(self, t):
        i, u = self.translate_t(t)
        return self.sectors[i].dy_dt(u)

    def graph_cp(self):
        return [[self.cp[j, i] for j in range(len(self.cp))] for i in range(len(self.cp[0]))]

    def plot(self, dt, show_polyline=True, plot=True, export=False, filename="curve.png", title=None):
        plt.clf()
        if title:
            plt.title(title)
        graph = self.graph(dt)
        # noinspection PyUnresolvedReferences
        if show_polyline:
            plt.plot(graph[0], graph[1], "blue", self.graph_cp()[0], self.graph_cp()[1], "orange")
        else:
            plt.plot(graph[0], graph[1])

        if plot:
            plt.show()

        if export:
            plt.savefig(filename)

    def modify_control_point(self, i, new_control_point):
        self.cp[i][0] = new_control_point[0]
        self.cp[i][1] = new_control_point[1]
        self.cp_enriched = self.cp
        self.enrich_control_points()
        self.sectors = [Bezier(np.array([self.cp_enriched[2*i], self.cp_enriched[2*i + 1], self.cp_enriched[2*i + 2]]))
                        for i in range((len(self.cp_enriched)-1)//2)]
