__version__ = '0.1.0'
print(f"Thank you for using tinyevent version {__version__}"
      f"\nplease report any indecencies to afmelin@github")

from .tinyevent_core import Event
from .tinyevent_core import post_event
from .tinyevent_core import queue
from .tinyevent_core import queue_length
from .tinyevent_core import get_index_by_value
from .tinyevent_core import pop_index
from .tinyevent_core import pop_newest
from .tinyevent_core import pop_oldest
from .tinyevent_core import pop_finished_timers
from .tinyevent_core import clear_queue
