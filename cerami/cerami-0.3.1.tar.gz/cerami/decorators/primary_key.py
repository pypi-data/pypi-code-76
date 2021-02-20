class primary_key(object):
    """A decorator to assign the primary key to a Model class"""

    def __init__(self, partition_key, sort_key=None):
        """constructor for the primary_key decorator

        Arguments:
        partition_key -- a string of the tables partition_key
        sort_key -- optional string of the sort_key for the table
        """
        self.partition_key = partition_key
        self.sort_key = sort_key

    def __call__(self, cls):
        """Automatically add _primary_key to the Model class"""
        column = getattr(cls, self.partition_key)
        if self.sort_key:
            cls._primary_key = (column, getattr(cls, self.sort_key))
        else:
            cls._primary_key = (column,)
        return cls

