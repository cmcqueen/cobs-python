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
