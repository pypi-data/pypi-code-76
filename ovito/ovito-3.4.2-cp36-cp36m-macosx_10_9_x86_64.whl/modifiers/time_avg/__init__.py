# Load dependencies
import ovito.modifiers.stdobj

# Load the native code modules.
from ovito.plugins.TimeAveragingPython import TimeAveragingModifier, TimeSeriesModifier

# Inject modifier classes into parent module.
ovito.modifiers.TimeAveragingModifier = TimeAveragingModifier
ovito.modifiers.TimeSeriesModifier = TimeSeriesModifier
ovito.modifiers.__all__ += ['TimeAveragingModifier', 'TimeSeriesModifier']
