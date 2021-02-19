"""Tests for bencode.py"""
import pytest

import bencode


@pytest.mark.parametrize(
    "data_object,bencode_string",
    [
        ([], b"le"),
        ({}, b"de"),
        (0, b"i0e"),
        (123, b"i123e"),
        (-123, b"i-123e"),
        (b"abc", b"3:abc"),
        ([123, b"abc"], b"li123e3:abce"),
        ({123: b"abc"}, b"di123e3:abce"),
        ([123, {b"abc": b"def"}], b"li123ed3:abc3:defee"),
        ({123: [b"abc", b"def"]}, b"di123el3:abc3:defee"),
    ],
)
def test_basic_ok(data_object, bencode_string):
    """Test basic encoding/decoding features"""
    assert bencode.encode(data_object) == bencode_string
    assert bencode.decode(bencode_string) == data_object


def test_decode_ok(datadir):
    """Try to decode a real torrent file"""
    # Load and decode the source torrent, remove "pieces" key for simplicity
    result = bencode.decode(datadir["big-buck-bunny.torrent"].read("rb"))
    result[b"info"][b"pieces"] = []

    assert result == {
        b"announce": b"udp://tracker.leechers-paradise.org:6969",
        b"announce-list": [
            [b"udp://tracker.leechers-paradise.org:6969"],
            [b"udp://tracker.coppersurfer.tk:6969"],
            [b"udp://tracker.opentrackr.org:1337"],
            [b"udp://explodie.org:6969"],
            [b"udp://tracker.empire-js.us:1337"],
            [b"wss://tracker.btorrent.xyz"],
            [b"wss://tracker.openwebtorrent.com"],
            [b"wss://tracker.fastcast.nz"],
        ],
        b"comment": b"WebTorrent <https://webtorrent.io>",
        b"created by": b"WebTorrent <https://webtorrent.io>",
        b"creation date": 1490916601,
        b"encoding": b"UTF-8",
        b"info": {
            b"files": [
                {b"length": 140, b"path": [b"Big Buck Bunny.en.srt"]},
                {b"length": 276134947, b"path": [b"Big Buck Bunny.mp4"]},
                {b"length": 310380, b"path": [b"poster.jpg"]},
            ],
            b"name": b"Big Buck Bunny",
            b"piece length": 262144,
            b"pieces": [],
        },
        b"url-list": [b"https://webtorrent.io/torrents/"],
    }


def test_decode_unsupported_data_type_1():
    """Try to decode unsupported object (a text string)"""
    with pytest.raises(ValueError) as excinfo:
        bencode.decode("abcd")

    assert str(excinfo.value) == (
        "Cannot decode data, expected bytes, got <class 'str'> instead."
    )


def test_decode_unsupported_data_type_2():
    """Try to decode unsupported object (a binary string of unknown type)"""
    with pytest.raises(ValueError) as excinfo:
        bencode.decode(b"abcd")

    assert str(excinfo.value) == (
        "Cannot decode data, expected the first byte to be one "
        "of 'd', 'i', 'l' or a digit, got 'a' instead."
    )


def test_decode_corrupted_byte_string(datadir):
    """Try to decode a corrupted bencoded string

    To simulate the corruption, we just try to decode the first part of the
    real torrent, starting from data[:1] and upt to the data[:-1]. ValueError
    should be raised in all cases (the error message may be different, of
    course).
    """
    # Load and decode the source torrent, remove "pieces" key for simplicity
    result = bencode.decode(datadir["big-buck-bunny.torrent"].read("rb"))
    result[b"info"][b"pieces"] = []

    # Encode data back to bencoded string
    source = bencode.encode(result)

    # Try to decode incomplete data
    for i in range(1, len(source)):
        with pytest.raises(ValueError):
            bencode.decode(source[:i])


def test_encode_unsupported_data_type():
    """Try to encode unsupported object (a Python set)"""
    with pytest.raises(ValueError) as excinfo:
        bencode.encode(set())

    assert str(excinfo.value) == (
        "Cannot encode data: objects of type <class 'set'> are not supported."
    )


def test_decode_torrent(datadir):
    """Try to decode a torrent file"""
    result = bencode.decode_torrent(
        datadir["big-buck-bunny.torrent"].read("rb")
    )
    assert result["info"]["pieces"].startswith("2020a7789d")
    result["info"]["pieces"] = []

    assert result == {
        "announce": "udp://tracker.leechers-paradise.org:6969",
        "announce-list": [
            ["udp://tracker.leechers-paradise.org:6969"],
            ["udp://tracker.coppersurfer.tk:6969"],
            ["udp://tracker.opentrackr.org:1337"],
            ["udp://explodie.org:6969"],
            ["udp://tracker.empire-js.us:1337"],
            ["wss://tracker.btorrent.xyz"],
            ["wss://tracker.openwebtorrent.com"],
            ["wss://tracker.fastcast.nz"],
        ],
        "comment": "WebTorrent <https://webtorrent.io>",
        "created by": "WebTorrent <https://webtorrent.io>",
        "creation date": 1490916601,
        "encoding": "UTF-8",
        "info": {
            "files": [
                {"length": 140, "path": ["Big Buck Bunny.en.srt"]},
                {"length": 276134947, "path": ["Big Buck Bunny.mp4"]},
                {"length": 310380, "path": ["poster.jpg"]},
            ],
            "name": "Big Buck Bunny",
            "piece length": 262144,
            "pieces": [],
        },
        "url-list": ["https://webtorrent.io/torrents/"],
    }


def test_decode_torrent_unsupported_data_type():
    """Try to decode unsupported object (a text string)"""
    with pytest.raises(ValueError) as excinfo:
        bencode.decode_torrent("abcd")

    assert str(excinfo.value) == (
        "Cannot decode data, expected bytes, got <class 'str'> instead."
    )


def test_decode_torrent_utf8_suffix():
    """Dictionary keys, which have ".utf-8" suffix, should be decoded using
    this encoding, even if another encoding is specified in the function call
    """
    special_string = "日本語"
    special_string_as_bytes = special_string.encode("utf8")

    data = {b"path.utf-8": special_string_as_bytes}
    torrent = bencode.encode(data)

    assert bencode.decode_torrent(torrent, "ascii") == {"path.utf-8": "日本語"}
