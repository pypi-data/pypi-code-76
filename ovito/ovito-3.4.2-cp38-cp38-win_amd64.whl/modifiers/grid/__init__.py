# Load dependencies
import ovito.modifiers.stdobj
import ovito.modifiers.stdmod
import ovito.modifiers.mesh

# Load the native code modules.
from ovito.plugins.GridPython import CreateIsosurfaceModifier

# Inject modifier classes into parent module.
ovito.modifiers.CreateIsosurfaceModifier = CreateIsosurfaceModifier
ovito.modifiers.__all__ += ['CreateIsosurfaceModifier']
