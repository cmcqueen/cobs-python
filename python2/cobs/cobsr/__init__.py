"""
Consistent Overhead Byte Stuffing/Reduced (COBS/R) encoding and decoding.

Functions are provided for encoding and decoding according to
the COBS/R method.

A pure Python implementation and a C extension implementation
are provided. If the C extension is not available for some reason,
the pure Python version will be used.
"""

try:
    from cobs.cobsr._cobsr_ext import *
    _using_extension = True
except ImportError:
    from cobs.cobsr._cobsr_py import *
    _using_extension = False

DecodeError.__module__ = 'cobs.cobsr'
