from pioneer.common import linalg
from pioneer.common.gui import Product, BVH
from pioneer.common.gui.Effect import Effect
from pioneer.common.gui.Geometry import Geometry
from pioneer.common.gui.Transforms import Transform
from pioneer.common.gui.utils import to_numpy, tf_to_numpy

from PyQt5.QtGui import QColor
from PyQt5.QtCore import pyqtProperty as Property, pyqtSignal as Signal, pyqtSlot as Slot, QObject, Q_CLASSINFO
from PyQt5.QtQml import QQmlListProperty

import numpy as np

class Renderable(Product.Product):
    def __init__( self, parent = None ):
        super(Renderable, self).__init__( parent )

class Actor( Renderable ):

    def __init__( self, parent = None, geometry = None, effect = None, transform = None, name = None, visible = True, bbox = None, type_id = -1, instance_id = -1):
        super(Actor, self).__init__( parent )
        self._geometry = None
        self._effect  = None
        self._transform = None
        self._visible = visible
        self._renderRank = 0
        self.bbox = bbox
        self.type_id = type_id
        self.instance_id = instance_id

        self.setObjectName(name)

        self.geometry = geometry
        self.effect = effect
        self.transform = transform
        self.visible = visible


    clicked = Signal(int, 'QVector3D', 'QVector3D', 'QVector3D', 'QVector3D', 'QVector3D', 'QVariant', 'QVariant'
                         , arguments = ['id', 'tuv', 'worldOrigin', 'worldDirection', 'localOrigin', 'localDirection', 'event', 'viewport'] )
    hovered = Signal(int, 'QVector3D', 'QVector3D', 'QVector3D', 'QVector3D', 'QVector3D', 'QVariant', 'QVariant'
                         , arguments = ['id', 'tuv', 'worldOrigin', 'worldDirection', 'localOrigin', 'localDirection', 'event', 'viewport'] )

    Product.InputProperty(vars(), Geometry, 'geometry')

    Product.InputProperty(vars(), Transform, 'transform')

    Product.InputProperty(vars(), Effect, 'effect')

    Product.InputProperty(vars(), bool, 'visible')

    Product.InputProperty(vars(), int, 'renderRank')



class Actors( Renderable ):

    def __init__(self, parent = None, name = None, bbox = None, shared_transform = None, scale = 1, all_vertices = [], type_id = -1, instance_id = -1):
        super(Actors, self).__init__( parent )
        self.setObjectName(name)
        self._renderables = []
        self._instanciator = None
        self._manually_added = []
        self.bbox = bbox
        self.scale = scale
        self.all_vertices = all_vertices
        self.type_id = type_id
        self.instance_id = instance_id

        # Warning: Not a scene graph, totally manual feature, you have share this transform yourself
        # it is meant to be used to access and modify a transformed manually shared among actors (Advanced users :-) )
          
        self.shared_transform = shared_transform 


    Q_CLASSINFO('DefaultProperty', 'renderables')

    @Property(QQmlListProperty)
    def renderables(self):
        return QQmlListProperty(Renderable, self, self._renderables)

    Product.InputProperty(vars(), QObject, 'instanciator')

    @Slot(Renderable)
    def addActor(self, actor):
        self._manually_added.append(actor)
        actor.setParent(self)
        self.makeDirty()
        return actor

    @Slot(Renderable)
    def removeActor(self, actor):
        if actor in self._manually_added:
            self._manually_added.remove(actor)
            actor.setParent(None)
            self.makeDirty()

    @Slot(Renderable)
    def clearActors(self):
        for a in self._manually_added:
            a.setParent(None)
        self._manually_added.clear()
        self.makeDirty()

    def children_actors(self):
        qml = [] if self._instanciator is None else self._instanciator.children()
        return self._manually_added + self._renderables + qml

    def actor_to_id(self, id_to_actors = None):

        if id_to_actors is None:
            id_to_actors = self.get_visible_actors()

        actor_to_id_ = {}
        for i, a in enumerate(id_to_actors):
            n = a.objectName()
            if not n:
                n = "anonymous"
            
            if n in actor_to_id_:
                actor_to_id_[n].append(i)
            else:
                actor_to_id_[n] = [i]
        return actor_to_id_
    



    def merged_bvhs(self):
        '''
            Warning, this will update actors
        '''
        bvhs = []
        matrices = []
        effects = []

        
        id_to_actors = self.get_visible_actors()
        for i, a in enumerate(id_to_actors):
            a.geometry.update()
            if a.transform:
                a.transform.update()
            bvh = a.geometry.goc_bvh(True)
            bvhs.append(bvh if bvh is None else bvh.bvh)

            matrices.append(tf_to_numpy(a.transform) if a.transform else np.eye(4, dtype = 'f4'))

            uniforms = {}
            for k,v, in a.effect.shader0.uniforms.items():
                uniforms[k] = to_numpy(v)

            attributes = {}
            for k,v in a.geometry.attribs.get_attributes().items():
                if v is not None:
                    attributes[k] = v.ndarray 

            textures = {}
            for k,v in a.effect.shader0.textures.items():
                textures[k] = v.ndarray 

            effects.append({ "type": a.effect.objectName()
            , "uniforms": uniforms
            , "textures": textures
            , "attribs": attributes})

        bvh, triangles_mapping, triangle_offsets, vertex_offsets = BVH.merge_bvhs(bvhs, matrices)

        return bvh, {'id_to_actors': id_to_actors
        , 'triangles_mapping': triangles_mapping
        , 'triangle_offsets': triangle_offsets
        , 'vertex_offsets': vertex_offsets
        , "effects": effects}

    def is_any_visible_actor_dirty(self):

        is_dirty = False

        def recursive_check(a):
            if issubclass(type(a), Actor):
                if a.visible:
                    return a.geometry.dirty | (a.transform.dirty if a.transform else False)
                return False
                
            elif issubclass(type(a), Actors):
                return a.is_any_visible_actor_dirty()
                              
            raise TypeError(type(a))

        for r in self._renderables:
            if recursive_check(r):
                return True

        for ma in self._manually_added:
            if recursive_check(ma):
                return True

        if self._instanciator:
            for c in self._instanciator.children():
                if recursive_check(ma):
                    return True
        
        return False

    def get_visible_actors(self):
        actors = set()

        def add_actor(a):
            if issubclass(type(a), Actor):
                if a.visible:
                    actors.add(a)
            elif issubclass(type(a), Actors):
                actors.update(a.get_visible_actors()) #union of sets

        for r in self._renderables:
            add_actor(r)

        for ma in self._manually_added:
            add_actor(ma)

        if self._instanciator:
            for c in self._instanciator.children():
                add_actor(c)
        

        return actors



