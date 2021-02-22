from cryolo.utils import BoundBox
from cryolo import CoordsIO
from cryoloBM import  helper
from os import path,makedirs, remove as os_remove

try:
    import PyQt4.QtCore as QtCore
except ImportError:
    import PyQt5.QtCore as QtCore

HELICON_SUFFIX ="_HELICON"

def prepare_vars_for_writing(box_dir,file_type, is_3D_tomo,picking_filament):
    d = path.join(box_dir, file_type)
    makedirs(d, exist_ok=True)
    if picking_filament:
        file_ext = ".cbox"
        write_coords_ = CoordsIO.write_cbox_file
        if file_type == "EMAN":
            file_ext = ".box"
            write_coords_ = [CoordsIO.write_eman1_filament_start_end, CoordsIO.write_eman1_helicon]
            makedirs(path.join(box_dir, file_type + HELICON_SUFFIX), exist_ok=True)
        elif file_type == "STAR":
            file_ext = ".star"
            write_coords_ = CoordsIO.write_star_filemant_file
        return file_ext, write_coords_

    file_ext = ".box"
    write_coords_ = CoordsIO.write_eman1_boxfile if is_3D_tomo is False else  CoordsIO.write_eman_boxfile3d

    if file_type == "STAR":
        file_ext = ".star"
        write_coords_ = CoordsIO.write_star_file
    elif file_type in ["CBOX", "CBOX_3D", "EMAN_3D", "CBOX_REFINED"]:
        file_ext = ".cbox"
        write_coords_ = CoordsIO.write_cbox_file
    return file_ext, write_coords_


def write_coordinates(pd, box_dictionary, empty_slice, ignored_slice,fname, box_dir, is_3D_tomo, file_ext, is_cbox, current_conf_thresh, upper_size_thresh,lower_size_thresh,boxsize,write_coords_, picking_filament):
    # only in a 3D tomo image we have to delete an existing file before starting to write the new one.
    # Basically because we write in append mode on a file the selected particles slice after slice
    overwrite = True
    box_file_path = None
    num_writtin_part = 0
    counter = 0
    slice_index = None
    boxes = []
    for filename, rectangles in box_dictionary.items():

        if pd.wasCanceled():
            break
        else:
            pd.show()
            val = int((counter + 1) * 100 / len(box_dictionary.items()))
            pd.setValue(val)
        QtCore.QCoreApplication.instance().processEvents()

        if is_3D_tomo is True:
            slice_index = int(filename)
            filename = fname

        box_filename = filename + file_ext
        box_file_path = path.join(box_dir, box_filename)

        if overwrite is True:
            overwrite = False
            if is_3D_tomo is True and path.isfile(box_file_path) is True:
                os_remove(box_file_path)
        if picking_filament is False:
            if is_cbox:
                rectangles = [
                    box for box in rectangles if
                    helper.check_if_should_be_visible(box, current_conf_thresh, upper_size_thresh,lower_size_thresh)
                ]
                # if self.use_estimated_size_checkbox.isChecked():
            if is_3D_tomo:
                real_rects = [rect.getSketch(circle=False) for rect in rectangles]
            else:
                real_rects = [rect.getSketch(circle=False) for rect in rectangles]
                 # todo: why i m doing the resize only for SPA? Anyway the code works properly
                for rect in real_rects:
                    helper.resize_box(rect, boxsize)

            num_writtin_part = num_writtin_part + len(real_rects)

            from cryolo.utils import BoundBox
            for rect_index, rect in enumerate(real_rects):
                x_lowerleft = int(rect.get_x())
                y_lowerleft = int(rect.get_y())
                boxize = int(rect.get_width())
                confidence = 1
                if rectangles[rect_index].get_confidence() is not None:
                    confidence = rectangles[rect_index].get_confidence()
                box = BoundBox(x=x_lowerleft, y=y_lowerleft, w=boxize, h=boxize, z=slice_index, c=confidence, depth=1)
                box.meta.update({'num_boxes':rectangles[rect_index].num_boxes})
                boxes.append(box)

        else:
            num_writtin_part = num_writtin_part + len(rectangles)
            boxes += rectangles

        counter = counter + 1
        if is_3D_tomo is False:
            if "write_eman1_filament_start_end" in str(write_coords_):
                write_coords_(boxes,box_file_path)
            elif "write_eman1_helicon" in str(write_coords_):
                write_coords_(boxes, box_file_path,filename)
            else:
                write_coords_(box_file_path, boxes)
            boxes = []

    if box_file_path and is_3D_tomo is True:
        print("Write", box_file_path)
        if is_cbox:
            write_coords_(box_file_path, boxes, empty_slice, ignored_slice)
        else:
            write_coords_(box_file_path, boxes)

    if picking_filament:
        print(num_writtin_part, "filaments written in '" + file_ext + "' file.")
    else:
        print(num_writtin_part, "particles written in '" + file_ext + "' file.")



