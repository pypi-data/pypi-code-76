# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import leb128 as lenc

import numpy as nmpy

import base64 as bs64
import sys as syst
from typing import Any, Optional, Tuple
import zlib as cmpr


array_t = nmpy.ndarray


# See also: nmpy.sctypes and nmpy.sctypeDict
# /!\ Some types have several codes (e.g., "l" = "p" = numpy.int64; see mpy.sctypeDict)
VALID_NUMPY_TYPES = "?" + nmpy.typecodes["AllInteger"] + nmpy.typecodes["Float"]


def PCA2BStream(mask: array_t, /) -> bytes:
    """"""
    # --- Storage
    dtype = mask.dtype
    byte_order = dtype.byteorder
    if byte_order == "=":
        if syst.byteorder == "big":
            byte_order = ">"
        else:
            byte_order = "<"
    if mask.flags["C_CONTIGUOUS"]:
        enumeration_order = "C"
    else:
        enumeration_order = "F"
    storage = byte_order + dtype.char + enumeration_order

    # --- Geometry
    geometry = [mask.ndim, *mask.shape]

    # --- Contents
    raveled_mask = nmpy.ravel(mask, order="K")
    n_elements = raveled_mask.size
    values = range(max(1, int(nmpy.max(raveled_mask))) + 1)
    streams = []
    for v_idx, value in enumerate(values[1:]):
        if values.__len__() > 2:
            binary_mask = raveled_mask == value
            first_value_is_one = binary_mask[0]
        else:
            # Avoid additional array allocation when already binary
            binary_mask = raveled_mask
            first_value = binary_mask[0]
            first_value_is_one = (first_value == True) or (first_value > 0)

        # --- First value indicator
        if first_value_is_one:
            first_value = b"1"
        else:
            first_value = b"0"

        # --- Run lengths
        jumps = nmpy.diff(binary_mask)
        jump_idc = nmpy.nonzero(jumps)[0]
        if jump_idc.size > 1:
            run_lengths = (
                [jump_idc[0] + 1]
                + nmpy.diff(jump_idc).tolist()
                + [n_elements - jump_idc[-1] - 1]
            )
        elif jump_idc.size > 0:
            run_lengths = [jump_idc[0] + 1, n_elements - jump_idc[0] - 1]
        else:
            run_lengths = [n_elements]

        # --- Numeric encoding ([geometry + ]run lengths)
        numeric_encoding = []
        if v_idx > 0:
            numbers = run_lengths
        else:
            numbers = geometry + run_lengths
        for number in numbers:
            numeric_encoding.append(lenc.u.encode(number))
        numeric_encoding = b"".join(numeric_encoding)

        # --- Compression
        if v_idx > 0:
            uncompressed = first_value + numeric_encoding
        else:
            uncompressed = bytes(storage, "ascii") + first_value + numeric_encoding
        compressed = cmpr.compress(uncompressed, cmpr.Z_BEST_COMPRESSION)
        if compressed.__len__() > uncompressed.__len__():
            stream = b"0" + uncompressed
        else:
            stream = b"1" + compressed
        streams.append(bs64.b85encode(stream))

    return b"\n".join(streams)


def BStream2PCA(stream: bytes, /) -> array_t:
    """"""
    output = None

    dtype_as_str = None
    enumeration_order = None
    shape = None

    for s_idx, str_line in enumerate(stream.split(b"\n")):
        # --- Decompression
        decoded = bs64.b85decode(str_line)
        if chr(decoded[0]) == "0":
            decompressed = decoded[1:]
        else:
            decompressed = cmpr.decompress(decoded[1:])

        # --- Storage
        if s_idx > 0:
            first_value_idx = 0
        else:
            *dtype_as_str, enumeration_order = decompressed[:3]
            dtype_as_str = chr(dtype_as_str[0]) + chr(dtype_as_str[1])
            if dtype_as_str[0] == "|":
                dtype_as_str = dtype_as_str[1]
            enumeration_order = chr(enumeration_order)
            first_value_idx = 3

        # --- Numbers ([geometry + ]run lengths)
        numbers = []
        c_idx = first_value_idx + 1
        while c_idx < decompressed.__len__():
            last_idx = c_idx
            while decompressed[last_idx] & 0b10000000 > 0:
                last_idx += 1
            encoded_value = decompressed[c_idx : (last_idx + 1)]
            decoded_value = lenc.u.decode(encoded_value)
            numbers.append(decoded_value)
            c_idx = last_idx + 1

        # --- Geometry
        if s_idx > 0:
            run_lengths_idx = 0
        else:
            ndim = numbers[0]
            shape = numbers[1 : (ndim + 1)]
            run_lengths_idx = ndim + 1

        # --- Contents
        first_value = int(chr(decompressed[first_value_idx]))
        run_lengths = numbers[run_lengths_idx:]
        value_groups = (
            _lgt * (2 ** ((_idx + first_value) % 2) - 1,)
            for _idx, _lgt in enumerate(run_lengths)
        )
        values = tuple(_elm for _grp in value_groups for _elm in _grp)

        # --- Array creation
        if output is None:
            output = nmpy.array(values, dtype=dtype_as_str)
            output = nmpy.reshape(output, shape, order=enumeration_order)
        else:
            value = s_idx + 1
            mask = nmpy.array(values, dtype=dtype_as_str)
            mask = nmpy.reshape(mask, shape, order=enumeration_order)
            output[mask > 0] = value

    return output


