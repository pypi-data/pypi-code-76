"""
This module contains classes related to :ref:`data visualization and rendering <rendering_intro>`.

**Rendering:**

  * :py:class:`Viewport`

**Rendering engines:**

  * :py:class:`OpenGLRenderer`
  * :py:class:`TachyonRenderer`
  * :py:class:`OSPRayRenderer`

**Data visualization elements:**

  * :py:class:`DataVis` (base class for all visual elements)
  * :py:class:`BondsVis`
  * :py:class:`DislocationVis`
  * :py:class:`ParticlesVis`
  * :py:class:`SimulationCellVis`
  * :py:class:`SurfaceMeshVis`
  * :py:class:`TrajectoryVis`
  * :py:class:`TriangleMeshVis`
  * :py:class:`VectorVis`

**Viewport overlays:**

  * :py:class:`ViewportOverlay` (base class for all overlay types)
  * :py:class:`ColorLegendOverlay`
  * :py:class:`CoordinateTripodOverlay`
  * :py:class:`PythonViewportOverlay`
  * :py:class:`TextLabelOverlay`

"""

# Load the native modules.
from ..plugins.PyScript import (RenderSettings, Viewport, ViewportConfiguration, OpenGLRenderer,
                                CoordinateTripodOverlay, PythonViewportOverlay, TextLabelOverlay,
                                FrameBuffer, ViewportOverlay)

# Load submodules.
from .data_vis import DataVis

import ovito

__all__ = ['RenderSettings', 'Viewport', 'ViewportConfiguration', 'OpenGLRenderer', 'DataVis',
        'CoordinateTripodOverlay', 'PythonViewportOverlay', 'TextLabelOverlay', 'ViewportOverlay']

def _Viewport_render_image(self, size=(640,480), frame=0, filename=None, background=(1.0,1.0,1.0), alpha=False, renderer=None, crop=False):
    """ Renders an image of the viewport's view.

        :param size: A pair of integers specifying the horizontal and vertical dimensions of the output image in pixels.
        :param int frame: The animation frame to render. Numbering starts at 0. See the :py:attr:`FileSource.num_frames <ovito.pipeline.FileSource.num_frames>` property for the number of loaded animation frames.
        :param str filename: The file path under which the rendered image should be saved (optional).
                             Supported output formats are: :file:`.png`, :file:`.jpeg` and :file:`.tiff`.
        :param background: A triplet of RGB values in the range [0,1] specifying the background color of the rendered image.
        :param alpha: This option makes the background transparent so that the rendered image may later be superimposed on a different backdrop.
                      When using this option, make sure to save the image in the PNG format in order to preserve the generated transparency information.
        :param renderer: The rendering engine to use. If set to ``None``, either OpenGL or Tachyon are used,
                         depending on the availablity of OpenGL in the current execution context.
        :param crop: This option cuts away border areas of the rendered image filled with the background color; the resulting image may thus turn out smaller than the requested *size*. 
        :returns: A `QImage <https://doc.qt.io/qtforpython/PySide2/QtGui/QImage.html>`__ object containing the rendered picture.

        **Populating the scene**

        Before rendering an image using this method, you should make sure the three-dimensional contains some
        visible objects. Typically this involves calling the :py:meth:`Pipeline.add_to_scene() <ovito.pipeline.Pipeline.add_to_scene>`
        method on a pipeline to insert its output data into the scene::

           pipeline = import_file('simulation.dump')
           pipeline.add_to_scene()

        **Selecting a rendering engine**

        OVITO supports several different rendering backends for producing pictures of the three-dimensional scene:

            * :py:class:`OpenGLRenderer`
            * :py:class:`TachyonRenderer`
            * :py:class:`OSPRayRenderer`

        Each of these backends exhibits specific parameters that control the image quality and other aspect of the image
        generation process. Typically, you would create an instance of one of these renderer classes, configure it and pass
        it to the :py:meth:`!render_image()` method:

        .. literalinclude:: ../example_snippets/viewport_select_renderer.py
           :lines: 5-

        Note that the :py:class:`OpenGLRenderer` backend may not be available when you are executing the script in a
        headless environment, e.g. on a remote HPC cluster without X display and OpenGL support.

        **Post-processing images**

        If the ``filename`` parameter is omitted, the method does not save the rendered image to disk.
        This gives you the opportunity to paint additional graphics on top before saving the
        `QImage <https://doc.qt.io/qtforpython/PySide2/QtGui/QImage.html>`__ later using its ``save()`` method:

        .. literalinclude:: ../example_snippets/render_to_image.py

        As an alternative to the direct method demonstrated above, you can also make use of a :py:class:`PythonViewportOverlay`
        to paint custom graphics on top of rendered images.
    """
    assert(len(size) == 2 and size[0]>0 and size[1]>0)
    assert(len(background) == 3)
    assert(background[0] >= 0.0 and background[0] <= 1.0)
    assert(background[1] >= 0.0 and background[1] <= 1.0)
    assert(background[2] >= 0.0 and background[2] <= 1.0)
    assert(renderer is None or isinstance(renderer, ovito.plugins.PyScript.SceneRenderer))

    # Rendering is a long-running operation, which is not permitted during viewport rendering or pipeline evaluation.
    # In these situations, the following function call will raise an exception.
    ovito.scene.request_long_operation()

    # Configure an ad-hoc RenderSettings object:
    settings = RenderSettings()
    settings.output_image_width, settings.output_image_height = size
    settings.background_color = background
    settings.generate_alpha = alpha
    if renderer:
        settings.renderer = renderer
    settings.range = RenderSettings.Range.CustomFrame
    settings.custom_frame = int(frame)

    if len(self.dataset.pipelines) == 0:
        print("Warning: The scene to be rendered is empty. Did you forget to add a pipeline to the scene using Pipeline.add_to_scene()?")

    if ovito.gui_mode:
        # Use the frame buffer of the GUI window for rendering.
        fb_window = self.dataset.container.window.frame_buffer_window
        fb = fb_window.create_frame_buffer(settings.output_image_width, settings.output_image_height)
        fb_window.show_and_activate()
    else:
        # Create a temporary offscreen frame buffer.
        fb = FrameBuffer(settings.output_image_width, settings.output_image_height)

    # Invoke the actual image rendering function.
    self.dataset.render_scene(settings, self, fb)

    # Crop away background pixels along the outer edges of the image if requested.
    if crop:
        fb.auto_crop()

    # Get the rendered image.
    img = fb.image

    # Save image to the output file if requested.
    if filename:
        if not img.save(filename):
            raise RuntimeError("Failed to save rendered image to output file '%s'" % filename)

    return img
