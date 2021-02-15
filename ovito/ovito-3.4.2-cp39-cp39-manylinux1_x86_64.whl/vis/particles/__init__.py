# Load dependencies
import ovito.vis
import ovito.vis.stdobj
import ovito.vis.stdmod
import ovito.vis.mesh
import ovito.vis.grid

# Load the native code module
from ovito.plugins.ParticlesPython import ParticlesVis, VectorVis, BondsVis, TrajectoryVis

# Inject selected classes into parent module.
ovito.vis.ParticlesVis = ParticlesVis
ovito.vis.VectorVis = VectorVis
ovito.vis.BondsVis = BondsVis
ovito.vis.TrajectoryVis = TrajectoryVis
ovito.vis.__all__ += ['ParticlesVis', 'VectorVis', 'BondsVis', 'TrajectoryVis']
