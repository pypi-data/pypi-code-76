import pkg_resources

__author__ = "Malte Vogl"
__email__ = "mvogl@mpiwg-berlin.mpg.de"
__credits__ = "GMPG, MPI for History of Science"

__version__ = pkg_resources.require(__package__)[0].version

from .generateCitationNetwork import GenerateCitationNet  # noqa: F401
from .scientificTopics import GenerateScienceTopics  # noqa: F401
