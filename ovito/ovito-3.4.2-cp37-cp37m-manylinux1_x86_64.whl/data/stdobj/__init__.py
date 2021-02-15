# Load dependencies
import ovito.data

# Load the native module.
import ovito.plugins.StdObjPython

from .simulation_cell import SimulationCell
from .property import Property
from .property_container import PropertyContainer
from .data_table import DataTable
from .data_collection import DataCollection

# Inject selected classes into parent module.
ovito.data.SimulationCell = SimulationCell
ovito.data.Property = Property
ovito.data.PropertyContainer = PropertyContainer
ovito.data.DataTable = DataTable
ovito.data.ElementType = ovito.plugins.StdObjPython.ElementType
ovito.data.__all__ += ['SimulationCell', 'Property', 'PropertyContainer', 'DataTable', 'ElementType']
