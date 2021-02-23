from .vps_ping import do_multi_ping


def test_pings():
    d = do_multi_ping(["1.1.1.1"])
    assert len(d) == 1

    assert d[0]
