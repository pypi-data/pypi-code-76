try:
    QT = 4
    import PyQt4
    from matplotlib.backends.backend_qt4agg import (
        NavigationToolbar2QT as NavigationToolbar,
    )
except ImportError:
    QT = 5
    import PyQt5
    from matplotlib.backends.backend_qt5agg import (
        NavigationToolbar2QT as NavigationToolbar,
    )


class Boxmanager_Toolbar(NavigationToolbar):
    def __init__(self, canvas_, parent_, fig, ax, boxmanager):
        self.fig = fig
        self.ax = ax
        self.dozoom = False
        self.boxmanager = boxmanager
        NavigationToolbar.__init__(self, canvas_, parent_)

    def press_zoom(self, event):
        super(Boxmanager_Toolbar, self).press_zoom(event)

    def zoom(self, *args):
        super(Boxmanager_Toolbar, self).zoom(args)

    def home(self, *args):
        # Restore

        self.boxmanager.delete_all_patches(self.boxmanager.rectangles)
        self.boxmanager.fig.canvas.restore_region(self.boxmanager.background_current)
        self.boxmanager.background_current = self.fig.canvas.copy_from_bbox(
            self.ax.bbox
        )
        self.boxmanager.draw_all_patches(self.boxmanager.rectangles)
        super(Boxmanager_Toolbar, self).home(args)

    def release_zoom(self, event):

        if not self._xypress:
            return
        self.dozoom = False
        for cur_xypress in self._xypress:
            x, y = event.x, event.y
            lastx = cur_xypress[0]
            lasty = cur_xypress[1]
            # ignore singular clicks - 5 pixels is a threshold
            if not (abs(x - lastx) < 5 or abs(y - lasty) < 5):
                self.dozoom = True
                self.boxmanager.delete_all_patches(self.boxmanager.rectangles)
                self.boxmanager.fig.canvas.restore_region(
                    self.boxmanager.background_current
                )
                self.boxmanager.zoom_update = True

        super(Boxmanager_Toolbar, self).release_zoom(event)

    def pan(self, *args):
        super(Boxmanager_Toolbar, self).pan(args)

    def drag_pan(self, event):
        print("drag pan")
        super(Boxmanager_Toolbar, self).drag_pan(event)
        # self.zoom_update = True
        self.boxmanager.delete_all_patches(self.boxmanager.rectangles)
        self.fig.canvas.restore_region(self.boxmanager.background_current)
        self.boxmanager.background_current = self.fig.canvas.copy_from_bbox(
            self.ax.bbox
        )
        # self.boxmanager.draw_all_patches(self.boxmanager.rectangles)
        self.boxmanager.zoom_update = True
