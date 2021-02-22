from os import listdir,path
from mrcfile import mmap as mrcfile_mmap        #it is not in the setup.py because it is already installed by cryolo
import numpy as np
from cryoloBM import MySketch
from cryolo import imagereader
from math import isnan
def get_all_loaded_filesnames(root):
    """
    get the list of the loaded file
    :param root: QtG.QTreeWidget obj
    :return: list of filenames
    """
    child_count = root.childCount()
    filenames = []
    for i in range(child_count):
        item = root.child(i)
        filename = path.splitext(item.text(0))[0]
        filenames.append(filename)
    return filenames

def resize_box(rect, new_size):
    """
    resize a 'matplotlib.patches.Rectangle' obj
    :param rect: a 'matplotlib.patches.Rectangle' obj
    :param new_size: new width and height
    :return: None
    """
    if isinstance(rect,MySketch.MyCircle) and rect.get_radius() != new_size:
        rect.set_radius = new_size
    elif isinstance(rect,MySketch.MyRectangle) and (rect.get_width() != new_size or rect.get_height() != new_size):
        height_diff = new_size - rect.get_height()
        width_diff = new_size - rect.get_width()
        newy = rect.get_y() - height_diff / 2
        newx = rect.get_x() - width_diff / 2
        rect.set_height(new_size)
        rect.set_width(new_size)
        rect.set_xy((newx, newy))


def get_only_files(dir_path,wildcard,is_list_tomo):
    """
    generate list of files in 'dir_path' path
    :param dir_path: path to the folder
    :param wildcard: using wildcard
    :param is_list_tomo: True if folder of 3D tomo
    :return: list of valid files in 'dir_path'
    """
    onlyfiles = [
        f
        for f in sorted(listdir(dir_path))
        if path.isfile(path.join(dir_path, f))
    ]

    if wildcard:
        import fnmatch
        onlyfiles = [
            f
            for f in sorted(listdir(dir_path))
            if fnmatch.fnmatch(f, wildcard)
        ]

    if is_list_tomo is False:
        onlyfiles = [
            i
            for i in onlyfiles
            if not i.startswith(".")
               and i.endswith((".jpg", ".jpeg", ".png", ".mrc", ".mrcs", ".tif", ".tiff", ".rec"))]
    else:
        onlyfiles_all = [i for i in onlyfiles if not i.startswith(".") and i.endswith((".mrc", ".mrcs",".rec"))]
        onlyfiles.clear()
        for f in onlyfiles_all:
            with mrcfile_mmap(path.join(dir_path, f), permissive=True, mode="r") as mrc:
                if len(mrc.data.shape) == 3:
                    onlyfiles.append(f)
                mrc.close()

    return onlyfiles


def filter_tuple_is_equal(a,b):
    return a[0]==b[0] and a[1]==b[1] and a[2] == b[2]


def is_helicon_with_particle_coords(path_f):
    with open(path_f) as f:
        first_line = f.readline()
        f.close()
    return "#micrograph" in first_line


def is_eman1_helicion(path_f):
    try:
        box_lines = np.atleast_2d(np.genfromtxt(path_f))
        if len(box_lines) < 2:
            return False
        return (
                len(box_lines[0]) == 5
                and box_lines[0][4] == -1
                and box_lines[1][4] == -2
        )
    except ValueError:
        return False


def getEquidistantRectangles(x_start, y_start, x_end, y_end, width, parts, edgecolor,is_circle = False, is_3d_tomo =False):
    #todo: to test it in real case situation ... e.g.: make sense num_boxes = 100?
    points = zip(
        np.linspace(x_start, x_end, parts + 1, endpoint=False),
        np.linspace(y_start, y_end, parts + 1, endpoint=False),
    )
    new_rectangles = []

    for point in points:
        sketch = MySketch.MySketch(xy =(point[0], point[1]), width=width, height=width, is_3d_tomo=is_3d_tomo,
                                 angle=0.0, est_size=None, confidence=1, only_3D_visualization=False,
                                 num_boxes=100, meta=None, z=None,
                                 linewidth=1, edgecolor=edgecolor, facecolor="none")
        new_rectangles.append(sketch)
    return new_rectangles


def get_file_type(file_path):
    im_type = None
    if file_path.endswith(("jpg", "jpeg", "png")):
        im_type = 0
    if file_path.endswith(("tif", "tiff")):
        im_type = 1
    if file_path.endswith(("mrc", "mrcs","rec")):
        im_type = 2
    return im_type


def read_image(file_path, use_mmap=False):
    im_type = get_file_type(file_path)

    img = imagereader.image_read(file_path, use_mmap=use_mmap)
    img = normalize_and_flip(img, im_type)
    return img

