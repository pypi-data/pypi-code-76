class Records:

    def __init__(self):

        a=1

    @property
    def record(self):

        record = {
            '@id': 'test_record_id',
            '@type': 'Test_record_type',
            'schema:name': 'test_name',
            'schema:url': 'https://www.test/com',
            'schema:email': 'test@test.com',
            'schema:givenname': 'test_given',
            'schema:familyname': 'test_family',
            'schema:contenturl': 'https://static.independent.co.uk/s3fs-public/thumbnails/image/2014/11/03/14/Kitten.jpg?width=1368'

        }

        return record


    @property
    def records(self):

        i = 0
        records = []

        while i < 10:
            record = self.record

            for p in record:
                if p != 'schema:contenturl':
                    record[p] = record[p] + str(i)

            records.append(record)
        
            i += 1

        return records