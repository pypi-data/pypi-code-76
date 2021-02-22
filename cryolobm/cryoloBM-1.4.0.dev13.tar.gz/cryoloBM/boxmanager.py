import os
import sys
import matplotlib.pyplot as plt

from mrcfile import mmap as mrcfile_mmap        #it is not in the setup.py because it is already installed by cryolo
import numpy as np
import random
from math import isnan
try:
    QT = 4
    import PyQt4.QtGui as QtG
    import PyQt4.QtCore as QtCore
    from PyQt4.QtGui import QFontMetrics
    from PyQt4.QtCore import pyqtSlot
    import matplotlib.backends.backend_qt4agg as plt_qtbackend
except ImportError:
    QT = 5
    import PyQt5.QtWidgets as QtG
    from PyQt5.QtGui import QFontMetrics
    import PyQt5.QtCore as QtCore
    from PyQt5.QtCore import pyqtSlot
    import matplotlib.backends.backend_qt5agg as plt_qtbackend

from os import path
from cryolo import imagereader, CoordsIO, grouping3d,  utils
from . import boxmanager_toolbar, MySketch, helper, helper_writer,visualization_3D_Window
import argparse
from copy import deepcopy

import cryoloBM.__init__ as ini

#todo: we disabled the real time tracing for the filament case. If in the future we decide to restore it do the following
    # 1) replace all the 'if self.preview_is_on and self.has_filament is False:' with 'if self.preview_is_on:'
        # except the one in 'def onclick'
    # NB: there are no more self.changed_slider_release() in the changed_slider* functions for the tracing params

class Params:
    """
    Used only in tomo folder case
    We storage the 'thresholding' and 'tracing' params in order to keep the state for each tomo
    """
    def __init__(self, tomo_name, filter_freq, upper_size_thresh, lower_size_thresh, conf_thresh, num_boxes_thresh,
                 min_width_edge, search_range, memory, min_length, win_size):
        self.tomo_name = tomo_name
        self.filter_freq = filter_freq
        self.upper_size_thresh = upper_size_thresh
        self.lower_size_thresh = lower_size_thresh
        self.conf_thresh = conf_thresh
        self.num_boxes_thresh = num_boxes_thresh
        self.min_width_edge = min_width_edge
        self.search_range = search_range
        self.memory=  memory
        self.min_length = min_length
        self.win_size =win_size

    def reset_to_default_values(self):
        """
        Reset to default value. Win_size default value is the box_size
        """
        self.filter_freq = DEFAULT_FILTER_FREQ
        self.upper_size_thresh = DEFAULT_UPPER_SIZE_THRESH
        self.lower_size_thresh = DEFAULT_LOWER_SIZE_THRESH
        self.conf_thresh = DEFAULT_CURRENT_CONF_THRESH
        self.num_boxes_thresh = DEFAULT_CURRENT_NUM_BOXES_THRESH
        self.min_width_edge = DEFAULT_MIN_WIDTH_EDGE
        self.search_range = DEFAULT_SEARCH_RANGE
        self.memory = DEFAULT_MEMORY
        self.min_length = DEFAULT_MIN_LENGTH
        self.win_size = DEFAULT_BOX_SIZE

    def has_same_tracing_params(self,param, has_filament = False):
        """
        :param param: a Params obj
        :param has_filament: True if we analyze filament
        Return True if param has the same tracing parameters
        """
        min_cond = self.min_length == param.min_length and self.memory == param.memory and self.search_range  == param.search_range
        if has_filament:
            return min_cond and self.min_width_edge == param.min_width_edge and self.win_size == param.win_size
        return self.min_length == param.min_length and self.memory == param.memory and self.search_range  == param.search_range

def create_parser(parser):
    parser.add_argument("-i", "--image_dir", help="Path to image directory.")

    parser.add_argument("-b", "--box_dir", help="Path to box directory.")

    parser.add_argument("--wildcard",
                           help="Wildcard for selecting spcific images (e.g *_new_*.mrc)")

    parser.add_argument("-t", "--is_tomo_dir", action="store_true",
                           help="Flag for specifying that the directory contains tomograms.")

