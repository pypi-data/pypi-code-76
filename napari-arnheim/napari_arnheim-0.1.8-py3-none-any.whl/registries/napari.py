

CURRENT_NAPARI = None

def set_current_viewer(viewer):
    print("Setting Current Viewer")
    global CURRENT_NAPARI
    CURRENT_NAPARI = viewer

def get_current_viewer():
    global CURRENT_NAPARI
    if CURRENT_NAPARI:
        return CURRENT_NAPARI
    else:
        raise Exception("There seems to be no napari viewer initilized")