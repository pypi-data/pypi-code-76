"""Top-level package for CY Quant Components."""

try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    __path__ = __import__('pkgutil').extend_path(__path__, __name__)

__author__ = """Gatro CY"""
__email__ = 'cragodn@gmail.com'
__version__ = '0.3.4'
