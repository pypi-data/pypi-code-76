# coding:utf-8
# author caturbhuja
# date   2020/11/4 3:49 下午 
# wechat chending2012 


class RedisMixin:
    """
    此类中均为伪方法，仅仅为了提供IDE的提示功能
    """
    # ---------------------------- redis ---------------------------------
    # redis 更多方法，请看redis.client
    # from redis import client
    # --------------------------------------------------------------------
    def get(self, name):
        """
        Return the value at key ``name``, or None if the key doesn't exist
        """

    def set(self, name, value,
            ex=None, px=None, nx=False, xx=False, keepttl=False):
        """
        Set the value at key ``name`` to ``value``

        ``ex`` sets an expire flag on key ``name`` for ``ex`` seconds.

        ``px`` sets an expire flag on key ``name`` for ``px`` milliseconds.

        ``nx`` if set to True, set the value at key ``name`` to ``value`` only
            if it does not exist.

        ``xx`` if set to True, set the value at key ``name`` to ``value`` only
            if it already exists.

        ``keepttl`` if True, retain the time to live associated with the key.
            (Available since Redis 6.0)
        """

    def mget(self, keys, *args):
        """
        Returns a list of values ordered identically to ``keys``
        """

    def mset(self, mapping):
        """
        Sets key/values based on a mapping. Mapping is a dictionary of
        key/value pairs. Both keys and values should be strings or types that
        can be cast to a string via str().
        """

    def lpush(self, name, *values):
        "Push ``values`` onto the head of the list ``name``"

    def lpop(self, name):
        "Remove and return the first item of the list ``name``"

    def lrange(self, name, start, end):
        """
        Return a slice of the list ``name`` between
        position ``start`` and ``end``

        ``start`` and ``end`` can be negative numbers just like
        Python slicing notation
        """

    def rpop(self, name):
        "Remove and return the last item of the list ``name``"

    def rpoplpush(self, src, dst):
        """
        RPOP a value off of the ``src`` list and atomically LPUSH it
        on to the ``dst`` list.  Returns the value.
        """

    def rpush(self, name, *values):
        "Push ``values`` onto the tail of the list ``name``"

    def sort(self, name, start=None, num=None, by=None, get=None,
             desc=False, alpha=False, store=None, groups=False):
        """
        Sort and return the list, set or sorted set at ``name``.

        ``start`` and ``num`` allow for paging through the sorted data

        ``by`` allows using an external key to weight and sort the items.
            Use an "*" to indicate where in the key the item value is located

        ``get`` allows for returning items from external keys rather than the
            sorted data itself.  Use an "*" to indicate where in the key
            the item value is located

        ``desc`` allows for reversing the sort

        ``alpha`` allows for sorting lexicographically rather than numerically

        ``store`` allows for storing the result of the sort into
            the key ``store``

        ``groups`` if set to True and if ``get`` contains at least two
            elements, sort will return a list of tuples, each containing the
            values fetched from the arguments to ``get``.

        """

    def scan(self, cursor=0, match=None, count=None, _type=None):
        """
        Incrementally return lists of key names. Also return a cursor
        indicating the scan position.

        ``match`` allows for filtering the keys by pattern

        ``count`` provides a hint to Redis about the number of keys to
            return per batch.

        ``_type`` filters the returned values by a particular Redis type.
            Stock Redis instances allow for the following types:
            HASH, LIST, SET, STREAM, STRING, ZSET
            Additionally, Redis modules can expose other types as well.
        """

    def pipeline(self, transaction=True, shard_hint=None):
        """
        Return a new pipeline object that can queue multiple commands for
        later execution. ``transaction`` indicates whether all commands
        should be executed atomically. Apart from making a group of operations
        atomic, pipelines are useful for reducing the back-and-forth overhead
        between the client and server.
        """

    def hget(self, name, key):
        "Return the value of ``key`` within the hash ``name``"
