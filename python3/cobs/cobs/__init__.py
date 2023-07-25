"""
Consistent Overhead Byte Stuffing (COBS) encoding and decoding.

Functions are provided for encoding and decoding according to
the basic COBS method.

The COBS variant "Zero Pair Elimination" (ZPE) is not
implemented.

A pure Python implementation and a C extension implementation
are provided. If the C extension is not available for some reason,
the pure Python version will be used.

References:
    http://www.stuartcheshire.org/papers/COBSforToN.pdf
    http://tools.ietf.org/html/draft-ietf-pppext-cobs-00
"""

try:
    from ._cobs_ext import *
    _using_extension = True
except ImportError:
    from ._cobs_py import *
    _using_extension = False

DecodeError.__module__ = 'cobs.cobs'

from .._version import *


def encoding_overhead(source_len):
    """Calculates the maximum overhead when encoding a message with the given length.
    The overhead is a maximum of [n/254] bytes (one in 254 bytes) rounded up."""
    if source_len == 0:
        return 1
    return (source_len + 253) // 254


def max_encoded_length(source_len):
    """Calculates how maximum possible size of an encoded message given the length of the
    source message."""
    return source_len + encoding_overhead(source_len)
