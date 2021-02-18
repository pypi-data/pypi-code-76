#!/usr/bin/env python

from AaronTools.geometry import Geometry

geom = Geometry("test.xyz")

geom.detect_components()

for comp in geom.components:
    if any(atom.element == "P" for atom in comp.atoms):
        print(comp.cone_angle(center=geom.center))
