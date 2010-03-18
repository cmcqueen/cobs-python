"""
Consistent Overhead Byte Stuffing (COBS) encoding and decoding.

Functions are provided for encoding and decoding according to
the basic COBS method.

The COBS variant "Zero Pair Elimination" (ZPE) is not
implemented.

A C extension implementation only is provided.

References:
    http://www.stuartcheshire.org/papers/COBSforSIGCOMM/
    http://www.stuartcheshire.org/papers/COBSforToN.pdf
"""

from cobs._cobsext import *
_using_extension = True
