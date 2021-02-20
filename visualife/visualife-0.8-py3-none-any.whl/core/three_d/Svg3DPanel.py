from math import pi, cos, sin, sqrt
from visualife.core.HtmlViewport import HtmlViewport
from visualife.core.styles import get_color, mix_colors_by_hex
from browser import document


class Sphere:
    """Represents a sphere for Svg3DPanel
    """

    def __init__(self, id, vertex, r, **kwargs):
        self.id = id
        self.v = vertex
        self.r = r
        self.params = kwargs


class SpheresGroup:
    def __init__(self, id, vertices, radii, **kwargs):
        """Represents a group of spheres for Svg3DPanel
        """
        self.id = id
        self.v = vertices
        self.r = radii
        self.params = kwargs

    @property
    def vertices(self):
        """A list of vertex indexes of this group of spheres"""
        return self.v

    @property
    def y(self):
        """A list of Y coordinates for all vertices of this group of spheres"""
        return [vi[1] + self.__offset_y for vi in self.v]


class Line:
    """Represents a line for Svg3DPanel
    """

    def __init__(self, id, vb, ve, **kwargs):
        self.id = id
        self.vb = vb
        self.ve = ve
        self.params = kwargs


class Face:
    """Represents a face for Svg3DPanel
    """

    def __init__(self, id, verts, **kwargs):
        self.id = id
        self.vertices = verts
        self.params = kwargs

    def average_z(self):
        """ Calculates average Z coordinate of this Face object
        :return: average Z
        """
        z = 0
        for vi in self.vertices: z += vi[2]

        return z / len(self.vertices)


