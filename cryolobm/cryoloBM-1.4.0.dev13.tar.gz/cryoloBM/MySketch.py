from matplotlib.patches import  Rectangle,Circle
from cryolo import utils

class MySketch:
    def __init__(self, xy=None, width=None, height=None, is_3d_tomo=False, angle=0.0, est_size=None, confidence=None, only_3D_visualization= False, num_boxes = 1, meta = None, z= None, **kwargs):
        """
        :param xy: tuple representing the bottom and left rectangle coordinates. In according with matplotlib.patches.py class Rectangle
        :param width: of the rect
        :param height: of the rect
        :param is_3d_tomo: True if the sketch will belong to a tomography
        :param angle: rotation in degrees anti-clockwise about *xy* (default is 0.0). In according with matplotlib.patches.py class Rectangle
        :param est_size: size estimated by crYOLO ( .cbox cases)
        :param confidence: confidence value estimated by crYOLO
        :param only_3D_visualization: If true this box is not a real box picked or detected by crYOLO but it is created in the 3D visualization feature
        :param num_boxes: number of boxes of the 3D particle (CBOX_3D file). in case of 2D it has value 1
        :param meta: meta data values of a Bbox instance
        :param z: slice in tomography

        NB:
        in case of particle a rectangle will be a square --> box_size = height = width (hence radius = width/2)
        In case of filament it will be NOT A SQUARE, we have to decide how manage some stuff BUT the radius = It would be size perpendicular to the filament
        """


        self.only_3D_visualization=only_3D_visualization
        self.meta = meta

        #it is the number of boxes of the 3D particle (CBOX_3D file). in case of 2D it has value 1
        # NB:
        #   the 'current_num_boxes_thresh' is set 0 for default, that means that in helper.check_if_should_be_visible
        #   2D particle (hence whose in the untraced_cbox files too) will be always visible when check 'box.num_boxes > num_boxes_thresh'
        self.num_boxes = num_boxes

        """
        Value used , together with meta["_filamentid"]for the filament tracking
        z = index tomo
        """
        self.z = z

        self.sketch_circle = MyCircle( xy=(xy[0]+width/2,xy[1]+width/2), radius=int(width / 2), is_3d_tomo = is_3d_tomo, est_size=est_size, confidence = confidence, **kwargs)
        self.sketch_rect = MyRectangle( xy=xy, width=width, height=height, is_3d_tomo = is_3d_tomo , angle=angle, est_size=est_size, confidence = confidence,  **kwargs)

    def get_as_BBox(self, confidence = None, z = None):
        """
        convert the sketch in a cryolo Bounding box and return it
        :param confidence: confidence value. 1 if the bbox will pass to cryolo.grouping3d.do_tracing
        :param z: slice of the 3D tomo, None otherwise
        return: a BBox
        """

        """
            NB:
                The x,y of a BBox are the center of the box
                The x,y of a circle_sketch are the center of the circle
                The x,y of a rect_sketch are the bottom and left rectangle coordinates
        """
        w = self.get_width()

        #The bbox are rectangles hence i need the x,y values of the rectangles sketch.
        xy = self.get_xy(circle=False)

        #depth is always 1 even in the tomo because the box are on a slice, hence in 2D hence depth=1
        b= utils.BoundBox(x=xy[0], y=xy[1], w=w, h=w, c=confidence, classes=["particle"], z=z, depth=1)
        meta = (w,w)
        if self.meta is not None and "est_box_size" in self.meta:
            meta = self.meta["est_box_size"]
        b.meta = {"boxsize_estimated": meta}       # i need it in the 'cryolo.grouping3d.convert_traces_to_bounding_boxes'
        return b

    def resize(self, new_size):
        confidence = self.get_confidence()
        is_3d_tomo =self.get_is_3d_tomo()
        color = self.getSketch().get_edgecolor()

        """est_size contained the estimated size of cryolo, when loaded from '.cbox' and should be never changed"""
        est_size = self.get_est_size()

        self.remove_instances()

        self.sketch_circle = MyCircle(xy=self.get_xy(circle=True), radius=new_size/2, is_3d_tomo=is_3d_tomo, est_size=est_size,
                                   confidence=confidence, linewidth=1, edgecolor=color, facecolor="none")

        xy = self.get_xy(circle=False)
        x = xy[0] + (self.get_width()-new_size)/2
        y = xy[1] + (self.get_width()-new_size)/2
        self.sketch_rect = MyRectangle(xy=(x,y), width=new_size, height=new_size, is_3d_tomo=is_3d_tomo,
                                      angle=self.get_angle(),est_size=est_size, confidence=confidence,
                                      linewidth=1, edgecolor=color, facecolor="none")
        self.createSketches()  # create the new instances

    def remove_instances(self):
        """
        Remove the instances of the sketches
        """
        self.sketch_circle.remove_istance()
        self.sketch_rect.remove_istance()

    def createSketches(self):
        """
        Create the instances of the sketches
        """
        self.getSketch(circle =True)
        self.getSketch(circle =False)

    def getSketch(self, circle = False):
        """
        Return an matplotlib instance of my sketch
        """
        if circle:
            return self.sketch_circle.getSketch()
        return self.sketch_rect.getSketch()

    def set_Sketches_visible(self,visible=True):
        self.getSketch(circle=True).set_visible(visible)
        self.getSketch(circle=False).set_visible(visible)

    def set_xy(self, xy, circle = False):
        if circle:
            self.sketch_circle.xy = xy
        else:
            self.sketch_rect.xy = xy

    def set_radius(self, radius):
        self.sketch_circle.radius = radius

    def set_width(self, width):
        self.sketch_rect.width = width

    def set_height(self, height):
        self.sketch_rect.height = height

    def set_is_3d_tomo(self, is_3d_tomo):
        self.sketch_rect.is_3d_tomo = is_3d_tomo
        self.sketch_circle.is_3d_tomo = is_3d_tomo

    def set_angle(self, angle):
        self.sketch_rect.angle = angle

    def set_est_size(self, est_size):
        self.sketch_rect.est_size = est_size
        self.sketch_circle.est_size = est_size

    def set_confidence(self, confidence):
        self.sketch_rect.confidence = confidence
        self.sketch_circle.confidence = confidence

    def get_xy(self, circle = False):
        if circle:
            return self.sketch_circle.xy
        return self.sketch_rect.xy

    def get_radius(self):
        return self.sketch_circle.radius

    def get_width(self):
        return self.sketch_rect.width

    def get_height(self):
        return self.sketch_rect.height

    def get_is_3d_tomo(self):
        return self.sketch_rect.is_3d_tomo

    def get_angle(self):
        return self.sketch_rect.angle

    def get_est_size(self, circle = False):
        if circle:
            return self.sketch_circle.est_size
        return self.sketch_rect.est_size

    def get_confidence(self):
        return self.sketch_rect.confidence



class MyCircle:
    def __init__(self, xy, radius, is_3d_tomo = False, est_size=None, confidence = None, **kwargs):
        self.confidence = confidence
        self.est_size = est_size
        self.is_3d_tomo = is_3d_tomo
        self.xy = xy
        self.radius = radius
        self.circleInstance = None
        self.kwargs = kwargs

    def getSketch(self):
        if self.circleInstance is None:
            self.circleInstance = Circle(xy=self.xy, radius=self.radius, **self.kwargs)
        return self.circleInstance

    def remove_istance(self):
        self.circleInstance = None


class MyRectangle:
    def __init__(self, xy, width, height, is_3d_tomo = False,  angle=0.0, est_size=None, confidence = None,  **kwargs):
        self.confidence = confidence
        self.est_size = est_size
        self.is_3d_tomo = is_3d_tomo
        self.xy = xy
        self.width = width
        self.height = height
        self.angle = angle
        self.rectInstance = None
        self.kwargs = kwargs

    def getSketch(self):
        if self.rectInstance is None:
            self.rectInstance = Rectangle(self.xy, self.width, self.height, self.angle, **self.kwargs)
        return self.rectInstance

    def remove_istance(self):
        self.rectInstance = None