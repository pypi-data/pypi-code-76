"""
This Python module defines various data object types, which are produced and processed within OVITO's data pipeline system.
It also provides the :py:class:`DataCollection` class as a container for such data objects as well as several utility classes for
computing neighbor lists or iterating over the bonds of particles.

**Data containers:**

  * :py:class:`DataObject` (base class for all data object types)
  * :py:class:`DataCollection` (an entire dataset made of several data objects)
  * :py:class:`PropertyContainer` (base container class storing a set of :py:class:`Property` arrays)
  * :py:class:`Particles` (specialized :py:class:`PropertyContainer` for particles)
  * :py:class:`Bonds` (specialized :py:class:`PropertyContainer` for bonds)
  * :py:class:`VoxelGrid` (specialized :py:class:`PropertyContainer` for 2d and 3d data grids)
  * :py:class:`DataTable` (specialized :py:class:`PropertyContainer` for tabulated data)

**Data objects:**

  * :py:class:`Property` (array of per-data-element property values)
  * :py:class:`SimulationCell` (simulation box geometry and boundary conditions)
  * :py:class:`SurfaceMesh` (triangle mesh describing the boundary surface of a spatial region)
  * :py:class:`TrajectoryLines` (set of particle trajectory lines)
  * :py:class:`DislocationNetwork` (set of discrete dislocation lines with Burgers vector information)

**Auxiliary data objects:**

  * :py:class:`ElementType` (base class for element type definitions)
  * :py:class:`ParticleType` (describes a single particle/atom type)
  * :py:class:`BondType` (describes a single bond type)
  * :py:class:`DislocationSegment` (a dislocation line in a :py:class:`DislocationNetwork`)

**Utility classes:**

  * :py:class:`CutoffNeighborFinder` (finds all neighboring particles within a cutoff distance)
  * :py:class:`NearestNeighborFinder` (finds *N* nearest neighbor particles)
  * :py:class:`BondsEnumerator` (used for efficiently iterating over the bonds of individual particles)

"""

import numpy as np

# Load the native modules.
from ..plugins.PyScript import DataObject

# Load submodules.
from .data_collection import DataCollection

__all__ = ['DataCollection', 'DataObject']
