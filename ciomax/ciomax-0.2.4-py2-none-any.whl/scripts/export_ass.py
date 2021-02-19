
import pymxs
import os
from ciomax.renderer import Renderer

rt = pymxs.runtime
def main(dialog, *args):

    renderer = Renderer.get()
    if not renderer.__class__.__name__ == "ArnoldRenderer":
        raise TypeError("Please the current renderer to Arnold")

    main_sequence = dialog.main_tab.section("FramesSection").main_sequence

    ass_file_prefix = args[0]

    print "Ensure directory ia avalable for ass files"
    _ensure_directory_for(ass_file_prefix)

    print "Closing render setup window if open..."
    if rt.renderSceneDialog.isOpen():
        rt.renderSceneDialog.close()

    print "Setting render time type to use a specified sequence..."
    rt.rendTimeType=4

    print "Setting the frame range..."
    rt.rendPickupFrames="{}-{}".format(main_sequence.start, main_sequence.end)

    print "Setting the by frame to 1..."
    rt.rendNThFrame=1

    print "Setting ass export to on..."
    rt.renderers.current.export_to_ass = True

    print "Setting the ass filepath to","{}.ass".format(ass_file_prefix)
    rt.renderers.current.ass_file_path = "{}.ass".format(ass_file_prefix)
    
    # Annoyingly, setting rendPickupFrames above is not enough. We have to
    # provide start and end again here.
    print "Exporting ass files..."
    rt.render(fromFrame=main_sequence.start,toFrame=main_sequence.end, vfb=False)

    # return list of ass files
    print "Done"
    return main_sequence.expand("{}####.ass".format(ass_file_prefix))
    
 

def _ensure_directory_for(path):
    """Ensure that the parent directory of `path` exists"""
    dirname = os.path.dirname(path)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
