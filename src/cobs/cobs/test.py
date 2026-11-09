"""
Consistent Overhead Byte Stuffing (COBS)

Unit Tests

This version is for Python 3.x.
"""

import unittest

from .. import cobs as cobs
from .._test import (
    CodecTestConfig,
    InputTypesTestMixin,
    NonZerosTestMixin,
    PredefinedDecodeErrorTestMixin,
    PredefinedEncodingsTestMixin,
    RandomDataTestMixin,
    UtilTestsMixin,
    ZerosTestMixin,
)
#from ..cobs import _cobs_py as cobs


class _CobsTestConfig(CodecTestConfig):
    codec = cobs
    predefined_encodings = [
        [ b"",                                  b"\x01"                                                         ],
        [ b"1",                                 b"\x021"                                                        ],
        [ b"12345",                             b"\x0612345"                                                    ],
        [ b"12345\x006789",                     b"\x0612345\x056789"                                            ],
        [ b"\x0012345\x006789",                 b"\x01\x0612345\x056789"                                        ],
        [ b"12345\x006789\x00",                 b"\x0612345\x056789\x01"                                        ],
        [ b"\x00",                              b"\x01\x01"                                                     ],
        [ b"\x00\x00",                          b"\x01\x01\x01"                                                 ],
        [ b"\x00\x00\x00",                      b"\x01\x01\x01\x01"                                             ],
        [ bytes(bytearray(range(1, 254))),      bytes(b"\xfe" + bytearray(range(1, 254)))                       ],
        [ bytes(bytearray(range(1, 255))),      bytes(b"\xff" + bytearray(range(1, 255)))                       ],
        [ bytes(bytearray(range(1, 256))),      bytes(b"\xff" + bytearray(range(1, 255)) + b"\x02\xff")         ],
        [ bytes(bytearray(range(0, 256))),      bytes(b"\x01\xff" + bytearray(range(1, 255)) + b"\x02\xff")     ],
    ]

    decode_error_test_strings = [
        b"\x00",
        b"\x05123",
        b"\x051234\x00",
        b"\x0512\x004",
    ]


class PredefinedEncodingsTests(_CobsTestConfig, PredefinedEncodingsTestMixin, unittest.TestCase):
    pass


class PredefinedDecodeErrorTests(_CobsTestConfig, PredefinedDecodeErrorTestMixin, unittest.TestCase):
    pass


class ZerosTest(_CobsTestConfig, ZerosTestMixin, unittest.TestCase):
    pass


class NonZerosTest(_CobsTestConfig, NonZerosTestMixin, unittest.TestCase):
    pass


class RandomDataTest(_CobsTestConfig, RandomDataTestMixin, unittest.TestCase):
    pass


class InputTypesTest(_CobsTestConfig, InputTypesTestMixin, unittest.TestCase):
    pass


class UtilTests(_CobsTestConfig, UtilTestsMixin, unittest.TestCase):
    pass


def runtests():
    unittest.main()


if __name__ == '__main__':
    runtests()
