"""node graph py wraper see cluster"""

import pypathing.scr.cy_nodeGraph as cy_node_graph
from numpy import ndarray, copy as npcopy, array
import typing
from math import sqrt, ceil
import tkinter

Cluster = cy_node_graph.PY_Cluster
"""A Cluster of nodes witch is basicly just a collection of nodes

        currently only 3 dimentions are suported
        """

node = cy_node_graph.PY_node
"""py node inplementation

        a node is a postion in a pathfinding maze
        it hase its owne ndimentional postion, id and edges connected to it
        """


edge = cy_node_graph.PY_edge
"""py edge implementation

        an edge is a path betwean 2 nodes of a certain lenth
        """

nodeGraph = cy_node_graph.Py_nodeGraph
"""py node Graph implementation

        an absract node Graph """

goalCluster = cy_node_graph.Py_GoalCluster
"""a cluster extension that uses goal based pathfinding
        """

def debugRenderDirections(goals: goalCluster, arr: ndarray, clus:Cluster, tk:tkinter.Tk=None, renderArrows=True):
    "debug function to debug the path finding sys it will draw arrows"
    width=500
    height=500
    level = 0
    dims = arr.shape[1:]

    def drawArrow(x, y, tox, toy):
        cv.create_line((x+.5)*width/dims[0], (y+.5)*height/dims[1],
                       (x+tox+1)*width/dims[0]/2, (y+toy+1)*height/dims[1]/2,
                       fill="red", arrow=tkinter.LAST)


    master = tkinter.Tk() if tk is None else tk
    cv = tkinter.Canvas(master, width=width, height=height)
    cv.pack()
    for y_id, row in enumerate(arr[0]):
        for x_id, val in enumerate(row):
            cv.create_rectangle((x_id)*  width/dims[0], (y_id)*    height/dims[1],
                                (x_id+1)*width/dims[0], (y_id+1)*height/dims[1],
                                fill="white" if val==1 else "black")

    if renderArrows: 
        for y_id, row in enumerate(arr[0]):
            for x_id, _ in enumerate(row):
                try:
                    node = clus.getnode((level, x_id, y_id))
                    toNode = goals.getNext(node)
                    drawArrow(x_id, y_id, int(toNode.position[1]), int(toNode.position[2]))
                except:
                    pass

    if tk is None: master.mainloop()
    return master, cv


def debugRender(arr3d: ndarray, poses: typing.List[node]=[], layers=None):
    import matplotlib.pyplot as plt
    layers = layers if layers!=None else range(0, arr3d.shape[0])
    size = ceil(sqrt(len(layers)))
    f, axarr = plt.subplots(ceil(len(layers)/size), size)
    axarr = array([axarr]).flatten()
    for idx, layer in enumerate(layers):
        arr = npcopy(arr3d[layer])
        for pos in poses:
            if pos.position[0] == layer:
                arr[pos.position[1], pos.position[2]] = 2
        
        axarr[idx].imshow(arr)
        axarr[idx].set_title(f"dim {layer}")

    plt.show()

def debugRenderCluster(graph: nodeGraph, 
                       arr:ndarray, 
                       layer=0, 
                       width=800, 
                       height=800, 
                       x=0, 
                       y=0, 
                       colors=["red", "green"], 
                       path=[], 
                       pathColor="gold", 
                       pathWidth=10,
                       renderNodes=True):
    "draw all nodes of a cluster" 
    #splitter = "[:2]"  
    master = tkinter.Tk()
    layerer = "[2]"
    cv = tkinter.Canvas(master, width=width, height=height)
    cv.pack()

    dims = arr.shape[1:]
    for x_id, row in enumerate(arr[0]):
        for y_id, val in enumerate(row):
            cv.create_rectangle(x+x_id*    width/dims[0], y+y_id*    height/dims[1],
                                x+(x_id+1)*width/dims[0], y+(y_id+1)*height/dims[1],
                                fill="white" if val==1 else "black")

    def render(graph, colors, w):
        if len(colors) == 0:
            return

        clus = graph.abstractCluster
        for element in graph.lowerNodeGraphs:
            render(element, colors[1:], w+1)

        _debugRenderClusterConnections(clus, cv, x, y, width, height, dims, colors, layer, w)

    if renderNodes: render(graph, colors, 1)

    if len(path)>0:
        lastPos = path[0].position[1:]
        for node in path:
            pos = node.position[1:]
            cv.create_line(x+width*(lastPos[0]+.5)/dims[0], y+height*(lastPos[1]+.5)/dims[1],
                        x+width*(pos[0]+.5)    /dims[0], y+height*(pos[1]+.5)    /dims[1],
                        fill=pathColor, width=pathWidth)
            lastPos = pos
    

    master.mainloop()

def debugRenderClusterConnections(clus, arr, color="red"):
    width=500
    height=500

    master = tkinter.Tk()
    cv = tkinter.Canvas(master, width=width, height=height)
    cv.pack()

    _debugRenderClusterConnections(clus, cv, 0, 0, width, width, arr.shape[1:], [color], 0, 10)



def _debugRenderClusterConnections(clus, cv, x, y, width, height, dims, colors, layer, w):
    nodes = clus.nodes
    for node in clus.nodes.values():
            for otherNodeid in node.connectedNodes:
                if otherNodeid == -1:
                    continue
                otherNode = nodes[otherNodeid]
                apos = node.position[1:]
                bpos = otherNode.position[1:]
                cv.create_line(x+width*(apos[0]+0.5)/dims[0], y+height*(apos[1]+0.5)/dims[1],
                               x+width*(bpos[0]+0.5)/dims[0], y+height*(bpos[1]+0.5)/dims[1],
                               fill=colors[0], width=w)

    for node in clus.nodes.values():
        pos = node.position[1:]
        l = node.position[0]
        if layer == l:
            cv.create_oval(x+width*(pos[0]+.3)/dims[0], y+height*(pos[1]+.3)    /dims[1], 
                           x+width*(pos[0]+.7)/dims[0], y+height*(pos[1]+.7)/dims[1], fill=colors[0])
