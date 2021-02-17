from time import time


event_queue = []


class Event:
    def __init__(self, val1: any, timer: int or float = None, frame_timer: int = None):
        self.val1 = val1

        # timing variables
        self.frame_timer = int(frame_timer) if isinstance(frame_timer, int or float) else None
        self.frame_count = 0
        self.created = time()
        self.timer = timer
        self.last_checked = 0

    def age(self) -> float:
        t = time()

        return t - self.created

    def creation_time(self):
        return self.created

    def check_timer(self) -> bool:
        """
        Checks if either of the two timers have expired - returns True if expired or False if not.

        timer: time based timer
        frame_timer: each check increases the frame count (frame_timer = 0 == same frame)
        """
        if self.timer:
            if self.created + self.timer >= time():
                return True
            else:
                return False

        if self.frame_timer:
            if self.frame_timer >= self.frame_count:
                return True
            else:
                self.frame_count += 1
                return False


def post_event(val1: any,
               timer: int or float = None,
               frame_timer: int = None) -> None:
    """
    Post a new event to the event queue. Sorts by event_config["sort_on_value"]
    """

    event_queue.append(Event(val1, timer, frame_timer))


def queue_length() -> int:
    """
    Length of queue
    """
    return len(event_queue)


def queue() -> bool:
    """
    Is there a queue?
    """
    return bool(event_queue)


def pop_oldest() -> Event or None:
    """
    Pop the oldest event
    """
    if queue():
        return event_queue.pop(0)


def pop_newest() -> Event or None:
    """
    Pop the most recently added event
    """
    if queue():
        n = queue_length()
        return event_queue.pop(n - 1)


def pop_index(index) -> Event or None:
    """
    Returns Event at index or None if index non-existent
    """
    try:
        return event_queue.pop(index)
    except IndexError:
        return None


def pop_timer_ended() -> Event or bool:
    """
    Returns first event found with timer expired, if none found, returns False
    """
    index = 0

    for e in event_queue:
        if e.timer:
            if e.check_timer():
                return event_queue.pop(index)
        index += 1

    return False


def clear_queue() -> bool:
    """
    Clear the queue, if no queue return False
    """
    if queue():
        event_queue.clear()
        return True

    else:
        return False


def pop_finished_timers() -> list or None:
    """
    Pops and returns all events that has an expired timer
    """
    timered_events = []

    index = 0
    for e in event_queue:
        if e.timer or e.frame_timer:
            if e.check_timer():
                return_event = event_queue.pop(index)
                timered_events.append(return_event)
        index += 1

    if timered_events:
        return timered_events
    else:
        return None


def get_index_by_value(value: any) -> int or None:
    """
    Returns index of the first event found containing value
    """
    index = 0

    for e in event_queue:
        if e.val == value:
            return index
        else:
            index += 1

    return None


def pop_by_value(value: any) -> Event or None:
    """
    Pops the first event with matching value
    """
    return pop_index(get_index_by_value(value))