Viewport.render_image = _Viewport_render_image

def _Viewport_render_anim(self, filename, size=(640,480), fps=10, background=(1.0,1.0,1.0), renderer=None, range=None, every_nth=1):
    """ Renders an animation sequence.

        :param str filename: The filename under which the rendered animation should be saved.
                             Supported video formats are: :file:`.avi`, :file:`.mp4`, :file:`.mov` and :file:`.gif`.
                             Alternatively, an image format may be specified (:file:`.png`, :file:`.jpeg`).
                             In this case, a series of image files will be produced, one for each frame, which
                             may be combined into an animation using an external video encoding tool of your choice.
        :param size: The resolution of the movie in pixels.
        :param fps: The number of frames per second of the encoded movie. This determines the playback speed of the animation.
        :param background: An RGB triplet in the range [0,1] specifying the background color of the rendered movie.
        :param renderer: The rendering engine to use. If none is specified, either OpenGL or Tachyon are used,
                         depending on the availablity of OpenGL in the script execution context.
        :param range: The interval of frames to render, specified in the form ``(from,to)``.
                      Frame numbering starts at 0. If no interval is specified, the entire animation is rendered, i.e.
                      frame 0 through (:py:attr:`FileSource.num_frames <ovito.pipeline.FileSource.num_frames>`-1).
        :param every_nth: Frame skipping interval in case you don't want to render every frame of a very long animation.

        See also the :py:meth:`.render_image` method for a more detailed discussion of some of these parameters.
    """
    assert(len(size) == 2 and size[0]>0 and size[1]>0)
    assert(fps >= 1)
    assert(every_nth >= 1)
    assert(len(background) == 3)
    assert(background[0] >= 0.0 and background[0] <= 1.0)
    assert(background[1] >= 0.0 and background[1] <= 1.0)
    assert(background[2] >= 0.0 and background[2] <= 1.0)
    assert(renderer is None or isinstance(renderer, ovito.plugins.PyScript.SceneRenderer))

    # Rendering is a long-running operation, which is not permitted during viewport rendering or pipeline evaluation.
    # In these situations, the following function call will raise an exception.
    ovito.scene.request_long_operation()

    # Configure a RenderSettings object:
    settings = RenderSettings()
    settings.output_image_width, settings.output_image_height = size
    settings.background_color = background
    settings.output_filename = str(filename)
    settings.save_to_file = True
    settings.frames_per_second = int(fps)
    if renderer:
        settings.renderer = renderer
    settings.every_nth_frame = int(every_nth)
    if range:
        settings.range = RenderSettings.Range.CustomInterval
        settings.custom_range_start, settings.custom_range_end = range
    else:
        settings.range = RenderSettings.Range.Animation

    if len(self.dataset.pipelines) == 0:
        print("Warning: The scene to be rendered is empty. Did you forget to add a pipeline to the scene using Pipeline.add_to_scene()?")

    if ovito.gui_mode:
        # Use the frame buffer of the GUI window for rendering.
        fb_window = self.dataset.container.window.frame_buffer_window
        fb = fb_window.create_frame_buffer(settings.output_image_width, settings.output_image_height)
        fb_window.show_and_activate()
    else:
        # Create a temporary off-screen frame buffer.
        fb = FrameBuffer(settings.output_image_width, settings.output_image_height)

    self.dataset.render_scene(settings, self, fb)
