import tempfile
import os
import unittest.mock
import shutil
import sys
import re

import numpy as np
from scipy.spatial import distance_matrix

import homcloud.interface as hc
import homcloud.paraview_interface as pv
import homcloud.utils as utils
import homcloud.pict.pict3d_vtk as pict3d_vtk
from homcloud.version import __version__

import matplotlib

matplotlib.rcParams['backend'] = "Agg"

import matplotlib.pyplot as plt  # NOQA


def self_check(args):
    print_version()
    self_check_alpha_shape_3()
    self_check_alpha_shape_3_with_weight()
    self_check_alpha_shape_3_periodic_with_weight()
    self_check_alpha_shape_2()
    self_check_grayscale_2D_bitmap()
    self_check_binary_2D_bitmap()
    self_check_binary_periodic_2D_bitmap()
    self_check_rips()
    if "--no-dipha" not in args:
        self_check_rips_maxvalue()
    self_check_plot_pd()
    self_check_optimal_volume()
    if "--no-paraview" not in args:
        self_check_paraview()


def print_version():
    print('HomCloud version: {}'.format(__version__))
    print('Python version: {}'.format(re.sub(r'[\r\n]', ' ', sys.version)))


def self_check_alpha_shape_3():
    print('Alpha Shape 3 ... ', end='')
    pc = np.random.uniform(0, 1.0, (100, 3))
    hc.PDList.from_alpha_filtration(pc)
    print("ok")


def self_check_alpha_shape_3_with_weight():
    print('Alpha Shape 3 with weights ... ', end='')
    pc = np.random.uniform(0, 1.0, (100, 3))
    weight = np.random.uniform(0.001, 0.05, 100)
    hc.PDList.from_alpha_filtration(pc, weight=weight)
    print('ok')


def self_check_alpha_shape_3_periodic_with_weight():
    print('Periodic Alpha Shape 3 with weights ... ', end='')
    pc = np.random.uniform(0, 1, (200, 3))
    weight = np.random.uniform(0.001, 0.05, 200)
    hc.PDList.from_alpha_filtration(
        pc, weight=weight, periodicity=[(0, 1), (0, 1), (0, 1)]
    )
    print('ok')


def self_check_alpha_shape_2():
    print('Alpha Shape 2 ... ', end='')
    pc = np.random.uniform(0, 1.0, (100, 2))
    hc.PDList.from_alpha_filtration(pc)
    print("ok")


def self_check_grayscale_2D_bitmap():
    print('Grayscale 2D bitmap ... ', end='')
    bitmap = np.random.uniform(0, 1.0, (128, 128))
    hc.PDList.from_bitmap_levelset(bitmap)
    print('ok')


def self_check_binary_2D_bitmap():
    print('Binary 2D bitmap ... ', end='')
    bitmap = np.random.uniform(0, 1.0, (128, 128))
    hc.PDList.from_bitmap_levelset(hc.distance_transform(bitmap < 0.2, True, "manhattan"))
    print('ok')


def self_check_binary_periodic_2D_bitmap():
    print('Binary 2D periodic bitmap ... ', end='')
    bitmap = np.random.uniform(0, 1.0, (128, 128))
    hc.PDList.from_bitmap_levelset(
        hc.distance_transform(bitmap < 0.2, True, "manhattan", (True, True))
    )
    print('ok')


def self_check_rips():
    print('Rips filtration ... ', end='')
    pc = np.random.uniform(0, 1.0, (64, 128))
    dmatrix = distance_matrix(pc, pc)
    hc.PDList.from_rips_filtration(dmatrix, maxdim=2)
    print('ok')


def self_check_rips_maxvalue():
    print('Rips filtration with maxvalue ... ', end='')
    pc = np.random.uniform(0, 1.0, (64, 128))
    dmatrix = distance_matrix(pc, pc)
    hc.PDList.from_rips_filtration(dmatrix, maxdim=2, maxvalue=0.01)
    print('ok')


def self_check_plot_pd():
    print('Plotting PD ... ', end='')
    pc = np.random.uniform(0, 1.0, (100, 3))
    pdlist = hc.PDList.from_alpha_filtration(pc)
    with tempfile.TemporaryDirectory() as tmpdir:
        for d in [0, 1, 2]:
            plt.clf()
            pdlist.dth_diagram(d).histogram().plot(colorbar={"type": "log"})
            plt.savefig(os.path.join(tmpdir, "PD.png"))
    plt.clf()
    print('ok')


def self_check_optimal_volume():
    print('Optimal Volume ... ', end='')
    pc = np.array([[0.0, 0.0, 0.0],
                   [8.0, 0.0, 0.0],
                   [5.0, 6.0, 0.0],
                   [4.0, 2.0, 6.0]])
    pdlist = hc.PDList.from_alpha_filtration(pc, save_boundary_map=True)
    pdlist[1].nearest_pair_to(16, 19).optimal_volume()
    pdlist[2].nearest_pair_to(19.6, 21).optimal_volume()
    print('ok')


def self_check_paraview():
    print('Paraview path: {0} ({1})'.format(utils.paraview_programname(),
                                            shutil.which(utils.paraview_programname())))
    print('Paraview fake invoke ... ', end='')
    with unittest.mock.patch('subprocess.check_call'):
        with unittest.mock.patch('subprocess.Popen'):
            utils.invoke_paraview("foo.vtk", wait=False)
            utils.invoke_paraview("foo.vtk", wait=True)
    print('ok')

    print('Paraview real invoke (VTK voxel) => Click "Apply" button and close opened window ... ', end='')
    sys.stdout.flush()

    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "voxel.vtk")
        with open(path, "w") as f:
            pict3d_vtk.write_vtk_file(f, "Voxel data",
                                      np.random.uniform(size=(10, 10, 10)))
        utils.invoke_paraview(path, wait=True)
    print('ok')

    print('Paraview real invoke (python pointcloud) => Close opened window ... ', end='')
    sys.stdout.flush()
    pv.show([
        pv.PointCloud.from_array(np.random.uniform(size=(100, 3))),
        pv.PointCloud.from_array(np.random.uniform(size=(100, 3))).set_color((1, 0, 0)),
    ], wait=True)
    print('ok')


if __name__ == '__main__':
    self_check(sys.argv[1:])
