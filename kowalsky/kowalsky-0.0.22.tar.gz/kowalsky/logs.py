import matplotlib.pyplot as plt
import pylab as pl
from IPython import display
import math


def calc_percent(part, all):
    return f"{round(part / all * 100)}%"


def make_pretty_pyplot():
    plt.style.use('ggplot')


class LivePyPlot:

    def __init__(self, direction):
        self.x = []
        self.y = []
        self.best = -math.inf if direction == 'maximize' else math.inf
        self.fn = max if direction == 'maximize' else min

    def __call__(self, new_point):
        self.best = self.fn(new_point, self.best)
        self.y.append(self.best)
        self.x.append(len(self.y))

        plt.title(f"Best: {self.best:.3}")
        plt.plot(self.x, self.y, color='red')

        display.clear_output(wait=True)
        display.display(pl.gcf())

    def clear(self):
        plt.close()
