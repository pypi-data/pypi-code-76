# Load dependencies
import ovito.modifiers.stdobj
import ovito.modifiers.mesh
import ovito.modifiers.grid
import ovito.modifiers.stdmod
import ovito.modifiers.particles

# Load the native code modules.
from ovito.plugins.CrystalAnalysisPython import DislocationAnalysisModifier, ElasticStrainModifier, GrainSegmentationModifier

# Inject modifier classes into parent module.
ovito.modifiers.DislocationAnalysisModifier = DislocationAnalysisModifier
ovito.modifiers.ElasticStrainModifier = ElasticStrainModifier
ovito.modifiers.GrainSegmentationModifier = GrainSegmentationModifier
ovito.modifiers.__all__ += ['DislocationAnalysisModifier', 'ElasticStrainModifier', 'GrainSegmentationModifier']

# Copy enum lists.
ElasticStrainModifier.Lattice = DislocationAnalysisModifier.Lattice
GrainSegmentationModifier.Type = ovito.modifiers.PolyhedralTemplateMatchingModifier.Type
