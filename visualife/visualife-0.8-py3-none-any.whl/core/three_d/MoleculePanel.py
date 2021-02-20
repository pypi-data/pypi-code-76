from visualife.data import *
from visualife.core.three_d.Svg3DPanel import *
from visualife.core.styles import atom_colors


class MoleculePanel(Svg3DPanel):
    """Represents a panel to display chemical molecules
    """

    def __init__(self, svg_canvas, width=500, height=500):
        super().__init__(svg_canvas, width, height)

    def set_molecule(self, atms, bonds, flag="H", s=40):

        self.scale = s
        """center of mass"""

        suma_x = 0
        suma_y = 0
        suma_z = 0

        for ai in atms:
            suma_x += ai.x
            suma_y += ai.y
            suma_z += ai.z

        self.center_x = suma_x / float(len(atms))
        self.center_y = suma_y / float(len(atms))
        self.center_z = suma_z / float(len(atms))

        for atom in atom_colors.keys():
          self.define_gradient("grad%s" % atom, ["0%", "white", "0.9"], ["100%", "%s" % atom_colors[atom], "1"])

        i = 0
        for ai in atms:
            
            c_x, c_y = ai[0] *self.scale-self.center_x * self.scale, ai[1] *self.scale-self.center_y * self.scale
            c_gradient = "grad%s" % ai.element
            c_r = vdw_atomic_radii[ai.element] * 5
            print("[MoleculePanel] placing atom at", c_x, c_y)
            if flag == "H":
              self.add_vertex(c_x,c_y,ai[2] * self.scale-self.center_z * self.scale)
              
              self.sphere_at("circle"+str(i),i,c_r,fill=atom_colors[ai.element], stroke_width=0, gradient=c_gradient)
              i += 1
            else:
              if ai.element != "H":
                self.add_vertex(c_x,c_y,ai[2] * self.scale-self.center_z * self.scale)
                self.sphere_at("circle"+str(i),i,c_r,fill=atom_colors[ai.element], stroke_width=0, gradient=c_gradient)
                i += 1

        i = 0
        for li in bonds:
            ind1 = li.atom1.id - 1
            ind2 = li.atom2.id - 1

            if int(li.type) >= 2:
                self.line_at("line" + str(i), ind1, ind2, stroke='black', stroke_width='5')
                self.line_at("doubleline" + str(i), ind1, ind2,  stroke='white', stroke_width='2')
            else:
                self.line_at("line" + str(i), ind1, ind2, stroke='black', stroke_width='2')
            i += 1
    

