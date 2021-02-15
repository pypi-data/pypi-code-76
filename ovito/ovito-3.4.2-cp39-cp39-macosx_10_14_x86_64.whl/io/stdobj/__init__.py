# Load dependencies
import ovito.io

# Load the native module.
from ovito.plugins.StdObjPython import DataTableExporter

# Register export formats.
ovito.io.export_file._formatTable["txt/table"] = DataTableExporter
# For backward compatibility with older development versions of OVITO:
ovito.io.export_file._formatTable["txt/series"] = DataTableExporter
