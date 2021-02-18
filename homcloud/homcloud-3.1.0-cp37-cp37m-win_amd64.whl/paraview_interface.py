"""
This module provides the paraview interface from homcloud.interface module.

The basic model of this module is "pipeline" model. A data object is
filtered by the chain of pipeline nodes, and the result is shown.
The objects of :class:`PipelineNode` correspond the node of the pipeline,
and you can adjust visualization by these objects.

You can use many methods of :class:`PipelineNode` to adjust the visualization,
and you can construct a new pipeline node by the following methods:

* :meth:`PipelineNode.threshold`
* :meth:`PipelineNode.clip_sphere`

Todo:

* Add clip_box method

"""
import numbers
import sys
from tempfile import NamedTemporaryFile
import os

import numpy as np
from forwardable import forwardable

import homcloud.utils as utils
import homcloud.pict.pict3d_vtk as pict3d_vtk
from homcloud.visualize_3d import ParaViewPolyLineDrawer


@forwardable()
class TempFile(object):
    def __init__(self, suffix):
        self.named_tempfile = NamedTemporaryFile("w+", suffix=suffix, delete=False)
        self.cleanup_done = False

    def_delegators("named_tempfile", "name, close, write")

    def cleanup(self):
        self.close()
        if not self.cleanup_done:
            os.unlink(self.name)
            self.cleanup_done = True

    def __del__(self):
        self.cleanup()

    # NOTE: __enter__ and __exit__ are not implemented since
    # in this module with statement is used to the class


class PipelineNode(object):
    """This class represents elements in a pipeline in ParaView.

    This class is the base class for paraview interface classes.
    You should not create an instance of this class directly.
    """

    def __init__(self, parent=None):
        self.index = new_index()
        self.parent = parent
        self._representation = None
        self.opacity = None
        self.color = None
        self.color_field = None
        self.colorbar_range = None
        self.pointsize = None
        self.linewidth = None

    def variable(self):
        return "s" + str(self.index)

    def to_paraview_node(self):
        """Returns self.
        """
        return self

    def representation(self):
        if self._representation:
            return self._representation
        if self.parent is None:
            return False
        return self.parent.representation()

    def write_code(self, out, already_written, isleaf):
        if self.variable() in already_written:
            return
        already_written.add(self.variable())
        if self.parent:
            self.parent.write_code(out, already_written, False)
        self.write_constructor(out)
        if isleaf:
            out.write("Show({})\n".format(self.variable()))
        self.write_specialized_code(out, already_written)
        if isleaf:
            self.write_displayproperty_code(out, already_written)

    def write_displayproperty_code(self, out, already_written):
        out.write("dp = GetDisplayProperties({})\n".format(self.variable()))
        if self.representation():
            out.write("dp.Representation = '{}'\n".format(self.representation()))
        if self.opacity is not None:
            out.write("dp.Opacity = {}\n".format(self.opacity))
        if self.pointsize is not None:
            out.write("dp.PointSize = {}\n".format(self.pointsize))
        if self.color_field is not None:
            self.write_color_filed(out)
        if self.color is not None:
            out.write("dp.AmbientColor = ({}, {}, {})\n".format(*self.color))
            out.write("dp.DiffuseColor = ({}, {}, {})\n".format(*self.color))
            out.write("dp.ColorArrayName = [dp.ColorArrayName[0], r'']\n")
        if self.linewidth is not None:
            out.write("dp.LineWidth = {}\n".format(self.linewidth))

    def write_color_filed(self, out):
        if self.colorbar_range is None:
            out.write(
                "dp.LookupTable = MakeBlueToRedLT(*{}."
                "{}[r'{}'].GetRange())\n".format(
                    self.variable(), self.data_attr_name(), self.color_field
                )
            )
        else:
            out.write("dp.LookupTable = MakeBlueToRedLT({}, {})\n".format(
                *self.colorbar_range
            ))
        out.write("dp.ColorArrayName = [r'{}', r'{}']\n".format(
            self.color_array_type(), self.color_field
        ))

    def write_specialized_code(self, out, already_written):
        pass

    def threshold(self, field, range):
        """
        Create a new pipeline node for thresholding whose parent
        is `self`.

        Only the elements whose `field` are in the `range` when
        the returned object is passed to :meth:`show`.

        Args:
            field (string): The name of the field which have the
                thresholded value.
            range (tuple[float, float] or float): The upper and lower bounds
                of the values.
                If an float number is given, the threshold is (range, range).

        Returns:
            Threshold: A new PipelineNode object for thresholding.

        """
        if isinstance(range, numbers.Number):
            range = (range, range)
        return Threshold(self, field, range)

    def clip_sphere(self, center, radius, inside_out=True):
        """
        Create a new pipeline node to clip the object with a
        sphere shape.

        Args:
            center (tuple[float, float, float]): The center of the
                clipping sphere
            radius (float): The radius of the clipping sphere
            inside_out (bool): If True, only the elements
                *in* the shpere are shown.
                If False, only the elements *outside* of the sphere is
                shown.

        Returns:
            SphereClip: A new PipelineNode object for sphere clipping.

        """
        return SphereClip(self, center, radius, inside_out)

    def color_by(self, field, range=None):
        """
        Set the coloring by field name.

        Args:
            field (string or int): The name of the field.
            range (tuple[float, float] or None): The upper and lower bounds
                of the colorbar. If None, the minimal and maximal values
                of the field are used.
        Returns:
            self
        """
        if isinstance(field, int):
            field = "Field {}".format(field)
        self.color_field = field
        self.colorbar_range = range
        return self

    def data_attr_name(self):
        return self.parent.data_attr_name()

    def color_array_type(self):
        return self.parent.color_array_type()

    def set_opacity(self, opacity):
        """
        Set the opacity.

        * 0.0 - completely transparent
        * 1.0 - completely opaque

        Args:
            opacity (float): The opacity.

        Returns:
            self
        """
        self.opacity = opacity
        return self

    def set_color(self, color):
        """
        Set the color.

        Args:
            color (tuple[float, float, float]): The RGB values (0.0 to 1.0)

        Returns:
            self
        """
        self.color = color
        return self

    def set_pointsize(self, size):
        """
        Set the pointsize.

        Args:
            pointsize (float): The size of the points

        Returns:
            self
        """
        self.pointsize = size
        return self

    def set_representation(self, rep):
        if rep not in ["Wireframe", "Points", "Surface", "Surface With Edges"]:
            raise(ValueError(
                "Representation {} is not acceptable".format(rep)
            ))
        self._representation = rep
        return self

    def set_linewidth(self, width):
        """
        Set the linewidth.

        Args:
            width (float): The width of the lines

        Returns:
            self
        """
        self.linewidth = width
        return self

    def debug_print(self):
        write_python_code(sys.stdout, [self])
        return self

    def cleanup(self):
        if self.parent:
            self.parent.cleanup()


