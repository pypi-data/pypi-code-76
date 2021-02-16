from napari_arnheim.widgets.arnheim import ArnheimWidget
import napari
from qasync import QEventLoop
import asyncio

class gui_qt:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
          
    def __enter__(self): 
        self.napari_context = napari.gui_qt()
        self.app = self.napari_context.__enter__()
        self.viewer = napari.Viewer()
        self.arnheim = ArnheimWidget()
        self.viewer.window.add_dock_widget(self.arnheim, area="right")

        self.loop = QEventLoop(self.app)
        asyncio.set_event_loop(self.loop)
        self.loop.__enter__()
        self.loop.run_until_complete(self.arnheim.connectBergen())
        return self.viewer
      
    def __exit__(self, exc_type, exc_value, exc_traceback):
        try:
            self.loop.run_forever()
        except Exception as e:
            print(e)

        self.loop.__exit__(exc_type, exc_value, exc_traceback)
        self.napari_context.__exit__(exc_type, exc_value, exc_traceback)
        