def normalize_and_flip(img, file_type):
    if file_type == 0:
        # JPG
        img = np.flip(img, 0)
    if file_type == 1 or file_type == 2:
        # tif /mrc
        if not np.issubdtype(img.dtype, np.float32):
            img = img.astype(np.float32)
        if len(img.shape) == 3:
            img = np.flip(img, 1)
        else:
            img = np.flip(img, 0)
        mean = np.mean(img)
        sd = np.std(img)
        img = (img - mean) / sd
        img[img > 3] = 3
        img[img < -3] = -3
    return img


def get_number_visible_boxes( rectangles):
    i = 0
    for box in rectangles:
        if box.is_figure_set():
            i = i + 1
    return i

def get_corresponding_box(x, y, rectangles, current_conf_thresh, box_size, get_low=False):
    a = np.array([x, y])

    for box in rectangles:
        b = np.array(box.get_xy())
        dist = np.linalg.norm(a - b)
        if get_low:
            if dist < box_size / 2 and box.get_confidence() < current_conf_thresh:
                return box
        else:
            if dist < box_size / 2 and box.get_confidence() > current_conf_thresh:
                return box
    return None

def check_if_should_be_visible( box, current_conf_thresh, upper_size_thresh, lower_size_thresh, num_boxes_thresh = 0, is_filament = True):
    #todo: change it in the 'GUI_feature' next febr2021

    # Cryolo returns estimated value = NaN for the filament mode. hence in these case we filter only in according with its num_boxes and confidence thresholding
    est_size = upper_size_thresh if is_filament else box.get_est_size()
    if isnan(est_size) :
        return True
    return box.get_confidence() > current_conf_thresh and upper_size_thresh >= est_size >= lower_size_thresh and box.num_boxes > num_boxes_thresh


def resize(boxes_in_dict, new_size):
    """
    Convert a list of boxes
    :param boxes_in_dict: list of MySketch obj
    :param new_size: the new size (radius if circle, height and width otherwise)
    :return False if there is nothing to convert
    """
    for b in boxes_in_dict:
        b.resize(new_size)



def resize_3d_filament(boxes_in_dict, factor):
    """
    Workaround for resizing the filament
    Convert a list of boxes
    :param boxes_in_dict: list of MySketch obj
    :param factor: reduction factor. e.g: old size=10 new=20 factor is 2
    :return False if there is nothing to convert
    """
    for b in boxes_in_dict:
        new_size = b.getSketch(circle=False).get_width()
        b.resize(int(new_size*factor))

def create_deep_copy_box_dict(d,is_tomo_folder = False, as_Bbox = False):
    """
    Since we cannot deepcopy 'self.box_dictionary' we have to duplicate it
    :param d: the self.box_dictionary
    :param is_tomo_folder: True if it is a folder of tomos
    :param as_Bbox: If true convert the sketches in cryolo BoundingBox
    :return the copy of the dict, if as_Bbox is True the sketches are cryolo BBox
    """

    if is_tomo_folder:
        out = {k: dict() for k in d.keys()}
        for k,d_in in d.items():
            for k2 in d[k].keys():
                out[k].update({k2:list()})
            for k_in,v_in in  d_in.items():
                for b in v_in:
                    sketch = MySketch.MySketch(xy=b.get_xy(), width=b.get_width(), height=b.get_height(),
                                      is_3d_tomo=b.get_is_3d_tomo(), angle=b.get_angle(), est_size=b.get_est_size(),
                                      confidence=b.get_confidence(), only_3D_visualization=b.only_3D_visualization,
                                      num_boxes=b.num_boxes, meta=b.meta, z=b.z,
                                      linewidth=1, edgecolor=b.getSketch().get_edgecolor(), facecolor="none")
                    if as_Bbox:
                        out[k][k_in].append(sketch.get_as_BBox(sketch.get_confidence(), k_in))
                    else:
                        out[k][k_in].append(sketch)
    else:
        out ={k:list() for k in d.keys()}
        for k,v in d.items():
            for b in v:
                sketch = MySketch.MySketch(xy=b.get_xy(), width=b.get_width(), height=b.get_height(),
                                           is_3d_tomo=b.get_is_3d_tomo(), angle=b.get_angle(),
                                           est_size=b.get_est_size(),
                                           confidence=b.get_confidence(), only_3D_visualization=b.only_3D_visualization,
                                           num_boxes=b.num_boxes, meta=b.meta, z=b.z,
                                           linewidth=1, edgecolor=b.getSketch().get_edgecolor(), facecolor="none")
                if as_Bbox:
                    out[k].append(sketch.get_as_BBox(sketch.get_confidence(), k))
                else:
                    out[k].append(sketch)

    return out



