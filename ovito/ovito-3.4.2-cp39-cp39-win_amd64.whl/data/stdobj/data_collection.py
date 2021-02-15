# Load dependencies
import ovito
from ovito.data import DataCollection
from ovito.data.data_objects_dict import DataObjectsDict

# Load the native code module
from ovito.plugins.StdObjPython import SimulationCell, DataTable

# Implementation of the DataCollection.tables attribute.
def _DataCollection_tables(self):
    """
    A dictionary view of all :py:class:`DataTable` objects in
    this data collection. Each :py:class:`DataTable` has a unique :py:attr:`~ovito.data.DataObject.identifier` key, 
    which can be used to look it up in this dictionary. You can use

    .. literalinclude:: ../example_snippets/data_collection_tables.py
        :lines: 9-9

    to find out which table identifiers exist in the dictionary. Modifiers that generate a data table typically 
    assign a predefined identifier, which can be found in their documentation.
    Use the key string to retrieve the desired :py:class:`DataTable` from the dictionary, e.g.

    .. literalinclude:: ../example_snippets/data_collection_tables.py
        :lines: 14-15

    """
    return DataObjectsDict(self, DataTable)
DataCollection.tables = property(_DataCollection_tables)

# Implementation of the DataCollection.cell attribute.
def _DataCollection_cell(self):
    """ 
    Returns the :py:class:`SimulationCell` object, which stores the cell vectors and periodic boundary
    condition flags, or ``None`` if there is no cell information associated with this data collection. 

    Note: The :py:class:`SimulationCell` data object may be read-only if it is currently shared by
    several data collections. Use the :py:attr:`!cell_` field instead to request a mutable cell object 
    if you intend to modify it.
    """
    return self.find(SimulationCell)
DataCollection.cell = property(_DataCollection_cell)

# Implementation of the DataCollection.cell_ attribute.
DataCollection.cell_ = property(lambda self: self.make_mutable(self.cell))

# For backward compatibility with older development versions of OVITO:
DataCollection.series = property(lambda self: self.tables)
