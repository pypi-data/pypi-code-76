from napari_arnheim.widgets.helper import Helper
from PyQt5.QtWidgets import QWidget
from napari import Viewer
from bergen import Bergen

class BaseWidget(QWidget):

    def __init__(self, *args, base = None, **kwargs):
        self.base = base
        assert self.base is not None, "Please provide a base argument if you want to access it further down.."
        super().__init__(*args, **kwargs)


    @property
    def helper(self) -> Helper:
        if hasattr(self.base, "helper"):
            return self.base.helper
        else:
            raise NotImplementedError("The base you specified has no valid Helper instance")

    @property
    def viewer(self) -> Viewer:
        if hasattr(self.base, "viewer"):
            return self.base.viewer
        else:
            raise NotImplementedError("The base you specified has no valid Viewer instance")

        print("Received")
        return None

    @property
    def bergen(self) -> Bergen:
        if hasattr(self.base, "bergen"):
            return self.base.bergen
        else:
            raise NotImplementedError("The base you specified has no valid Bergen instance")



class BaseMixin:

    def __init__(self, *args, base = None, **kwargs):
        self.base = base
        assert self.base is not None, "Please provide a base argument if you want to access it further down.."
        super().__init__(*args, **kwargs)


    @property
    def helper(self) -> Helper:
        if hasattr(self.base, "helper"):
            return self.base.helper
        else:
            raise NotImplementedError("The base you specified has no valid Helper instance")




    @property
    def viewer(self) -> Viewer:
        if hasattr(self.base, "viewer"):
            return self.base.viewer
        else:
            raise NotImplementedError("The base you specified has no valid Viewer instance")

        print("Received")
        return None

    @property
    def bergen(self) -> Bergen:
        if hasattr(self.base, "bergen"):
            return self.base.bergen
        else:
            raise NotImplementedError("The base you specified has no valid Bergen instance")
