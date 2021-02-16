from boiler import definitions


def test_consistent_activity_types():
    for a_type in definitions.CurrentActivityType:
        assert a_type.value == definitions.ActivityType(a_type.value).value
