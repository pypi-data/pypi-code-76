from redis_pal import RedisPal


def echo(arg):
    return arg


def setup():
    return "test", RedisPal()


def test_reprs():
    _, rp = setup()
    print(rp.__repr__())
    print(rp.__str__())
    assert rp.__str__() == rp.__repr__()


def test_int():
    key, rp = setup()
    # Integer
    inp = 1
    rp.set(key, inp)
    ans = rp.get(key)
    assert isinstance(ans, int)
    assert inp == ans


def test_float():
    key, rp = setup()
    # Float
    inp = 1.23
    rp.set(key, inp)
    ans = rp.get(key)
    assert isinstance(ans, float)
    assert inp == ans


def test_str():
    key, rp = setup()
    # String
    inp = "Test"
    rp.set(key, inp)
    ans = rp.get(key)
    assert isinstance(ans, str)
    assert str(inp) == ans


def test_bytes():
    key, rp = setup()
    # Bytes
    inp = b"Test"
    rp.set(key, inp)
    ans = rp.get(key)
    assert isinstance(ans, bytes)
    assert inp == ans


def test_func():
    key, rp = setup()
    # Function
    inp = echo
    rp.set(key, inp)
    ans = rp.get(key)
    assert ans(123) == 123


def test_numpy():
    import numpy as np
    key, rp = setup()
    # Numpy array
    inp = np.array([0, 1, 2, 3, 4])
    rp.set(key, inp)
    ans = rp.get(key)
    assert isinstance(ans, np.ndarray)
    assert inp[0] == ans[0]
    assert inp[1] == ans[1]
    assert inp[2] == ans[2]
    assert inp[3] == ans[3]
    assert inp[4] == ans[4]


def test_generator():
    key, rp = setup()
    inp = (num ** 2 for num in range(5))
    try:
        rp.set(key, inp)
        raise Exception("Could pickle a generator and shouldn't")
    except Exception:
        return


def test_unpickle_fail():
    _, rp = setup()
    try:
        rp._deserialize(b"\x80\x04}q\x00X\x01\x10\x00\x00aj\x01K{s.")
        raise Exception("Could unpickle corrupted data and shouldn't")
    except:
        return


def test_deserialize_bool():
    _, rp = setup()
    rp.set("test", True)
    assert rp.get("test")
    rp.set("test", False)
    assert not rp.get("test")


def test_force_dill():
    _, rp = setup()
    inp = compile("", "", "exec")
    enc = rp._serialize(inp)
    assert rp._deserialize(enc) == inp


def test_timestamp():
    from time import time
    start = time()
    key, rp = setup()
    # Integer
    inp = 1
    rp.set(key, inp)
    ans = rp.get_with_timestamp(key)
    assert isinstance(ans["value"], int)
    assert inp == ans["value"]
    assert (ans["last_modified"] - start) < 1


def test_zero_timestamp():
    _, rp = setup()
    ans = rp.get_with_timestamp("RANDOM_UNSET_KEY")
    assert ans["value"] is None
    assert ans["last_modified"] == 0


def test_None():
    _, rp = setup()
    inp = None
    ans = rp.get("RANDOM_UNSET_KEY")
    assert ans is None
    assert inp == ans
