import re

runs = re.compile(r"([^0-9])\1+")
antiruns = re.compile(r"([^0-9])([0-9]+)")

def runlength_encode(text: str) -> str:
    """ Runlength encodes text.
        Text should not contain any numbers.
    """
    return runs.sub(
        lambda m: m.group(0)[0] + str(len(m.group(0))), text
    )


def runlength_decode(text: str) -> str:
    """ Reverses runlength encoding on text
    """
    return antiruns.sub(lambda m: m.group(1) * int(m.group(2)), text)
