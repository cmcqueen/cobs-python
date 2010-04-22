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
    http://www.stuartcheshire.org/papers/COBSforSIGCOMM/
    http://www.stuartcheshire.org/papers/COBSforToN.pdf
"""

try:
    from cobs.cobs._cobs_ext import *
    _using_extension = True
except ImportError:
    from cobs.cobs._cobs_py import *
    _using_extension = False
