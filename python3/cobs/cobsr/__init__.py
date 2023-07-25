"""
Consistent Overhead Byte Stuffing/Reduced (COBS/R) encoding and decoding.

Functions are provided for encoding and decoding according to
the COBS/R method.

A pure Python implementation and a C extension implementation
are provided. If the C extension is not available for some reason,
the pure Python version will be used.
"""

try:
    from ._cobsr_ext import *
    _using_extension = True
except ImportError:
    from ._cobsr_py import *
    _using_extension = False

DecodeError.__module__ = 'cobs.cobsr'

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
