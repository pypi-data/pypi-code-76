# Load dependencies
import ovito.modifiers.grid
import ovito.modifiers.particles

# Load the native code modules.
from ovito.plugins.SpatialBinningPython import SpatialBinningModifier

# Inject modifier classes into parent module.
ovito.modifiers.SpatialBinningModifier = SpatialBinningModifier
ovito.modifiers.__all__ += ['SpatialBinningModifier']

# For backward compatibility with OVITO 2.9.0:
ovito.modifiers.BinAndReduceModifier = SpatialBinningModifier
ovito.modifiers.__all__ += ['BinAndReduceModifier']