class VTK(PipelineNode):
    """
    This class represents a VTK data source in paraview.
    """

    def __init__(self, path, gui_name=None, file=None):
        super().__init__()
        self.path = path
        self.gui_name = gui_name if gui_name is not None else path
        self.file = file

    def cleanup(self):
        if self.file:
            self.file.cleanup()

    def write_constructor(self, out):
        out.write("{} = LegacyVTKReader(FileNames=r'{}',"
                  " guiName=r'{}')\n".format(
                      self.variable(), self.path, self.gui_name
                  ))

    def data_attr_name(self):
        return "CellData"

    def color_array_type(self):
        return "CELLS"


class XMLVTI(PipelineNode):
    """
    This class represents a VTI data source in XML format in paraview.
    """

    def __init__(self, path, gui_name, file=None):
        super().__init__()
        self.path = path
        self.gui_name = gui_name if gui_name is not None else path
        self.file = file
        self._representation = "Surface"
        self.color_field = "value"

    def cleanup(self):
        if self.file:
            self.file.cleanup()

    def write_constructor(self, out):
        out.write("{} = XMLImageDataReader(FileName=r'{}', "
                  "guiName=r'{}')\n".format(
                      self.variable(), self.path, self.gui_name
                  ))

    def data_attr_name(self):
        return "CellData"

    def color_array_type(self):
        return "CELLS"


def VoxelData(array, gui_name=None, offsets=[0, 0, 0]):
    """
    Returns :class:`PipelineNode` object representing a voxel data.

    Args:
        array (numpy.ndarray): An array.
        gui_name (string or None): The name shown in Pipeline Browser
            in paraview's GUI.

    Returns:
        VTK: A pipeline node object
    """
    f = TempFile(".vti")
    pict3d_vtk.write_vti_xmlfile(f, array, offsets)
    f.close()
    return XMLVTI(f.name, gui_name, f)


def PolyLine(array, gui_name=None):
    """
    Returns :class:`PipelineNode` object representing a polyline.

    Args:
        array (numpy.ndarray): An array of points.
        gui_name (string or None): The name shown in Pipeline Browser
            in paraview's GUI.

    Returns:
        VTK: A pipeline node object
    """
    f = TempFile(".vtk")
    drawer = ParaViewPolyLineDrawer(2, array, {})
    drawer.write(f)
    f.close()
    return VTK(f.name, gui_name, f).set_representation("Wireframe")


