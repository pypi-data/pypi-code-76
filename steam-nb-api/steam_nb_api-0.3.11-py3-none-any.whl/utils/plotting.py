from py4j.java_gateway import launch_gateway, java_import, JavaGateway, JavaObject, GatewayParameters, Py4JNetworkError

# Launch a Gateway in a new Java process, this returns port
port = launch_gateway(classpath='../steam/*')

# JavaGateway instance is connected to a Gateway instance on the Java side
gateway = JavaGateway(gateway_parameters=GatewayParameters(port=port))

import matplotlib.lines as lines
import matplotlib.patches as patches
import numpy as np

Point = gateway.jvm.model.geometry.basic.Point
Line = gateway.jvm.model.geometry.basic.Line
Arc = gateway.jvm.model.geometry.basic.Arc
Circumference = gateway.jvm.model.geometry.basic.Circumference
Area = gateway.jvm.model.geometry.basic.Area
HyperLine = gateway.jvm.model.geometry.basic.HyperLine
Element = gateway.jvm.model.geometry.Element
Domain = gateway.jvm.model.domains.Domain
AirDomain = gateway.jvm.model.domains.database.AirDomain
AirFarFieldDomain = gateway.jvm.model.domains.database.AirFarFieldDomain
IronDomain = gateway.jvm.model.domains.database.IronDomain
HoleDomain = gateway.jvm.model.domains.database.HoleDomain
CoilDomain = gateway.jvm.model.domains.database.CoilDomain
MatDatabase = gateway.jvm.model.materials.database.MatDatabase
ConfigSigma = gateway.jvm.config.ConfigSigma
TxtSigmaServer = gateway.jvm.server.TxtSigmaServer
MagnetMPHBuilder = gateway.jvm.comsol.MagnetMPHBuilder
Cable = gateway.jvm.model.geometry.coil.Cable
Winding = gateway.jvm.model.geometry.coil.Winding
Pole = gateway.jvm.model.geometry.coil.Pole
Coil = gateway.jvm.model.geometry.coil.Coil

def plot_multiple_areas(ax, areas):
    for area in areas:
        plot_area(ax, area)

def plot_area(ax, area):
    hls = area.getHyperLines()
    for hl in hls:
        last_dot_index = hl.toString().rfind('.')
        at_index = hl.toString().find('@')
        class_name = hl.toString()[last_dot_index+1:at_index]
        if class_name =='Line':
            ax.add_line(lines.Line2D([hl.getKp1().getX(), hl.getKp2().getX()], [hl.getKp1().getY(), hl.getKp2().getY()]))
        elif class_name =='Arc':
            start_angle = np.arctan2(hl.getKp1().getY() - hl.getKpc().getY(), hl.getKp1().getX() - hl.getKpc().getX()) * 180 / np.pi
            end_angle = start_angle + hl.getDTheta()*180/np.pi
            r = np.sqrt((hl.getKp1().getY() - hl.getKpc().getY())**2 + (hl.getKp1().getX() - hl.getKpc().getX())**2)
            ax.add_patch(patches.Arc([hl.getKpc().getX(), hl.getKpc().getY()], 2*r, 2*r, 0, start_angle, end_angle))
        elif class_name =='Circumference':
            r = hl.getRadius()
            ax.add_patch(patches.Arc([hl.getCenter().getX(), hl.getCenter().getY()], 2*r, 2*r, 0, 0, 360))
        else:
            raise ValueError('Not supported Hyperline object!')