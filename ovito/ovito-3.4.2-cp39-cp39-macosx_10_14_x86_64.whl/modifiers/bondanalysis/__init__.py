# Load dependencies
import ovito.modifiers.particles

# Load the native code modules.
from ovito.plugins.BondAnalysisPython import BondAnalysisModifier

# Inject modifier classes into parent module.
ovito.modifiers.BondAnalysisModifier = BondAnalysisModifier
ovito.modifiers.__all__ += ['BondAnalysisModifier']
