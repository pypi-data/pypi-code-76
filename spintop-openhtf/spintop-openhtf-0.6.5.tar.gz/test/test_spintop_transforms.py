from datetime import datetime, timedelta
from openhtf.core.test_record import TestRecord

from spintop.models import SpintopTestRecord
from spintop.utils import utcnow_aware

from spintop_openhtf.transforms.openhtf_fmt import OpenHTFTestRecordTransformer
from spintop_openhtf.transforms.openhtf_gen import OpenHTFTestsGenerator


generator = OpenHTFTestsGenerator()
transformer = OpenHTFTestRecordTransformer()

generate_transform = generator + transformer

def test_generate():
    tests = list(generator.generate(count=2))

    assert len(tests) == 2
    assert isinstance(tests[0], TestRecord)

def test_transform():

    now = utcnow_aware()
    min_datetime = now - timedelta(minutes=1)
    max_datetime = now + timedelta(minutes=1)


    spintop_records = list(generate_transform.generate(count=2))

    assert len(spintop_records) == 2
    assert isinstance(spintop_records[0], SpintopTestRecord)
    
    for record in spintop_records:
        assert min_datetime < record.test_id.start_datetime < max_datetime

