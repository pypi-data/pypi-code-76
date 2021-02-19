"""Sphinx configuration file for TSSW package"""

from documenteer.sphinxconfig.stackconf import build_package_configs
import lsst.ts.idl


_g = globals()
_g.update(build_package_configs(project_name="ts_idl", version=lsst.ts.idl.__version__))

intersphinx_mapping["ts_xml"] = ("https://ts-xml.lsst.io", None)  # noqa
