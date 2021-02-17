import json

from .record import _type_lookup, UsageRecord, UsageRecordError


class UsageMessageException(Exception):
    """
    Exception for invalid data in a UsageMessage
    """
    pass


class _UsageRecordList:
    def __init__(self, in_list=[]):
        self._list = in_list
        self._record_type = None
        if not self._check_usage_type():
            self._list = []
            raise UsageMessageException('Cannot create a UsageMessage with mixed types')

    def _check_usage_type(self):
        if self._record_type is None and len(self._list) > 0:
            rt = self._list[0].record_type.lower().capitalize()
            if rt not in ['Compute', 'Storage', 'Adjustment']:
                raise UsageMessageException('Invalid usage type {}'
                                            .format(rt))
            self._record_type = rt
        # iterate over list records and check against stored type
        return all([x.record_type.lower().capitalize() == self._record_type for x in self._list])

    def append(self, item):
        if not isinstance(item, UsageRecord):
            raise UsageMessageException("Can't add something that isn't a UsageRecord")
        if (self._record_type is not None and
                item.record_type != self._record_type):
            raise UsageMessageException("Can't add a {} record to a {} message"
                                        .format(item.record_type, self._record_type))
        self._list.append(item)
        if not self._check_usage_type():
            self._list.pop()
            raise UsageMessageException('Cannot create a UsageMessage with mixed types')

    def extend(self, items):
        for item in items:
            self.append(item)

    def __getitem__(self, i):
        return self._list.__getitem__(i)

    def __len__(self):
        return len(self._list)

    def __repr__(self):
        return "<UsageRecordList: {s._record_type} type, length {l}>".format(s=self, l=len(self))


class UsageMessage:
    def __init__(self, records):
        self.records = _UsageRecordList(records)

    @classmethod
    def from_dict(cls, input_dict):
        """
        Returns a UsageMessage from a provided dictionary
        """
        ut = input_dict['Records'][0]['UsageType']
        ur_class = _type_lookup(ut)
        records = [ur_class.from_dict(d) for d in input_dict['Records']]
        return cls(records)

    @classmethod
    def from_json(cls, input_json):
        input_dict = json.loads(input_json)
        return cls.from_dict(input_dict)

    def as_dict(self):
        """
        Returns a dictionary version of this record
        """
        d = {
            'UsageType': self.records._record_type,
            'Records': [r.as_dict() for r in self.records]
        }
        return d

    def json(self, **json_kwargs):
        """
        Returns a json version of this message
        """
        return json.dumps(self.as_dict(), **json_kwargs)

    def pretty_print(self):
        """
        prints() a pretty version of the JSON of this packet
        """
        print(self.json(indent=4, sort_keys=True))

    def _chunked(self, chunk_size=1000):
        """
        Generator that yields UsageMessages with a maximum of chunk_size number
        UsageRecords. Useful for not going over the 256kb POST limit
        """
        for i in range(0, len(self.records), chunk_size):
            r = self.records[i:i+chunk_size]
            yield self.__class__(r)


class UsageMessageError:
    def __init__(self, error, message):
        self._error = error
        self.message = message

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, _):
        pass

    @classmethod
    def from_dict(cls, input_dict):
        error = input_dict.pop('Error', None)
        message = UsageMessage.from_dict(input_dict)
        return cls(error, message)

    @classmethod
    def from_json(cls, input_json):
        d = json.loads(input_json)
        return cls.from_dict(d)

    def as_dict(self):
        d = {'Error': self._error}
        d.update(self.message.as_dict())
        return d

    def json(self, **json_kwargs):
        return json.dumps(self.as_dict(), **json_kwargs)

    def pretty_print(self):
        """
        prints() a pretty version of the JSON of this packet
        """
        print(self.json(indent=4, sort_keys=True))

    def __repr__(self):
        return "<UsageMessageError: {s._error}>".format(s=self)