argparser = argparse.ArgumentParser(
    description="Train and validate crYOLO on any dataset",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
create_parser(argparser)



INDEX_TAB_TRACING = 3 # FOR REMOVING THE TAB

DEFAULT_BOX_SIZE = 200
DEFAULT_UPPER_SIZE_THRESH = 99999
DEFAULT_LOWER_SIZE_THRESH = 0
DEFAULT_CURRENT_CONF_THRESH = 0.3
DEFAULT_FILTER_FREQ = 0.1
DEFAULT_CURRENT_NUM_BOXES_THRESH = 0
DEFAULT_MIN_NUM_BOXES_THRESH = 0
DEFAULT_MAX_NUM_BOXES_THRESH = 100
DEFAULT_MIN_WIDTH_EDGE = 0.2
DEFAULT_BOX_DISTANCE_FILAMENT_PICKING = 5

#default value for tracing
DEFAULT_SEARCH_RANGE  = 5
DEFAULT_MEMORY =  0
DEFAULT_MIN_LENGTH =  5

CIRCLE = 'Circle'
RECT = 'Rectangle'

PARTICLE = 'Particle'
FILAMENT = 'Filament'

class picked_filament:
    """
    A picked filament
    In the rectangular visualization we lose the left half of the first square box (the one on the first point of the filament)
    """
    def __init__(self, box_size, is_3D_tomo=True):
        """
        :param box_size:
        :param is_3D_tomo:
        """
        self.boxsize = box_size
        self.begin_fil = list()        # event position obj ... the first click (got via on_click)
        self.end_fil = list          # event position obj ... the las click (got via on_release or on_move)

        self.filament=utils.Filament(list())        # crYOLO filament object

        self.is_3D_tomo=is_3D_tomo

        self.angle = None
        self.offset = None          # offset to center the filament (i.e.: for default we pick via mouse on the left corner but we need to pick on the center of the filament)
        self.rect_vect = None       # versor of the rectangle
        self.orth_vect = None       # versor orthogonal to self.rect_vect

        # distance between the first and last sketch
        self.width = box_size
        self.height = box_size

    def set_first(self,event):
        """
        It sets the first element
        :param event: click event via 'onclick
        """
        self.begin_fil = [event.xdata,event.ydata]
        self.end_fil =  [event.xdata,event.ydata]

    def append_sketch(self,sketch):
        """
        Append sketch to le list
        :param sketch: MySketch obj
        """
        self.filament.add_box(sketch)

    def reset_sketches(self):
        self.filament.boxes = list()


    def set_line_params(self):
        """
        Calculate params of the line got from  'begin_fil' and 'end_fil'
        """
        self.rect_vect = np.array(self.end_fil) - np.array(self.begin_fil)
        self.width = np.linalg.norm(self.rect_vect)
        self.angle = np.rad2deg(np.arctan2(self.rect_vect[1], self.rect_vect[0]))

        # calculate offset to filament start. this has the effect that filaments can picked centerd.
        self.orth_vect = np.array(self.rect_vect)/self.width # normalized vector
        help = self.orth_vect[0]
        self.orth_vect[0] = self.orth_vect[1]
        self.orth_vect[1] = -1*help  #now it orthogonal to rect_vect
        self.offset = self.orth_vect * self.height/2 # offset for drawing.


    def get_R(self):
        """
        Returns the rotation matrix of the rectangle as np array
        """
        theta = -np.radians(self.angle)
        c, s = np.cos(theta), np.sin(theta)
        return np.array(((c, -s), (s, c)))


    def get_coordinate_rect(self):
        """
        returns the real coordinate of the rectangles as np array
        -) each row is a point x,y.
        -) first row =bottom left corner
        -) second row = bottom right corner
        -) third row = top left corner
        -) fourth row = top right corner
        """
        norm_v_ort = self.orth_vect/np.linalg.norm(self.orth_vect)
        scale_v_ort = norm_v_ort*self.height

        corner_0 = np.array(self.begin_fil)-np.array(self.offset)
        corner_1 = corner_0 + scale_v_ort
        corner_2 = corner_0 + self.rect_vect
        corner_3 = corner_2 + scale_v_ort
        return np.vstack((corner_0, corner_1, corner_2, corner_3))


    def  get_rotated_coordinate_rect(self):
        """
        Returns the coordinate of the rect on the x axis
        """
        return self.get_R()@self.get_coordinate_rect().T


    def fill_sketches(self, box_distance = 1, as_bbox = False, z=None):
        """
        It is used for saving data on file
        Create a square box every 'box_distance' point on the central line of the filament
        :param box_distance: sampling step
        :param as_bbox: convert the sketches in cryolo.bbox
        :param z:   in case of filament in a tomo I need to know the slice
        """
        self.set_line_params()
        self.reset_sketches()
        Nboxes = int(self.width//box_distance)
        boxcoords = np.linspace(self.begin_fil, self.end_fil,Nboxes,endpoint=True)

        for row in boxcoords:
            x = row[0]
            y = row[1]
            # the bbox considers the center of the rect. For saving on file purpose
            # the matplotli Rectangle considers the bottom left corner and the angle. For real time overlapping visualization purpose
            x = x - self.height / 2 if as_bbox else x + self.offset[0]
            y = y - self.height / 2 if as_bbox else y + self.offset[1]

            sketch = MySketch.MySketch(xy=(x, y), width=self.boxsize, height=self.boxsize,
                                       is_3d_tomo=self.is_3D_tomo, angle=self.angle, est_size=self.boxsize, confidence=1,
                                       only_3D_visualization=False, num_boxes=1, meta=None, z=z,
                                       linewidth=1, edgecolor="r", facecolor="none")
            if as_bbox:
                self.append_sketch(sketch.get_as_BBox(confidence=1, z=z))
            else:
                self.append_sketch(sketch)


    def get_sketches(self):
        return self.filament.boxes


    def get_rect_sketch(self):
        self.set_line_params()

        # for centering on x i have to calculate, geometrically, it. It does not deserve calulate it
        return  MySketch.MySketch(xy=(self.begin_fil[0] + self.offset[0], self.begin_fil[1] + self.offset[1]) , width=self.width, height=self.height,
                                       is_3d_tomo=self.is_3D_tomo, angle=self.angle, est_size=self.boxsize, confidence=1,
                                       only_3D_visualization=False, num_boxes=1, meta=None, z=None,
                                       linewidth=1, edgecolor="r", facecolor="none")



class MainWindow(QtG.QMainWindow):
    def __init__(self, font, images_path=None, boxes_path=None, wildcard=None, parent=None, is_tomo_dir=None):

        # For avoiding err msg, due to the sketches visualization, when loading filament
        self.is_loading_boxes = False

        self.box_distance_filament_picking = DEFAULT_BOX_DISTANCE_FILAMENT_PICKING
        self.params = dict()
        self.trace_all = False
        '''
            for optimization purpose in the 3D visualization (cbox or emn3D cases) we create the visualization,
            (via 'fill_next_prev_slice'), only once at the beginning. After that we will switch between the
            sketches saved in the istances of MySketch class
        '''
        self.first_call_use_circle_changed = True

        # when we trace using 'trace' button we want to check the 'preview' checkbox without running its connected box
        # the 'run_via_trace_button' variable is an helper variable to do that
        self.run_via_trace_button = False

        # used folder tomo case to avoid to pop up continuously the apply_to_all_the_tomo_question's question when moving the slider
        self.is_slider_pressed = False
        #  used folder tomo case to avoid to pop up continuously the apply_to_all_the_tomo_question's question when loading the data
        self.is_loading_max_min_sizes = False
        # used folder tomo case to avoid to pop up continuously the apply_to_all_the_tomo_question's question when:
        # -) resetting via File->reset
        # -) change tomo and load its params
        self.is_updating_params = False

        #true if we are picking filament for saving data for training crYOLO
        self.picking_filament = False
        self.picked_filament_list = list()          # list of picking_filament obj on the current image
        self.picked_filament_dictionary = dict()    # same syntax as self.box_dictionary for collecting the picked filament

        # after picking a filament (in the onrelease funtion) i save its boxes here to avoid to unfold it every time in the
        # real-time visualization step (in the onmove function)
        self.picked_filament_as_rect_dictionary = list()    # collect the rects representing the filaments

        self.removing_picked_filament = False

        # used in the tomo cases in the cbox/cbox untraced
        self.has_filament = False
        self.filament_dict = dict()

        self.preview_win = None
        self.is_folder_3D_tomo = False
        self.is_3D_tomo=False
        self.index_3D_tomo=None
        self.im = None
        self.rectangles = []
        self.current_image3D_mmap = None

        # last* variables are used to clean the boxes when we switch between 3D tomo images in a list of images
        self.last_file_3D_tomo=None
        self.last_index_3D_tomo = None
        self.last_filename_in_tomo_folder = None

        self.use_circle = False # for default draw the rectangle
        self.active_3D_visualization = False  # for default does not show the 3D visualization


        # The 'est_size' instance of a Sketch Class contains the estimated size of cryolo, when loaded from '.cbox',
        # and should be never changed
        self.est_box_from_cbox = None

        self.preview_is_on = False


        super(MainWindow, self).__init__(parent)
        # SETUP QT
        self.font = font

        self.setWindowTitle("BoxManager " + ini.__version__)
        central_widget = QtG.QWidget(self)

        self.setCentralWidget(central_widget)

        # Center on screen
        resolution = QtG.QDesktopWidget().screenGeometry()
        self.move(
            (resolution.width() / 2) - (self.frameSize().width() / 2),
            (resolution.height() / 2) - (self.frameSize().height() / 2),
            )

        # Setup Menu
        close_action = QtG.QAction("Close", self)
        close_action.setShortcut("Ctrl+Q")
        close_action.setStatusTip("Leave the app")
        close_action.triggered.connect(self.close_boxmanager)

        open_image_folder = QtG.QAction("Micrograph folder", self)
        open_image_folder.triggered.connect(self.open_image_folder)

        open_image_3D_folder = QtG.QAction("Folder", self)
        open_image_3D_folder.triggered.connect(self.open_image3D_folder)

        open_image3D_tomo = QtG.QAction("File", self)
        open_image3D_tomo.triggered.connect(self.open_image3D_tomo)

        import_box_folder = QtG.QAction("Import box files", self)
        import_box_folder.triggered.connect(self.load_box_files)

        save_data = QtG.QAction("Save", self)
        save_data.triggered.connect(self.write_all_type)

        resetMenu = QtG.QAction("Reset", self)
        resetMenu.triggered.connect(self.reset_config)

        self.show_confidence_histogram_action = QtG.QAction(
            "Confidence histogram", self
        )
        self.show_confidence_histogram_action.triggered.connect(
            self.show_confidence_histogram
        )
        self.show_confidence_histogram_action.setEnabled(False)

        self.show_size_distribution_action = QtG.QAction("Size distribution", self)
        self.show_size_distribution_action.triggered.connect(
            self.show_size_distribution
        )
        self.show_size_distribution_action.setEnabled(False)

        self.mainMenu = self.menuBar()
        self.fileMenu = self.mainMenu.addMenu("&File")
        openMenu = self.fileMenu.addMenu("&Open")
        openMenuSPA = openMenu.addMenu("&SPA")
        openMenuTomo = openMenu.addMenu("&Tomogram")
        openMenuSPA.addAction(open_image_folder)
        openMenuTomo.addAction(open_image_3D_folder)
        openMenuTomo.addAction(open_image3D_tomo)

        self.fileMenu.addAction(import_box_folder)
        self.fileMenu.addAction(save_data)
        self.fileMenu.addAction(resetMenu)

        self.fileMenu.addAction(close_action)
        self.image_folder = ""

        self.plotMenu = self.mainMenu.addMenu("&Plot")
        self.plotMenu.addAction(self.show_confidence_histogram_action)
        self.plotMenu.addAction(self.show_size_distribution_action)

        # Setup tree
        self.layout = QtG.QGridLayout(central_widget)
        self.setMenuBar(self.mainMenu)

        self.tree = QtG.QTreeWidget(self)
        self.tree.setHeaderHidden(True)
        self.layout.addWidget(self.tree, 0, 0, 1, 3)
        self.tree.currentItemChanged.connect(self._event_image_changed)
        self.tree.itemChanged.connect(self._event_checkbox_changed)

        # Setup params and related Qt object used in the tabs
        # VISUALIZATION TAB
        self.boxsize = DEFAULT_BOX_SIZE
        self.boxsize_line = QtG.QLineEdit(str(self.boxsize))
        self.button_set_box_size = QtG.QPushButton("Set")
        self.boxsize_label = QtG.QLabel("Box size: ")

        self.use_circle_label = QtG.QLabel("Visualization: ")

        self.use_circle_combobox = QtG.QComboBox()

        self.use_estimated_size_label = QtG.QLabel("Use estimated size:")
        self.use_estimated_size_checkbox = QtG.QCheckBox()

        self.picking_label = QtG.QLabel("Picking:")
        self.picking_filament_combox = QtG.QComboBox()

        # THRESHOLDING TAB
        self.lower_size_thresh_label = QtG.QLabel("Minimum size: ")
        self.lower_size_thresh = DEFAULT_LOWER_SIZE_THRESH
        self.lower_size_thresh_slide = QtG.QSlider(QtCore.Qt.Horizontal)
        self.lower_size_thresh_line = QtG.QLineEdit(str(DEFAULT_LOWER_SIZE_THRESH))

        self.upper_size_thresh_label = QtG.QLabel("Maximum size: ")
        self.upper_size_thresh = DEFAULT_UPPER_SIZE_THRESH
        self.upper_size_thresh_slide = QtG.QSlider(QtCore.Qt.Horizontal)
        self.upper_size_thresh_line = QtG.QLineEdit(str(DEFAULT_UPPER_SIZE_THRESH))

        self.current_conf_thresh = DEFAULT_CURRENT_CONF_THRESH
        self.conf_thresh_label = QtG.QLabel("Confidence threshold: ")
        self.conf_thresh_slide = QtG.QSlider(QtCore.Qt.Horizontal)
        self.conf_thresh_line = QtG.QLineEdit(str(DEFAULT_CURRENT_CONF_THRESH))

        self.current_num_boxes_thresh = DEFAULT_CURRENT_NUM_BOXES_THRESH
        self.num_boxes_thres_label = QtG.QLabel("Number boxes threshold: ")
        self.num_boxes_thresh_slide = QtG.QSlider(QtCore.Qt.Horizontal)
        self.num_boxes_thresh_line = QtG.QLineEdit(str(DEFAULT_CURRENT_NUM_BOXES_THRESH))

        # FILTERING TAB
        self.filter_freq = DEFAULT_FILTER_FREQ
        self.filter_line = QtG.QLineEdit(str(self.filter_freq))
        self.low_pass_filter_label = QtG.QLabel("Low pass filter cut-off: ")
        self.button_apply_filter = QtG.QPushButton("Apply")
        self.janny_label = QtG.QLabel("Janny denoising: ")
        self.button_janny = QtG.QPushButton("Run")

        # TRACING TAB
        self.preview_label = QtG.QLabel("Preview")
        self.preview_checkbox = QtG.QCheckBox()
        self.button_trace = QtG.QPushButton("Trace")

        self.search_range = DEFAULT_SEARCH_RANGE
        self.search_range_line = QtG.QLineEdit(str(self.search_range))
        self.search_range_label = QtG.QLabel("Search range: ")
        self.search_range_slider = QtG.QSlider(QtCore.Qt.Horizontal)

        self.memory = DEFAULT_MEMORY
        self.memory_line = QtG.QLineEdit(str(self.memory))
        self.memory_label = QtG.QLabel("Memory: ")
        self.memory_slider = QtG.QSlider(QtCore.Qt.Horizontal)

        self.min_length = DEFAULT_MIN_LENGTH
        self.min_length_line = QtG.QLineEdit(str(self.min_length))
        self.min_length_label = QtG.QLabel("Minimum length: ")
        self.min_length_slider = QtG.QSlider(QtCore.Qt.Horizontal)

        # param for tracking the filament
        self.win_size = None     # it will set for default to 'self.box_size'
        self.win_size_line = QtG.QLineEdit()
        self.win_size_label = QtG.QLabel("Window size: ")
        self.win_size_slider = QtG.QSlider(QtCore.Qt.Horizontal)

        self.min_width_edge = DEFAULT_MIN_WIDTH_EDGE
        self.min_width_edge_line = QtG.QLineEdit(str(int(self.min_width_edge*100)))# becuase the slider moves of 1 unit and we need a value beteen 0 and 1
        self.min_width_edge_label = QtG.QLabel("Minimum width edge: ")
        self.min_width_edge_slider = QtG.QSlider(QtCore.Qt.Horizontal)



        # add tabs
        self.tabs = QtG.QTabWidget()
        self.tab_visualization=QtG.QWidget()
        self.tab_thresholding = QtG.QWidget()
        self.tab_tracing = QtG.QWidget()
        self.tab_filtering = QtG.QWidget()

        self.tabs.addTab(self.tab_visualization, "Visualization")
        self.tabs.addTab(self.tab_thresholding, "Thresholding")
        self.tabs.addTab(self.tab_filtering, "Filtering")

        #create the tabs
        # the tracing is available only after loading a 'cbox_untraced' file.
        # The table 'self.create_tab_tracing()' will be create in the '_import_boxes*' functions
        self.create_tab_visualization()
        self.create_tab_filtering()
        self.create_tab_thresholding()

        #add tabs to widget
        line_counter = 1
        # picking_filament
        self.picking_label.setEnabled(True)
        self.layout.addWidget(self.picking_label, line_counter, 0)
        line_counter = line_counter + 1
        self.picking_filament_combox.addItems([PARTICLE,FILAMENT])
        self.picking_filament_combox.setEnabled(True)
        self.picking_filament_combox.currentIndexChanged.connect(self.picking_filament_changed)
        self.layout.addWidget(self.picking_filament_combox, line_counter, 0)
        line_counter = line_counter + 1

        self.layout.addWidget(self.tabs, line_counter, 0)

        # Draw 3D visualization
        self.active_3D_visualization_label = QtG.QLabel()
        self.active_3D_visualization_label.setText("Show 3D visualization:")
        self.active_3D_visualization_label.setEnabled(False)
        #self.layout.addWidget(self.active_3D_visualization_label, line_counter, 0)

        self.active_3D_visualization_checkbox = QtG.QCheckBox()
        #self.layout.addWidget(self.active_3D_visualization_checkbox, line_counter, 1)
        self.active_3D_visualization_checkbox.stateChanged.connect(
            self.active_3D_visualization_changed
        )
        self.active_3D_visualization_checkbox.setEnabled(False)

        # Show image selection
        self.show()



        # in case of folder of tomo it will be a dict of Thorsten original self.box_dictionary (k=filename, v=list sketches)
        # k1=tomo_filename v1=dict (same as Thorsten original self.box_dictionary)
        # NB:
        #   in filament case the boxes, which belong to the same filament, have the same color

        """
            it contains always the boxmanager sketches. In case of loading value from cbox_3D file I fill it with 
            the smaller boxes for the 3D visualization (via 'fill_next_prev_slice')
        """
        self.box_dictionary = {}

        # it is used for tracing, hence only when cbox_untraced file is loaded
        self.box_dictionary_3D_view = {}

        """
        It contains ONLY AND ALWAYS the 2D boxes of 'self.box_dictionary'
        (or 'self.box_dictionary_3D_view' in the preview_run ... because 'fill_next_prev_slice')
        """
        self.box_dictionary_without_3D_visual= {}

        # for avoid to trace a dict again when it was already traced using the current/saved params ( tomo folder case only)
        self.box_dict_traced = {}
        # k= tomo_filename. Contains the values for the 'tracing' parameters silder
        self.smallest_image_dim = {}
        self.tot_frames = {}

        # k=tomo_filename v= item
        self.item_3D_filename = {}

        self.plot = None
        self.fig = None
        self.ax = None

        self.moving_box = None

        self.zoom_update = False
        self.doresizing = False
        self.current_image_path = None
        self.background_current = None
        self.background_current_onmove = None
        #self.background_current_remove_picked_fil = None
        self.unsaved_changes = False
        self.is_cbox = False
        self.is_cbox_untraced = False
        self.eman_3D = False                #todo: is it True? to manage the EMAN 3D folder (it has a .box old format got from??) anyway now we save always in cbox format
        self.toggle = False
        self.use_estimated_size = False
        self.wildcard = wildcard
        if images_path:
            if is_tomo_dir is True:
                img_loaded = self._open_image3D_folder(images_path)
                self.is_folder_3D_tomo = True
            else:
                img_loaded = self._open_image_folder(images_path)
            if img_loaded:
                self.button_apply_filter.setEnabled(True)
            if boxes_path:
                if is_tomo_dir is False:
                    self._import_boxes(box_dir=boxes_path, keep=False)
                else:
                    self._import_boxes_3D_tomo_folder(box_dir=boxes_path, keep=False)
                    self._apply_3d_visualization_in_tomo_case()

    def close_boxmanager(self):
        if self.unsaved_changes:
            msg = "All loaded boxes are discarded. Are you sure?"
            reply = QtG.QMessageBox.question(
                self, "Message", msg, QtG.QMessageBox.Yes, QtG.QMessageBox.Cancel
            )

            if reply == QtG.QMessageBox.Cancel:
                return
        self.close()

    def closeEvent(self, event):
        self.close_boxmanager()

    def _set_first_time_img(self,im):
        """
        Set the variable to show an image
        :param im: np array
        :return: none
        """
        # Create figure and axes
        self.fig, self.ax = plt.subplots(1)

        self.ax.xaxis.set_visible(False)
        self.ax.yaxis.set_visible(False)

        self.fig.tight_layout()
        self.fig.canvas.set_window_title(
            os.path.basename(self.current_image_path)
        )
        # Display the image
        self.im = self.ax.imshow(
            im, origin="lower", cmap="gray", interpolation="Hanning"
        )  #

        self.plot = QtG.QDialog(self)
        self.plot.canvas = plt_qtbackend.FigureCanvasQTAgg(self.fig)
        self.plot.canvas.mpl_connect("button_press_event", self.onclick)
        self.plot.canvas.mpl_connect("key_press_event", self.myKeyPressEvent)
        self.plot.canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.plot.canvas.setFocus()
        self.plot.canvas.mpl_connect("button_release_event", self.onrelease)
        self.plot.canvas.mpl_connect("motion_notify_event", self.onmove)
        self.plot.canvas.mpl_connect("resize_event", self.onresize)
        self.plot.canvas.mpl_connect("draw_event", self.ondraw)
        self.plot.toolbar = boxmanager_toolbar.Boxmanager_Toolbar(
            self.plot.canvas, self.plot, self.fig, self.ax, self
        )  # plt_qtbackend.NavigationToolbar2QT(self.plot.canvas, self.plot)
        layout = QtG.QVBoxLayout()
        layout.addWidget(self.plot.toolbar)
        layout.addWidget(self.plot.canvas)
        self.plot.setLayout(layout)
        self.plot.canvas.draw()
        self.plot.show()
        self.background_current = self.fig.canvas.copy_from_bbox(self.ax.bbox)


    def _event_checkbox_changed(self,item, column):
        if column == 0:
            if item.childCount()>0:
                for child_index in range(item.childCount()):
                    item.child(child_index).setCheckState(0,item.checkState(0))

    def update_picking_filament_dict(self):
        if self.picking_filament:
            if self.is_folder_3D_tomo is True:
                f_name = os.path.splitext(os.path.basename(self.current_image_path.split('/')[-1]))[0]
                if self.index_3D_tomo not in self.picked_filament_dictionary[f_name]:
                    self.picked_filament_dictionary[f_name].update({self.index_3D_tomo: list()})
            else:
                # if it is a single 3D image tomo pure_filename identifies the slice of the tomo
                f_name = self.get_current_purefilename() if self.is_3D_tomo is False else self.index_3D_tomo
                if f_name not in self.picked_filament_dictionary:
                    self.picked_filament_dictionary.update({f_name: list()})

    def _event_image_changed(self, root_tree_item):

        not_the_same_tomo = False   # var used to close the preview win (trace option) in tomo folder case
        if (
                root_tree_item is not None
                and root_tree_item.childCount() == 0
                and self.current_image_path is not None
        ):
            last_filename_in_tomo_folder_helper= self.last_filename_in_tomo_folder   # used for tracing the last folder name in case of picking filament
            if self.is_folder_3D_tomo is True:
                self.current_image_path = os.path.join(self.image_folder,root_tree_item.parent().text(0))

            if self.is_3D_tomo is False:
                self.current_tree_item = root_tree_item
                filename = root_tree_item.text(0)

                pure_filename = self.get_current_purefilename()
                if self.picking_filament:
                    self.picked_filament_dictionary[pure_filename] = self.picked_filament_list

                # convert circle to rect or viceversa in the current image (in case you need it)
                self.current_image_path = os.path.join(self.image_folder, str(filename))

                # use pure_filename to delete the patches in the previous image
                if pure_filename in self.box_dictionary:
                    self.rectangles = self.box_dictionary[pure_filename]
                    self.delete_all_patches(self.rectangles)
                else:
                    self.rectangles = []

                if self.picking_filament:
                    current_filename = self.get_current_purefilename()
                    self.update_picking_filament_dict()
                    self.picked_filament_list = self.picked_filament_dictionary[current_filename]
                    self.picked_filament_as_rect_dictionary = list()
                    for f in self.picked_filament_list:
                        self.picked_filament_as_rect_dictionary.append(f.get_rect_sketch())
                    self.box_dictionary[current_filename] = self.picked_filament_as_rect_dictionary
                    self.ax.patches=list()

                prev_size = imagereader.read_width_height(self.current_image_path)
                self.fig.canvas.set_window_title(os.path.basename(self.current_image_path))
                img = helper.read_image(self.current_image_path)
                prev_size = prev_size[::-1]
                if prev_size == img.shape:
                    self.im.set_data(img)
                else:
                    self.im = self.ax.imshow(
                        img, origin="lower", cmap="gray", interpolation="Hanning"
                    )


                self.plot.setWindowTitle(os.path.basename(self.current_image_path))
                self.fig.canvas.draw()
                self.background_current = self.fig.canvas.copy_from_bbox(self.ax.bbox)
                self.update_boxes_on_current_image()
            else:
                if self.is_folder_3D_tomo is True:
                    pure_filename = os.path.splitext(os.path.basename(self.current_image_path.split('/')[-1]))[0]

                    # allow to separate the boxes present in the 'index_3D_tomo' slice between different tomo
                    if self.last_filename_in_tomo_folder != pure_filename:
                        not_the_same_tomo = True
                        self.delete_all_patches(self.rectangles)
                        self.current_image3D_mmap= helper.read_image(self.current_image_path, use_mmap=True)
                        self.last_filename_in_tomo_folder=pure_filename
                        self.memory_slider.setMaximum(int(self.tot_frames[pure_filename] - 1))
                        self.min_length_slider.setMaximum(int(self.tot_frames[pure_filename] - 1))
                        self.search_range_slider.setMaximum(int(self.smallest_image_dim[pure_filename] - 1))
                        self.load_tomo_params(pure_filename)

                    # load the boxes already selected in the 'index_3D_tomo' slice
                    if self.picking_filament and last_filename_in_tomo_folder_helper in self.box_dictionary and self.index_3D_tomo in self.box_dictionary[last_filename_in_tomo_folder_helper]:
                        self.picked_filament_dictionary[last_filename_in_tomo_folder_helper][self.index_3D_tomo] = self.picked_filament_list
                    if pure_filename in self.box_dictionary and self.index_3D_tomo in self.box_dictionary[pure_filename]:
                        self.rectangles = self.box_dictionary[pure_filename][self.index_3D_tomo]
                    self.last_file_3D_tomo = pure_filename
                    self.delete_all_patches(self.rectangles)
                elif self.index_3D_tomo in self.box_dictionary :
                    if self.picking_filament:
                        self.picked_filament_dictionary[self.index_3D_tomo] =self.picked_filament_list
                    self.rectangles = self.box_dictionary[self.index_3D_tomo]
                    self.delete_all_patches(self.rectangles)
                    self.last_index_3D_tomo = self.index_3D_tomo
                else:
                    self.rectangles = []

                self.index_3D_tomo = int(root_tree_item.text(0))
                if self.picking_filament:
                    self.update_picking_filament_dict()
                    if self.is_folder_3D_tomo:
                        self.picked_filament_list = self.picked_filament_dictionary[pure_filename][self.index_3D_tomo]
                    else:
                        self.picked_filament_list = self.picked_filament_dictionary[self.index_3D_tomo]
                    self.picked_filament_as_rect_dictionary = list()
                    for f in self.picked_filament_list:
                        self.picked_filament_as_rect_dictionary.append(f.get_rect_sketch())
                    if self.is_folder_3D_tomo:
                        self.box_dictionary[pure_filename][self.index_3D_tomo]=self.picked_filament_as_rect_dictionary
                    else:
                        self.box_dictionary[self.index_3D_tomo]=self.picked_filament_as_rect_dictionary
                    self.ax.patches=list()

                self.last_index_3D_tomo = self.index_3D_tomo

                img = self.current_image3D_mmap[self.index_3D_tomo, :, :]
                self.im.set_data(img)                   # all the slice have the same size

                title=os.path.basename(self.current_image_path)+"\tindex: "+str(self.index_3D_tomo)
                self.plot.setWindowTitle(title)
                self.fig.canvas.draw()
                self.background_current = self.fig.canvas.copy_from_bbox(self.ax.bbox)
                self.update_boxes_on_current_image()

                if self.preview_win and self.preview_win.is_visible():
                    if not_the_same_tomo:
                        self.preview_win.plot.close()
                        if self.box_dict_traced[self.get_current_purefilename()]:
                            self.preview_win = visualization_3D_Window.PreviewWindow(self.font, self.get_patches())
                            self.preview_win.display_img(self.current_image_path, img, self.index_3D_tomo)
                    else:
                        self.preview_win.set_list_patches(self.get_patches())
                        self.preview_win.display_img(self.current_image_path, img,self.index_3D_tomo)
                print("3D tomo implementing ... pressed index tomo: "+str(self.index_3D_tomo))

    def lower_size_label_changed(self):
        try:
            new_value = int(float(self.lower_size_thresh_line.text()))
            upper_value = self.upper_size_thresh_slide.value()
            if new_value >= upper_value:
                return
        except ValueError:
            return
        self.lower_size_thresh_slide.setValue(new_value)

        if self.preview_is_on:
            self.preview_win.set_list_patches(self.get_patches())
            self.preview_win.display_img(self.current_image_path, None, self.index_3D_tomo)

    def upper_size_label_changed(self):
        try:
            new_value = int(float(self.upper_size_thresh_line.text()))
            lower_value = self.lower_size_thresh_slide.value()
            if new_value <= lower_value:
                return
        except ValueError:
            return
        self.upper_size_thresh_slide.setValue(new_value)

        if self.preview_is_on:
            self.preview_win.set_list_patches(self.get_patches())
            self.preview_win.display_img(self.current_image_path, None, self.index_3D_tomo)

    @pyqtSlot()
    def conf_thresh_label_changed(self):
        try:
            new_value = float(self.conf_thresh_line.text())
            if new_value > 1.0 or new_value < 0:
                return
        except ValueError:
            return
        self.current_conf_thresh = new_value
        self.conf_thresh_slide.setValue(new_value * 100)

        if self.preview_is_on:
            self.preview_win.set_list_patches(self.get_patches())
            self.preview_win.display_img(self.current_image_path, None, self.index_3D_tomo)

    @pyqtSlot()
    def searchRange_label_changed(self):
        try:
            new_value = int(self.search_range_line.text())
            if new_value > self.smallest_image_dim[self.get_current_purefilename()]or new_value < 0:
                return
        except ValueError:
            return
        self.search_range = new_value
        self.search_range_slider.setValue(new_value)

        if self.preview_is_on and self.has_filament is False:
            self.preview_run(only_reload=True)

    @pyqtSlot()
    def memory_label_changed(self):
        try:
            new_value = int(self.memory_line.text())
            if new_value > self.smallest_image_dim[self.get_current_purefilename()] or new_value < 0:
                return
        except ValueError:
            return
        self.memory = new_value
        self.memory_slider.setValue(new_value)

        if self.preview_is_on and self.has_filament is False:
            self.preview_run(only_reload=True)

    @pyqtSlot()
    def min_length_label_changed(self):
        try:
            new_value = int(self.min_length_line.text())
            if new_value > self.smallest_image_dim[self.get_current_purefilename()] or new_value < 0:
                return
        except ValueError:
            return
        self.min_length = new_value
        self.min_length_slider.setValue(new_value)

        if self.preview_is_on and self.has_filament is False:
            self.preview_run(only_reload=True)

    @pyqtSlot()
    def num_boxes_thresh_label_changed(self):
        try:
            new_value = int(self.num_boxes_thresh_line.text())
            if DEFAULT_MAX_NUM_BOXES_THRESH < new_value or new_value < DEFAULT_MIN_NUM_BOXES_THRESH :
                self.err_message("Invalid value. It has to between "+str(DEFAULT_MIN_NUM_BOXES_THRESH) +" and "+str(DEFAULT_MAX_NUM_BOXES_THRESH))
                self.num_boxes_thresh_line.setText(str(self.current_num_boxes_thresh))
                return
        except ValueError as err:
            if err.args[0].split(":")[-1].replace('\'','') != ' ':          # otherwise i get errmsg when i put an empty string (basically when i delete the values
                self.err_message("Invalid value. It has to be a number")
                self.num_boxes_thresh_line.setText(str(self.current_num_boxes_thresh))
            return
        self.current_num_boxes_thresh = new_value
        self.num_boxes_thresh_slide.setValue(new_value)

        if self.preview_is_on:
            self.preview_win.set_list_patches(self.get_patches())
            self.preview_win.display_img(self.current_image_path, None, self.index_3D_tomo)

    @pyqtSlot()
    def num_boxes_thresh_changed(self):
        self.trace_all = False
        self.current_num_boxes_thresh = self.num_boxes_thresh_slide.value()
        if self.is_updating_params is False and self.is_folder_3D_tomo and self.is_slider_pressed is False:
            reply = self.apply_to_all_the_tomo_question("Number boxes threshold")
            if reply == QtG.QMessageBox.Yes:
                for p in self.params.values():
                    self.trace_all = True
                    p.num_boxes_thresh = self.current_num_boxes_thresh
            else:
                self.params[self.get_current_purefilename()].num_boxes_thresh = self.current_num_boxes_thresh

        self.num_boxes_thresh_line.setText("" + str(self.current_num_boxes_thresh))

        # avoid to update when the slider is still pressed
        if self.is_slider_pressed is False:

            if self.background_current:
                self.update_boxes_on_current_image()
                self.fig.canvas.restore_region(self.background_current)
                self.unsaved_changes = True
            if self.is_3D_tomo:
                self.update_3D_counter()
                self.update_tree_boxsizes()


    @pyqtSlot()
    def conf_thresh_changed(self):
        self.trace_all = False
        try:
            self.current_conf_thresh = float(self.conf_thresh_slide.value()) / 100
            if self.is_updating_params is False and self.is_folder_3D_tomo and self.is_slider_pressed is False:
                reply = self.apply_to_all_the_tomo_question("confidence threshold")
                if reply == QtG.QMessageBox.Yes:
                    self.trace_all = True
                    for p in self.params.values():
                        p.conf_thresh = self.current_conf_thresh

                else:
                    self.params[self.get_current_purefilename()].conf_thresh = self.current_conf_thresh
        except ValueError:
            return
        try:
            if (
                    np.abs(float(self.conf_thresh_line.text()) - self.current_conf_thresh)
                    >= 0.01
            ):
                self.conf_thresh_line.setText("" + str(self.current_conf_thresh))
        except ValueError:
            self.conf_thresh_line.setText("" + str(self.current_conf_thresh))

        # avoid to update when the slider is still pressed
        if self.is_slider_pressed is False or self.is_3D_tomo is False:
            self.update_boxes_on_current_image()
            self.fig.canvas.restore_region(self.background_current)
            self._draw_all_boxes()
            self.unsaved_changes = True
            self.update_tree_boxsizes()
            if self.is_3D_tomo:
                self.update_3D_counter(self.box_dictionary_without_3D_visual)

    @pyqtSlot()
    def changed_slider_release_conf_thresh(self):
        self.is_slider_pressed = False
        # I have to run it again for update the sketches
        self.conf_thresh_changed()
        self.changed_slider_release()

    @pyqtSlot()
    def changed_slider_release_memory_changed(self):
        self.is_slider_pressed = False
        # I have to run it again for update the sketches
        self.memory_changed()


    @pyqtSlot()
    def changed_slider_release_searchRange(self):
        self.is_slider_pressed = False
        # I have to run it again for update the sketches
        self.searchRange_changed()


    @pyqtSlot()
    def changed_slider_release_min_length_changed(self):
        self.is_slider_pressed = False
        # I have to run it again for update the sketches
        self.min_length_changed()


    @pyqtSlot()
    def changed_slider_release_min_width_edge(self):
        self.is_slider_pressed = False
        # I have to run it again for update the sketches
        self.min_width_edge_changed()


    @pyqtSlot()
    def changed_slider_release_win_size(self):
        self.is_slider_pressed = False
        # I have to run it again for update the sketches
        self.win_size_changed()



    @pyqtSlot()
    def changed_slider_release_num_boxes_thresh(self):
        self.is_slider_pressed = False
        # I have to run it again for update the sketches
        self.num_boxes_thresh_changed()
        self.changed_slider_release()

    @pyqtSlot()
    def changed_slider_release_upper_size_thresh(self):
        self.is_slider_pressed = False
        # I have to run it again for update the sketches
        self.upper_size_thresh_changed()
        self.changed_slider_release()

    @pyqtSlot()
    def changed_slider_release_lower_size_thresh(self):
        self.is_slider_pressed = False
        # I have to run it again for update the sketches
        self.lower_size_thresh_changed()
        self.changed_slider_release()

    @pyqtSlot()
    def slider_pressed(self):
        self.is_slider_pressed = True

    @pyqtSlot()
    def changed_slider_release(self):
        # we do not want live tracing for filament case
        # real time visualization and thresholding will be managed directly in their function
        if self.preview_is_on and self.has_filament is False:
            self.preview_run(only_reload = True)

    @pyqtSlot()
    def min_width_edge_label_changed(self):
        try:
            new_value = float(self.min_width_edge_line.text())
            if new_value < 0:
                return
        except ValueError:
            return
        self.min_width_edge = new_value
        self.min_width_edge_slider.setValue(new_value)

        if self.preview_is_on and self.has_filament is False:
            self.preview_run(only_reload=True)

    @pyqtSlot()
    def win_size_label_changed(self):
        try:
            new_value = float(self.win_size_line.text())
            if new_value < 0:
                return
        except ValueError:
            return
        self.win_size = new_value
        self.win_size_slider.setValue(new_value)

        if self.preview_is_on and self.has_filament is False:
            self.preview_run(only_reload=True)


    def upper_size_thresh_changed(self):
        self.trace_all = False
        self.upper_size_thresh = int(float(self.upper_size_thresh_slide.value()))
        if self.is_updating_params is False and self.is_folder_3D_tomo and self.is_slider_pressed is False:
            if self.is_loading_max_min_sizes is False:
                reply = self.apply_to_all_the_tomo_question("Maximum size")
                if reply == QtG.QMessageBox.Yes:
                    self.trace_all = True
                    for p in self.params.values():
                        p.upper_size_thresh = self.upper_size_thresh
                else:
                    self.params[self.get_current_purefilename()].upper_size_thresh = self.upper_size_thresh
            else:
                for p in self.params.values():
                    p.upper_size_thresh = self.upper_size_thresh

        self.upper_size_thresh_line.setText("" + str(self.upper_size_thresh))
        if self.upper_size_thresh <= self.lower_size_thresh:
            self.lower_size_thresh_slide.setValue(self.upper_size_thresh - 1)

        if self.is_slider_pressed is False or self.is_3D_tomo is False:
            self.update_boxes_on_current_image()
            self.fig.canvas.restore_region(self.background_current)
            self._draw_all_boxes()
            self.unsaved_changes = True
            self.update_tree_boxsizes()


    def lower_size_thresh_changed(self):
        self.trace_all = False
        self.lower_size_thresh = int(float(self.lower_size_thresh_slide.value()))
        if self.is_updating_params is False and self.is_folder_3D_tomo and self.is_slider_pressed is False:
            if self.is_loading_max_min_sizes is False:
                reply = self.apply_to_all_the_tomo_question("Minimum size")
                if reply == QtG.QMessageBox.Yes:
                    self.trace_all = True
                    for p in self.params.values():
                        p.lower_size_thresh = self.lower_size_thresh
                else:
                    self.params[self.get_current_purefilename()].lower_size_thresh = self.lower_size_thresh
            else:
                for p in self.params.values():
                    p.lower_size_thresh = self.lower_size_thresh

        self.lower_size_thresh_line.setText("" + str(self.lower_size_thresh))
        if self.lower_size_thresh >= self.upper_size_thresh:
            self.upper_size_thresh_slide.setValue(self.lower_size_thresh + 1)

        if self.is_slider_pressed is False or self.is_3D_tomo is False:
            self.update_boxes_on_current_image()
            self.fig.canvas.restore_region(self.background_current)
            self._draw_all_boxes()
            self.unsaved_changes = True
            self.update_tree_boxsizes()

    def _get_list_boxes_for_histograms(self):
        """
        Refactoring function.
        Return the correct list of list of boxes for 'show_confidence_histogram' and 'show_size_distribution'
        """
        add_in_title=""
        if self.is_folder_3D_tomo:
            fname=self.get_current_purefilename()
            list_boxes = [*self.box_dictionary_without_3D_visual[fname].values()]
            add_in_title = " of "+fname
        elif self.is_3D_tomo:
            list_boxes = [*self.box_dictionary_without_3D_visual.values()]
        else:
            list_boxes = [*self.box_dictionary.values()]
        return list_boxes,add_in_title
    def show_confidence_histogram(self):

        confidence = []
        list_boxes,add_in_title=self._get_list_boxes_for_histograms()

        for boxes in list_boxes:
                for box in boxes:
                    confidence.append(box.get_confidence())
        fig = plt.figure()

        width = max(10, int((np.max(confidence) - np.min(confidence)) / 0.05))
        plt.hist(confidence, bins=width)
        plt.title("Confidence distribution"+add_in_title)
        bin_size_str = "{0:.2f}".format(
            ((np.max(confidence) - np.min(confidence)) / width)
        )
        plt.xlabel("Confidence (Bin size: " + bin_size_str + ")")
        plt.ylabel("Count")

        plot = QtG.QDialog(self)
        plot.canvas = plt_qtbackend.FigureCanvasQTAgg(fig)
        layout = QtG.QVBoxLayout()
        layout.addWidget(plot.canvas)
        plot.setLayout(layout)
        plot.setWindowTitle("Size distribution")
        plot.canvas.draw()
        plot.show()

    def show_size_distribution(self):

        estimated_size = []
        list_boxes, add_in_title = self._get_list_boxes_for_histograms()

        for boxes in list_boxes:
                for box in boxes:
                    estimated_size.append(box.get_est_size())

        fig = plt.figure()

        width = max(10, int((np.max(estimated_size) - np.min(estimated_size)) / 10))
        plt.hist(estimated_size, bins=width)
        plt.title("Particle diameter distribution"+add_in_title)
        plt.xlabel("Partilce diameter [px] (Bin size: " + str(width) + "px )")
        plt.ylabel("Count")

        plot = QtG.QDialog(self)
        plot.canvas = plt_qtbackend.FigureCanvasQTAgg(fig)
        layout = QtG.QVBoxLayout()
        layout.addWidget(plot.canvas)
        plot.setLayout(layout)
        plot.setWindowTitle("Size distribution")
        plot.canvas.draw()
        plot.show()

    def apply_filter(self):
        try:
            self.filter_freq = float(self.filter_line.text())
        except ValueError:
            return
        if self.filter_freq < 0.5 and self.filter_freq >= 0:
            import cryolo.lowpass as lp

            if self.is_3D_tomo is False:
                img = lp.filter_single_image(self.current_image_path, self.filter_freq)
                im_type = helper.get_file_type(self.current_image_path)
                img = helper.normalize_and_flip(img,im_type)
            else:
                img = helper.read_image(self.current_image_path,use_mmap=True)
                img = lp.filter_single_image_from_np_array(img[self.index_3D_tomo, :, :],self.filter_freq)
            img = np.squeeze(img)
            self.delete_all_patches(self.rectangles)
            self.im.set_data(img)
            self.fig.canvas.draw()
            self.background_current = self.fig.canvas.copy_from_bbox(self.ax.bbox)
            self.update_boxes_on_current_image()
        else:
            msg = "Frequency has to be between 0 and 0.5."
            QtG.QMessageBox.information(self, "Message", msg)


    def box_size_changed(self):
        old_boxsize = self.boxsize
        try:
            self.boxsize = int(float(self.boxsize_line.text()))
        except ValueError:
            self.err_message("Invalid value. It has to be a number")
            return
        if self.boxsize >= 0:
            if self.active_3D_visualization is True:
                """
                It is the case of a cbox file.
                I have to resize the original value present in the cbox file and then create the 3D visualization
                In box_dictionary_without_3D_visual I'll always have the value saved in the file
                in box_dictionary I could have already the 3D visualization
                """

                # the _sketch_changed ll resize both the dict and copy box_dictionary in box_dictionary_without_3D_visual
                self.delete_all_boxes() # clean box_dictionary
                self._sketch_changed(only_resize=True, new_size=self.boxsize,remove_all_sketches=False)
                self.box_dictionary = helper.create_deep_copy_box_dict(self.box_dictionary_without_3D_visual,
                                                                       self.is_folder_3D_tomo)
                self.fill_next_prev_slice()
                self.update_3D_counter()
                self.update_tree_boxsizes()
            else:
                if self.picking_filament:
                    self.delete_all_boxes(clean_box_dictionary = False)
                    self.resize_pickedfilament_stuff(self.boxsize)
                    self.update_boxes_on_current_image()
                    return
                #resize the present sketches
                self._sketch_changed(only_resize=True, new_size=self.boxsize,remove_all_sketches=True)




            if self.has_filament:
                self.resize_filament_stuff(float(self.boxsize/old_boxsize))

                if self.preview_win and self.preview_is_on is False:
                    self.preview_win.set_list_patches(self.get_patches())
                    self.preview_win.reload_img()

            if self.background_current:
                self.update_boxes_on_current_image()
                self.fig.canvas.restore_region(self.background_current)
                self.unsaved_changes = True

            if self.preview_is_on:
                self.trace_all = False
                self.preview_win.set_list_patches(self.get_patches())
                self.preview_win.display_img(self.current_image_path, None, self.index_3D_tomo)

    def resize_pickedfilament_stuff(self,new_size):
        """
        Resize, like reference in C++, all the picked filament dict
        Resize all the filament in box_dictionary too in order to create the sketches to draw them correctly
        """
        if self.is_folder_3D_tomo is False:
            for k in self.picked_filament_dictionary.keys():
                self.box_dictionary[k] = list()
                for i in range(len(self.picked_filament_dictionary[k])):
                    self.picked_filament_dictionary[k][i].boxsize=new_size
                    self.picked_filament_dictionary[k][i].height = new_size
                    helper.resize(self.picked_filament_dictionary[k][i].filament.boxes, new_size)
                    self.box_dictionary[k].append(self.picked_filament_dictionary[k][i].get_rect_sketch())
        else:
            for f, _ in self.item_3D_filename.items():
                for k in self.picked_filament_dictionary[f].keys():
                    self.box_dictionary[f][k] = list()
                    for i in range(len(self.picked_filament_dictionary[f][k])):
                        self.picked_filament_dictionary[f][k][i].boxsize = new_size
                        self.picked_filament_dictionary[f][k][i].height = new_size
                        helper.resize(self.picked_filament_dictionary[f][k][i].filament.boxes, new_size)
                        self.box_dictionary[f][k].append(self.picked_filament_dictionary[f][k][i].get_rect_sketch())

        # i resize them instead of assigning to the correct 'self.picked_filament_dictionary' to avoid to set again all the internal params (e.g.: est_size value)
        for i in range(len(self.picked_filament_list)):
            self.picked_filament_list[i].boxsize = new_size
            self.picked_filament_list[i].height = new_size
            helper.resize(self.picked_filament_list[i].filament.boxes, new_size)


    def resize_filament_stuff(self,factor):
        #todo: ha senso questa? funziona? dovrei implementarla come fatto per resize_pickedfilament_stuff
        """ Resize the filament_dict (used in the tracking) and the box_dictionar_3D_view (used in the visualization) """
        if self.is_folder_3D_tomo is False:
            for index in self.filament_dict.keys():
                for filament in self.filament_dict[index]:
                    for b in filament.boxes:
                        b.w *= factor
                        b.h *= factor
            for index in self.box_dictionary_3D_view.keys():
                helper.resize_3d_filament(self.box_dictionary_3D_view[index], factor)
        else:
            for f, _ in self.item_3D_filename.items():
                for index in self.filament_dict[f].keys():
                    for filament in self.filament_dict[f][index]:
                        for b in filament.boxes:
                            b.w *= factor
                            b.h *= factor
                for index in self.box_dictionary_3D_view[f].keys():
                    helper.resize_3d_filament(self.box_dictionary_3D_view[f][index], factor)


    def picking_filament_changed(self):
        self.picking_filament = self.picking_filament_combox.currentText() == FILAMENT
        print(self.picking_filament)


    def use_circle_changed(self):
        """
        Call when the 'use_circle' checkbox is activated/deactivated
        """
        if self.picking_filament:
            if self.is_loading_boxes:
                return
            errmsg = QtG.QErrorMessage(self)
            errmsg.showMessage("Only the rectangle visualization is enabled when picking filaments")
            self.use_circle_combobox.setCurrentText(RECT)
            self.use_circle = False
            return

        self.use_circle = self.use_circle_combobox.currentText() == CIRCLE
        if self.box_dictionary:
            self._sketch_changed(only_resize=False,new_size=None,remove_all_sketches=True)
            # when we change the sketches and the cbox or eman3D is loaded we have to create the 3d visualization only the first time
            if (self.is_cbox or self.eman_3D) and self.is_3D_tomo and self.first_call_use_circle_changed:
                self.box_dictionary_without_3D_visual = helper.create_restore_box_dict(self.box_dictionary,self.is_folder_3D_tomo)
                self.fill_next_prev_slice()
                self.update_3D_counter(helper.create_restore_box_dict(self.box_dictionary, self.is_folder_3D_tomo))
                self.first_call_use_circle_changed = False

        if self.preview_is_on:
            self.preview_win.set_list_patches(self.get_patches())
            self.preview_win.display_img(self.current_image_path, None, self.index_3D_tomo)


    def get_patches(self):
        boxes=[]
        purefilename = None
        if self.last_filename_in_tomo_folder is None and self.index_3D_tomo in self.box_dictionary_3D_view:
            boxes = self.box_dictionary_3D_view[self.index_3D_tomo]
        elif self.last_filename_in_tomo_folder is not None and self.index_3D_tomo in self.box_dictionary_3D_view[self.last_filename_in_tomo_folder]:
            # case 3D folder
            boxes = self.box_dictionary_3D_view[self.last_filename_in_tomo_folder][self.index_3D_tomo]
            purefilename = self.last_filename_in_tomo_folder

        current_conf_thresh, upper_size_thresh, lower_size_thresh, current_num_boxes_thresh = self.get_threshold_params_for_given_tomo(purefilename)
        visible_rects = [box.getSketch(circle = self.use_circle) for box in boxes if
                         helper.check_if_should_be_visible(box,current_conf_thresh, upper_size_thresh, lower_size_thresh, current_num_boxes_thresh, is_filament = self.has_filament)]
        return visible_rects


    def preview(self):
        if self.current_image3D_mmap is None:
            errmsg = QtG.QErrorMessage(self)
            errmsg.showMessage("Please open a tomo image or a folder of tomo images first")
            return

        self.preview_is_on = self.preview_checkbox.isChecked()

        # workaround to check the 'preview' box and set the self.preview_is_on var when running the trace via 'trace' button
        # i cannot just let run this function because using the 'trace' btn we could decide to trace on all the tomo in the tomo folder case
        if self.run_via_trace_button:
            return

        if self.preview_is_on:
            self.trace_all = False
            self.preview_run(only_reload = False)
            self.button_trace.setEnabled(False)
        else:
            self.button_trace.setEnabled(True)

    def trace_values(self, fname,param):
        """
        :param fname: in folder case it is the name of the tomo on which perform the trace
        """
        if self.has_filament:
            filament_dict = self.filament_dict[fname] if self.is_folder_3D_tomo else self.filament_dict
            return grouping3d.do_tracing_filaments(filament_dict,param.search_range, param.memory, param.conf_thresh, param.min_width_edge,param.win_size)
        else:
            box_dict = helper.create_restore_box_dict(self.box_dictionary, self.is_folder_3D_tomo, as_Bbox=True)
            if self.is_folder_3D_tomo:
                box_dict = box_dict[fname]
            d = grouping3d.do_tracing(box_dict,param.search_range, param.memory, param.conf_thresh, param.min_length)
            if d:
                d = utils.non_maxima_suppress_fast_3d(d, 0.3, param.conf_thresh)
        return  d


    def preview_run(self, only_reload = False):
        """
        This function will collect the params, run the tracing and show the result
        :param only_reload: If True it show the result on the current image
        """
        # run the tracing
        self.blur_while_tracing()
        purefilename = self.get_current_purefilename()
        d = None
        if self.trace_all:
            for f in [*self.item_3D_filename]:
                self.box_dict_traced[f] = self.trace_values(f,self.params[f])
                if purefilename == f:
                    d = self.box_dict_traced[f]
        else:
            p=Params(None, None, self.upper_size_thresh, self.lower_size_thresh, self.current_conf_thresh, self.current_num_boxes_thresh,
                 self.min_width_edge, self.search_range, self.memory, self.min_length, self.win_size)
            d = self.trace_values(purefilename,p)

        if self.has_filament is False:
            if self.is_folder_3D_tomo:
                for f in [*self.box_dict_traced]:
                    self.box_dictionary_3D_view[f] = helper.convert_list_bbox_to_dict_sketch(self.box_dict_traced[f])
                    self.box_dictionary_without_3D_visual[f] = helper.convert_list_bbox_to_dict_sketch(self.box_dict_traced[f])
                self.fill_next_prev_slice(self.box_dictionary_3D_view,self.box_dictionary_without_3D_visual,[*self.box_dict_traced])

            else:
                self.box_dictionary_3D_view = helper.convert_list_bbox_to_dict_sketch(d)
                self.box_dictionary_without_3D_visual = helper.convert_list_bbox_to_dict_sketch(d)
                self.fill_next_prev_slice(self.box_dictionary_3D_view)
        else:
            if self.is_folder_3D_tomo:
                for f in [*self.box_dict_traced]:
                    self.box_dictionary_3D_view.update({f: dict()})
                    self.convert_filamentList_to_box_dictionary(self.box_dictionary_3D_view, self.box_dict_traced[f],f)
            else:
                self.convert_filamentList_to_box_dictionary(self.box_dictionary_3D_view, d)

        patches = self.get_patches()
        if self.preview_win is None:
            self.preview_win = visualization_3D_Window.PreviewWindow(self.font, patches)
            only_reload = False
        else:
            self.preview_win.set_list_patches(patches)

        if only_reload:
            self.preview_win.reload_img()
        else:
            img = self.current_image3D_mmap[self.index_3D_tomo, :, :]
            self.preview_win.display_img(self.current_image_path, img, self.index_3D_tomo)
        self.unblur_after_tracing()



    def trace(self):
        """
            This button traces the particles and show them in the 'preview' 3D windows.
            The button is visible only if 'preview' checkbox is not checked
        """
        if self.current_image3D_mmap is None:
            errmsg = QtG.QErrorMessage(self)
            errmsg.showMessage("Please open a tomo image or a folder of tomo images first")
            return

        self.trace_all = False

        # # workaround to check the 'preview' box and set the self.preview_is_on var when running the trace via 'trace' button
        self.run_via_trace_button = True
        self.preview_checkbox.setCheckState(QtCore.Qt.Checked)
        self.run_via_trace_button = False

        if self.is_folder_3D_tomo :
            msg = "Do you want to apply the trace to all tomographies? "
            reply = QtG.QMessageBox.question(self, "Message", msg, QtG.QMessageBox.Yes, QtG.QMessageBox.No)
            if reply == QtG.QMessageBox.Yes:
                self.trace_all = True
                for p in self.params.values():
                    p.memory = self.memory
                    p.search_range = self.search_range
                    p.min_length = self.min_length
                    p.win_size = self.win_size
                    p.min_width_edge = self.min_width_edge

        self.preview_run(only_reload = False)



    def janny(self):
        # todo: run the run_janny
        print("button 'run janny'")


    @pyqtSlot()
    def searchRange_changed(self):
        self.trace_all = False
        purefilename = self.get_current_purefilename()
        value =int(self.search_range_slider.value())
        try:
            if 0 <= value < self.smallest_image_dim[purefilename]-1:
                self.search_range = value
            else:
                self.err_message("the value has to be in [0 - "+str(self.smallest_image_dim[purefilename]-1)+"]")
            if self.is_updating_params is False and self.is_folder_3D_tomo and self.is_slider_pressed is False:
                reply = self.apply_to_all_the_tomo_question("Search range")
                if reply == QtG.QMessageBox.Yes:
                    self.trace_all = True
                    for p in self.params.values():
                        p.search_range = self.search_range
                else:
                    self.params[purefilename].search_range = self.search_range
        except ValueError:
            return

        self.search_range_line.setText("" + str(self.search_range))

        if self.preview_is_on and self.has_filament is False:
            self.preview_run(only_reload=True)


    @pyqtSlot()
    def memory_changed(self):
        self.trace_all = False
        purefilename = self.get_current_purefilename()
        value =int(self.memory_slider.value())
        try:
            if 0 <= value < self.tot_frames[purefilename]-1:
                self.memory = value
            else:
                self.err_message("the value has to be in [0 - "+str(self.tot_frames[purefilename]-1)+"]")
            if self.is_updating_params is False and self.is_folder_3D_tomo and self.is_slider_pressed is False:
                reply = self.apply_to_all_the_tomo_question("Memory")
                if reply == QtG.QMessageBox.Yes:
                    self.trace_all = True
                    for p in self.params.values():
                        p.memory = self.memory
                else:
                    self.params[purefilename].memory = self.memory
        except ValueError:
            return

        self.memory_line.setText("" + str(self.memory))

        if self.preview_is_on and self.has_filament is False:
            self.preview_run(only_reload=True)


    @pyqtSlot()
    def win_size_changed(self):
        self.trace_all = False
        value =int(self.win_size_slider.value())
        try:
            if value >= 0:
                self.win_size = value
            else:
                self.err_message("the value has to be in [0 - 1]")
            if self.is_updating_params is False and self.is_folder_3D_tomo and self.is_slider_pressed is False:
                reply = self.apply_to_all_the_tomo_question("Window size")
                if reply == QtG.QMessageBox.Yes:
                    self.trace_all = True
                    for p in self.params.values():
                        p.win_size = self.win_size
                else:
                    self.params[self.get_current_purefilename()].win_size = self.win_size
        except ValueError:
            return

        self.win_size_line.setText("" + str(self.win_size))

        if self.preview_is_on and self.has_filament is False:
            self.preview_run(only_reload=True)

    @pyqtSlot()
    def min_width_edge_changed(self):
        self.trace_all = False
        value =int(self.min_width_edge_slider.value())
        try:
            if value >= 0:
                self.min_width_edge = value
            else:
                self.err_message("the value has to be in [0 - 1]")
            if self.is_updating_params is False and self.is_folder_3D_tomo and self.is_slider_pressed is False:
                reply = self.apply_to_all_the_tomo_question("Minimum width edge")
                if reply == QtG.QMessageBox.Yes:
                    self.trace_all = True
                    for p in self.params.values():
                        p.min_width_edge = self.min_width_edge
                else:
                    self.params[self.get_current_purefilename()].min_width_edge = self.min_width_edge
        except ValueError:
            return

        self.min_width_edge_line.setText("" + str(self.min_width_edge))

        if self.preview_is_on and self.has_filament is False:
            self.preview_run(only_reload=True)

    @pyqtSlot()
    def min_length_changed(self):
        purefilename = self.get_current_purefilename()
        self.trace_all = False
        value =int(self.min_length_slider.value())
        try:
            if 0 <= value < self.tot_frames[purefilename]-1:
                self.min_length = value
            else:
                self.err_message("the value has to be in [0 - "+str(self.tot_frames[purefilename]-1)+"]")
            if self.is_updating_params is False and self.is_folder_3D_tomo and self.is_slider_pressed is False:
                reply = self.apply_to_all_the_tomo_question("Minimum length")
                if reply == QtG.QMessageBox.Yes:
                    self.trace_all = True
                    for p in self.params.values():
                        p.min_length = self.min_length
                else:
                    self.params[purefilename].min_length = self.min_length
        except ValueError:
            return

        self.min_length_line.setText("" + str(self.min_length))

        if self.preview_is_on and self.has_filament is False:
            self.preview_run(only_reload=True)


    def err_message(self, err_msg = "Invalid value"):
        errmsg = QtG.QErrorMessage(self)
        errmsg.showMessage(err_msg)

    def active_3D_visualization_changed(self):
        """
        Call when the 'use_circle' checkbox is activated/deactivated
        """
        if self.is_3D_tomo is False:
            self.active_3D_visualization_checkbox.setEnabled(False)
        else:
            self.active_3D_visualization_checkbox.setEnabled(True)
        self.active_3D_visualization = self.active_3D_visualization_checkbox.isChecked()

        if self.active_3D_visualization:
            self.box_dictionary_without_3D_visual = helper.create_restore_box_dict(self.box_dictionary, self.is_folder_3D_tomo)
            self.fill_next_prev_slice()
        else:
            self.delete_all_boxes()
            self.box_dictionary = helper.create_restore_box_dict(self.box_dictionary_without_3D_visual,
                                                                 self.is_folder_3D_tomo)
            pure_filename = os.path.splitext(os.path.basename(self.current_image_path.split('/')[-1]))[0]
            all_sketches = []
            if self.is_folder_3D_tomo:
                if pure_filename in self.box_dictionary and self.index_3D_tomo in self.box_dictionary[pure_filename]:
                    all_sketches=self.box_dictionary[pure_filename][self.index_3D_tomo]
            else:
                if self.index_3D_tomo in self.box_dictionary:
                    all_sketches = self.box_dictionary[self.index_3D_tomo]

            # remove all the sketches
            self.delete_all_patches(all_sketches, update=False)
            self.fig.canvas.draw()

            #draw the pickled sketches
            if self.is_folder_3D_tomo:
                self.rectangles = self.box_dictionary[pure_filename][self.index_3D_tomo] if self.index_3D_tomo in self.box_dictionary[pure_filename] else []
            else:
                self.rectangles = self.box_dictionary[self.index_3D_tomo] if self.index_3D_tomo in self.box_dictionary else []
            self.draw_all_patches(self.rectangles)
            self._draw_all_boxes()
            self.update_tree_boxsizes()
        print("self.active_3D_visualization is: "+str(self.active_3D_visualization))


    #todo: test it deeply
    def fill_next_prev_slice(self, box_dict = None, box_dict_without_3D_visual = None, list_item_3D_filename = None):
        """
        Create a new rect/circle from the x,y coordinate in the next-prev 'self.box_size-1' slices
        """
        # if i fill a dictionary to pass the value to the preview window i do not have to change the self.box_dictionary and redraw
        toupdate = False
        if box_dict_without_3D_visual is None:
            box_dict_without_3D_visual = self.box_dictionary_without_3D_visual
        if list_item_3D_filename is None:
            list_item_3D_filename = [*self.item_3D_filename]
        if box_dict is None:
            box_dict = self.box_dictionary
            toupdate = True

        if self.is_folder_3D_tomo:
            for f in list_item_3D_filename:
                tot_slice = self.tot_frames[f]
                for index, boxes in box_dict_without_3D_visual[f].items():
                    original_size = int(boxes[0].get_width())
                    prev_slices = range(index - 1, index - original_size, -1)
                    next_slices = range(index + 1, index + original_size)

                    for b in boxes:
                        new_size = original_size - 2
                        for j in range(original_size - 1):
                            if new_size > 0:  # rect has to decrease of 2 and we avoid to create rect with not positivce width
                                sketch = helper.create_sketch(b,j,new_size,self.est_box_from_cbox)
                                sketch.set_Sketches_visible(True)
                                if prev_slices[j] >= 0:
                                    if prev_slices[j] in box_dict[f]:
                                        box_dict[f][prev_slices[j]].append(sketch)
                                    else:
                                        box_dict[f][prev_slices[j]] = [sketch]
                                if next_slices[j] < tot_slice:
                                    if next_slices[j] in box_dict[f]:
                                        box_dict[f][next_slices[j]].append(sketch)
                                    else:
                                        box_dict[f][next_slices[j]] = [sketch]
                                new_size = new_size - 2
                            else:
                                break
        else:
            for index,boxes in box_dict_without_3D_visual.items():
                if boxes:
                    original_size = int(boxes[0].get_width())
                    prev_slices = range(index -1,index - original_size , -1)
                    next_slices = range(index + 1, index + original_size)

                    for b in boxes:
                        new_size = original_size - 2
                        for j in range(original_size-1):
                            if new_size > 0:  # rect has to decrease of 2 and we avoid to create rect with not positivce width
                                sketch = helper.create_sketch(b, j, new_size,self.est_box_from_cbox)
                                if prev_slices[j] >= 0:
                                    if prev_slices[j] in box_dict:
                                        box_dict[prev_slices[j]].append(sketch)
                                    else:
                                        box_dict[prev_slices[j]] = [sketch]
                                if next_slices[j] < self.current_image3D_mmap.shape[0]:
                                    if next_slices[j] in box_dict:
                                        box_dict[next_slices[j]].append(sketch)
                                    else:
                                        box_dict[next_slices[j]] = [sketch]
                                new_size = new_size - 2
                            else:
                                break
            if toupdate:
                self.rectangles = box_dict[self.index_3D_tomo] if self.index_3D_tomo in box_dict else []

        if toupdate:
            self.draw_all_patches(self.rectangles)
            self._draw_all_boxes()
            self.update_tree_boxsizes()


    def _remove_all_sketch(self):
        """
        Remove all the sketches from the instance variables and from the shown image
        """
        self.box_dictionary_without_3D_visual = helper.create_deep_copy_box_dict(self.box_dictionary,self.is_folder_3D_tomo)
        self.delete_all_boxes()
        self.box_dictionary = helper.create_deep_copy_box_dict(self.box_dictionary_without_3D_visual,
                                                               self.is_folder_3D_tomo)

    def _sketch_changed(self, only_resize=False, new_size=None, remove_all_sketches = True):
        """
        Convert rect to circle and viceversa on the current image.
        Resize all the sketches
        remove_all_sketches --> used for optimization purpose. It is False only in box_size_changed when cbox file is loaded
        Return False if there is nothing to convert in the self.box_dictionary
        """
        if remove_all_sketches:
            self._remove_all_sketch()

        # convert and draw the new patches
        pure_filename = os.path.splitext(os.path.basename(self.current_image_path.split('/')[-1]))[0]
        if self.is_3D_tomo is False:
            if only_resize:
                for index in self.box_dictionary.keys():
                    helper.resize(self.box_dictionary[index], new_size)
            self.rectangles = self.box_dictionary[pure_filename] if pure_filename in self.box_dictionary else []
            self.draw_all_patches(self.rectangles)
            self._draw_all_boxes()
        elif only_resize:
            for f, _ in self.item_3D_filename.items():
                if self.is_folder_3D_tomo:
                    for index in self.box_dictionary[f].keys():
                        helper.resize(self.box_dictionary[f][index], new_size)
                    for index in self.box_dictionary_without_3D_visual[f].keys():
                        helper.resize(self.box_dictionary_without_3D_visual[f][index], new_size)

                if self.is_folder_3D_tomo is False or (self.is_folder_3D_tomo is True and f == pure_filename):
                    list_index = self.box_dictionary[f].keys() if self.is_folder_3D_tomo else self.box_dictionary.keys()
                    for index in list_index:
                        if self.is_folder_3D_tomo is False:
                            helper.resize(self.box_dictionary[index], new_size)

                    # update self.box_dictionary_without_3D_visual
                    list_index = self.box_dictionary_without_3D_visual[
                        f].keys() if self.is_folder_3D_tomo and f in self.box_dictionary_without_3D_visual else self.box_dictionary_without_3D_visual.keys()
                    for index in list_index:
                        if self.is_folder_3D_tomo is False:
                            helper.resize(self.box_dictionary_without_3D_visual[index], new_size)

        self.update_tree_boxsizes()
        self.update_boxes_on_current_image()
        return

    @pyqtSlot()
    def use_estimated_size_changed(self):
        self.use_estimated_size = self.use_estimated_size_checkbox.isChecked()

        # remove all the boxes and re create the original box_dict (NB: the size could the original or the estimated)
        self.delete_all_boxes()
        self.box_dictionary = helper.create_deep_copy_box_dict(self.box_dictionary_without_3D_visual,self.is_folder_3D_tomo)

        # Change the size from estimated to the actual box_size or viceversa
        if self.use_estimated_size:
            self._sketch_changed(only_resize=True, new_size=self.est_box_from_cbox, remove_all_sketches=True)
        else:
            self._sketch_changed(only_resize=True, new_size=self.boxsize, remove_all_sketches=True)

        # create the new 3D visualization
        if self.is_3D_tomo:
            self.fill_next_prev_slice()
        if self.preview_is_on:
            self.trace_all = False
            self.preview_run(only_reload=True)

        self.button_set_box_size.setEnabled(not self.use_estimated_size)
        self.boxsize_line.setEnabled(not self.use_estimated_size)
        self.boxsize_label.setEnabled(not self.use_estimated_size)

        self.upper_size_thresh_line.setEnabled(self.use_estimated_size)
        self.upper_size_thresh_slide.setEnabled(self.use_estimated_size)

        self.lower_size_thresh_line.setEnabled(self.use_estimated_size)
        self.lower_size_thresh_slide.setEnabled(self.use_estimated_size)

    def delete_all_boxes(self,clean_box_dictionary = True):
        if self.is_folder_3D_tomo is True:
            for filename in self.box_dictionary.keys():
                for _, rectangles in self.box_dictionary[filename].items():
                    self.delete_all_patches(rectangles)
        else:
            for _, rectangles in self.box_dictionary.items():
                self.delete_all_patches(rectangles)

        self.rectangles = []

        if self.box_dictionary and clean_box_dictionary:
            self.clean_box_dictionary()

        self.update_boxes_on_current_image()
        if self.background_current is not None:
            self.fig.canvas.restore_region(self.background_current)

    def update_boxes_on_current_image(self):
        if self.current_image_path is None:
            return

        if self.is_folder_3D_tomo is True:
            pure_filename = os.path.splitext(os.path.basename(self.current_image_path.split('/')[-1]))[0]
            if pure_filename in self.box_dictionary and self.index_3D_tomo in self.box_dictionary[pure_filename]:
                self.rectangles = self.box_dictionary[pure_filename][self.index_3D_tomo]
                self.delete_all_patches(self.rectangles, update=True)
                self.draw_all_patches(self.rectangles)
                self._draw_all_boxes()
        else:
            # if it is a single 3D image tomo pure_filename identifies the slice of the tomo
            pure_filename = self.get_current_purefilename() if self.is_3D_tomo is False else self.index_3D_tomo
            if pure_filename in self.box_dictionary:
                self.rectangles = self.box_dictionary[pure_filename]
                self.delete_all_patches(self.rectangles, update=True)
                self.draw_all_patches(self.rectangles)
                self._draw_all_boxes()

    def delete_all_patches(self, rects, update=False):
        state = self.get_filter_state()
        purefilename = self.get_current_purefilename() if self.is_folder_3D_tomo else None
        current_conf_thresh, upper_size_thresh, lower_size_thresh, current_num_boxes_thresh = self.get_threshold_params_for_given_tomo(purefilename)
        for box in rects:
            if helper.check_if_should_be_visible(box,current_conf_thresh, upper_size_thresh, lower_size_thresh, current_num_boxes_thresh, is_filament = self.has_filament)==False or update==False:
                # since after the refactoring a obj MySketch has both the rectangle and circle matplot instances
                # i have to delete both. Otherwise if a switch more than once the sketch's 'visualization' they will be overlapped
                box.set_Sketches_visible(False)
                rect = box.getSketch(circle=False)
                circle = box.getSketch(circle=True)
                if circle.is_figure_set() and circle in self.ax.patches:
                    circle.remove()
                if rect.is_figure_set() and rect in self.ax.patches:
                    rect.remove()
            if not helper.filter_tuple_is_equal(self.get_filter_state(),state):
                break


    def create_box_dict_of_filament_obj(self):
        """
        Return the box_dictionary for writing on file.
        It is used basically for creating a list of Filament obj from a list of  filament rect box
        """

        if self.is_folder_3D_tomo:
            out = {k: dict() for k in [*self.picked_filament_dictionary]}
            for k, d_in in self.picked_filament_dictionary.items():
                for k2 in [*self.picked_filament_dictionary[k]]:
                    out[k].update({k2: list()})
                for k_in, v_in in d_in.items():
                    for f in v_in:
                        f.fill_sketches(box_distance=self.box_distance_filament_picking,as_bbox=True,z=k_in)
                        out[k][k_in].append(f.filament)

        else:
            out = {k: list() for k in [*self.picked_filament_dictionary]}
            for k,v in self.picked_filament_dictionary.items():
                z = k if self.is_3D_tomo else None
                for f in v:
                    f.fill_sketches(box_distance=self.box_distance_filament_picking,as_bbox=True,z=z)
                    out[k].append(f.filament)
        return out


    def _write_all_type_classic(self, box_dir, selected_slice):
        """
        It saves on file the results after a classic picking ( no optimizing result case)
        :param box_dir: main directory where save the results
        :param selected_slice: list or dict ( in case of folder of tomo) of slices to save
        """
        box_dictionary_to_save, ignored_slice, empty_slice = helper_writer.prepare_output(slices=selected_slice,
                                                                                          input_box_dict=self.box_dictionary,
                                                                                          is_folder_3D_tomo=self.is_folder_3D_tomo)
        if self.picking_filament:
            box_dictionary_to_save =self.create_box_dict_of_filament_obj()

        for file_type in ["STAR", "CBOX", "EMAN"]:
            is_cbox = file_type == "CBOX"

            # the picked filament will be saved only in cbox format
            if self.picking_filament and self.is_3D_tomo and is_cbox is False:
                continue

            file_name = self.get_current_purefilename()
            d = os.path.join(box_dir, file_type)

            file_ext, write_coords_ = helper_writer.prepare_vars_for_writing(box_dir, file_type, self.is_3D_tomo,self.picking_filament)

            pd = QtG.QProgressDialog("Write box files to " + box_dir, "Cancel", 0, 100, self)
            pd.show()
            if self.is_folder_3D_tomo is True:
                if file_type == "CBOX" and self.picking_filament is False:
                    # we want to save ANYWAY all the selected boxes
                    cbox_dictionary_to_save = helper.create_restore_box_dict(self.box_dictionary,self.is_folder_3D_tomo)
                    helper_writer.write_coordinates_3d_folder(pd, cbox_dictionary_to_save,
                                                              empty_slice, ignored_slice, self.is_folder_3D_tomo, is_cbox,
                                                              self.current_conf_thresh, self.upper_size_thresh,
                                                              self.lower_size_thresh, self.boxsize, write_coords_,
                                                              file_ext,d, self.picking_filament)
                else:
                    helper_writer.write_coordinates_3d_folder(pd, box_dictionary_to_save, empty_slice,ignored_slice, self.is_folder_3D_tomo, is_cbox,
                                                              self.current_conf_thresh, self.upper_size_thresh,
                                                              self.lower_size_thresh, self.boxsize, write_coords_, file_ext,
                                                              d,self.picking_filament)
                continue

            # create an empty file name for the not checked micrograph file
            if self.is_3D_tomo is False:
                for f in empty_slice:
                    with open(path.join(d, f + file_ext),"w"):
                        pass

            if file_type == "CBOX":
                if self.is_3D_tomo is True and picked_filament is False:
                    # we want to save ANYWAY all the selected boxes
                    box_dictionary_to_save = helper.create_restore_box_dict(self.box_dictionary,self.is_folder_3D_tomo)

                helper_writer.write_coordinates(pd, box_dictionary_to_save,
                                                empty_slice, ignored_slice, file_name, d, self.is_3D_tomo, file_ext,
                                                is_cbox, self.current_conf_thresh,
                                                self.upper_size_thresh, self.lower_size_thresh, self.boxsize,
                                                write_coords_, self.picking_filament)
            elif self.is_3D_tomo is False:
                if file_type == "EMAN" and self.picking_filament:
                    for write_coords in write_coords_:
                        box_dir = d+helper_writer.HELICON_SUFFIX if "write_eman1_helicon" in str(write_coords) else d
                        helper_writer.write_coordinates(pd, box_dictionary_to_save, empty_slice, ignored_slice, file_name,
                                                        box_dir, self.is_3D_tomo, file_ext,
                                                        is_cbox, self.current_conf_thresh,
                                                        self.upper_size_thresh, self.lower_size_thresh, self.boxsize,
                                                        write_coords, self.picking_filament)
                else:
                    helper_writer.write_coordinates(pd, box_dictionary_to_save, empty_slice, ignored_slice, file_name, d, self.is_3D_tomo, file_ext,
                                                    is_cbox, self.current_conf_thresh,
                                                    self.upper_size_thresh, self.lower_size_thresh, self.boxsize, write_coords_, self.picking_filament)

    def _write_all_type_optimization(self, box_dir, selected_slice):
        """
        It saves on file the results after the optimization ( cbox_untraced case)
        :param box_dir: main directory where save the results
        :param selected_slice: list or dict ( in case of folder of tomo) of slices to save
        """
        if self.picking_filament:
            print("Something is wrong in '_write_all_type_optimization'. The filament picking option is not implemented")
            return
        # in this dictionaray i am sure that we have the result (converted in sketches) of 'do_tracing'
        self.box_dictionary_without_3D_visual = helper.create_deep_copy_box_dict(self.box_dictionary_3D_view,
                                                                                 self.is_folder_3D_tomo, False)

        """
        We save on file all the 3D boxes (the output of 'grouping3d.do_tracing' and 'frontend.non_maxima_suppress_fast_3d')
        from latest tracing
        """
        for file_type in ["STAR", "CBOX_3D", "EMAN_3D", "CBOX_REFINED", "COORDS"]:

            is_cbox = "CBOX" in file_type or "EMAN_3D" in file_type       # because in EMAN_3D output we want to have the same as in CBOX_3D

            file_name = self.get_current_purefilename()
            d = os.path.join(box_dir, file_type)

            file_ext, write_coords_ = helper_writer.prepare_vars_for_writing(box_dir, file_type, self.is_3D_tomo,picking_filament=False)

            if file_type == "COORDS":
                write_coords_ = CoordsIO. write_coords_file

            pd = QtG.QProgressDialog("Write box files to " + box_dir, "Cancel", 0, 100, self)
            pd.show()

            if file_type == "CBOX_REFINED":
                box_dictionary_to_save, ignored_slice, empty_slice = helper_writer.prepare_output(slices=selected_slice,
                                                                                                  input_box_dict=self.box_dictionary_without_3D_visual,
                                                                                                  is_folder_3D_tomo=self.is_folder_3D_tomo)

                # at 19.02.21 the picking filament is not enabled
                if self.is_folder_3D_tomo is True:
                    helper_writer.write_coordinates_3d_folder(pd, box_dictionary_to_save, empty_slice, ignored_slice,
                                                              self.is_folder_3D_tomo, is_cbox,
                                                              self.current_conf_thresh, self.upper_size_thresh,
                                                              self.lower_size_thresh, self.boxsize, write_coords_,
                                                              file_ext,
                                                              d,picking_filament=False)
                else:
                    helper_writer.write_coordinates(pd, box_dictionary_to_save, empty_slice, ignored_slice, file_name, d,
                                                    self.is_3D_tomo, file_ext,
                                                    is_cbox, self.current_conf_thresh,
                                                    self.upper_size_thresh, self.lower_size_thresh, self.boxsize,
                                                    write_coords_,picking_filament=False)

                continue

            if self.is_folder_3D_tomo is True:
                # we want to save ANYWAY all the selected boxes
                helper_writer.write_coordinates_3d_folder(pd, self.box_dictionary_without_3D_visual, [], [],
                                                              self.is_folder_3D_tomo, is_cbox,
                                                              self.current_conf_thresh, self.upper_size_thresh,
                                                              self.lower_size_thresh, self.boxsize, write_coords_,
                                                              file_ext,
                                                              d,picking_filament=False)
            else:
                helper_writer.write_coordinates(pd, self.box_dictionary_without_3D_visual, [], [], file_name, d,
                                                self.is_3D_tomo, file_ext,
                                                is_cbox, self.current_conf_thresh,
                                                self.upper_size_thresh, self.lower_size_thresh, self.boxsize,
                                                write_coords_,picking_filament=False)

        QtG.QMessageBox.warning(self, "Info", "Only the file saved in 'CBOX_REFINED' are usable to retrain crYOLO")
        return

    def write_all_type(self):
        """
        Write on file in star,cbox and box format.
        """
        result =True

        if self.active_3D_visualization:
            msg ="The saved coordinates cannot be used for training crYOLO"
            QtG.QMessageBox.warning(self, "Info", msg)


        # get the selected, via checkbox, slices/micrographs
        selected_slice = dict() if self.is_folder_3D_tomo else list()
        for root_index in range(self.tree.invisibleRootItem().childCount()):
            root_element = self.tree.invisibleRootItem().child(root_index) # can be tomogram or a folder
            for child_index in range(root_element.childCount()):
                if self.is_folder_3D_tomo:
                    selected_slice_child = list()
                    for child_child_index in range(root_element.child(child_index).childCount()):
                        if root_element.child(child_index).child(child_child_index).checkState(0) == QtCore.Qt.Checked:
                            selected_slice_child.append(child_child_index)
                    selected_slice.update({os.path.splitext(os.path.basename(root_element.child(child_index).text(0)))[0]:selected_slice_child})
                elif root_element.child(child_index).checkState(0) == QtCore.Qt.Checked:
                    if self.is_3D_tomo:
                        selected_slice.append(child_index)
                    else:
                        selected_slice.append(os.path.splitext(os.path.basename(root_element.child(child_index).text(0)))[0])


        box_dir = str(QtG.QFileDialog.getExistingDirectory(self, "Select Box Directory"))
        if box_dir == "":
            return

        # Remove untitled from path if untitled not exists
        if box_dir[-8] == "untitled" and os.path.isdir(box_dir):
            box_dir = box_dir[:-8]

        if box_dir == "":
            return

        if self.picking_filament:
            self.box_distance_filament_picking, result = QtG.QInputDialog.getInt(self,"Inter-box distance", "Please set the inter-box distance (in pixel) for each filament:", value=   DEFAULT_BOX_DISTANCE_FILAMENT_PICKING)

        if result:
            if self.is_cbox_untraced:
                self._write_all_type_optimization(box_dir,selected_slice)
            else:
                self._write_all_type_classic(box_dir, selected_slice)
        else:
            errmsg = QtG.QErrorMessage(self)
            errmsg.showMessage("Invalid Box distance value. It has to be an integer")
            return


        self.unsaved_changes = False


    def load_box_files(self):

        # reset the threshold. They are used to detect the number of visible element on an image
        #       See 'helper.check_if_should_be_visible' used in 'self.update_3D_counter'
        #   e.g.: If i load 'cbox_untraced' and then on the same sample i load the 'EMAN 3D' using the thresold set
        #       for 'cbox_untraced' tthe counter can not recognize the correct amount of visible boxes
        self.is_loading_boxes = True
        self.upper_size_thresh = DEFAULT_UPPER_SIZE_THRESH
        self.upper_size_thresh_line.setText(str(DEFAULT_UPPER_SIZE_THRESH))
        self.lower_size_thresh = DEFAULT_LOWER_SIZE_THRESH
        self.lower_size_thresh_line.setText(str(DEFAULT_LOWER_SIZE_THRESH))
        self.is_cbox = False
        self.eman_3D = False
        keep = False
        if self.unsaved_changes:
            msg = "There are unsaved changes. Are you sure?"
            reply = QtG.QMessageBox.question(
                self, "Message", msg, QtG.QMessageBox.Yes, QtG.QMessageBox.Cancel
            )

            if reply == QtG.QMessageBox.Cancel:
                return

        # It considers the 3d single image or the 2D_images folder
        show_question_box = len(self.box_dictionary) > 0 and self.is_folder_3D_tomo is False


        if self.is_folder_3D_tomo is True:
            for f in self.box_dictionary.keys():
                if len(self.box_dictionary[f]) > 0:
                    show_question_box = True
                    break

        if show_question_box:
            msg = "Keep old boxes loaded and show the new ones in a different color?"
            reply = QtG.QMessageBox.question(
                self, "Message", msg, QtG.QMessageBox.Yes, QtG.QMessageBox.No
            )

            if reply == QtG.QMessageBox.Yes:
                keep = True


        if self.plot is not None or self.is_folder_3D_tomo is True:
            box_dir = str(
                QtG.QFileDialog.getExistingDirectory(self, "Select Box Directory")
            )

            if box_dir == "":
                return

            if self.preview_win and self.preview_win.plot:
                self.preview_win.plot.close()
                self.preview_is_on = False

            self.is_cbox = False
            self.is_cbox_untraced = False

            if keep is False:
                self.delete_all_boxes()
                self.first_call_use_circle_changed = True  # for the 3D visualization POV it is like a resetting

            # the tracing is available only after loading a 'cbox_untraced' file
            if self.tabs:
                self.tabs.removeTab(INDEX_TAB_TRACING)

            if self.is_3D_tomo is False:
                self._import_boxes(box_dir, keep)
            elif self.is_folder_3D_tomo is True:
                self._import_boxes_3D_tomo_folder(box_dir, keep)
            else:
                self._import_boxes_3D_tomo(box_dir, keep)

            self._apply_3d_visualization_in_tomo_case()

            # picking filament is not possible after loading from file
            self.picking_filament_combox.setCurrentText(PARTICLE)
            self.blur_picking_filament()
        else:
            errmsg = QtG.QErrorMessage(self)
            errmsg.showMessage("Please open an image folder first")

        # otherwise in same cases (e.g: SPA) using the estimate_size param will be not able to reload the data
        if bool(self.box_dictionary_without_3D_visual) is False:
            self.box_dictionary_without_3D_visual = helper.create_deep_copy_box_dict(self.box_dictionary,self.is_folder_3D_tomo)

        if self.preview_is_on:
            self.trace_all = False
            self.preview_run(only_reload = True)
        self.is_loading_boxes = False


    def _apply_3d_visualization_in_tomo_case(self):
        """
        Called only in 'load_box_files'. I had to crete this function because i need it in case of run the sw via commandline
        """
        if self.is_cbox_untraced and self.is_3D_tomo:
            self.use_circle_combobox.setCurrentText(CIRCLE)
            self.update_boxes_on_current_image()
            self.update_3D_counter()
        elif (self.is_cbox or self.eman_3D) and self.is_3D_tomo:
            self.active_3D_visualization = True
            # it happened when the user load a .cbox file and then want to open another .cbox file on the save tomo/folder of tomos
            if self.use_circle_combobox.currentText() == CIRCLE and self.first_call_use_circle_changed:
                self.use_circle_changed()
            self.use_circle_combobox.setCurrentText(CIRCLE)
            # self.active_3D_visualization_checkbox.setChecked(True)
            self.active_3D_visualization_label.setEnabled(True)


    def _import_boxes_3D_tomo_folder(self, box_dir, keep=False):
        """
        It is the adaptation of '_import_boxes_3D_tomo' to work on the 'Open 3D image folder' case
        """
        import time as t
        pd = None
        # I set both to False here because this function is callable from console and not just via GUI
        self.is_cbox = False
        self.is_cbox_untraced = False
        self.eman_3D = False
        t_start = t.time()

        all_image_filenames = helper.get_all_loaded_filesnames(self.tree.invisibleRootItem().child(0))

        onlyfiles = [
            f
            for f in os.listdir(box_dir)
            if os.path.isfile(os.path.join(box_dir, f))
               and not f.startswith(".")
               and os.path.splitext(f)[0] in all_image_filenames
               and (f.endswith(".box") or f.endswith(".star") or f.endswith(".cbox"))

        ]

        if len(onlyfiles)>0:
            pd = QtG.QProgressDialog("Load box files...", "Cancel", 0, 100, self)
            pd.show()

        for file_index, fname in enumerate(onlyfiles):
            if pd.wasCanceled():
                break
            else:
                pd.show()
                pd.setValue(int((file_index + 1) * 100 / len(onlyfiles)))
            QtCore.QCoreApplication.instance().processEvents()

            path_3d_file = os.path.join(box_dir,fname)

            is_star_file = path_3d_file.split(".")[-1] =="star"
            is_cbox_file = path_3d_file.endswith(".cbox")

            fname = os.path.splitext(os.path.basename(path_3d_file))[0]

            if keep is False:
                rand_color = "r"
            else:
                rand_color = random.choice(["b", "c", "m", "y", "k", "w"])

            self.setWindowTitle("BoxManager " + ini.__version__ + " (Showing: " + box_dir + ")")
            box_imported = 0

            if is_star_file:
                boxes = CoordsIO.read_star_file(path_3d_file,self.boxsize)
            elif is_cbox_file:
                boxes = CoordsIO.read_cbox_boxfile(path_3d_file)
                if boxes:
                    if isinstance(boxes[0], utils.Filament):
                        self.create_filament_dict(boxes,fname)
                        box_imported = self.convert_filamentList_to_box_dictionary(self.box_dictionary,boxes, fname)
                        self.has_filament = True
                    if boxes[0]:
                        b = boxes[0].boxes[0] if self.has_filament else boxes[0]
                        self.is_cbox = not helper.is_cbox_untraced(b)
                        self.is_cbox_untraced = helper.is_cbox_untraced(b)
                        self.est_box_from_cbox = self.box_to_rectangle(b, None).get_est_size()
            else:
                boxes = CoordsIO.read_eman1_boxfile(path_3d_file,is_SPA=False, box_size_default=DEFAULT_BOX_SIZE)

            if self.has_filament is False:
                updated_entries = []
                for box in boxes:
                    rect = self.box_to_rectangle(box, rand_color)
                    box_imported += 1
                    if int(box.z) in self.box_dictionary[fname]:
                        self.box_dictionary[fname][int(box.z)].append(rect)
                    else:
                        self.box_dictionary[fname][int(box.z)] = [rect]
                    updated_entries.append((fname,str(int(box.z)))) #todo: ask Thorsten why it append it for each box instead of every time a new items in the self.box_dictionary is created

                self.set_checkstate_tree_leafs(self.tree.invisibleRootItem(), updated_entries,QtCore.Qt.Checked)

            self.show_loaded_boxes(self.box_dictionary[fname])

            print("Total time", t.time() - t_start)
            print("Total imported particles: ", box_imported)

        if self.is_cbox_untraced:
            self.create_tab_tracing()
        if pd:
            pd.close()
        self.update_3D_counter(self.box_dictionary)


    def _import_boxes_3D_tomo(self, box_dir, keep=False):
        import time as t

        box_imported = 0
        t_start = t.time()
        path_3d_file = os.path.join(box_dir,self.get_current_purefilename())
        pd = QtG.QProgressDialog("Load box files...", "Cancel", 0, 1, self)
        pd.show()
        pd.setValue(0)


        if os.path.isfile(path_3d_file+".star") is True:
            boxes = CoordsIO.read_star_file(path_3d_file+".star",self.boxsize)
        elif os.path.isfile(path_3d_file+".box") is True:
            boxes = CoordsIO.read_eman1_boxfile(path_3d_file+".box",is_SPA=False, box_size_default=DEFAULT_BOX_SIZE)
            self.eman_3D = True
        elif os.path.isfile(path_3d_file+".cbox") is True:
            boxes = CoordsIO.read_cbox_boxfile(path_3d_file+".cbox")
            if boxes:
                if isinstance(boxes[0],utils.Filament):
                    self.create_filament_dict(boxes)
                    box_imported = self.convert_filamentList_to_box_dictionary(self.box_dictionary,boxes)
                    self.has_filament = True
                if boxes[0]:
                    b = boxes[0].boxes[0] if self.has_filament else boxes[0]
                    self.is_cbox = not helper.is_cbox_untraced(b)
                    self.is_cbox_untraced = helper.is_cbox_untraced(b)
                    self.est_box_from_cbox = self.box_to_rectangle(b, None).get_est_size()
                    if self.is_cbox_untraced:
                        self.create_tab_tracing()

        else:
            errmsg = QtG.QErrorMessage(self)
            errmsg.showMessage("Error: no valid .star, .box or .cbox files found in directory '"+box_dir+"'")
            pd.close()
            return

        if keep is False:
            rand_color = "r"
        else:
            rand_color = random.choice(["b", "c", "m", "y", "k", "w"])

        self.setWindowTitle("Box manager (Showing: " + box_dir + ")")

        if self.has_filament is False:
            updated_entries = []
            for  box in boxes:
                rect = self.box_to_rectangle(box, rand_color)
                box_imported += 1
                if box.z in self.box_dictionary:
                    self.box_dictionary[int(box.z)].append(rect)
                else:
                    self.box_dictionary[int(box.z)] = [rect]
                updated_entries.append(str(int(box.z)))             #todo: ask Thorsten why it append it for each box instead of every time a new items in the self.box_dictionary is created
            self.set_checkstate_tree_leafs(self.tree.invisibleRootItem(), updated_entries, QtCore.Qt.Checked)
        self.show_loaded_boxes(self.box_dictionary)

        print("Total time", t.time() - t_start)
        print("Total imported particles: ", box_imported)
        pd.close()


    def convert_filamentList_to_box_dictionary(self, box_dict, filaments, fname=None):
        """
        :param box_dict: box_dictionary into convert
        :param filaments: list of filaments got from cbox file CoordsIO.read_cbox_boxfile
        :param fname: filename  file filename in case of SPA, tomo filename in case of folder
        """
        box_imported = 0
        updated_entries = []
        if self.is_folder_3D_tomo:
            for f in filaments:
                rand_color = random.choice(["b", "c", "m", "y", "k", "w"])
                for box in f.boxes:
                    box_imported += 1
                    rect = self.box_to_rectangle(box, rand_color)
                    if int(box.z) in box_dict[fname]:
                        box_dict[fname][int(box.z)].append(rect)
                    else:
                        box_dict[fname][int(box.z)] = [rect]
                        updated_entries.append((fname, str(int(box.z))))
        else:
            for f in filaments:
                rand_color = random.choice(["b", "c", "m", "y", "k", "w"])
                for box in f.boxes:
                    box_imported += 1
                    rect = self.box_to_rectangle(box, rand_color)
                    if fname:
                        if fname in box_dict:
                            box_dict[fname].append(rect)
                        else:
                            box_dict[fname] = [rect]
                    else:
                        if box.z in box_dict:
                            box_dict[int(box.z)].append(rect)
                        else:
                            box_dict[int(box.z)] = [rect]
                            updated_entries.append(str(int(box.z)))


        if self.has_filament is False:
            self.set_checkstate_tree_leafs(self.tree.invisibleRootItem(), updated_entries, QtCore.Qt.Checked)

        return box_imported


    def _import_boxes(self, box_dir, keep=False):
        import time as t

        pd = None
        # I set both to False here because this function is callable from console and not just via GUI
        self.is_cbox = False
        self.is_cbox_untraced = False   # it is available only for the tomo
        t_start = t.time()
        self.setWindowTitle("Box manager (Showing: " + box_dir + ")")
        box_imported = 0
        all_image_filenames = helper.get_all_loaded_filesnames(self.tree.invisibleRootItem().child(0))

        onlyfiles = [
            f
            for f in os.listdir(box_dir)
            if os.path.isfile(os.path.join(box_dir, f))
               and not f.startswith(".")
               and os.path.splitext(f)[0] in all_image_filenames
               and (
                       f.endswith(".box")
                       or f.endswith(".txt")
                       or f.endswith(".star")
                       or f.endswith(".cbox")
               )
               and os.stat(os.path.join(box_dir, f)).st_size != 0
        ]
        colors = ["b", "r", "c", "m", "y", "k", "w"]
        if keep == False:
            rand_color = "r"
        else:
            rand_color = random.choice(colors)
            while rand_color == "r":
                rand_color = random.choice(colors)
        star_dialog_was_shown = False
        filaments_imported = 0

        self.conf_thresh_line.setEnabled(False)
        self.conf_thresh_slide.setEnabled(False)
        self.conf_thresh_label.setEnabled(False)
        self.use_estimated_size_label.setEnabled(False)
        self.use_estimated_size_checkbox.setEnabled(False)
        self.show_confidence_histogram_action.setEnabled(False)
        self.show_size_distribution_action.setEnabled(False)


        if len(onlyfiles)>0:
            pd = QtG.QProgressDialog("Load box files...", "Cancel", 0, 100, self)
            pd.show()
        updated_entries = []
        is_star_startend = False
        for file_index, file in enumerate(onlyfiles):
            if pd and pd.wasCanceled():
                pd.close()
                break
            else:
                pd.show()
                pd.setValue(int((file_index + 1) * 100 / len(onlyfiles)))
            QtCore.QCoreApplication.instance().processEvents()

            path = os.path.join(box_dir, file)
            is_eman1_startend = False


            is_helicon = CoordsIO.is_eman1_helicon(path)
            if not is_helicon:
                is_eman1_startend = CoordsIO.is_eman1_filament_start_end(path)

            if not is_helicon and not is_eman1_startend:
                if file.endswith(".star") and star_dialog_was_shown == False:
                    msg = "Are the star files containing filament coordinates (start/end)?"
                    reply = QtG.QMessageBox.question(
                        self, "Message", msg, QtG.QMessageBox.Yes, QtG.QMessageBox.No
                    )
                    if reply == QtG.QMessageBox.Yes:
                        is_star_startend = True
                    star_dialog_was_shown = True

            if is_helicon or is_eman1_startend or is_star_startend:
                rects = []
                dict_entry_name = file[:-4]
                if is_helicon:
                    filaments = CoordsIO.read_eman1_helicon(path)
                elif is_eman1_startend:
                    filaments = CoordsIO.read_eman1_filament_start_end(path)
                elif is_star_startend:
                    print("Read filaments", path)
                    filaments = CoordsIO.read_star_filament_file(
                        path=path, box_width=100
                    )
                    dict_entry_name = file[:-5]

                filaments_imported = filaments_imported + len(filaments)
                for fil in filaments:
                    new_rand_color = random.choice(colors)
                    while new_rand_color == rand_color:
                        new_rand_color = random.choice(colors)
                    rand_color = new_rand_color
                    rect = [self.box_to_rectangle(box, rand_color) for box in fil.boxes]
                    rects.extend(rect)
                    box_imported = box_imported + len(rects)
                self.box_dictionary[dict_entry_name] = rects
            else:
                self.is_cbox = False
                if path.endswith(".box"):
                    boxes = CoordsIO.read_eman1_boxfile(path,is_SPA=True)
                if path.endswith(".star"):
                    boxes = CoordsIO.read_star_file(path,self.boxsize)
                if path.endswith(".cbox"):
                    boxes = CoordsIO.read_cbox_boxfile(path)
                    self.is_cbox = True
                    if boxes:
                        if isinstance(boxes[0], utils.Filament):
                            f_name= os.path.splitext(os.path.basename(path))[0]
                            self.create_filament_dict(boxes,f_name)
                            box_imported = self.convert_filamentList_to_box_dictionary(self.box_dictionary, boxes,f_name)
                            self.has_filament = True
                            self.est_box_from_cbox = self.box_to_rectangle( boxes[0].boxes[0], None).get_est_size()
                        else:
                            self.est_box_from_cbox = self.box_to_rectangle(boxes[0], None).get_est_size()


                dict_entry_name = os.path.splitext(file)[0]
                if self.is_cbox and self.has_filament:
                    for box in boxes:
                        rects = [self.box_to_rectangle(b, rand_color) for b in box.boxes]
                else:
                    rects = [self.box_to_rectangle(box, rand_color) for box in boxes]
                    box_imported = box_imported + len(rects)

                if dict_entry_name in self.box_dictionary:
                    self.box_dictionary[dict_entry_name].extend(rects)
                else:
                    self.box_dictionary[dict_entry_name] = rects
            updated_entries.append(dict_entry_name)

        self.set_checkstate_tree_leafs(self.tree.invisibleRootItem(), updated_entries, QtCore.Qt.Checked)
        self.show_loaded_boxes(self.box_dictionary)

        print("Total time", t.time() - t_start)
        print("Total imported particles: ", box_imported)
        if filaments_imported > 0:
            print("Total imported filaments: ", filaments_imported)
        if pd:
            pd.close()

    def show_loaded_boxes(self,box_dict):

        if self.is_cbox  or self.is_cbox_untraced:
            self.conf_thresh_line.setEnabled(True)
            self.conf_thresh_slide.setEnabled(True)
            self.conf_thresh_label.setEnabled(True)
            self.use_estimated_size_label.setEnabled(True)
            self.use_estimated_size_checkbox.setEnabled(True)
            self.show_confidence_histogram_action.setEnabled(True)
            self.show_size_distribution_action.setEnabled(True)
            if self.has_filament is False:
                self.upper_size_thresh_label.setEnabled(True)
                self.upper_size_thresh_slide.setEnabled(True)
                self.upper_size_thresh_line.setEnabled(True)
                self.lower_size_thresh_label.setEnabled(True)
                self.lower_size_thresh_slide.setEnabled(True)
                self.lower_size_thresh_line.setEnabled(True)
            if self.is_3D_tomo:
                self.num_boxes_thresh_slide.setEnabled(True)
                self.num_boxes_thresh_line.setEnabled(True)
                self.num_boxes_thres_label.setEnabled(True)


        self.update_boxes_on_current_image()
        self.boxsize_line.setText(str(self.boxsize))

        # In case of cbox files (not filament case), set the minimum and maximum
        if self.has_filament is False and (self.is_cbox or self.is_cbox_untraced):
            self.is_loading_max_min_sizes = True
            min_size = 99999
            max_size = -99999
            for _, rectangles in box_dict.items():
                for rect in rectangles:
                    if rect.get_est_size() > max_size:
                        max_size = rect.get_est_size()
                    if rect.get_est_size() < min_size:
                        min_size = rect.get_est_size()
            self.upper_size_thresh_slide.setMaximum(max_size)
            self.upper_size_thresh_slide.setMinimum(min_size)
            self.upper_size_thresh_slide.setValue(max_size)
            self.upper_size_thresh_line.setText("" + str(max_size))
            self.lower_size_thresh_slide.setMaximum(max_size)
            self.lower_size_thresh_slide.setMinimum(min_size)
            self.lower_size_thresh_slide.setValue(min_size)
            self.lower_size_thresh_line.setText("" + str(min_size))
            self.is_loading_max_min_sizes = False

        # Update particle numbers
        self.update_tree_boxsizes()

    def get_filter_state(self):
        lowersize = int(float(self.lower_size_thresh_line.text()))
        uppersize = int(float(self.lower_size_thresh_line.text()))
        conf = float(self.conf_thresh_slide.value())
        return (lowersize,uppersize,conf)

    def set_checkstate_tree_leafs(self, item, entries, state):
        child_count = item.childCount()
        child_child_counter = item.child(0).childCount()
        if child_child_counter>0:
            for child_id in range(child_count):
                self.set_checkstate_tree_leafs(item.child(child_id),entries,state)
        else:
            for child_id in range(child_count):
                parent_identifier = os.path.splitext(item.text(0))[0]
                dict_identifier = os.path.splitext(item.child(child_id).text(0))[0]
                if len(entries) == 0:
                    return
                if type(entries[0]) is tuple:
                    parent_entries = [entry[0] for entry in entries]
                    child_entries = [entry[1] for entry in entries]
                    for k in range(len(entries)):
                        if parent_identifier == parent_entries[k] and dict_identifier == child_entries[k]:
                            item.child(child_id).setCheckState(0,state)

                else:
                    if dict_identifier in entries:
                        item.child(child_id).setCheckState(0,state)


    def update_tree_boxsizes(self, update_current=False):
        state = self.get_filter_state()

        def update(boxes, item, fname =None):
            current_conf_thresh, upper_size_thresh, lower_size_thresh, current_num_boxes_thresh = self.get_threshold_params_for_given_tomo(fname)
            res = [helper.check_if_should_be_visible(box,current_conf_thresh, upper_size_thresh, lower_size_thresh, current_num_boxes_thresh, is_filament = self.has_filament) for box in boxes]

            num_box_vis = int(np.sum(res))
            item.setText(1, "{0:> 4d}  / {1:> 4d}".format(num_box_vis, len(res)))

        if update_current:
            item = self.tree.currentItem()
            filename = os.path.splitext(item.text(0))[0]

            if self.is_folder_3D_tomo is True:
                f_name = os.path.splitext(os.path.basename(self.current_image_path.split('/')[-1]))[0]
                update(self.box_dictionary[f_name][self.index_3D_tomo], item, f_name)
            elif self.is_3D_tomo is True:
                update(self.box_dictionary[self.index_3D_tomo], item)
            else:
                update(self.box_dictionary[filename], item)

        else:
            root = self.tree.invisibleRootItem().child(0)
            child_count = root.childCount()

            for i in range(child_count):
                QtCore.QCoreApplication.instance().processEvents()
                if not helper.filter_tuple_is_equal(self.get_filter_state(),state):
                    break
                item = root.child(i)
                filename = os.path.splitext(item.text(0))[0]
                if self.is_folder_3D_tomo is False:
                    if self.is_3D_tomo is True:
                        filename=int(filename)
                    if filename in self.box_dictionary:
                        update(self.box_dictionary[filename], item)
                    else:
                        item.setText(1,"")
                else:
                    for j in range(item.childCount()):
                        item_item=item.child(j)
                        if filename in self.box_dictionary.keys() and j in self.box_dictionary[filename]:
                            update(self.box_dictionary[filename][j], item_item,filename)
                        else:
                            item_item.setText(1,"")


    def create_filament_dict(self, filaments, fname = None):
        """
        :param filaments: list of filaments got from cbox file CoordsIO.read_cbox_boxfile
        :param fname: filename  file filename in case of SPA, tomo filename in case of folder
        """
        if self.is_folder_3D_tomo:
            for f in filaments:
                if f.boxes:
                    if fname in self.filament_dict and int(f.boxes[0].z) in self.filament_dict[fname]:
                        self.filament_dict[fname][int(f.boxes[0].z)].append(f)
                    elif fname in self.filament_dict:
                        self.filament_dict[fname][int(f.boxes[0].z)] = [f]
        else:
            for f in filaments:
                if f.boxes:
                    index = fname if fname else int(f.boxes[0].z)
                    if index in self.filament_dict:
                        self.filament_dict[index].append(f)
                    else:
                        self.filament_dict[index] = [f]


    def boxes_to_rectangle(self,boxes,color):
        return [self.box_to_rectangle(box, color) for box in boxes]


    def box_to_rectangle(self, box, color):
        num_boxes = 1
        width = int(box.w)
        height = int(box.h)
        avg_size = (width + height) // 2
        self.boxsize = avg_size
        est_size = avg_size
        meta = None
        if "est_box_size" in box.meta:
            meta = {"est_box_size": box.meta["est_box_size"]}
            est_size = (box.meta["est_box_size"][0] + box.meta["est_box_size"][1]) // 2
        if 'num_boxes' in box.meta and self.is_cbox and isnan(box.meta["num_boxes"]) is False:
            num_boxes = box.meta["num_boxes"]

        confidence = box.c if box.c is not None else 1
        return  MySketch.MySketch(xy =(int(box.x), int(box.y)), width=width, height=height, is_3d_tomo=self.is_3D_tomo,
                                 angle=0.0, est_size=est_size, confidence=confidence, only_3D_visualization=False,
                                 num_boxes=num_boxes, meta=meta, z=box.z,
                                 linewidth=1, edgecolor=color, facecolor="none")


    def draw_all_patches(self, rects):
        state = self.get_filter_state()
        purefilename = self.get_current_purefilename() if self.is_folder_3D_tomo else None
        current_conf_thresh, upper_size_thresh, lower_size_thresh, current_num_boxes_thresh = self.get_threshold_params_for_given_tomo(purefilename)
        visible_rects = [box.getSketch(circle=self.use_circle) for box in rects if helper.check_if_should_be_visible(box,current_conf_thresh, upper_size_thresh, lower_size_thresh, current_num_boxes_thresh, is_filament = self.has_filament)]

        for rect in visible_rects:
            if rect.get_visible()==False:
                rect.set_visible(True)
            if rect not in self.ax.patches:
                self.ax.add_patch(rect)
            if not helper.filter_tuple_is_equal(self.get_filter_state(),state):
                break

    def _set_selected_folder(self):
        """
        :return: the folder name, as string, selected by the user via GUI
        """
        selected_folder = str(
            QtG.QFileDialog.getExistingDirectory(self, "Select Image Directory")
        )

        if selected_folder == "":
            return

        if self.unsaved_changes:
            msg = "All loaded boxes are discarded. Are you sure?"
            reply = QtG.QMessageBox.question(
                self, "Message", msg, QtG.QMessageBox.Yes, QtG.QMessageBox.Cancel
            )

            if reply == QtG.QMessageBox.Cancel:
                return

        self.current_image_path = None
        return selected_folder

    def open_image3D_folder(self):
        """
        Let the user choose the image folder and adds it to the ImageFolder-Tree
        :return: none
        """
        # When we select it we open the first slice of the first tomo in the folder.
        # This operation is in the catch of a try-catch statement that is raised in case of self.im = None
        self.im = None
        selected_folder=self._set_selected_folder()
        img_loaded = self._open_image3D_folder(selected_folder)
        if img_loaded:
            self.button_apply_filter.setEnabled(True)

        self.unsaved_changes = False

    def open_image_folder(self):
        """
        Let the user choose the image folder and adds it to the ImageFolder-Tree
        :return: none
        """
        img_loaded = self._open_image_folder(self._set_selected_folder())
        if img_loaded:
            self.button_apply_filter.setEnabled(True)
        self.unsaved_changes = False

    def open_image3D_tomo(self):
        """
        Let the user choose the image 3D  adds it slice to the ImageFolder-Tree.
        :return: none
        """
        self.reset_config(new_img=True)
        self.is_3D_tomo = True
        self.index_3D_tomo = 0
        selected_image = QtG.QFileDialog.getOpenFileName(self, "Select 3D Image File")[0]


        if selected_image == "":
            return

        if self.unsaved_changes:
            msg = "All loaded boxes are discarded. Are you sure?"
            reply = QtG.QMessageBox.question(
                self, "Message", msg, QtG.QMessageBox.Yes, QtG.QMessageBox.Cancel
            )

            if reply == QtG.QMessageBox.Cancel:
                return

        self.current_image_path = selected_image
        img_loaded = self._open_single_image3D(self.current_image_path)

        if img_loaded:
            self.button_apply_filter.setEnabled(True)

        self.unsaved_changes = False


    def _open_single_image3D(self, path):
        if path.endswith(("mrc","mrcs","rec")) is False:
            errmsg = QtG.QErrorMessage(self)
            errmsg.showMessage("ERROR: The image '" + str(path) + "' has an invalid format. Must be in .mrc or .mrcs format")
            return False
        self.current_image3D_mmap = helper.read_image(path,use_mmap=True) #imagereader.image_read(path,use_mmap=True)

        if len(self.current_image3D_mmap.shape) !=3:
            errmsg = QtG.QErrorMessage(self)
            errmsg.showMessage("ERROR: The image '"+str(path)+"' is not a 3D image")
            return False

        root = QtG.QTreeWidgetItem([path])
        root.setCheckState(0, QtCore.Qt.Unchecked)

        # init item filename and slice_tomo
        purefilename = self.get_current_purefilename()
        self.item_3D_filename.update({purefilename: root})
        self.tot_frames.update({purefilename: self.current_image3D_mmap.data.shape[0]})
        self.smallest_image_dim.update({purefilename: min(self.current_image3D_mmap.data.shape[1], self.current_image3D_mmap.data.shape[2])})

        self.reset_tree(root,path)

        if self.current_image3D_mmap.shape[0] > 0:
            for i in range(self.current_image3D_mmap.shape[0]):
                QtCore.QCoreApplication.instance().processEvents()
                c = QtG.QTreeWidgetItem([str(i)])
                c.setCheckState(0, QtCore.Qt.Unchecked)
                root.addChild( c)
        else:
            errmsg = QtG.QErrorMessage(self)
            errmsg.showMessage("ERROR: The image '"+str(path)+"' is recognized as a 3D image but has no slice (i.e.: mrc.data.shape[0]<1")
            return False

        root.setExpanded(True)
        # Show first image
        img_data=self.current_image3D_mmap[int(root.child(0).text(0)), :, :]
        self.current_tree_item = root.child(0)

        self.rectangles = []
        # Create figure and axes

        self._set_first_time_img(img_data)

        self.tree.setCurrentItem(
            self.tree.invisibleRootItem().child(0).child(0)
        )
        self.plot.setWindowTitle(os.path.basename(self.current_image_path))
        return True

    def _open_image3D_folder(self, path):
        """
        Reads the image folder, setup the folder daemon and signals
        :param path: Path to image3D folder
        """
        self.reset_config(new_img=True)
        self.is_3D_tomo = True
        self.is_folder_3D_tomo = True
        self.index_3D_tomo =0
        self.last_index_3D_tomo = self.index_3D_tomo
        self.image_folder = path
        root,onlyfiles,all_items=self._list_files_in_folder(path,True)
        if root is not False and onlyfiles is not False and all_items is not False:
            if onlyfiles:
                root.setExpanded(True)
                self.current_image_path = self.image_folder
                index=0
                for f in onlyfiles:
                    purefilename = os.path.splitext(os.path.basename(f))[0]
                    self.picked_filament_dictionary.update({purefilename:{}})
                    self.box_dictionary.update({purefilename:{}})
                    self.box_dict_traced.update({purefilename: {}})
                    self.filament_dict.update({purefilename: {}})
                    self.item_3D_filename.update({purefilename: root.child(index)})
                    with mrcfile_mmap(os.path.join(self.image_folder,f), permissive=True, mode="r") as mrc:
                        self.tot_frames.update({purefilename: mrc.data.shape[0]})
                        self.smallest_image_dim.update({purefilename: min(mrc.data.shape[1],mrc.data.shape[2])})
                        if mrc.data.shape[0] > 0:
                            if self.current_image3D_mmap is None:
                                self.current_image_path=os.path.join(self.image_folder, f)
                                self.current_image3D_mmap= helper.read_image(self.current_image_path, use_mmap=True)
                                title = os.path.basename(self.current_image_path) + "\tindex: " + str(self.index_3D_tomo)
                            for i in range(mrc.data.shape[0]):
                                QtCore.QCoreApplication.instance().processEvents()
                                c = QtG.QTreeWidgetItem([str(i)])
                                c.setCheckState(0, QtCore.Qt.Unchecked)
                                root.child(index).addChild(c)
                        index+=1
                        mrc.close()

            self.fill_params(self.item_3D_filename.keys())

            if self.current_image3D_mmap is not None:
                self._set_first_time_img(self.current_image3D_mmap[0, :, :])
                # child_1 = folder  child_2 = list of tomo  child_3 = list of slices
                self.tree.setCurrentItem(self.tree.invisibleRootItem().child(0).child(0).child(0))
                self.plot.setWindowTitle(title)
                return True

        errmsg = QtG.QErrorMessage(self)
        errmsg.showMessage("ERROR: The folder '" + str(path) + "' does not have tomogram")
        return False

    def _open_image_folder(self, path):
        """
        Reads the image folder, setup the folder daemon and signals
        :param path: Path to image folder
        """
        self.reset_config(new_img=True)
        self.image_folder = path
        root,onlyfiles,all_items=self._list_files_in_folder(path,False)
        if root is not False and onlyfiles is not False and all_items is not False:

            if onlyfiles:
                root.setExpanded(True)
                # Show first image
                self.current_image_path = os.path.join(
                    self.image_folder, str(root.child(0).text(0))
                )
                self.current_tree_item = root.child(0)
                im = helper.read_image(self.current_image_path)

                if len(im.shape) !=2:
                    errmsg = QtG.QErrorMessage(self)
                    errmsg.showMessage("Please open an image folder with micrographs")
                    return False

                self.rectangles = []
                self._set_first_time_img(im)

                self.tree.setCurrentItem(
                    self.tree.invisibleRootItem().child(0).child(0)
                )
                self.plot.setWindowTitle(os.path.basename(self.current_image_path))
                return True
            return False

    def myKeyPressEvent(self, event):
        if event.name == "key_press_event" and event.key == "h":
            # if it is a 3D tomo pure_filename identifies the slice of the tomo
            pure_filename = os.path.basename(self.current_image_path)[:-4] if self.is_3D_tomo is False else self.index_3D_tomo

            if pure_filename in self.box_dictionary:
                rects = self.box_dictionary[pure_filename]
                if self.toggle:
                    self.draw_all_patches(rects)
                    self.fig.canvas.draw()
                    self.toggle = False
                else:
                    self.delete_all_patches(rects)
                    self.fig.canvas.draw()
                    self.toggle = True

    def ondraw(self, event):
        if self.zoom_update:
            self.zoom_update = False
            self.background_current = self.fig.canvas.copy_from_bbox(self.ax.bbox)
            self.draw_all_patches(self.rectangles)
            self._draw_all_boxes()

    def onresize(self, event):
        self.delete_all_patches(self.rectangles)
        self.fig.canvas.draw()
        self.background_current = self.fig.canvas.copy_from_bbox(self.ax.bbox)
        self.draw_all_patches(self.rectangles)


    def onmove(self, event):
        if event.inaxes != self.ax:
            return
        if event.button == 1:
            if self.picking_filament is False:
                if self.moving_box is not None:
                    rect_width = self.moving_box.getSketch().get_width()
                    x = event.xdata - rect_width / 2
                    y = event.ydata - rect_width / 2

                    # set the new x,y coordinate for the rectangle sketch
                    self.moving_box.getSketch(circle=False).set_x(x)
                    self.moving_box.getSketch(circle=False).set_y(y)
                    self.moving_box.set_xy((x,y), circle=False)

                    # set the new x,y coordinate for the circle sketch
                    self.moving_box.getSketch(circle=True).center=(event.xdata,event.ydata)
                    self.moving_box.set_xy((event.xdata,event.ydata), circle=True)

                    self.boxsize = rect_width  # Update the current boxsize

                    self.fig.canvas.restore_region(self.background_current)
                    ## draw all boxes again
                    self._draw_all_boxes()
            else:
                self.picked_filament_list[-1].end_fil = [event.xdata,event.ydata]

                # remove all the boxes from the current image
                pure_filename_folder_case = os.path.splitext(os.path.basename(self.current_image_path.split('/')[-1]))[0]
                pure_filename = self.get_current_purefilename() if self.is_3D_tomo is False else self.index_3D_tomo

                if self.is_folder_3D_tomo is True:
                    if pure_filename_folder_case in self.box_dictionary and self.index_3D_tomo in self.box_dictionary[pure_filename_folder_case]:
                        self.rectangles = self.box_dictionary[pure_filename_folder_case][self.index_3D_tomo]
                        self.box_dictionary[pure_filename_folder_case][self.index_3D_tomo] = list()
                    else:
                        self.box_dictionary[pure_filename_folder_case].update({self.index_3D_tomo: list()})
                else:
                    # if it is a single 3D image tomo pure_filename identifies the slice of the tomo
                    if pure_filename in self.box_dictionary:
                        self.rectangles = self.box_dictionary[pure_filename]
                        self.box_dictionary[pure_filename]= list()
                    else:
                        self.box_dictionary.update({pure_filename: list()})

                # clean the image removing the patches and save as current background
                self.delete_all_patches(self.rectangles)
                self.background_current_onmove = self.fig.canvas.copy_from_bbox(self.ax.bbox)
                self.rectangles = list()

                # fill again the current image with boxes
                sketch = self.picked_filament_list[-1].get_rect_sketch()
                if self.is_folder_3D_tomo is True:
                    self.box_dictionary[pure_filename_folder_case][self.index_3D_tomo].append(sketch)
                else:
                    self.box_dictionary[pure_filename].append(sketch)
                self.rectangles.append(sketch)

                #todo: for debug if the square boxes are exactly on the ractangle uncomment the following line
                #self.picked_filament_list[-1].fill_sketches(box_distance=1)
                #self.rectangles+=self.picked_filament_list[-1].get_sketches()

                self.draw_all_patches(self.rectangles)
                self._draw_all_boxes()

                # i do not why but whitout the following instruction it plots everything i selected while presing the button
                self.fig.canvas.restore_region(self.background_current_onmove)



    def onrelease(self, event):
        if self.picking_filament is False:
            self.moving_box = None
        elif self.removing_picked_filament is False :
            self.picked_filament_list[-1].end_fil = [event.xdata,event.ydata]
            sketch = self.picked_filament_list[-1].get_rect_sketch()

            # Add the patch to the Axes otherwise i cannot visualize them correctly when
            self.ax.add_patch(sketch.getSketch(self.use_circle))
            self.ax.draw_artist(sketch.getSketch(self.use_circle))
            self.picked_filament_as_rect_dictionary.append(sketch)

            if self.is_3D_tomo is False:
                self.picked_filament_dictionary[self.get_current_purefilename()] = self.picked_filament_list
                self.box_dictionary[self.get_current_purefilename()] = self.picked_filament_as_rect_dictionary
            elif self.is_folder_3D_tomo:
                pure_filename = os.path.splitext(os.path.basename(self.current_image_path.split('/')[-1]))[0]
                self.picked_filament_dictionary[pure_filename][self.index_3D_tomo] = self.picked_filament_list
                self.box_dictionary[pure_filename][self.index_3D_tomo] = self.picked_filament_as_rect_dictionary
            else:
                self.picked_filament_dictionary[self.index_3D_tomo] = self.picked_filament_list
                self.box_dictionary[self.index_3D_tomo]= self.picked_filament_as_rect_dictionary

            self.update_tree_boxsizes(True)
            if self.is_3D_tomo:
                self.update_3D_counter()

        self.removing_picked_filament = False


    def is_click_into_box(self, index,x,y):
        # rotate the box and the clicked point on the x axis and then easily check if the totated point is into the rotated box
        f = self.picked_filament_list[index]

        rotated_corners=f.get_rotated_coordinate_rect()

        rotated_point = f.get_R() @ np.array((x, y)).T
        max_value = np.amax(rotated_corners,axis=1)
        min_value = np.amin(rotated_corners, axis=1)

        if min_value[0]< rotated_point[0] <max_value[0] and min_value[1]<rotated_point[1]<max_value[1]:
            return True

        return False

    def remove_picked_filament(self,x,y):
        self.removing_picked_filament = True
        a = np.array([x, y])
        box = None
        index = None

        for index, box in enumerate(self.rectangles):
            if self.is_click_into_box(index,x,y):
                del self.rectangles[self.rectangles.index(box)]
                self.delete_all_patches(self.rectangles)
                self.fig.canvas.restore_region(self.background_current)
                self.draw_all_patches(self.rectangles)
                self._draw_all_boxes()

                # for updating n the correct way the trees i have to set the correctly value in the box_dictionary
                if self.is_folder_3D_tomo is True:
                    pure_filename = os.path.splitext(os.path.basename(self.current_image_path.split('/')[-1]))[0]
                    if pure_filename in self.box_dictionary and self.index_3D_tomo in self.box_dictionary[pure_filename]:
                        self.box_dictionary[pure_filename][self.index_3D_tomo] = self.rectangles
                    if pure_filename in self.picked_filament_dictionary and self.index_3D_tomo in self.picked_filament_dictionary[pure_filename]:
                        self.picked_filament_dictionary[pure_filename][self.index_3D_tomo]  = self.picked_filament_list
                else:
                    # if it is a single 3D image tomo pure_filename identifies the slice of the tomo
                    pure_filename = self.get_current_purefilename() if self.is_3D_tomo is False else self.index_3D_tomo
                    if pure_filename in self.box_dictionary:
                        self.box_dictionary[pure_filename] = self.rectangles
                    if pure_filename in self.picked_filament_dictionary:
                        self.picked_filament_dictionary[pure_filename] = self.picked_filament_list

                self.update_tree_boxsizes(True)
                if self.is_3D_tomo:
                    self.update_3D_counter()
                break
            else:
                box = None

        if box is not None:
            self.picked_filament_list.pop(index)
            self.rectangles = [f.get_rect_sketch() for f in self.picked_filament_list]
            self.unsaved_changes = True





    def onclick(self, event):
        # The code about the 3D visualization will be used in the next release and it will be not removed
        # that means that when this function is run we have always:
        #   self.active_3D_visualization = False
        #   change_active_3D_visualization = False
        if self.active_3D_visualization:
            errmsg = QtG.QErrorMessage(self)
            errmsg.showMessage("Picking in 3D boxes is not supported. If you want to create training data, please reset the boxmanager (File -> Reset) and place your boxes sliceswise.")
            return


        change_active_3D_visualization = False
        if self.active_3D_visualization:
            self.active_3D_visualization_checkbox.setChecked(False)         #it calls in automatic self.active_3D_visualization_changed()
            change_active_3D_visualization = True

        if self.plot.toolbar._active is not None:
            return

        modifiers = QtG.QApplication.keyboardModifiers()

        if event.xdata is None or event.ydata is None or event.xdata < 0 or event.ydata < 0:
            return
        y = event.ydata - self.boxsize / 2
        x = event.xdata - self.boxsize / 2

        # after starting picking is not possible to switch from picking box and filament. you have to reset
        self.blur_picking_filament()


        if self.is_folder_3D_tomo is True:
            pure_filename =  os.path.splitext(os.path.basename(self.current_image_path.split('/')[-1]))[0] #self.current_image_path.split('/')[-1]
            if pure_filename in self.box_dictionary and self.index_3D_tomo in self.box_dictionary[pure_filename]:
                self.rectangles = self.box_dictionary[pure_filename][self.index_3D_tomo]
            else:
                self.rectangles = []
                self.box_dictionary[pure_filename][self.index_3D_tomo] = self.rectangles
        else:
            # if it is a single 3D image tomo pure_filename identifies the slice of the tomo
            pure_filename = self.get_current_purefilename() if self.is_3D_tomo is False else self.index_3D_tomo
            if pure_filename in self.box_dictionary:
                self.rectangles = self.box_dictionary[pure_filename]
            else:
                self.rectangles = []
                self.box_dictionary[pure_filename] = self.rectangles

        if self.picking_filament:
            if modifiers == QtCore.Qt.ControlModifier:
                self.remove_picked_filament(event.xdata, event.ydata)
                if len(self.picked_filament_list) == 0:
                    self.tree.selectedItems()[0].setCheckState(0, QtCore.Qt.Unchecked)
                return
            self.use_circle_combobox.setCurrentText(RECT)
            new_filament = picked_filament(box_size=self.boxsize,is_3D_tomo=self.is_3D_tomo)
            new_filament.set_first(event = event)
            self.picked_filament_list.append(new_filament)
            # we need it for the first image displayed if the 'picking filament' flag is not active
            self.update_picking_filament_dict()
            self.tree.selectedItems()[0].setCheckState(0, QtCore.Qt.Checked)

            return


        if (
                modifiers == QtCore.Qt.ControlModifier
                or modifiers == QtCore.Qt.MetaModifier
        ):
            # Delete box
            box = helper.get_corresponding_box(
                x,
                y,
                self.rectangles,
                self.current_conf_thresh,
                self.boxsize
            )

            if box is not None:
                self.delete_box(box)
        else:
            self.moving_box = helper.get_corresponding_box(
                x,
                y,
                self.rectangles,
                self.current_conf_thresh,
                self.boxsize
            )
            if self.moving_box is None:

                # Delete lower confidence box if available
                box = helper.get_corresponding_box(
                    x,
                    y,
                    self.rectangles,
                    self.current_conf_thresh,
                    self.boxsize,
                    get_low=True,
                )

                if box is not None:
                    self.rectangles.remove(box)

                # Create new box
                est_size = self.est_box_from_cbox if self.is_cbox else self.boxsize

                rect = MySketch.MySketch(xy=(x,y), width=self.boxsize, height=self.boxsize,
                                         is_3d_tomo=self.is_3D_tomo, angle=0.0, est_size=est_size, confidence=1,
                                         only_3D_visualization=False, num_boxes=1, meta=None, z=None,
                                         linewidth=1, edgecolor="r", facecolor="none")

                # plot and consider as new rect only the one with the starting size of the box (i.e.: got via file or set via GUI)
                self.moving_box = rect
                self.rectangles.append(rect)
                # Add the patch to the Axes
                self.ax.add_patch(rect.getSketch(self.use_circle))
                self.ax.draw_artist(rect.getSketch(self.use_circle))

                self.fig.canvas.blit(self.ax.bbox)
                self.unsaved_changes = True
                self.update_tree_boxsizes(update_current=True)

                if self.preview_is_on and self.has_filament is False:
                    self.trace_all = False
                    self.preview_run(only_reload=True)

            if change_active_3D_visualization:
                self.active_3D_visualization_checkbox.setChecked(True)
                self.update_tree_boxsizes(update_current=True)

            if self.is_3D_tomo:
                self.update_3D_counter()
            # self.fig.canvas.draw()

        if len(self.rectangles) > 0:
            self.tree.selectedItems()[0].setCheckState(0, QtCore.Qt.Checked)
        else:
            self.tree.selectedItems()[0].setCheckState(0, QtCore.Qt.Unchecked)



    def delete_box(self, box):
        box.getSketch(circle=self.use_circle).remove()
        del self.rectangles[self.rectangles.index(box)]
        self.fig.canvas.restore_region(self.background_current)
        self._draw_all_boxes()
        self.unsaved_changes = True
        self.update_tree_boxsizes(update_current=True)

    def _draw_all_boxes(self):
        state = self.get_filter_state()
        for box in self.rectangles:
            rect = box.getSketch(self.use_circle)
            self.ax.draw_artist(rect)
            if not helper.filter_tuple_is_equal(self.get_filter_state(),state):
                break
        self.fig.canvas.blit(self.ax.bbox)


    # REFACTORING FUNCTIONS
    def reset_tree(self, root, title):
        self.tree.clear()
        self.tree.setColumnCount(2)
        self.tree.setHeaderHidden(False)
        self.tree.setHeaderLabels(["Filename", "Number of boxes"])
        if self.plot is not None:
            self.plot.close()
        self.rectangles = []
        self.box_dictionary = {}
        self.tree.addTopLevelItem(root)
        fm = QFontMetrics(self.font)
        w = fm.width(title)
        self.tree.setMinimumWidth(w + 150)
        self.tree.setColumnWidth(0, 300)

    def _list_files_in_folder(self,path,is_list_tomo=False):
        """
        :param path: path to the folder
        :param is_list_tomo: True if folder of 3D tomo
        :return root: the QTreeWidgetItem
        :return onlyfiles: list of valid 3D tomo files
        :return all_items: items of the root (one for each valid file)
        """
        if path != "" and path is not None:
            title = os.path.join(str(path), self.wildcard) if self.wildcard else str(path)
            root = QtG.QTreeWidgetItem([title])
            root.setCheckState(0, QtCore.Qt.Unchecked)
            self.reset_tree(root, title)

            onlyfiles = helper.get_only_files(path,self.wildcard,is_list_tomo)
            all_items = [QtG.QTreeWidgetItem([file]) for file in onlyfiles]

            pd = None
            if len(all_items) > 0:
                pd = QtG.QProgressDialog("Load images", "Cancel", 0, 100, self)
                pd.show()
            for item_index, item in enumerate(all_items):
                pd.show()
                QtCore.QCoreApplication.instance().processEvents()
                pd.setValue(int((item_index+1)*100/len(all_items)))
                item.setCheckState(0, QtCore.Qt.Unchecked)
                root.addChild(item)
            return root,onlyfiles,all_items
        return False,False,False

    def clean_box_dictionary(self):
        root = self.tree.invisibleRootItem().child(0)
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            if self.is_folder_3D_tomo is True:
                for index in range(item.childCount()):
                    item.child(index).setText(1, "")
            elif self.is_3D_tomo is True:
                item.setText(1, "")


        if self.is_folder_3D_tomo is True:
            for filename in self.box_dictionary.keys():
                self.box_dictionary[filename] = {}
        else:
            self.box_dictionary = {}

    def update_3D_counter(self, box_dict = None):
        """
        It updates the number of total particles in a single tomo
        """
        if box_dict is None:
            box_dict = self.box_dictionary
        for f, f_item in self.item_3D_filename.items():
            tot_res, tot_num_box_vis = 0, 0
            if box_dict:        # after resetting via File->reset the self.box_dictionary is empty
                list_index = box_dict[f].keys() if self.is_folder_3D_tomo else box_dict.keys()
                for index in list_index:
                    boxes = box_dict[f][index] if self.is_folder_3D_tomo else box_dict[index]
                    fname = f if self.is_folder_3D_tomo else None
                    current_conf_thresh, upper_size_thresh, lower_size_thresh, current_num_boxes_thresh = self.get_threshold_params_for_given_tomo(fname)
                    res = [helper.check_if_should_be_visible(box,current_conf_thresh, upper_size_thresh, lower_size_thresh, current_num_boxes_thresh, is_filament = self.has_filament) for box in boxes if box.only_3D_visualization is False]
                    tot_res += len(res)
                    tot_num_box_vis += int(np.sum(res))

            f_item.setText(1, "{0:> 4d}  / {1:> 4d}".format(tot_num_box_vis, tot_res))

    def reset_config(self, new_img=False):
        """
        Restore the default option
        :param new_img: If False it will not reset the variables related to the last case. False when you click on 'reset' in the GUI menu
        """
        self.trace_all = False
        self.is_updating_params = True
        if self.preview_win and self.preview_win.plot:
            self.preview_win.plot.close()
        if self.box_dictionary:
            self.delete_all_boxes()
            # I have to redraw on the current image to delete the drawn sketches
            self.delete_all_patches([], update=True)
            self.draw_all_patches([])
            self._draw_all_boxes()
            self.update_3D_counter()
            self.update_tree_boxsizes()


        self.picked_filament_dictionary = deepcopy(self.box_dictionary)
        self.filament_dict = deepcopy(self.box_dictionary)
        self.picked_filament_list = list()


        # uncheck all the checked slices (tomo cases) or images (SPA cases)
        for root_index in range(self.tree.invisibleRootItem().childCount()):
            root_element = self.tree.invisibleRootItem().child(root_index) # can be tomogram or a folder
            for child_index in range(root_element.childCount()):
                if self.is_folder_3D_tomo:
                    for child_child_index in range(root_element.child(child_index).childCount()):
                        root_element.child(child_index).child(child_child_index).setCheckState(0, QtCore.Qt.Unchecked)
                else:
                    root_element.child(child_index).setCheckState(0, QtCore.Qt.Unchecked)

        self.has_filament = False
        self.active_3D_visualization_label.setEnabled(False)
        self.use_circle_combobox.setCurrentText(RECT)
        #self.active_3D_visualization_checkbox.setChecked(False) for now is not available
        self.active_3D_visualization = False
        self.box_dictionary_without_3D_visual = {}
        self.boxsize = DEFAULT_BOX_SIZE
        self.boxsize_line.setText(str(self.boxsize))
        self.upper_size_thresh = DEFAULT_UPPER_SIZE_THRESH
        self.upper_size_thresh_line.setText(str(DEFAULT_UPPER_SIZE_THRESH))
        self.lower_size_thresh = DEFAULT_LOWER_SIZE_THRESH
        self.lower_size_thresh_line.setText(str(DEFAULT_LOWER_SIZE_THRESH))
        self.current_conf_thresh = DEFAULT_CURRENT_CONF_THRESH
        self.conf_thresh_line.setText(str(DEFAULT_CURRENT_CONF_THRESH))
        self.current_num_boxes_thresh =DEFAULT_CURRENT_NUM_BOXES_THRESH
        self.num_boxes_thresh_line.setText(str(DEFAULT_CURRENT_NUM_BOXES_THRESH))
        self.filter_freq = DEFAULT_FILTER_FREQ
        self.filter_line.setText(str(self.filter_freq))
        self.use_estimated_size = False
        self.est_box_from_cbox = None
        self.is_cbox = False
        self.eman_3D = False
        self.is_cbox_untraced = False
        self.rectangles = []
        self.preview_is_on = False

        self.button_trace.setEnabled(True)

        if new_img:
            self.is_folder_3D_tomo = False
            self.is_3D_tomo = False
            self.index_3D_tomo = None
            self.last_file_3D_tomo = None
            self.last_index_3D_tomo = None
            self.last_filename_in_tomo_folder = None
            self.im = None
            self.item_3D_filename = {}
            self.current_image3D_mmap = None
        elif self.picking_filament:             # workaround: otherwise it is not able to remove the picked filaments
            self.ax.patches = list()
            self.background_current = self.fig.canvas.copy_from_bbox(self.ax.bbox)
        self.picking_filament_combox.setCurrentText(PARTICLE)

        # the tracing is available only after loading a 'cbox_untraced' file
        if self.tabs:
            self.tabs.removeTab(INDEX_TAB_TRACING)

        # blur the thresholding option
        self.num_boxes_thresh_slide.setEnabled(False)
        self.num_boxes_thresh_line.setEnabled(False)
        self.num_boxes_thres_label.setEnabled(False)
        self.conf_thresh_line.setEnabled(False)
        self.conf_thresh_slide.setEnabled(False)
        self.conf_thresh_label.setEnabled(False)
        self.use_estimated_size_label.setEnabled(False)
        self.use_estimated_size_checkbox.setEnabled(False)
        self.show_confidence_histogram_action.setEnabled(False)
        self.show_size_distribution_action.setEnabled(False)
        self.upper_size_thresh_label.setEnabled(False)
        self.upper_size_thresh_slide.setEnabled(False)
        self.upper_size_thresh_line.setEnabled(False)
        self.lower_size_thresh_label.setEnabled(False)
        self.lower_size_thresh_slide.setEnabled(False)
        self.lower_size_thresh_line.setEnabled(False)

        #unblur picking filament
        self.picking_label.setEnabled(True)
        self.picking_filament_combox.setEnabled(True)
        self.picking_filament_combox.setCurrentText(PARTICLE) # it sets self.picking_filament = False

        self.unsaved_changes = False

        if self.params:
            for p in self.params.values():
                p.reset_to_default_values()

        self.is_updating_params = False
        self.first_call_use_circle_changed = True
        self.is_loading_boxes = False
        print("Restore the default option")


    def create_tab_visualization(self):
        line_counter = 1
        layout = QtG.QGridLayout()

        # Box size setup
        layout.addWidget(self.boxsize_label, line_counter, 0)
        self.boxsize_line.returnPressed.connect(self.box_size_changed)
        layout.addWidget(self.boxsize_line, line_counter, 1)
        self.button_set_box_size.clicked.connect(self.box_size_changed)
        layout.addWidget(self.button_set_box_size, line_counter, 2)
        line_counter = line_counter + 1

        # Use circle instead of rectangle
        self.use_circle_label.setEnabled(True)
        layout.addWidget(self.use_circle_label, line_counter, 0)
        self.use_circle_combobox.addItems([RECT,CIRCLE])
        self.use_circle_combobox.currentIndexChanged.connect(self.use_circle_changed)
        self.use_circle_combobox.setEnabled(True)
        layout.addWidget(self.use_circle_combobox, line_counter, 1)
        line_counter = line_counter + 1

        # Show estimated size
        self.use_estimated_size_label.setEnabled(False)
        layout.addWidget(self.use_estimated_size_label, line_counter, 0)
        layout.addWidget(self.use_estimated_size_checkbox, line_counter, 1)
        self.use_estimated_size_checkbox.stateChanged.connect(self.use_estimated_size_changed)
        self.use_estimated_size_checkbox.setEnabled(False)
        self.tab_visualization.setLayout(layout)


    def create_tab_thresholding(self):
        line_counter = 1
        layout = QtG.QGridLayout()

        # Lower size
        layout.addWidget(self.lower_size_thresh_label, line_counter, 0)
        self.lower_size_thresh_label.setEnabled(False)
        self.lower_size_thresh_slide.setMinimum(DEFAULT_LOWER_SIZE_THRESH)
        self.lower_size_thresh_slide.setMaximum(500)
        self.lower_size_thresh_slide.setValue(DEFAULT_LOWER_SIZE_THRESH)
        self.lower_size_thresh_slide.valueChanged.connect(
            self.lower_size_thresh_changed
        )
        self.lower_size_thresh_slide.sliderPressed.connect(self.slider_pressed)
        self.lower_size_thresh_slide.sliderReleased.connect(self.changed_slider_release_lower_size_thresh)
        self.lower_size_thresh_slide.setTickPosition(QtG.QSlider.TicksBelow)
        self.lower_size_thresh_slide.setTickInterval(1)
        self.lower_size_thresh_slide.setEnabled(False)
        layout.addWidget(self.lower_size_thresh_slide, line_counter, 1)

        self.lower_size_thresh_line.textChanged.connect(self.lower_size_label_changed)
        self.lower_size_thresh_line.setEnabled(False)
        layout.addWidget(self.lower_size_thresh_line, line_counter, 2)

        line_counter = line_counter + 1

        # Upper size threshold
        layout.addWidget(self.upper_size_thresh_label, line_counter, 0)
        self.upper_size_thresh_label.setEnabled(False)
        self.upper_size_thresh_slide.setMinimum(0)
        self.upper_size_thresh_slide.setMaximum(DEFAULT_UPPER_SIZE_THRESH)
        self.upper_size_thresh_slide.setValue(DEFAULT_UPPER_SIZE_THRESH)
        self.upper_size_thresh_slide.valueChanged.connect(
            self.upper_size_thresh_changed
        )
        self.upper_size_thresh_slide.sliderPressed.connect(self.slider_pressed)
        self.upper_size_thresh_slide.sliderReleased.connect(self.changed_slider_release_upper_size_thresh)
        self.upper_size_thresh_slide.setTickPosition(QtG.QSlider.TicksBelow)
        self.upper_size_thresh_slide.setTickInterval(1)
        self.upper_size_thresh_slide.setEnabled(False)
        layout.addWidget(self.upper_size_thresh_slide, line_counter, 1)
        self.upper_size_thresh_line.textChanged.connect(self.upper_size_label_changed)
        self.upper_size_thresh_line.setEnabled(False)
        layout.addWidget(self.upper_size_thresh_line, line_counter, 2)

        line_counter = line_counter + 1

        # Confidence threshold setup
        layout.addWidget(self.conf_thresh_label, line_counter, 0)
        self.conf_thresh_label.setEnabled(False)
        self.conf_thresh_slide.setMinimum(0)
        self.conf_thresh_slide.setMaximum(100)
        self.conf_thresh_slide.setValue(30)
        self.conf_thresh_slide.valueChanged.connect(self.conf_thresh_changed)
        self.conf_thresh_slide.sliderPressed.connect(self.slider_pressed)
        self.conf_thresh_slide.sliderReleased.connect(self.changed_slider_release_conf_thresh)
        self.conf_thresh_slide.setTickPosition(QtG.QSlider.TicksBelow)
        self.conf_thresh_slide.setTickInterval(1)
        self.conf_thresh_slide.setEnabled(False)
        layout.addWidget(self.conf_thresh_slide, line_counter, 1)
        self.conf_thresh_line.textChanged.connect(self.conf_thresh_label_changed)
        self.conf_thresh_line.setEnabled(False)
        layout.addWidget(self.conf_thresh_line, line_counter, 2)

        line_counter = line_counter + 1

        # number of boxes threshold setup
        layout.addWidget(self.num_boxes_thres_label, line_counter, 0)
        self.num_boxes_thres_label.setEnabled(False)
        self.num_boxes_thresh_slide.setMinimum(DEFAULT_MIN_NUM_BOXES_THRESH)
        self.num_boxes_thresh_slide.setMaximum(DEFAULT_MAX_NUM_BOXES_THRESH)
        self.num_boxes_thresh_slide.setValue(DEFAULT_CURRENT_NUM_BOXES_THRESH)
        self.num_boxes_thresh_slide.valueChanged.connect(self.num_boxes_thresh_changed)
        self.num_boxes_thresh_slide.sliderPressed.connect(self.slider_pressed)
        self.num_boxes_thresh_slide.sliderReleased.connect(self.changed_slider_release_num_boxes_thresh)
        self.num_boxes_thresh_slide.setTickPosition(QtG.QSlider.TicksBelow)
        self.num_boxes_thresh_slide.setTickInterval(1)
        self.num_boxes_thresh_slide.setEnabled(False)
        layout.addWidget(self.num_boxes_thresh_slide, line_counter, 1)
        self.num_boxes_thresh_line.textChanged.connect(self.num_boxes_thresh_label_changed)
        self.num_boxes_thresh_line.setEnabled(False)
        layout.addWidget(self.num_boxes_thresh_line, line_counter, 2)

        self.tab_thresholding.setLayout(layout)


    def create_tab_tracing(self):
        self.tabs.addTab(self.tab_tracing, "Tracing")
        purefilename = self.get_current_purefilename()
        line_counter = 1
        layout = QtG.QGridLayout()

        #run tracing_searchRange
        layout.addWidget(self.search_range_label, line_counter, 0)
        self.search_range_slider.setMinimum(0)
        self.search_range_slider.setMaximum(int(self.smallest_image_dim[purefilename]-1)) # it will be change if we change tomo
        self.search_range_slider.setValue(DEFAULT_SEARCH_RANGE)
        self.search_range_slider.valueChanged.connect(self.searchRange_changed)
        self.search_range_slider.sliderPressed.connect(self.slider_pressed)
        self.search_range_slider.sliderReleased.connect(self.changed_slider_release_searchRange)
        self.search_range_slider.setTickPosition(QtG.QSlider.TicksBelow)
        self.search_range_slider.setTickInterval(1)
        layout.addWidget(self.search_range_slider, line_counter, 1)
        self.search_range_line.textChanged.connect(self.searchRange_label_changed)
        layout.addWidget(self.search_range_line, line_counter, 2)
        line_counter += 1

        #run tracing_memory
        layout.addWidget(self.memory_label, line_counter, 0)
        self.memory_slider.setMinimum(0)
        self.memory_slider.setMaximum(int(self.tot_frames[purefilename]-1))    # it will be change if we change tomo
        self.memory_slider.setValue(DEFAULT_MEMORY)
        self.memory_slider.valueChanged.connect(self.memory_changed)
        self.memory_slider.sliderPressed.connect(self.slider_pressed)
        self.memory_slider.sliderReleased.connect(self.changed_slider_release_memory_changed)
        self.memory_slider.setTickPosition(QtG.QSlider.TicksBelow)
        self.memory_slider.setTickInterval(1)
        layout.addWidget(self.memory_slider, line_counter, 1)
        self.memory_line.textChanged.connect(self.memory_label_changed)
        layout.addWidget(self.memory_line, line_counter, 2)
        line_counter += 1

        #run tracing_min_length
        layout.addWidget(self.min_length_label, line_counter, 0)
        self.min_length_slider.setMinimum(0)
        self.min_length_slider.setMaximum(int(self.tot_frames[purefilename]-1))    # it will be change if we change tomo
        self.min_length_slider.setValue(DEFAULT_MIN_LENGTH)
        self.min_length_slider.valueChanged.connect(self.min_length_changed)
        self.min_length_slider.sliderPressed.connect(self.slider_pressed)
        self.min_length_slider.sliderReleased.connect(self.changed_slider_release_min_length_changed)
        self.min_length_slider.setTickPosition(QtG.QSlider.TicksBelow)
        self.min_length_slider.setTickInterval(1)
        layout.addWidget(self.min_length_slider, line_counter, 1)
        self.min_length_line.textChanged.connect(self.min_length_label_changed)
        layout.addWidget(self.min_length_line, line_counter, 2)
        line_counter += 1

        if self.has_filament:
            layout.addWidget(self.min_width_edge_label, line_counter, 0)
            self.min_width_edge_slider.setMinimum(0)
            self.min_width_edge_slider.setMaximum(100)
            self.min_width_edge_slider.setValue(int(DEFAULT_MIN_WIDTH_EDGE*100))
            self.min_width_edge_slider.valueChanged.connect(self.min_width_edge_changed)
            self.min_width_edge_slider.sliderPressed.connect(self.slider_pressed)
            self.min_width_edge_slider.sliderReleased.connect(self.changed_slider_release_min_width_edge)
            self.min_width_edge_slider.setTickPosition(QtG.QSlider.TicksBelow)
            self.min_width_edge_slider.setTickInterval(1)
            layout.addWidget(self.min_width_edge_slider, line_counter, 1)
            self.min_width_edge_line.textChanged.connect(self.min_width_edge_label_changed)
            layout.addWidget(self.min_width_edge_line, line_counter, 2)
            line_counter += 1

            self.win_size = self.boxsize
            layout.addWidget(self.win_size_label, line_counter, 0)
            self.win_size_line.setText(str(self.win_size))
            self.win_size_slider.setMinimum(0)
            self.win_size_slider.setValue(self.win_size)
            self.min_width_edge_slider.valueChanged.connect(self.win_size_changed)
            self.min_width_edge_slider.sliderPressed.connect(self.slider_pressed)
            self.win_size_slider.sliderReleased.connect(self.changed_slider_release_win_size)
            self.win_size_slider.setTickPosition(QtG.QSlider.TicksBelow)
            self.win_size_slider.setTickInterval(1)
            layout.addWidget(self.win_size_slider, line_counter, 1)
            self.win_size_line.textChanged.connect(self.win_size_label_changed)
            layout.addWidget(self.win_size_line, line_counter, 2)
            line_counter += 1

        # run the 3D preview
        self.preview_label.setEnabled(True)                         # if i set it as local var when i reload a img it will be not aligned. no idea why
        layout.addWidget(self.preview_label, line_counter, 0)
        self.preview_checkbox.stateChanged.connect(self.preview)
        self.preview_checkbox.setEnabled(True)
        layout.addWidget(self.preview_checkbox, line_counter, 1)

        # run the 3D trace
        self.button_trace.clicked.connect(self.trace)
        self.button_trace.setEnabled(True)
        layout.addWidget(self.button_trace, line_counter, 2)

        self.tab_tracing.setLayout(layout)


    def create_tab_filtering(self):
        line_counter = 1
        layout = QtG.QGridLayout()

        #todo: uncomment these lines when the janny option will be implemented
        """
        It is still not implemented and we make it invisibl 
        #run janny
        self.janny_label.setEnabled(True)
        layout.addWidget(self.janny_label, line_counter, 0)
        self.button_janny.clicked.connect(self.janny)
        layout.addWidget(self.button_janny, line_counter, 1)
        line_counter += 1
        """

        # Low pass filter setup
        self.low_pass_filter_label.setEnabled(True)
        layout.addWidget(self.low_pass_filter_label, line_counter, 0)
        layout.addWidget(self.filter_line, line_counter, 1)
        self.button_apply_filter.clicked.connect(self.apply_filter)
        self.button_apply_filter.setEnabled(False)
        layout.addWidget(self.button_apply_filter, line_counter, 2)

        self.tab_filtering.setLayout(layout)


    def blur_while_tracing(self):
        self.num_boxes_thresh_line.setEnabled(False)
        self.memory_line.setEnabled(False)
        self.min_length_line.setEnabled(False)
        self.search_range_line.setEnabled(False)
        self.conf_thresh_line.setEnabled(False)
        self.boxsize_line.setEnabled(False)
        self.filter_line.setEnabled(False)
        self.min_width_edge_line.setEnabled(False)
        self.win_size_line.setEnabled(False)

        self.num_boxes_thres_label.setEnabled(False)
        self.memory_label.setEnabled(False)
        self.min_length_label.setEnabled(False)
        self.search_range_label.setEnabled(False)
        self.conf_thresh_label.setEnabled(False)
        self.boxsize_label.setEnabled(False)
        self.use_estimated_size_label.setEnabled(False)
        self.use_circle_label.setEnabled(False)
        self.janny_label.setEnabled(False)
        self.low_pass_filter_label.setEnabled(False)
        self.min_width_edge_label.setEnabled(False)
        self.win_size_label.setEnabled(False)

        self.num_boxes_thresh_slide.setEnabled(False)
        self.conf_thresh_slide.setEnabled(False)

        self.memory_slider.setEnabled(False)
        self.min_length_slider.setEnabled(False)
        self.search_range_slider.setEnabled(False)
        self.button_set_box_size.setEnabled(False)
        self.button_trace.setEnabled(False)
        self.button_janny.setEnabled(False)
        self.button_apply_filter.setEnabled(False)
        self.min_width_edge_slider.setEnabled(False)
        self.win_size_slider.setEnabled(False)

        self.use_estimated_size_checkbox.setEnabled(False)
        self.use_circle_combobox.setEnabled(False)


    def unblur_after_tracing(self):
        self.num_boxes_thresh_line.setEnabled(True)
        self.memory_line.setEnabled(True)
        self.min_length_line.setEnabled(True)
        self.search_range_line.setEnabled(True)
        self.conf_thresh_line.setEnabled(True)
        self.boxsize_line.setEnabled(True)

        self.num_boxes_thres_label.setEnabled(True)
        self.memory_label.setEnabled(True)
        self.min_length_label.setEnabled(True)
        self.search_range_label.setEnabled(True)
        self.conf_thresh_label.setEnabled(True)
        self.boxsize_label.setEnabled(True)
        self.use_estimated_size_label.setEnabled(True)
        self.use_circle_label.setEnabled(True)
        self.janny_label.setEnabled(True)
        self.low_pass_filter_label.setEnabled(True)
        self.filter_line.setEnabled(True)

        self.num_boxes_thresh_slide.setEnabled(True)
        self.conf_thresh_slide.setEnabled(True)

        self.memory_slider.setEnabled(True)
        self.min_length_slider.setEnabled(True)
        self.search_range_slider.setEnabled(True)
        self.button_set_box_size.setEnabled(True)
        self.button_trace.setEnabled(True)
        self.button_janny.setEnabled(True)
        self.button_apply_filter.setEnabled(True)

        self.use_estimated_size_checkbox.setEnabled(True)
        self.use_circle_combobox.setEnabled(True)

        if self.has_filament:
            self.min_width_edge_line.setEnabled(True)
            self.min_width_edge_slider.setEnabled(True)
            self.min_width_edge_label.setEnabled(True)
            self.win_size_line.setEnabled(True)
            self.win_size_slider.setEnabled(True)
            self.win_size_label.setEnabled(True)

    def load_tomo_params(self,pure_filename):
        """
        reset the param f the given tomo, it is basically used in '_event_image_changed'
        :param pure_filename: name of the tomo
        """
        self.is_loading_max_min_sizes = True
        self.is_updating_params = True
        self.upper_size_thresh = self.params[pure_filename].upper_size_thresh
        self.upper_size_thresh_line.setText(str(self.upper_size_thresh))
        self.lower_size_thresh = self.params[pure_filename].lower_size_thresh
        self.lower_size_thresh_line.setText(str(self.lower_size_thresh))
        self.current_conf_thresh = self.params[pure_filename].conf_thresh
        self.conf_thresh_line.setText(str(self.current_conf_thresh))
        self.current_num_boxes_thresh =self.params[pure_filename].num_boxes_thresh
        self.num_boxes_thresh_line.setText(str(self.current_num_boxes_thresh))
        if self.is_cbox_untraced:
            self.memory = self.params[pure_filename].memory
            self.memory_line.setText(str(self.memory))
            self.search_range = self.params[pure_filename].search_range
            self.search_range_line.setText(str(self.search_range))
            self.min_length = self.params[pure_filename].min_length
            self.min_length_line.setText(str(self.min_length))
            if self.has_filament:
                self.win_size = self.params[pure_filename].win_size
                self.win_size_line.setText(str(self.win_size))
                self.min_width_edge = self.params[pure_filename].min_width_edge
                self.min_width_edge_line.setText(str(self.min_width_edge))
        self.is_updating_params = False

    def fill_params(self,list_files):
        """
        filter_freq, upper_size_thresh, lower_size_thresh, conf_thresh, min_num_boxes_thresh,
                 max_num_boxes_thresh, min_width_edge,
                 search_range, memory, min_length
        """
        for f in list_files:
            self.params.update({f: Params(f, DEFAULT_FILTER_FREQ, DEFAULT_UPPER_SIZE_THRESH, DEFAULT_LOWER_SIZE_THRESH,
                                          DEFAULT_CURRENT_CONF_THRESH, DEFAULT_CURRENT_NUM_BOXES_THRESH,
                                          DEFAULT_MIN_WIDTH_EDGE, DEFAULT_SEARCH_RANGE,
                                          DEFAULT_MEMORY,DEFAULT_MIN_LENGTH,DEFAULT_BOX_SIZE)})

    def get_threshold_params_for_given_tomo(self,name_tomo=None):
        """
        Return the param for the current tomo
        """
        if name_tomo:
            p = self.params[name_tomo]
            return p.conf_thresh, p.upper_size_thresh, p.lower_size_thresh, p.num_boxes_thresh
        return self.current_conf_thresh, self.upper_size_thresh, self.lower_size_thresh, self.current_num_boxes_thresh

    def apply_to_all_the_tomo_question(self,name_param):
        msg = "Do you want to change '"+name_param+"' to all tomographies"
        reply = QtG.QMessageBox.question(self, "Message", msg, QtG.QMessageBox.Yes, QtG.QMessageBox.No)
        return reply

    def get_current_purefilename(self):
        return os.path.splitext(os.path.basename(self.current_image_path))[0] if self.current_image_path else None

    def blur_picking_filament(self):
        # blur picking filament
        self.picking_label.setEnabled(False)
        self.picking_filament_combox.setEnabled(False)

def start_boxmanager(image_dir, box_dir, wildcard, is_tomo_dir):
    app = QtG.QApplication(sys.argv)
    gui = MainWindow(app.font(), images_path=image_dir, boxes_path=box_dir, wildcard=wildcard, is_tomo_dir=is_tomo_dir)
    sys.exit(app.exec_())


def run(args=None):
    args = argparser.parse_args()
    image_dir = args.image_dir
    box_dir = args.box_dir
    wildcard = args.wildcard
    is_tomo_dir=args.is_tomo_dir
    start_boxmanager(image_dir, box_dir, wildcard, is_tomo_dir=is_tomo_dir)


if __name__ == "__main__":
    run()