def BStreamDetails(
    stream: bytes,
    /,
    *,
    details: str = "+",
    should_print: bool = True,
    should_return: bool = False,
) -> Optional[Any]:
    """
    Details: if "+", retrieve all details. Otherwise, pick among:
    m: maximum value in array (also number of sub_streams)
    c: compression indicator (string of zeros and ones, one per sub-stream)
    e: endianness
    t: dtype type code
    T: dtype name
    o: enumeration order
    v: first value (0 for 0 or False, 1 for non-zero or True)
    d: array dimension
    l: array lengths per dimension
    """
    if not (should_print or should_return):
        return None

    if details == "+":
        output = {}
    else:
        output = {_key: None for _key in details}

    sub_streams = stream.split(b"\n")
    if ("m" in details) or (details == "+"):
        output["m"] = sub_streams.__len__()

    for s_idx, str_line in enumerate(sub_streams):
        # --- Decompression
        decoded = bs64.b85decode(str_line)
        compression_indicator = chr(decoded[0])
        if ("c" in details) or (details == "+"):
            if ("c" in output) and (output["c"] is not None):
                output["c"] = output["c"] + compression_indicator
            else:
                output["c"] = compression_indicator
        if compression_indicator == "0":
            decompressed = decoded[1:]
        else:
            decompressed = cmpr.decompress(decoded[1:])

        # --- Storage
        if s_idx > 0:
            first_value_idx = 0
        else:
            *dtype_as_str, enumeration_order = decompressed[:3]
            dtype_as_str = chr(dtype_as_str[0]) + chr(dtype_as_str[1])
            if ("e" in details) or (details == "+"):
                output["e"] = dtype_as_str[0]
            if ("t" in details) or (details == "+"):
                output["t"] = dtype_as_str[1]
            if ("T" in details) or (details == "+"):
                output["T"] = nmpy.sctypeDict[dtype_as_str[1]].__name__
            enumeration_order = chr(enumeration_order)
            if ("o" in details) or (details == "+"):
                output["o"] = enumeration_order
            first_value_idx = 3

        # --- Contents
        if ("v" in details) or (details == "+"):
            first_value = chr(decompressed[first_value_idx])
            if ("v" in output) and (output["v"] is not None):
                output["v"] = output["v"] + first_value
            else:
                output["v"] = first_value

        if (s_idx > 0) or (
            ("d" not in details) and ("l" not in details) and (details != "+")
        ):
            continue

        # --- Numbers ([geometry + ]run lengths)
        numbers = []
        c_idx = first_value_idx + 1
        expected_n_numbers = 1  # In fact, at least one
        while (c_idx < decompressed.__len__()) and (
            numbers.__len__() < expected_n_numbers
        ):
            last_idx = c_idx
            while decompressed[last_idx] & 0b10000000 > 0:
                last_idx += 1
            encoded_value = decompressed[c_idx : (last_idx + 1)]
            decoded_value = lenc.u.decode(encoded_value)
            if (numbers.__len__() == 0) and (("l" in details) or (details == "+")):
                expected_n_numbers = decoded_value + 1
            numbers.append(decoded_value)
            c_idx = last_idx + 1

        # --- Geometry
        if ("d" in details) or (details == "+"):
            output["d"] = numbers[0]
        if ("l" in details) or (details == "+"):
            output["l"] = tuple(numbers[1 : (numbers[0] + 1)])

    if should_print:
        for key, value in output.items():
            print(f"{key} = {value}")

    if should_return:
        if details == "+":
            return output
        else:
            output = tuple(output.values())
            if output.__len__() > 1:
                return output
            elif output.__len__() > 0:
                return output[0]
            else:
                return output  # Empty tuple

    return None


def PCAIsValid(mask: array_t, /) -> Tuple[bool, Optional[str]]:
    """"""
    issue = None

    if issue is None:
        if mask.dtype.char not in VALID_NUMPY_TYPES:
            issue = f"{mask.dtype.name}: Invalid type with code {mask.dtype.char}; Expected codes={VALID_NUMPY_TYPES}"

    if issue is None:
        unique_values = tuple(nmpy.unique(mask))
        if (unique_values != (False, True)) and (
            not set(unique_values).issubset(range(int(unique_values[-1]) + 1))
        ):
            issue = (
                "Mask is neither a boolean mask nor a numeric mask with integer values"
            )

    return issue is None, issue
