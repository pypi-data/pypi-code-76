from napari_arnheim.widgets.arnheim import ArnheimWidget
import napari
from qasync import QEventLoop
import asyncio
import sys



with napari.gui_qt() as app:
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    viewer = napari.Viewer()
    arnheim = ArnheimWidget()
    viewer.window.add_dock_widget(arnheim, area="right")

    with loop:
        loop.run_until_complete(arnheim.connectBergen())
        try:
            sys.exit(loop.run_forever())
        except Exception as e:
            loop.stop()