Viewport.render_anim = _Viewport_render_anim

def _Viewport_zoom_all(self, size=(640,480)):
    """ Repositions the viewport camera such that all objects in the scene become completely visible.
        The current orientation (:py:attr:`camera_dir`) of the viewport's camera is maintained but
        the :py:attr:`camera_pos` and :py:attr:`fov` parameters are adjusted by this method.

        :param size: Size in pixels of the image that is going to be renderer from this viewport.
                     This information is used to compute the aspect ratio of the viewport rectangle into which 
                     the visible objects should be fitted. The tuple should match the *size* argument being passed
                     to :py:meth:`render_image`.

        Note that this method uses an axis-aligned bounding box computed at frame 0 of the
        loaded trajectory enclosing all visible objects to position the viewport camera. 
        Make sure to call :py:meth:`Pipeline.add_to_scene() <ovito.pipeline.Pipeline.add_to_scene>` prior
        to this method to insert some visible object(s) to the scene first.
    """
    assert(len(size) == 2 and size[0] > 0 and size[1] > 0)
    aspect_ratio = size[1] / size[0]
    self.zoomToSceneExtents(aspect_ratio)
Viewport.zoom_all = _Viewport_zoom_all

# Implementation of the Viewport.create_widget() method:
def _Viewport_create_widget(self, parent = None):
    """
    Creates a visual widget for displaying the three-dimensional scene in an interactive window.
    It may be used in a Python script to display a simulation dataset on screen and build grapical user interfaces. 
    The method craete an interactive window accepting mouse inputs from the user similar to the viewport windows 
    found in the OVITO desktop application.

    :param parent: An optional Qt widget that should serve as parent of the newly created viewport widget. 
    :returns: A new `QWidget <https://doc.qt.io/qtforpython/PySide2/QtWidgets/QWidget.html>`__ displaying the three-dimenensional scene as seen through the virtual viewport.

    The Qt widget created by this method is linked to this :py:class:`!Viewport` instance. 
    Any changes your Python script makes to the non-visual :py:class:`!Viewport` instance,
    for example setting :py:attr:`camera_pos` or :py:attr:`camera_dir`, will be automatically reflected by the 
    visual viewport widget. Vice versa will mouse interactions by the user with the viewport widget
    automatically lead to changes of the corresponding fields of the :py:class:`!Viewport` instance.

    **Note:** This method has experimental status and is currently available only in the OVITO package for Anaconda.
    It will *not* work when being called from a script running in the :program:`ovitos` interpreter or when using the PyPI/pip 
    OVITO package! Please contact the OVITO developer if you are interested in the broader application of this 
    function.

    The following example program demonstrates the use of the :py:meth:`!create_widget` method. Please see the 
    `Qt for Python <https://doc.qt.io/qtforpython/>`__ documentation for general information on how to build graphical 
    user interfaces with the Qt framework.

    .. literalinclude:: ../example_snippets/viewport_create_widget.py
        :lines: 5-

    """
    import shiboken2 as shiboken
    import PySide2.QtWidgets
    # Note: This method requires a full GUI-enabled build of OVITO. 
    # Thus, it won't work in the stripped-down PyPI/pip OVITO package, which does not include the 
    # GUI modules of OVITO. 
    import ovito.plugins.PyScriptGui 

    assert(parent is None or isinstance(parent, PySide2.QtWidgets.QWidget))
    vpwin_ptr = ovito.plugins.PyScriptGui.ViewportWindow._create(self, 0 if parent is None else shiboken.getCppPointer(parent))
    return shiboken.wrapInstance(vpwin_ptr, PySide2.QtWidgets.QOpenGLWidget)
