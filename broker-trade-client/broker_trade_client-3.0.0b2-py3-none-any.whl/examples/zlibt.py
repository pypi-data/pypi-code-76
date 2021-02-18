import zlib
import time

data = """aa"""


def _inflate(data):
    """
    Helper function from okex to decompress the raw pushed data from okex websocket subscription
    """
    decompress = zlib.decompressobj(
        -zlib.MAX_WBITS  # see above
    )
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return inflated


if __name__ == '__main__':

    zdata = zlib.compress(b'abdu9ik3jkdkf33')
    start = time.time()
    print(_inflate(zdata))
    end = time.time()
    print("time: %s" % (end-start))
