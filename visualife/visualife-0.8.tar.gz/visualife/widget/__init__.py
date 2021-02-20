""" The widgets package contains all the widgets provided by library, i.e. independent web-page components
devised to display data in an interactive manner.
"""
try:
    from visualife.widget.FileReaderWidget import *
    from visualife.widget.GLViewerWidget import GLViewerWidget
    from visualife.widget.SequenceViewer import SequenceViewer
    from visualife.widget.StructureViewer import StructureViewer
    from visualife.widget.SecondaryStructureViewer import SecondaryStructureViewer
    from visualife.widget.TooltipWidget import TooltipWidget
    from visualife.widget.TableWidget import TableWidget
    from visualife.widget.MSAViewer import MSAViewer
    from visualife.widget.SequenceFeaturesBar import SequenceFeaturesBar
except:
    pass