class PointCloud(PipelineNode):
    """
    This class represents a pointcloud data source in paraview.

    Args:
        path (string): The filepath of the pointcloud.
        dim (int): The dimension of the space in which the pointcloud lives.
        delimiter (string): The delimiter of elements in a pointcloud file.
           If you want to show a CSV file, please specify ",".
        gui_name (string or None): The name shown in Pipeline Browser
            in paraview's GUI.

    Notes:
       This is constructed by CSVReader and TableToPoints.
    """

    def __init__(self, path, dim=3, delimiters=" ", gui_name=None, file=None):
        super().__init__()
        self.path = path
        self.dim = dim
        self.delimiters = delimiters
        self.gui_name = gui_name or self.path
        self.file = file
        assert dim in [2, 3]

    def cleanup(self):
        if self.file:
            self.file.cleanup()

    @staticmethod
    def from_array(array, dim=3, gui_name=None):
        """
        Construct a pipeline node for pointcloud from an ndarray object.

        Args:
            array (nupmy.ndarray): The pointcloud data.
            dim (int): The dimension of the space in which the
                pointcloud lives.
            gui_name (string): The name shown in Pipeline Browser in paraview's
                GUI.

        Returns:
            PointCloud: A pipeline node object.
        """
        f = TempFile(".txt")
        np.savetxt(f, array)
        f.close()
        return PointCloud(f.name, dim, " ", gui_name, f)

    def representation(self):
        return "Points"

    def write_constructor(self, out):
        def quote(s):
            return s.translate({
                "\t": "\\t", "\n": "\\n",
            })

        out.write(
            "s = CSVReader(FileName=r'{}', FieldDelimiterCharacters='{}',"
            " guiName=r'{}', HaveHeaders=0)\n".format(
                self.path, quote(self.delimiters), self.gui_name
            ))

        out.write(self.table_to_points_template().format(self.variable()))

    def table_to_points_template(self):
        if self.dim == 3:
            return "{} = TableToPoints(s, XColumn='Field 0', YColumn='Field 1', ZColumn='Field 2')\n"
        elif self.dim == 2:
            return "{} = TableToPoints(s, XColumn='Field 0', YColumn='Field 1', ZColumn='Field 0', a2DPoints=1)\n"

    def data_attr_name(self):
        return "PointData"

    def color_array_type(self):
        return "POINTS"


class Threshold(PipelineNode):
    """
    This class represents a pipeline node for thresholding.

    You should construct the instance of this class by
    :meth:`PipelineNode.threshold`.
    """

    def __init__(self, parent, field, range):
        super().__init__(parent)
        self.field = field
        self.range = range

    def write_constructor(self, out):
        out.write("{} = Threshold({})\n".format(self.variable(),
                                                self.parent.variable()))

    def write_specialized_code(self, out, already_written):
        out.write("{}.Scalars = ['CELLS', r'{}']\n".format(
            self.variable(), self.field
        ))
        out.write("{}.ThresholdRange = ({}, {})\n".format(
            self.variable(), self.range[0], self.range[1]
        ))


class SphereClip(PipelineNode):
    """
    This class represents a pipeline node for sphere clipping.

    You should construct the instance of this class
    by :meth:`PipelineNode.clip_sphere`.
    """

    def __init__(self, parent, center, radius, inside_out=True):
        super().__init__(parent)
        self.center = center
        self.radius = radius
        self.inside_out = inside_out

    def write_constructor(self, out):
        out.write("{} = Clip({}, InsideOut={}, ClipType='Sphere')\n".format(
            self.variable(), self.parent.variable(), int(self.inside_out),
        ))

    def write_specialized_code(self, out, already_written):
        out.write("{}.ClipType.Center = [{}, {}, {}]\n".format(
            self.variable(), *self.center
        ))
        out.write("{}.ClipType.Radius = {}\n".format(
            self.variable(), self.radius
        ))


def write_python_code(out, sources):
    """
    Write a python code generated by `sources` to `out`.

    Args:
        out (io-like): The output IO object.
        sources (list of PipelineNode): Pipeline nodes to be output.
    """
    already_written = set()
    out.write("from paraview.simple import *\n")
    for source in sources:
        source.write_code(out, already_written, True)

    out.write("Render()\n")


def show(sources, path=None, wait=True):
    """
    Shows `sources` by invoking paraview.

    Args:
        sources (list of PipelineNode): Pipeline nodes to be output.
        path (string or None): The output filename. If this parameter
            is None, a temporary filepath is generated and use it.
        wait (bool): If True, this function returns after paraview stops.
            If False, this function returns immediately after
            paraview is invoked by using backgroup process mechanism.
    """
    f = open(path, "w") if path else TempFile(".py")
    nodes = [s.to_paraview_node() for s in sources]
    write_python_code(f, nodes)
    f.close()
    # sp.run(["cmd.exe", "/k", "type", path])

    def finalize():
        if isinstance(f, TempFile):
            f.cleanup()
        for node in nodes:
            node.cleanup()

    utils.invoke_paraview("--script={}".format(f.name), wait=wait, finalize=finalize)


current_index = 0


def new_index():
    global current_index
    current_index += 1
    return current_index
