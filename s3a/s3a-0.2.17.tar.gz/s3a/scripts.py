from pathlib import Path

from pyqtgraph.Qt import QtGui, QtWidgets, QtCore
import pyqtgraph as pg
import fire

def _s3agui(**kwargs):
  app = pg.mkQApp()
  here = Path(__file__).parent
  splash = QtWidgets.QSplashScreen(QtGui.QPixmap(str(here/'icons'/'s3asplash.svg')),
                                   QtCore.Qt.WindowStaysOnTopHint)
  splash.show()
  app.processEvents()
  from s3a import S3A, appInst

  win = S3A(**kwargs)
  splash.finish(win)

  QtCore.QTimer.singleShot(0, win.showMaximized)
  appInst.exec_()

def s3agui():
  fire.Fire(_s3agui)

if __name__ == '__main__':
    s3agui()