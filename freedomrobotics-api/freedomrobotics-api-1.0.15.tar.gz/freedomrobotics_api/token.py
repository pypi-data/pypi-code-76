import logging

from .entity import Entity

logger = logging.getLogger(__name__)


class Token(Entity):

    def _make_url(self):
        return "/tokens/{}".format(self._id)
