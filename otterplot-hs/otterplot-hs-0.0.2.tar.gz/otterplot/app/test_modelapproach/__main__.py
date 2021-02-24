# -*- coding: utf-8 -*-
r"""
main module for testing the model api approach
"""
import matplotlib.pyplot as plt
from otterplot.model.cotterplotter import COtterPlotter


def main() -> None:
    r"""
    main function
    """
    l_otterplotter = COtterPlotter(plotmode='presentation', extent='broad', figheight=4, grid=(1, 1))

    # new devel
    """l_otterplotter.adjustlimits(ax_nr=0, xlims=(0, 1), ylims=(2, 4))
    l_otterplotter.adjustticks(x_major=0.2, x_minor=0.05, y_major=0.5, y_minor=0.1)
    l_otterplotter.adjustticklabels(0, which=(False, True, True, False))
    l_otterplotter.adjustlabels(0, xlabel='xlabel', ylabel='ylabel',xpos='top',ypos='left')
    l_otterplotter.adjustticklabels(1, which=(False, True, False, True))
    l_otterplotter.adjustlabels(1,xlabel='xlabel', ylabel='ylabel',xpos='top',ypos='right')
    l_otterplotter.adjustticklabels(2, which=(True, False, True, False))
    l_otterplotter.adjustlabels(2,xlabel='xlabel', ylabel='ylabel',xpos='bottom',ypos='left')
    l_otterplotter.adjustticklabels(3, which=(True, False, False, True))
    l_otterplotter.adjustlabels(3,xlabel='xlabel', ylabel='ylabel',xpos='bottom',ypos='right')
    ax = l_otterplotter.axes[0]
    """
    # ax.plot([-5,5],[0,0],'k-')

    plt.savefig('test.png')


if __name__ == "__main__":
    main()
