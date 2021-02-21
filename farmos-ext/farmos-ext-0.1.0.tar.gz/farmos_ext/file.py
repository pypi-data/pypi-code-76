
from __future__ import annotations

from datetime import datetime
import os

from typing import Dict, Optional, TYPE_CHECKING

from farmos_ext.farmobj import FarmObj

if TYPE_CHECKING:
    from farmos_ext.farm import Farm  # pylint: disable=cyclic-import


class File(FarmObj):

    def __init__(self, farm: Farm, keys: Dict = None):
        if 'resource' not in keys:
            super().__init__(farm, keys)
        elif 'resource' in keys and keys['resource'] == 'file':
            super().__init__(
                farm, farm.file.get({'id': keys['id']})['list'][0])
        else:
            raise KeyError('Key resource does not have value log')

    @property
    def mime(self) -> Optional[str]:
        return self.attr('mime', str)

    @property
    def size(self) -> Optional[int]:
        return self.attr('size', int)

    @property
    def url(self) -> Optional[str]:
        return self.attr('url', str)

    @property
    def id(self) -> Optional[int]:  # pylint: disable=invalid-name
        return self.attr('fid', int)

    @property
    def timestamp(self) -> Optional[datetime]:
        return FarmObj.timestamp_to_datetime(self.attr('timestamp', int))

    @property
    def owner(self):
        return None

    def download(self):
        data = self.farm.session.get(self.url)
        path = os.path.join(self.farm.local_resources, 'files', self.name)
        open(path, 'wb').write(data.content)
        return path