Viewport.create_widget = _Viewport_create_widget

# Here only for backward compatibility with OVITO 2.9.0:
def _get_RenderSettings_custom_range(self):
    """
    Specifies the range of animation frames to render if :py:attr:`range` is set to ``CustomInterval``.

    :Default: ``(0,100)``
    """
    return (self.custom_range_start, self.custom_range_end)
def _set_RenderSettings_custom_range(self, range):
    if len(range) != 2: raise TypeError("Tuple or list of length two expected.")
    self.custom_range_start = range[0]
    self.custom_range_end = range[1]
RenderSettings.custom_range = property(_get_RenderSettings_custom_range, _set_RenderSettings_custom_range)

# Here only for backward compatibility with OVITO 2.9.0:
def _get_RenderSettings_size(self):
    """
    The size of the image or movie to be generated in pixels.

    :Default: ``(640,480)``
    """
    return (self.output_image_width, self.output_image_height)
def _set_RenderSettings_size(self, size):
    if len(size) != 2: raise TypeError("Tuple or list of length two expected.")
    self.output_image_width = size[0]
    self.output_image_height = size[1]
RenderSettings.size = property(_get_RenderSettings_size, _set_RenderSettings_size)

# Here only for backward compatibility with OVITO 2.9.0:
def _get_RenderSettings_filename(self):
    """
    A string specifying the file path under which the rendered image or movie should be saved.

    :Default: ``None``
    """
    if self.save_to_file and self.output_filename: return self.output_filename
    else: return None
def _set_RenderSettings_filename(self, filename):
    if filename:
        self.output_filename = filename
        self.save_to_file = True
    else:
        self.save_to_file = False
RenderSettings.filename = property(_get_RenderSettings_filename, _set_RenderSettings_filename)

# Implement FrameBuffer.image property (requires conversion to a Shiboken object).
def _get_FrameBuffer_image(self):
    import shiboken2 as shiboken
    import PySide2.QtGui
    img = PySide2.QtGui.QImage(shiboken.wrapInstance(self._image, PySide2.QtGui.QImage))
    return img
FrameBuffer.image = property(_get_FrameBuffer_image)

# Here only for backward compatibility with OVITO 2.9.0:
def _Viewport_render(self, settings = None):
    # Renders an image or movie of the viewport's view.
    #
    #    :param settings: A settings object, which specifies the resolution, background color, output filename etc. of the image to be rendered.
    #                     If ``None``, the global settings are used (given by :py:attr:`DataSet.render_settings <ovito.DataSet.render_settings>`).
    #    :type settings: :py:class:`RenderSettings`
    #    :returns: A `QImage <https://doc.qt.io/qtforpython/PySide2/QtGui/QImage.html>`__ object on success, which contains the rendered picture;
    #              ``None`` if the rendering operation has been canceled by the user.
    if settings is None:
        settings = self.dataset.render_settings
    elif isinstance(settings, dict):
        settings = RenderSettings(settings)
    if len(self.dataset.pipelines) == 0:
        print("Warning: The scene to be rendered is empty. Did you forget to add a pipeline to the scene using Pipeline.add_to_scene()?")
    if ovito.gui_mode:
        # Use the frame buffer of the GUI window for rendering.
        fb_window = self.dataset.container.window.frame_buffer_window
        fb = fb_window.create_frame_buffer(settings.output_image_width, settings.output_image_height)
        fb_window.show_and_activate()
    else:
        # Create a temporary off-screen frame buffer.
        fb = FrameBuffer(settings.size[0], settings.size[1])
    self.dataset.render_scene(settings, self, fb)
    return fb.image
Viewport.render = _Viewport_render

# Here only for backward compatibility with OVITO 2.9.0:
def _ViewportConfiguration__len__(self):
    return len(self.viewports)
ViewportConfiguration.__len__ = _ViewportConfiguration__len__

# Here only for backward compatibility with OVITO 2.9.0:
def _ViewportConfiguration__iter__(self):
    return self.viewports.__iter__()
ViewportConfiguration.__iter__ = _ViewportConfiguration__iter__

# Here only for backward compatibility with OVITO 2.9.0:
def _ViewportConfiguration__getitem__(self, index):
    return self.viewports[index]
ViewportConfiguration.__getitem__ = _ViewportConfiguration__getitem__