class Svg3DPanel:
    """Represents a panel for displaying 3D objects
    """

    def __init__(self, svg_canvas, width, height):
        self.__alpha = 0
        self.__beta = 0
        self.__width = width
        self.__height = height
        self.__is_dragged = False
        self.__vertices = []
        self.__spheres = []
        self.__sphere_groups = []
        self.__faces = []           # Contains Face objects
        self.__lines = []
        self.__gradients = []
        self.__drawing = HtmlViewport(svg_canvas, 0, 0, width, height)  # This values must match the size of the SVG element!!!
        self.__drawing.clear()
        self.__scale = 1
        self.__offset_x = width/2   # Center of the SVG element: this should be half of SVG box size
        self.__offset_y = height/2  # Center of the SVG element: this should be half of SVG box size
        self.__center_x = 0         # Center of rotation : X
        self.__center_y = 0         # Center of rotation : Y
        self.__center_z = 0         # Center of rotation : Z
        self.__prev_rotation_x = 0  # X coordinate from the most recent rotation - to check the direction
        self.__prev_rotation_y = 0  # Y coordinate from the most recent rotation - to check the direction
        # four elements used to construct rotation matrices: sin(alpha), cos(alpha), sin(beta), cos(beta)
        self.__light =  self.normalize([0.5, -0.2, -2])
        self.__ambient_light = 0.1
        self.__z_order = False

    @property
    def offset_x(self):
        """ Center of the SVG element: this should be half of SVG box size"""
        return self.__offset_x

    @property
    def offset_y(self):
        """ Center of the SVG element: this should be half of SVG box size"""
        return self.__offset_y

    @offset_x.setter
    def offset_x(self, x):
        self.__offset_x = x

    @offset_y.setter
    def offset_y(self, y):
        self.__offset_y = y

    @property
    def center_x(self):
        """ Center of rotation : X"""
        return self.__center_x

    @property
    def center_y(self):
        """ Center of rotation : Y"""
        return self.__center_y

    @property
    def center_z(self):
        """ Center of rotation : Z"""
        return self.__center_z

    @property
    def drawing(self):
        """Viewport for this object"""
        return self.__drawing

    @property
    def scale(self):
        """Returns current scale"""
        return self.__scale

    @property
    def z_order(self):
        return self.__z_order

    @z_order.setter
    def z_order(self, flag):
        self.__z_order = flag

    def clear(self):
        """Clears whole scene"""
        self.__drawing.clear()
        self.__vertices.clear()
        self.__spheres.clear()
        self.__faces.clear()
        self.__lines.clear()

    def count_vertices(self):
        """Count the current number of vertics"""
        return len(self.__vertices)

    def count_spheres(self):
        """Count the current number of speres"""
        return len(self.__spheres)

    def count_faces(self):
        """Count the current number of faces"""
        return len(self.__faces)

    def count_lines(self):
        """Count the current number of lines"""
        return len(self.__lines)

    def add_vertex(self, x, y, z):
        """Adds a vertex to the scene"""
        self.__vertices.append( [x, y, z] )
        return len(self.__vertices) - 1

    def sphere_at(self, id, v_index, r, **kwargs):
        """Adds sphere in the position of vertex given by index"""
        self.__spheres.append( Sphere(id, self.__vertices[v_index], r, **kwargs) )
        
    def add_sphere(self, id, x, y, z, r, **kwargs):
        """Adds sphere at (x,y,z) and also adds a vertex with this coordinates"""
        i = self.add_vertex(x, y, z)
        self.sphere_at(id, i, r, **kwargs)
        return i

    def append_spheres_group(self, spheres_group):
        """Adds spheres group to the scene"""
        self.__sphere_groups.append(spheres_group)

    def line_at(self, id, vb_index, ve_index, **kwargs):
        """Adds line from vertex with index vb_index to vertex with index ve_index """
        self.__lines.append( Line(id, self.__vertices[vb_index], self.__vertices[ve_index], **kwargs) )

    def face_at(self, id, points, **kwargs):
        """Adds face defined by the list of vertices' ids"""
        verts = []
        for i in points: verts.append(self.__vertices[i])
        self.__faces.append( Face(id, verts,  **kwargs) )

    def rotate_vertices(self):
        """Rotates a vertix with current alpha and beta values """

        __sa = sin(self.__alpha)
        __ca = cos(self.__alpha)
        __sb = sin(self.__beta)
        __cb = cos(self.__beta)
        for v in self.__vertices:

            x_przed = v[0] - self.__center_x
            y_przed = v[1] - self.__center_y
            z_przed = v[2] - self.__center_z

            """Wokół X"""
            y_po = (y_przed * __cb - z_przed * __sb)
            z = (y_przed * __sb + z_przed * __cb)

            """Wokół Y"""
            x_po = (z * __sa + x_przed * __ca)
            z_po = (z * __ca - x_przed * __sa)

            """Dodajemy z powrotem odjęte wartości, zapis punktów po"""
            v[0] = x_po + self.__center_x
            v[1] = y_po + self.__center_y
            v[2] = z_po + self.__center_z

    @staticmethod
    def subtract_vectors(vi, vj):
        """Substruct vi-vj """
        return [vi[0] - vj[0], vi[1] - vj[1], vi[2] - vj[2]]

    @staticmethod
    def length(v):
        """Calculates length of vector"""
        return sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2])

    @staticmethod
    def normalize(v):
        """Normalize vector - it will have length 1"""
        ll = Svg3DPanel.length(v)
        v[0] /= ll
        v[1] /= ll
        v[2] /= ll
        return v

    @staticmethod
    def plane_normal(verts):
        v1 = Svg3DPanel.subtract_vectors(verts[0], verts[1])
        v2 = Svg3DPanel.subtract_vectors(verts[0], verts[2])

        return [v1[1] * v2[2] - v1[2] * v2[1], v1[2] * v2[0] - v1[0] * v2[2], v1[0] * v2[1] - v1[1] * v2[0]]

    @staticmethod
    def dot_product(vi, vj):
        """Calculates dot product"""
        return vi[0]*vj[0] + vi[1]*vj[1] + vi[2]*vj[2]

    def define_gradient(self, id, stop1, stop2):
        """Adds gradient to gradiens list"""
        self.__gradients.append([id, stop1, stop2])

    def draw(self):
        """Draws all elements in the scene"""

        self.rotate_vertices()
        self.__drawing.clear()

        # ---------- Draw gradients
        for g in self.__gradients:
            self.__drawing.radial_gradient(g[0],g[1],g[2])

        # ---------- Draw faces: make a deep copy to apply Z-buffering
        if self.__z_order:
            faces_copy = []
            for f in self.__faces: faces_copy.append((f.average_z(), f))
            faces_copy.sort(key=lambda x: x[0])
            fc = [f[1] for f in faces_copy]
        else:
            fc = self.__faces

        black = str(get_color("black"))
        for f in fc:
            fnorm = self.normalize(self.plane_normal(f.vertices))
            if fnorm[2] > 0: continue
            dp = Svg3DPanel.dot_product(self.__light, fnorm)

            light_fraction = self.__ambient_light + (1 - self.__ambient_light) * max(0, dp)
            clr = f.params.get('fill', '#0000ff')
            if clr[0] != '#': clr = str(get_color(clr))

            fill = mix_colors_by_hex(clr, light_fraction, black)
            for v in f.vertices :
                v[0] += self.__offset_x
                v[1] = -v[1] + self.__offset_y
            self.__drawing.polygon(f.id, f.vertices, fill=fill, stroke='white', stroke_width=1)
            for v in f.vertices :
                v[0] -= self.__offset_x
                v[1] = -v[1] + self.__offset_y

        # Draw lines
        for l in self.__lines:
            vb = l.vb
            ve = l.ve
            self.__drawing.line(l.id, vb[0] + self.__offset_x, -vb[1] +  self.__offset_y, ve[0] + self.__offset_x, -ve[1] +  self.__offset_y, **l.params)

        # Draw spheres as circles
        for c in self.__spheres:
            cc = c.v
            self.__drawing.circle(c.id, cc[0] + self.__offset_x, -cc[1] +  self.__offset_y, c.r, **c.params)

        # Draw spheres as circles
        for g in self.__sphere_groups:
            x, y = [], []
            for vi in g.v:
                x.append(self.__vertices[vi][0] + self.__offset_x)
                y.append(self.__vertices[vi][1] + self.__offset_y)

            self.__drawing.circles_group(g.id, x, y, "black", g.r)

        # Draw the square events will be bound to
        self.__drawing.rect("drag-element", 0, 0,  self.__width, self.__height,
                            style="""fill:white; opacity:0.0; stroke_width:0;""")

        # finalize the drawing. This actually sends the above SVG to a browser
        self.__drawing.close()
        document['drag-element'].bind("mousedown", self.start_drag)
        document['drag-element'].bind("mouseup", self.end_drag)
        document['drag-element'].bind("mousemove", self.drag)

        #document.bind("keydown", self.key_pressed)

    def start_drag(self, evt):
        """ Function called when "mousedown" event is recorded; drag is started at that moment

        @param evt: event object passed by a web browser
        """
        self.__prev_rotation_x = evt.x
        self.__prev_rotation_y = evt.y
        self.__is_dragged = True

    def drag(self, evt):
        """ Performs the actual drag action

        @param evt: event object passed by a web browser; mouse coordinates are extracted from it
        """

        if not self.__is_dragged: return
        """Kąty"""

        self.__alpha = (evt.x - self.__prev_rotation_x) / 100
        self.__beta = (evt.y - self.__prev_rotation_y) / 100
        self.__prev_rotation_x = evt.x
        self.__prev_rotation_y = evt.y

        self.draw()

    def end_drag(self, evt):
        """ Function called when "mouseup" event is recorded; drag is stopped at that moment

        @param evt: event object passed by a web browser
        """
        self.__is_dragged = False

    def key_pressed(self, evt):
        """Rotates elements in the scene after pressing arrows keys"""
        if evt.keyCode == "LEFT" : self.__beta += 0.1
        elif evt.keyCode == "RIGHT" : self.__beta -= 0.1
        elif evt.keyCode == "UP": self.__alpha += 0.1
        elif evt.keyCode == "DOWN": self.__alpha -= 0.1
        self.draw()