def create_restore_box_dict(d,is_tomo_folder = False, conf_thr = 0, as_Bbox = False):
    """
    Since we cannot deepcopy 'self.box_dictionary' we have to duplicate it
    :param d: the self.box_dictionary
    :param is_tomo_folder: True if it is a folder of tomos
    :param conf_thr: confidence threshold. All the boxes with higher confidence will be returned (for cbox manipulation)
    :param as_Bbox: If true convert the sketches in cryolo BoundingBox
    :return the copy of the dict, if as_Bbox is True the sketches are cryolo BBox
    """

    if is_tomo_folder:
        out = {k: dict() for k in d.keys()}
        for k,d_in in d.items():
            for k2 in d[k].keys():
                out[k].update({k2:list()})
            for k_in,v_in in  d_in.items():
                for b in v_in:
                    if b.only_3D_visualization is False and b.get_confidence() > conf_thr:
                        sketch = MySketch.MySketch(xy=b.get_xy(), width=b.get_width(), height=b.get_height(),
                                                   is_3d_tomo=b.get_is_3d_tomo(), angle=b.get_angle(),
                                                   est_size=b.get_est_size(),
                                                   confidence=b.get_confidence(),
                                                   only_3D_visualization=b.only_3D_visualization,
                                                   num_boxes=b.num_boxes, meta=b.meta, z=b.z,
                                                   linewidth=1, edgecolor=b.getSketch().get_edgecolor(),
                                                   facecolor="none")
                        if as_Bbox:
                            out[k][k_in].append(sketch.get_as_BBox(sketch.get_confidence(), k_in))
                        else:
                            out[k][k_in].append(sketch)
    else:
        out ={k:list() for k in d.keys()}
        for k,v in d.items():
            for b in v:
                if b.only_3D_visualization is False and b.get_confidence() > conf_thr:
                    sketch = MySketch.MySketch(xy=b.get_xy(), width=b.get_width(), height=b.get_height(),
                                      is_3d_tomo=b.get_is_3d_tomo(), angle=b.get_angle(), est_size=b.get_est_size(),
                                      confidence=b.get_confidence(), only_3D_visualization=b.only_3D_visualization,
                                      num_boxes=b.num_boxes, meta=b.meta, z=b.z,
                                      linewidth=1, edgecolor=b.getSketch().get_edgecolor(), facecolor="none")
                    if as_Bbox:
                        out[k].append(sketch.get_as_BBox(sketch.get_confidence(), k))
                    else:
                        out[k].append(sketch)

    return out


def convert_list_bbox_to_dict_sketch(boxes_list, col ='r'):
    """
    Convert the list of Bbox (see 'cryolo.grouping3d.do_tracing' for the syntax), in a dict of sketches
    :param boxes_list: list of BoundingBox instances
    :param col: color of the edge
    :return dict of sketches (k = frame number, v = list of sketches)
    """
    box_dict = dict()
    num_boxes = 1
    for b in boxes_list:
        if 'num_boxes' in b.meta:
            num_boxes = b.meta["num_boxes"]
        x = b.x
        y = b.y
        #todo: in the future it could be necessary change something (e.g.:'est_size = b.w')
        sketch = MySketch.MySketch(xy=(x,y), width=b.w, height=b.h,
                                   is_3d_tomo=True, angle=0.0, est_size=b.w,
                                   confidence=b.c, only_3D_visualization=False,
                                   num_boxes=num_boxes, meta=None, z=None,
                                   linewidth=1, edgecolor=col, facecolor="none")
        if b.z in box_dict:
            box_dict[int(b.z)].append(sketch)
        else:
            box_dict[int(b.z)] = [sketch]


    return box_dict

def unfold_filament(list_filament):
    """
    Used during the import from cbox files
    After loading we have a list of filament obj that is basically a list of list Bbox obj
    This function create a single list of Bbox.
    """
    boxes = list()
    for count,f in enumerate(list_filament):
        for b in f.boxes:
            b.meta.update({'_filamentid':count})
            boxes.append(b)
    return boxes

def is_cbox_untraced(b):
    """
    :param b: loaded box of a cbox file
    return False True if the file is cobx_untraced
    """

    # micrograph case has always b.depth == None and crYOLO will never spawn a untraced file for micrograph case
    if b.depth is not None and isnan(b.depth) is False:
        return int(b.depth) == 1
    return False


def create_sketch(box, delta, size,est_box_from_cbox):
    # because if the data are loaded from .cbox the est_size must not be changed
    est_size = est_box_from_cbox if est_box_from_cbox is not None else box.get_width()
    xy = box.get_xy(circle = False)
    return MySketch.MySketch(xy=(xy[0] + delta, xy[1] + delta), width=size, height=size, is_3d_tomo=box.get_is_3d_tomo(),
                             angle=box.get_angle(), est_size=est_size, confidence=box.get_confidence(),
                             only_3D_visualization=True, num_boxes=box.num_boxes, meta=None, z=None,
                             linewidth=1, edgecolor=box.getSketch().get_edgecolor(), facecolor="none")