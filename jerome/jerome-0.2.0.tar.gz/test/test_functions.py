from sys import getsizeof  # noqa: E902

import pytest
from jerome.bw.burrowswheeler import forward_bw, reverse_bw
from jerome.glosser import degloss, gloss
from jerome.runlength import runlength_encode, runlength_decode


@pytest.fixture(scope="session")
def glossmark(k):
    return next(k)


def test_forward_bw(jabber):
    rolled = forward_bw(jabber)
    assert (len(rolled) - 1) == len(jabber)


def test_reverse_bw(jabber, forward_bwjabber):
    reverse_bwed = reverse_bw(forward_bwjabber)
    assert reverse_bwed == jabber


def test_runlength_encoding(jabber):
    run = runlength_encode(jabber)
    jsize = getsizeof(jabber)
    rsize = getsizeof(run)
    assert jsize > rsize
    jlen = len(jabber)
    rlen = len(run)
    assert jlen > rlen


def test_runlength_restore(forward_bwjabber, runforward_bwjabber):
    restored = runlength_decode(runforward_bwjabber)
    assert forward_bwjabber == restored


def test_deglosser(glossy, printable, glossmark):
    deglossed, glossfile = degloss(glossy, mark=glossmark, allowed=printable)
    assert len(glossy) == len(deglossed)
    for c in deglossed:
        if c != glossmark:
            assert c in printable


def test_glosser(deglossed, glossy):
    assert glossy == gloss(*deglossed)