def write_coordinates_3d_folder(pd, box_dictionary, empty_slice, ignored_slice, is_folder_3D_tomo, is_cbox, current_conf_thresh, upper_size_thresh, lower_size_thresh, boxsize, write_coords_, file_ext, box_dir, picking_filament):
    num_writtin_part = 0

    for filename in box_dictionary.keys():
        counter = 0
        overwrite = True
        boxes = []
        for index, rectangles in box_dictionary[filename].items():

            if pd.wasCanceled():
                break
            else:
                pd.show()
                val = int((counter + 1) * 100 / len(box_dictionary[filename].items()))
                pd.setValue(val)
            QtCore.QCoreApplication.instance().processEvents()

            box_filename = filename + file_ext
            box_file_path = path.join(box_dir, box_filename)

            if overwrite is True:
                overwrite = False
                if is_folder_3D_tomo is True and path.isfile(box_file_path) is True:
                    os_remove(box_file_path)
            if picking_filament is False:
                if is_cbox:
                    rectangles = [
                        box for box in rectangles if
                        helper.check_if_should_be_visible(box, current_conf_thresh, upper_size_thresh,lower_size_thresh)
                    ]
                    # if self.use_estimated_size_checkbox.isChecked():
                real_rects = [rect.getSketch(circle=False) for rect in rectangles]
                for rect in real_rects:
                    helper.resize_box(rect, boxsize)
                num_writtin_part = num_writtin_part + len(real_rects)


                for rect_index, rect in enumerate(real_rects):
                    confidence = 1
                    if rectangles[rect_index].get_confidence() is not None:
                        confidence = rectangles[rect_index].get_confidence()
                    x_lowerleft = int(rect.get_x())
                    y_lowerleft = int(rect.get_y())
                    boxize = int(rect.get_width())
                    box = BoundBox(x=x_lowerleft, y=y_lowerleft, w=boxize, h=boxize, c=confidence, depth=1)
                    box.z = index
                    boxes.append(box)
            else:
                num_writtin_part = num_writtin_part + len(rectangles)
                boxes += rectangles

            if is_cbox:
                write_coords_(box_file_path, boxes, empty_slice[filename], ignored_slice[filename])
            else:
                write_coords_(box_file_path, boxes)

            counter = counter + 1
    if picking_filament:
        print(num_writtin_part, "filaments written in '" + file_ext + "' file.")
    else:
        print(num_writtin_part, "particles written in '" + file_ext + "' file.")


def prepare_output(slices, input_box_dict, is_folder_3D_tomo):
    """
    Select the data for writing on  file
    :param slices: list of slices to save
    :param input_box_dict: box dictionary containing the selected sketches (i.e.: self.box_dictionary)
    :param is_folder_3D_tomo
    :return The smaller boxes, those created for 3D visualization will be ignored.
            box_dict: box_dict format with slice containing boxes in 'self.box_dictionary' format. (dict of dict in case 3D folder)
            slice_ignored: list of slice with boxes but their checkbox are unchecked  (dict of list in case 3D folder)
            slice_empty: list of slice without boxes but their checkbox are checked (dict of list in case 3D folder)
    """
    box_dict = dict()
    slice_ignored = dict() if is_folder_3D_tomo else list()
    slice_empty = dict() if is_folder_3D_tomo else list()

    if is_folder_3D_tomo:
        for f_name, slices_f_name in slices.items():
            # I insert the f_name even in slice_ignored and slice_empty because they could not  be in self.box_dictionary
            box_dict.update({f_name: dict()})
            slice_ignored.update({f_name: list()})
            slice_empty.update({f_name: list()})
            for index in slices_f_name:
                if f_name in input_box_dict.keys() and index in input_box_dict[f_name]:
                    box_dict[f_name].update({index: input_box_dict[f_name][index]})

        box_dict = helper.create_restore_box_dict(box_dict, is_folder_3D_tomo)
        for f_name, slices_f_name in helper.create_restore_box_dict(input_box_dict, is_folder_3D_tomo).items():
            if not box_dict[f_name].keys():  # case we ignore the whole tomo
                slice_ignored[f_name] = list(input_box_dict[f_name].keys())
                continue
            for index in slices_f_name:
                if index not in box_dict[f_name].keys():
                    slice_ignored[f_name].append(index)

        for f_name, slices_f_name in slices.items():
            for index in slices_f_name:
                if index not in input_box_dict[f_name].keys():
                    slice_empty[f_name].append(index)
    else:
        for index in slices:
            if index in input_box_dict.keys():
                box_dict.update({index: input_box_dict[index]})

        box_dict = helper.create_restore_box_dict(box_dict, is_folder_3D_tomo)
        for index in helper.create_restore_box_dict(input_box_dict, is_folder_3D_tomo):
            if index not in slices:
                slice_ignored.append(index)

        for index in slices:
            if index not in box_dict.keys():
                slice_empty.append(index)

    return box_dict, slice_ignored, slice_empty