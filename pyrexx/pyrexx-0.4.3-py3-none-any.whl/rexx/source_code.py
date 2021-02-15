class SourceCode:

    def __init__(self, code=None):
        if code:
            self.code = code
            self.records = self.code.split('\n')
        else:
            self.code = ''
            self.records = []

    def __len__(self):
        """Return the size of source code in records."""
        return len(self.records) - 1

    def append_record(self, record, index=None):
        if index:
            self.records.insert(index, record)
        else:
            self.records.append(record)
        self.code = "\n".join(self.records)

    def append_records(self, records):
        self.records.extend(records)
        self.code = "\n".join(self.records)
