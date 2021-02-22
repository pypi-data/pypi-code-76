import glob
import sys
import os
import numpy as np
import csv
import re
from cryolo import CoordsIO


def read_eman1_helicon_micrgraph_name(path):
    with open(path, "r") as csvfile:
        csvlines = csvfile.readlines()
        for index, row in enumerate(csvlines):
            if row.startswith("#micrograph"):
                pat = "#micrograph:\s(.+)"
                reexp_res = re.findall(pat,row)
                return reexp_res[0]

def write_coords_file(path, array):
    np.savetxt(path, array, delimiter=" ", fmt="%10.5f")

    '''
    with open(path, "w") as coordsfile:
        boxwriter = csv.writer(
            coordsfile, delimiter=" ", quotechar="|", quoting=csv.QUOTE_NONE
        )

        for row in array:
            boxwriter.writerow([row[0], row[1], row[2]])
    '''


def scale(input_path,
          output_path,
          input_type,
          input_ext,
          scale_factor):
    '''
    This function reads the coordinates in the input_type given the input_type, scales them
    according the scale_factor and write them back into the output_path
    :param input_path:
    :param output_path:
    :param input_type:
    :param input_ext: Input file extension
    :param scale_factor:
    :return:
    '''

    # 1. Read data according input_type.
    # 2. Call respective scale function
    # 3. Write to disk

    os.makedirs(output_path, exist_ok=True)
    if os.path.isfile(input_path):
        files = [input_path]
    else:
        path = os.path.join(os.path.abspath(input_path), "*" + input_ext)
        files = glob.glob(path)

    if input_type == "coords":
        list_of_coords = [np.atleast_2d(np.genfromtxt(pth)) for pth in files]
        list_of_scaled_coords = scale_coords(list_of_coords, scale_factor)
        for file_index, pth in enumerate(files):
            output_file_path = os.path.join(output_path,os.path.basename(pth))
            write_coords_file(output_file_path,list_of_scaled_coords[file_index])

    elif input_type == "fil-seg":
        for pth in files:
            print("Convert", pth)
            filaments_per_file = CoordsIO.read_eman1_helicon(pth)
            mic_name = read_eman1_helicon_micrgraph_name(pth)
            scaled_filaments = scale_filament(filaments_per_file,scale_factor)
            output_file_path = os.path.join(output_path, os.path.basename(pth))
            CoordsIO.write_eman1_helicon(scaled_filaments, output_file_path, mic_name)
    else:
        print("Not yet implemented input type:", input_type)
        sys.exit(0)


def scale_filament(filaments, scale):
    import copy
    scaled_filaments = []
    for fil in filaments:
        sfil = copy.deepcopy(fil)
        for box in sfil.boxes:
            box.x = box.x * scale
            box.y = box.y * scale
            box.h = box.h * scale
            box.w = box.w * scale
        scaled_filaments.append(sfil)
    return scaled_filaments

def scale_coords(list_of_coords, scale):
    #np.atleast_2d(np.genfromtxt(pth))
    scaled = []
    for coords in list_of_coords:
        coords_scaled = coords * scale
        scaled.append(coords_scaled)
    return scaled
    #np.savetxt(os.path.join(os.path.abspath(out_path), os.path.basename(pth)), coords_scaled,
    #           delimiter=" ", fmt="%10.5f")

def scale_fil_seg():
    pass